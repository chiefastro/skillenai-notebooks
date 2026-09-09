#!/usr/bin/env python3
"""Bucket a job title into a data-org function. Order matters: most specific first."""
import re

def _c(p): return re.compile(p, re.I)

# Titles that LOOK data-ish but are not data-team roles.
EXCLUDE = [
    _c(r"\b(aspiring|seeking|student|graduate student|looking for|open to work|unemployed)\b"),
    _c(r"\b(intern|internship|trainee|apprentice|fellow|bootcamp)\b"),
    _c(r"\b(quality assurance|\bqa\b|test|sdet)\b"),
    _c(r"\b(cyber ?security|information security|infosec|security|soc|grc|compliance|fraud)\b"),
    _c(r"\bprogrammer[ /-]?analyst\b|\banalyst[ /-]?programmer\b"),
    _c(r"\b(financial|finance|fp&a|accounting|credit|budget|treasury|actuarial|investment|equity|portfolio|risk)\s+analyst\b"),
    _c(r"\b(clinical|medical|laboratory|lab)\s+data\b"),
    _c(r"\bdata\s+(entry|center|centre|steward|governance|privacy|protection)\b"),
    _c(r"\b(master data|data governance|data quality analyst)\b"),
    _c(r"\b(supply chain|logistics|procurement|hr|people|talent|marketing|sales|crm|seo|policy|research)\s+analyst\b"),
    _c(r"\bgis\b|\bgeospatial\b"),
    _c(r"\b(professor|lecturer|postdoc|post-doc|phd candidate|teaching)\b"),
    _c(r"\b(ms|m\.s\.|msc|bs|b\.s\.|ba|mba|master'?s|bachelor'?s|masters|degree|candidate)\b\s*(in|of)?\b"),
    _c(r"\bproduct manager\b|\bprogram manager\b|\bproject manager\b"),
]

# (bucket, pattern) — evaluated in order.
RULES = [
    ("Analytics Engineering", _c(r"\banalytics?\s+engineer")),
    ("ML / AI Engineering",   _c(r"\b(machine learning|\bml\b|\bai\b|artificial intelligence|deep learning|mlops|ml ?ops)\b.{0,20}\b(engineer|architect|developer)\b")),
    ("ML / AI Engineering",   _c(r"\b(machine learning|\bml\b)\s+scientist\b")),
    ("Data Engineering",      _c(r"\bdata\s+(engineer|architect|infrastructure|platform)")),
    ("Data Engineering",      _c(r"\b(etl|elt|big data|data warehouse|data pipeline|databricks|snowflake)\b.{0,20}\b(engineer|developer|architect)\b")),
    ("Data Engineering",      _c(r"\b(etl|elt)\s+developer\b")),
    ("Data Science",          _c(r"\bdata\s+scientist\b|\bdata science\b|\bdecision scientist\b")),
    ("Analytics / BI",        _c(r"\bbusiness intelligence\b|\bbi\s+(analyst|developer|engineer|architect|manager)\b")),
    ("Analytics / BI",        _c(r"\bdata\s+analyst\b|\bdata analytics\b|\banalytics\s+(analyst|specialist|consultant)\b")),
    ("Analytics / BI",        _c(r"\b(insights?|reporting|product|marketing)\s+analyst\b")),
    ("Analytics / BI",        _c(r"\b(quantitative|research)\s+analyst\b")),
    ("Database Admin",        _c(r"\bdatabase\s+(administrator|admin|engineer)\b|\bdba\b")),
]

# Leadership over the data org (counted separately; these are "cats" too).
LEAD = _c(r"\b(head|director|vp|vice president|chief|manager|lead|principal|senior manager)\b")
LEAD_DATA = _c(r"\b(head|director|vp|vice president|chief|manager)\b.{0,30}\b(data|analytics|insights?|business intelligence|machine learning|\bai\b)\b")
DATA_LEAD2 = _c(r"\b(data|analytics|insights?|business intelligence)\b.{0,30}\b(head|director|vp|vice president|manager)\b")

def classify(title):
    t = (title or "").strip()
    if not t or len(t) > 120:
        return None
    for ex in EXCLUDE:
        if ex.search(t):
            return None
    for bucket, pat in RULES:
        if pat.search(t):
            return bucket
    if LEAD_DATA.search(t) or DATA_LEAD2.search(t):
        return "Data Leadership"
    return None

def is_lead(title):
    return bool(LEAD.search(title or ""))
