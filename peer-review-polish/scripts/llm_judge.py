#!/usr/bin/env python3
"""Blind LLM classification of peer reviews: machine-drafted vs human-written.

Design notes:
  - BLIND. The judge never sees the venue or year. Labels are attached after scoring.
  - Balanced sample from ICLR 2024 and ICLR 2026, shuffled.
  - Structured outputs (validated Pydantic), never JSON parsed out of prose.
  - The judge is asked for a 0-100 likelihood plus the single strongest signal, so we
    can check WHAT it keys on -- if it keys on em dashes we have circularity with the
    typography finding and must say so.
"""
import json, glob, random, asyncio, collections, os, sys
from pydantic import BaseModel
from typing import Literal
import anthropic

class Judgment(BaseModel):
    llm_likelihood: int          # 0-100
    primary_signal: str          # strongest single cue, <=12 words
    signal_type: Literal["typography","vocabulary","structure","substance","none"]

SYSTEM = """You are judging whether a machine-learning conference peer review was
substantially drafted by a large language model, or written by a human researcher.

Judge the WRITING, not the quality of the review. A short, blunt, or poorly written
review is often strongly human. A fluent, well-organised review is not automatically
machine-written -- many researchers write well, and many use a model only to fix
grammar, which is not "drafted by a model".

Signals that a human wrote it: specific engagement with the paper's actual content
(equation numbers, figure numbers, named baselines, citations the reviewer supplies),
idiosyncratic voice, domain in-jokes, non-native English phrasing, terse or uneven
structure, genuine uncertainty about their own expertise.

Signals of machine drafting: generic praise that could apply to any paper, symmetric
strengths/weaknesses scaffolding, fluent prose with no concrete specifics, restating
the abstract instead of evaluating it, uniform sentence rhythm.

Return a likelihood from 0 (certainly human) to 100 (certainly machine-drafted)."""
import os
DATA = os.environ.get("PRP_DATA", "_data")   # collected notes; override with PRP_DATA
OUT  = os.environ.get("PRP_OUT", ".")       # figures/CSVs written here

def load_pool():
    seen={}
    for p in glob.glob(f"{DATA}/*.jsonl"):
        for l in open(p):
            try: r=json.loads(l)
            except Exception: continue
            if r.get("id"): seen[r["id"]]=r
    TEXT=("summary","strengths","weaknesses","questions","review","metareview","comment","limitations")
    by=collections.defaultdict(list)
    for r in seen.values():
        c=r.get("content") or {}
        t="\n".join(f"{k.upper()}: {v}" for k,v in c.items() if isinstance(v,str) and (k in TEXT or len(v)>120))
        if 1500<=len(t)<=6000:
            by[(r.get("domain"),r["kind"])].append((r["id"],t))
    return by

async def main(n_per=300):
    by=load_pool()
    random.seed(99)
    groups=[("ICLR.cc/2024/Conference","Official_Review","2024_review"),
            ("ICLR.cc/2026/Conference","Official_Review","2026_review"),
            ("ICLR.cc/2026/Conference","Meta_Review","2026_meta")]
    items=[]
    for dom,kind,lab in groups:
        pool=by.get((dom,kind),[])
        k=min(n_per,len(pool))
        if k<30: print(f"skip {lab}: only {len(pool)}"); continue
        for nid,t in random.sample(pool,k): items.append({"lab":lab,"id":nid,"text":t})
    random.shuffle(items)
    print(f"judging {len(items)} reviews blind ({collections.Counter(i['lab'] for i in items)})",flush=True)
    client=anthropic.AsyncAnthropic()
    sem=asyncio.Semaphore(12); out=[]
    async def one(it):
        async with sem:
            for attempt in range(4):
                try:
                    r=await client.messages.parse(
                        model="claude-opus-5", max_tokens=2000,
                        output_config={"effort":"low"},
                        system=SYSTEM,
                        messages=[{"role":"user","content":it["text"]}],
                        output_format=Judgment)
                    j=r.parsed_output
                    out.append({**{k:it[k] for k in ("lab","id")},
                                "score":j.llm_likelihood,"signal":j.primary_signal,
                                "stype":j.signal_type})
                    return
                except anthropic.RateLimitError:
                    await asyncio.sleep(8*(attempt+1))
                except Exception as e:
                    if attempt==3: print("  ERR",type(e).__name__,str(e)[:110],flush=True)
                    else: await asyncio.sleep(4*(attempt+1))
    tasks=[asyncio.create_task(one(i)) for i in items]
    done=0
    for f in asyncio.as_completed(tasks):
        await f; done+=1
        if done%100==0: print(f"  {done}/{len(items)}",flush=True)
    with open(f"{DATA}/judgments.jsonl","w") as fh:
        for o in out: fh.write(json.dumps(o)+"\n")
    print(f"DONE {len(out)} judgments",flush=True)

asyncio.run(main())
