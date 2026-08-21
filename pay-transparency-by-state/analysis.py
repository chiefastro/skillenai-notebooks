#!/usr/bin/env python3
"""
Pay transparency by state: what share of job postings disclose a salary?

Reproduces every figure and CSV in this folder from the Skillenai jobs index.
Requires SKILLENAI_INSIGHTS_API_KEY in the environment.

    python3 analysis.py
"""
import json, math, os, time, urllib.request
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch

API = os.environ.get("API_URL", "https://api.skillenai.com") + "/v1/query/search"
KEY = os.environ["SKILLENAI_INSIGHTS_API_KEY"]

# ---------------------------------------------------------------- palette
# dataviz categorical slots 1-3; validated all-pairs, light mode
C_POSTING, C_REQUEST, C_NONE = "#2a78d6", "#eb6834", "#1baf7a"
SURFACE, INK, INK_2, GRID = "#fcfcfb", "#0b0b0b", "#52514e", "#e2e1dc"
LBL = {"posting": "Salary required in posting",
       "request": "Disclosure on request only",
       "none":    "No disclosure law"}
COLOR = {"posting": C_POSTING, "request": C_REQUEST, "none": C_NONE}

# ------------------------------------------------------- law reference
# Posting-disclosure mandates, with effective dates. Sources: state statutes /
# employment-law trackers, verified Aug 2026.
LAW = {
    "Colorado": ("posting", "2021-01-01"), "California": ("posting", "2023-01-01"),
    "Washington": ("posting", "2023-01-01"), "New York": ("posting", "2023-09-17"),
    "Hawaii": ("posting", "2024-01-01"), "District of Columbia": ("posting", "2024-06-30"),
    "Maryland": ("posting", "2024-10-01"), "Illinois": ("posting", "2025-01-01"),
    "Minnesota": ("posting", "2025-01-01"), "New Jersey": ("posting", "2025-06-01"),
    "Vermont": ("posting", "2025-07-01"), "Massachusetts": ("posting", "2025-10-29"),
    "Virginia": ("posting", "2026-07-01"), "Maine": ("posting", "2026-07-28"),
    "Connecticut": ("request", "2021-10-01"), "Nevada": ("request", "2021-10-01"),
    "Rhode Island": ("request", "2023-01-01"),
}
# Laws that took effect inside the data window - excluded from group aggregates
MIDWINDOW = {"Virginia", "Maine"}
cat = lambda s: LAW.get(s, ("none", None))[0]

# ------------------------------------------------------------- filters
# Platforms where the salary parser is known-reliable. Excluded:
#   breezyhr / workable / workday  - extractedText not captured, salary ~0%
#   lever                          - partial text capture, salary ~5%
#   usajobs                        - federal; pay is public by statute, not state law
GOOD_PLATFORMS = ["greenhouse", "schema_org", "ashby", "smartrecruiters", "icims"]
# Placeholders and job-board republishers - not employers
REPUBLISHERS = ["Speechify", "Confidential", "agency", "Together", "Hire Feed", "Hired",
                "Jobs Ai", "Quik Hire Staffing", "Truelogic", "TalentAlly",
                "INSPYR Solutions", "Internal Postings"]
# City names the geocoder collapses to one wrong state (e.g. every "Lexington" is
# tagged Kentucky, including MIT Lincoln Laboratory, which is in Lexington MA).
AMBIGUOUS_CITIES = ["Lexington", "Springfield", "Portland", "Arlington", "Kansas City",
                    "Charleston", "Aurora", "Pasadena", "Salem"]
MIN_N = 200


def post(body, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(
                API, data=json.dumps(body).encode(),
                headers={"X-API-Key": KEY, "Content-Type": "application/json"})
            return json.load(urllib.request.urlopen(req))
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(6 * (i + 1))


def fetch_state_rates():
    body = {"indices": ["prod-enriched-jobs"], "query": {
        "size": 0, "track_total_hits": True,
        "query": {"bool": {
            "filter": [{"term": {"locationCountry": "US"}},
                       {"terms": {"platform": GOOD_PLATFORMS}},
                       {"exists": {"field": "locationAdmin1"}}],
            "must_not": [{"terms": {"companyCanonicalName.keyword": REPUBLISHERS}},
                         {"term": {"locationAdmin1": ""}},
                         {"terms": {"locationCity": AMBIGUOUS_CITIES}}]}},
        "aggs": {"st": {"terms": {"field": "locationAdmin1", "size": 60},
                        "aggs": {"sal": {"filter": {"exists": {"field": "salaryMin"}}}}}}}}
    rows = []
    for b in post(body)["aggregations"]["st"]["buckets"]:
        n, s = b["doc_count"], b["sal"]["doc_count"]
        if n < MIN_N:
            continue
        p = s / n
        rows.append({"state": b["key"], "law": cat(b["key"]),
                     "effective": LAW.get(b["key"], (None, None))[1],
                     "n": n, "disclosed": s, "pct": round(100 * p, 1),
                     "ci95": round(100 * 1.96 * math.sqrt(p * (1 - p) / n), 1),
                     "law_took_effect_mid_window": b["key"] in MIDWINDOW})
    return sorted(rows, key=lambda r: -r["pct"])


# --------------------------------------------------------------- figures
def style(ax):
    ax.set_facecolor(SURFACE)
    for sp in ("top", "right", "left"):
        ax.spines[sp].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK_2, labelsize=9, length=0)


