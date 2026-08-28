#!/usr/bin/env python3
"""Step 1 — discover the AI skill vocabulary from the corpus.

We do NOT hard-code a list of AI skills. Hard-coding biases the result toward
what the author already knows and misses fast-emerging tools (MCP did not exist
when a 2024 list would have been written).

Instead we aggregate the entity-resolved skills the enrichment pipeline already
extracted from job postings, take the top N by posting count, and use that as
the measurement vocabulary for step 2.

Output: skills_vocab.json  — [{"name": "LLMs", "n": 10451}, ...]

Usage:
    source .env                                   # SKILLENAI_INSIGHTS_API_KEY
    python 01_discover_skill_vocab.py
"""
import json
import os
import urllib.request

API_URL = os.environ.get("API_URL", "https://api.skillenai.com")
API_KEY = os.environ["SKILLENAI_INSIGHTS_API_KEY"]

# Jobs corpus starts 2026-03-10; see the no-YoY caveat in the README.
WINDOW_START = "2026-03-01"
TOP_N = 400


def search(body: dict, indices: list[str]) -> dict:
    req = urllib.request.Request(
        f"{API_URL}/v1/query/search",
        data=json.dumps({"query": body, "indices": indices}).encode(),
        headers={"X-API-Key": API_KEY, "Content-Type": "application/json"},
    )
    return json.load(urllib.request.urlopen(req))


def main() -> None:
    # `entities` is a nested field. The query endpoint caps aggregation nesting
    # at 3 levels, so nested -> filter -> terms is exactly at the limit.
    resp = search(
        {
            "size": 0,
            "query": {"range": {"postedAt": {"gte": WINDOW_START}}},
            "aggs": {
                "e": {
                    "nested": {"path": "entities"},
                    "aggs": {
                        "sk": {
                            "filter": {"term": {"entities.resolved.entityType": "skill"}},
                            "aggs": {
                                "top": {
                                    "terms": {
                                        "field": "entities.resolved.canonicalName.keyword",
                                        "size": TOP_N,
                                    }
                                }
                            },
                        }
                    },
                }
            },
        },
        ["prod-enriched-jobs"],
    )

    buckets = resp["aggregations"]["e"]["sk"]["top"]["buckets"]
    vocab = [{"name": b["key"], "n": b["doc_count"]} for b in buckets]
    with open("skills_vocab.json", "w") as fh:
        json.dump(vocab, fh, indent=1)
    print(f"discovered {len(vocab)} skills -> skills_vocab.json")
    for v in vocab[:25]:
        print(f"  {v['n']:>8,}  {v['name']}")


if __name__ == "__main__":
    main()
