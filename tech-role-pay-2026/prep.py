"""Clean + normalize the salaried extract. Records WHY each row is dropped."""
import json, re, sys
import pandas as pd, numpy as np

SRC = sys.argv[1]; OUT = sys.argv[2]
rows = [json.loads(l) for l in open(SRC)]
df = pd.DataFrame(rows)
print("raw rows:", len(df))
print("\ncolumn non-null coverage:")
for c in df.columns:
    print(f"  {c:26s} {df[c].notna().mean()*100:5.1f}%")

# ---- 1. pay-unit normalization -------------------------------------------
mn = pd.to_numeric(df["salaryMin"], errors="coerce")
mx = pd.to_numeric(df["salaryMax"], errors="coerce")
df["_mn"], df["_mx"] = mn, mx

def unit(row_mx):
    if pd.isna(row_mx): return "na"
    if row_mx <= 300: return "hourly"
    if row_mx <= 5000: return "ambiguous"   # weekly / biweekly / monthly - undecidable
    return "annual"
df["_unit"] = mx.map(unit)
print("\npay-unit classification:")
print(df["_unit"].value_counts().to_string())

df.loc[df["_unit"]=="hourly", ["_mn","_mx"]] = df.loc[df["_unit"]=="hourly", ["_mn","_mx"]]*2080
df["mid"] = (df["_mn"]+df["_mx"])/2

drop = {}
keep = df["_unit"].isin(["hourly","annual"])
drop["ambiguous_or_missing_unit"] = int((~keep).sum())
keep &= df["_mx"] >= df["_mn"]
keep &= df["mid"].between(30_000, 1_200_000)
drop["implausible_annual_midpoint"] = int(len(df) - drop["ambiguous_or_missing_unit"] - keep.sum())

# ---- 2. spam employer ----------------------------------------------------
SPAM = {"speechify"}
is_spam = df["companyCanonicalName"].fillna("").str.lower().isin(SPAM)
drop["spam_employer"] = int((keep & is_spam).sum())
keep &= ~is_spam

df = df[keep].copy()
print("\ndrops:", json.dumps(drop, indent=2))
print("clean rows:", len(df))

# ---- 3. role family normalization ---------------------------------------
LEVEL_WORDS = r"(?:senior|sr\.?|staff|principal|distinguished|lead|junior|jr\.?|entry[- ]level|entry|associate|mid[- ]level|intermediate|chief|head of|vp of|director of|manager of|ii|iii|iv|i)"
def family(role):
    if not isinstance(role,str) or not role.strip(): return None
    r = role.strip().lower()
    r = re.sub(r"[,(].*$", "", r)                       # drop team suffixes
    r = re.sub(r"\s*[-|/]\s*(?:remote|hybrid|onsite|us|usa).*$", "", r)
    # strip leading + trailing level words repeatedly
    for _ in range(3):
        r = re.sub(rf"^{LEVEL_WORDS}\s+", "", r).strip()
        r = re.sub(rf"\s+{LEVEL_WORDS}$", "", r).strip()
    r = re.sub(r"\s+", " ", r)
    # variant normalization
    subs = [
        (r"^full[\s-]?stack", "full stack"),
        (r"^fullstack", "full stack"),
        (r"^machine learning\b", "ml"),
        (r"^artificial intelligence\b", "ai"),
        (r"^ai/ml\b", "ml"),
        (r"^front[\s-]?end", "frontend"),
        (r"^back[\s-]?end", "backend"),
        (r"^dev ?ops", "devops"),
        (r"^sre$", "site reliability engineer"),
        (r"^software development engineer", "software engineer"),
        (r"^software dev engineer", "software engineer"),
    ]
    for pat,rep in subs: r = re.sub(pat, rep, r)
    r = re.sub(r"\bsoftware developer\b", "software engineer", r)
    r = re.sub(r"\bdeveloper\b", "engineer", r)
    r = re.sub(r"\bengineer\b$", "engineer", r)
    return r.strip()

df["family"] = df["role"].map(family)

# ---- 4. seniority buckets ------------------------------------------------
IC = {"entry":"Entry","junior":"Entry","mid":"Mid","senior":"Senior",
      "staff":"Staff+","principal":"Staff+"}
MGMT = {"manager":"Management","director":"Management","vp":"Exec","c-level":"Exec"}
def bucket(s):
    if not isinstance(s,str): return None
    s = s.strip().lower()
    if s in IC: return IC[s]
    if s in MGMT: return MGMT[s]
    return None            # intern, lead -> excluded (lead = title-inflation grab-bag)
df["level"] = df["seniorityLevel"].map(bucket)
print("\nseniorityLevel raw:")
print(df["seniorityLevel"].fillna("(none)").value_counts().head(15).to_string())
print("\nlevel bucket:")
print(df["level"].fillna("(excluded)").value_counts().to_string())

df.to_parquet(OUT)
print("\nwrote", OUT)
print("\ntop 40 families by clean salaried volume:")
print(df["family"].value_counts().head(40).to_string())