def titles(fig, title, subtitle):
    """Title block in figure coords so it can never collide with the axes."""
    fig.text(0.012, 0.975, title, fontsize=15, weight="bold", color=INK, va="top")
    fig.text(0.012, 0.933, subtitle, fontsize=9.5, color=INK_2, va="top")


def fig1_states(rows, path):
    rows = sorted(rows, key=lambda r: r["pct"])
    fig, ax = plt.subplots(figsize=(10, 12), facecolor=SURFACE)
    y = range(len(rows))
    ax.barh(list(y), [r["pct"] for r in rows],
            color=[COLOR[r["law"]] for r in rows], height=0.72, zorder=3)
    for i, r in enumerate(rows):
        star = " *" if r["law_took_effect_mid_window"] else ""
        ax.text(r["pct"] + 0.7, i, f"{r['pct']:.1f}%{star}", va="center",
                fontsize=8.5, color=INK_2)
    ax.set_yticks(list(y))
    ax.set_yticklabels([r["state"] for r in rows], fontsize=9, color=INK)
    ax.set_xlim(0, max(r["pct"] for r in rows) * 1.16)
    ax.set_xlabel("% of job postings that disclose a salary", fontsize=10, color=INK_2)
    ax.xaxis.grid(True, color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    style(ax)
    ax.legend(handles=[Patch(facecolor=COLOR[k], label=LBL[k])
                       for k in ("posting", "request", "none")],
              loc="lower right", frameon=False, fontsize=9.5, labelcolor=INK_2)
    fig.tight_layout(rect=[0, 0.032, 1, 0.925])
    titles(fig, "Does the job posting tell you what it pays?",
           "Share of US job postings disclosing a salary, by state · Skillenai index, 2026")
    fig.text(0.012, 0.014, "* law took effect during the data window",
             fontsize=8, color=INK_2)
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def fig2_gap(rows, path):
    act = [r for r in rows if not r["law_took_effect_mid_window"]]
    cats = ("posting", "request", "none")
    FN = {"posting": 0.22, "request": 0.10, "none": 0.07}   # measured parser miss rates
    parsed, corrected, ns = [], [], []
    for c in cats:
        sel = [r for r in act if r["law"] == c]
        n = sum(r["n"] for r in sel); s = sum(r["disclosed"] for r in sel)
        p = s / n
        parsed.append(100 * p); corrected.append(100 * (p + (1 - p) * FN[c])); ns.append(n)
    fig, ax = plt.subplots(figsize=(9, 5.4), facecolor=SURFACE)
    x = range(len(cats))
    ax.bar([i - 0.19 for i in x], parsed, width=0.36,
           color=[COLOR[c] for c in cats], zorder=3)
    ax.bar([i + 0.19 for i in x], corrected, width=0.36,
           color=[COLOR[c] for c in cats], alpha=0.42, zorder=3,
           hatch="///", edgecolor=SURFACE, linewidth=1.6)
    for i, (a, b) in enumerate(zip(parsed, corrected)):
        ax.text(i - 0.19, a + 1.0, f"{a:.1f}%", ha="center", fontsize=10, color=INK)
        ax.text(i + 0.19, b + 1.0, f"~{b:.0f}%", ha="center", fontsize=10, color=INK_2)
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{LBL[c]}\nN={ns[i]:,}" for i, c in enumerate(cats)],
                       fontsize=9.5, color=INK)
    ax.set_ylabel("% of postings disclosing salary", fontsize=10, color=INK_2)
    ax.set_ylim(0, max(corrected) * 1.22)
    ax.yaxis.grid(True, color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    style(ax)
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    titles(fig, f"A posting mandate nearly triples salary disclosure ({parsed[0]/parsed[2]:.1f}x)",
           "Solid = measured in our index.  Hatched = adjusted for the measured parser miss rate.")
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)


ABBR = {"Colorado": "CO", "California": "CA", "Washington": "WA", "New York": "NY",
        "Hawaii": "HI", "District of Columbia": "DC", "Maryland": "MD", "Illinois": "IL",
        "Minnesota": "MN", "New Jersey": "NJ", "Vermont": "VT", "Massachusetts": "MA",
        "Virginia": "VA", "Maine": "ME", "Delaware": "DE"}


def fig3_wave(path):
    """Cumulative adoption on a TRUE date axis - spacing by event index would
    flatten the acceleration, which is the whole point of the figure."""
    import datetime as dt
    import matplotlib.dates as mdates
    events = sorted((v[1], k) for k, v in LAW.items() if v[0] == "posting")
    events.append(("2027-09-26", "Delaware"))
    # bucket by month: VA and ME are both July 2026 and would overlap as points
    by_date = {}
    for d, s in events:
        by_date.setdefault(d[:7], []).append(ABBR[s])
    dates = sorted(by_date)
    xs = [dt.date.fromisoformat(d + "-01") for d in dates]
    ys, run = [], 0
    for d in dates:
        run += len(by_date[d]); ys.append(run)
    # extend the line to "today" so the last step reads as a level, not a stop
    xs_p, ys_p = xs + [dt.date(2027, 12, 31)], ys + [ys[-1]]

    fig, ax = plt.subplots(figsize=(11, 5.6), facecolor=SURFACE)
    ax.step(xs_p, ys_p, where="post", color=C_POSTING, lw=2.2, zorder=3)
    ax.scatter(xs, ys, s=44, color=C_POSTING, zorder=4,
               edgecolor=SURFACE, linewidth=1.8)
    # all labels ABOVE the line (a below-label lands on the incoming flat segment);
    # alternate the height, and nudge horizontally where two effective dates are
    # only weeks apart (NJ 2025-06 / VT 2025-07) so the text boxes clear each other
    for i, (x, y, d) in enumerate(zip(xs, ys, dates)):
        dx = 0
        near_prev = i > 0 and (x - xs[i - 1]).days < 120
        near_next = i < len(xs) - 1 and (xs[i + 1] - x).days < 120
        if near_prev:
            dx = 16
        elif near_next:
            dx = -16
        ax.annotate("·".join(by_date[d]), (x, y), textcoords="offset points",
                    xytext=(dx, 12 if i % 2 == 0 else 27), ha="center",
                    fontsize=8.5, color=INK_2, weight="bold")
    today = dt.date(2026, 8, 20)
    ax.axvline(today, color=INK_2, lw=1.0, ls=(0, (4, 3)), zorder=2)
    ax.annotate("today", (today, 1.2), fontsize=8.5, color=INK_2,
                xytext=(5, 0), textcoords="offset points")
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.set_ylim(0, max(ys) + 2.4)
    ax.set_ylabel("Jurisdictions requiring salary in postings", fontsize=10, color=INK_2)
    ax.yaxis.grid(True, color=GRID, lw=0.8, zorder=0)
    ax.set_axisbelow(True)
    style(ax)
    fig.tight_layout(rect=[0, 0, 1, 0.9])
    titles(fig, "An active wave: one state in 2021, fifteen by 2027",
           "Cumulative jurisdictions requiring a salary range in job postings, by effective date")
    fig.savefig(path, dpi=150, facecolor=SURFACE)
    plt.close(fig)


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    rows = fetch_state_rates()
    json.dump(rows, open(os.path.join(here, "state_disclosure_rates.json"), "w"), indent=1)
    with open(os.path.join(here, "state_disclosure_rates.csv"), "w") as f:
        f.write("state,law_category,effective_date,postings,disclosed,"
                "pct_disclosing,ci95_pp,law_took_effect_mid_window\n")
        for r in rows:
            f.write(f"{r['state']},{r['law']},{r['effective'] or ''},{r['n']},"
                    f"{r['disclosed']},{r['pct']},{r['ci95']},"
                    f"{str(r['law_took_effect_mid_window']).lower()}\n")
    fig1_states(rows, os.path.join(here, "01_state_disclosure.png"))
    fig2_gap(rows, os.path.join(here, "02_mandate_gap.png"))
    fig3_wave(os.path.join(here, "03_regulation_wave.png"))

    act = [r for r in rows if not r["law_took_effect_mid_window"]]
    for c in ("posting", "request", "none"):
        sel = [r for r in act if r["law"] == c]
        n = sum(r["n"] for r in sel); s = sum(r["disclosed"] for r in sel)
        print(f"{c:<9} states={len(sel):>2} N={n:>7} pooled={100*s/n:5.1f}%")
    print(f"total N={sum(r['n'] for r in rows):,} across {len(rows)} states")


if __name__ == "__main__":
    main()
