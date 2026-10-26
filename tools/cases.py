"""Case-study prose. Every number comes from the project's own README. Estimates are labelled as estimates."""
from charts import *


def kpis(items):
    return '<ul class="kpis">' + "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in items) + "</ul>"


def table(head, rows, num_cols=()):
    th = "".join(f'<th{" class=num" if i in num_cols else ""}>{h}</th>' for i, h in enumerate(head))
    tr = "".join("<tr>" + "".join(f'<td{" class=num" if i in num_cols else ""}>{c}</td>' for i, c in enumerate(r)) + "</tr>" for r in rows)
    return f'<div class="tbl-wrap"><table class="tbl"><thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>'


CASES = {}

# ============================================================ 01 MF4
CASES["mf4-log-analytics"] = dict(
    says="The flagship. Two clocks, <mark>one</mark> truth.",
    lede="Dual-path controllers are hard to inspect by hand: two processors, separate time bases, hundreds of power-ups per test campaign. This pipeline reads the recordings and answers, for every start-up, which path came first, by how many milliseconds, and why.",
    live_label="Open the interactive workflow",
    beats=[
        ("Q", "Question", "Which processor starts first, and can I trust the timestamps?", f"""
<p>In a dual-path controller, a master and a slave processor each keep their own clock. To check a start-up rule you scroll through timestamps in a measurement tool, correct for the clock offset in your head, and repeat that for every power-up in every file.</p>
<p>A long-duration test campaign makes that expensive. My worked example: 10 recordings of about 4 GB each, with 57 to 60 start-ups per recording.</p>
{kpis([("≈585", "start-up cycles to check (570 to 600)"), ("≈10 min", "per cycle by hand (my estimate)"), ("95–100 h", "manual analysis, about 12 working days")])}
"""),
        ("M", "Method", "Find every power-up, correct the clocks, then check the answer a second way", """
<ol>
<li><b>Load.</b> Open large MF4 files lazily with <code>asammdf</code> and find the two path channel groups from their acquisition source.</li>
<li><b>Segment.</b> Split the recording into power-ups by detecting init-flag falling edges, merged within one second.</li>
<li><b>Measure.</b> Count resets per path, detect reboot data gaps, find each path's first application update.</li>
<li><b>Correct.</b> Estimate the clock offset between the paths from matching inter-processor alive-counter pairs, with a linear fit to absorb drift.</li>
<li><b>Cross-check.</b> Compute a second start difference from each path's own clock, which needs no offset estimate at all.</li>
<li><b>Judge.</b> Combine both into a verdict (<code>PA_FIRST</code>, <code>SAME_FRAME</code>, <code>PB_BEFORE_PA</code>, <code>INCONCLUSIVE</code>) and a result (<code>OK</code>, <code>NOK</code>, <code>CHECK</code>, <code>INFO</code>).</li>
<li><b>Report.</b> One CSV row per power-up (60 columns), plus a local browser dashboard with charts, a timeline view and filters.</li>
</ol>
<p><b>Why two methods?</b> The corrected difference depends on the offset estimate; the offset-free one does not. A violation is only reported when both agree, so false alarms from timestamp artefacts get filtered out.</p>
"""),
        ("R", "Result", "About 95 hours of checking becomes about 2.5 hours of unattended analysis", kpis([("95 h → 2.5 h", "estimated, per 10-recording campaign"), ("≈39×", "faster (97% less time)"), ("≈15 s", "per cycle, against about 10 min by hand")]) + """
<p>The bigger win is what the method catches. On the synthetic demo recording that ships with the repo, start-up #6 looks fine in the raw timestamps (+2.0 ms) but is a real violation once the 3.2 ms clock offset between the paths is removed.</p>
""" + fig(diverging([
            ("#1 clean start", 2.0, "bar-a", "OK"), ("#2 clean start", 0.8, "bar-a", "OK"), ("#3 same sample", 0.0, "bar-a", "OK"),
            ("#4 one reset", 1.2, "bar-a", "OK"), ("#5 resets on both", 0.6, "bar-a", "OK"), ("#6 path B first", -1.2, "bar-bad", "NOK"), ("#7 max resets", 5.0, "bar-c", "INFO")], -2, 6),
            "Bar chart of corrected start difference in milliseconds for seven synthetic power-ups. Start-up 6 is negative, minus 1.2 milliseconds, flagged NOK. The others are zero or positive.",
            "Corrected start difference (PB minus PA) for the 7 power-ups of the synthetic demo recording. Negative means path B started first. #6 is the violation the raw timestamps hid.") + """
<p>Everything runs from the command line or a dependency-free local dashboard (a small Python <code>http.server</code> backend and one HTML/JS page, bound to localhost). Results are cached by file, settings, signal map and script hash, so reopening a file is instant.</p>
"""),
        ("C", "Caveat", "What the numbers do and don’t say", """
<ul>
<li>The tool time was measured <b>once</b>, on a 3.4 GB recording (peak memory about 5.7 GB) while another analysis was running. Treat it as an upper bound.</li>
<li>The manual time per cycle (about 10 minutes) is <b>my estimate</b>, not a benchmark. Recording time and the time spent deciding what to fix are not counted, because they are needed either way.</li>
<li>The public repo uses a <b>synthetic</b> recording. Channel names are not hard-coded; a signal map file points the tool at real ones, and the real signal map stays out of git.</li>
</ul>
<p>The interactive workflow page lets you change those assumptions and see the estimate move.</p>
"""),
    ],
)

# ============================================================ 02 ChatGPT reviews
CASES["chatgpt-review-analysis"] = dict(
    says="Stars say <mark>how much</mark>. Text says why.",
    lede="A star rating shows how much users like an app, not why. The review text holds the why, but nobody can read 197,000 reviews by hand. So I taught Python to read them, and checked where it was wrong.",
    beats=[
        ("Q", "Question", "What do users feel about ChatGPT, how strongly, and about what?", """
<ol>
<li>What is the general <b>sentiment</b>? (polarity: positive, neutral, negative)</li>
<li>How <b>strong</b> are the opinions? (subjectivity: 0 factual to 1 opinionated)</li>
<li>Which <b>features</b> do people praise or criticise most?</li>
</ol>
<p>The data: Google Play reviews of the ChatGPT Android app, from 25 July 2023 to 23 August 2024.</p>
"""),
        ("M", "Method", "Clean, score, validate, then look for themes", """
<ul>
<li><b>Prepare.</b> Standardise column names, drop 6 empty reviews and 3,573 duplicate review IDs. Duplicate <i>text</i> stays: two people who wrote "good" are two votes.</li>
<li><b>Score.</b> TextBlob polarity and subjectivity. Positive above +0.05, negative below −0.05. Chosen because it returns both numbers, is fast and is explainable.</li>
<li><b>Validate.</b> Compare sentiment with star ratings, study the mismatches, and check non-English reviews separately.</li>
<li><b>Mine.</b> Top words and two-word phrases for 4–5★ and 1–2★ reviews, keeping negations so "not working" stays distinct.</li>
<li><b>Aspects.</b> Share of praise and criticism mentioning errors, login, pricing, accuracy and helpfulness.</li>
</ul>
"""),
        ("R", "Result", "People like it. They are annoyed by reliability and access, not by the AI", kpis([("193,148", "reviews after cleaning"), ("4.51 / 5", "average rating"), ("76 · 21 · 4", "% positive, neutral, negative"), ("0.25", "rating vs polarity (Spearman)")]) + fig(
            stack([("Positive", 76, "bar-good"), ("Neutral", 21, "bar-c"), ("Negative", 4, "bar-bad")]),
            "Stacked bar: 76 percent positive, 21 percent neutral, 4 percent negative reviews.",
            "Sentiment split of 193,148 reviews (rounded, so the parts sum to 101%).") + """
<p>Praise is about usefulness: <i>helpful, best ever, helps a lot, user friendly</i>. Criticism is mostly about reliability and access:</p>
""" + fig(pairs([("Errors & reliability", 18, 2), ("Answer accuracy", 14, 7), ("Login / verification", 11, 0.3), ("Pricing & limits", 8, 1)], 20, ("In 1–2★ reviews", "In 4–5★ reviews")),
            "Paired bars comparing how often four themes appear in low-star and high-star reviews. Errors and reliability: 18 percent versus 2 percent. Accuracy: 14 versus 7. Login: 11 versus 0.3. Pricing: 8 versus 1.",
            "Share of reviews mentioning each theme. Reliability and login problems are almost exclusive to low-star reviews.") + """
<p>Stars and text disagree more than you would expect: the correlation is only 0.25, and about 1 in 8 low-star reviews use clearly positive wording (probable mis-taps, mixed reviews, typos such as "Nott good").</p>
"""),
        ("C", "Caveat", "A lexicon-based model has blind spots", """
<ul>
<li>TextBlob misses sarcasm, slang and context, and the median review is only 4 words. About 20% of reviews score exactly 0.</li>
<li>It is English-only. Reviews with emoji or other languages land in "neutral" about twice as often (about 35% against 18%), which inflates the neutral share.</li>
<li>Aspect detection uses simple keyword rules, so the percentages are a lower bound.</li>
<li>One platform and about 13 months of data.</li>
</ul>
<p><b>Ideas for further work:</b> transformer-based multilingual sentiment, language detection, topic modelling on 1–2★ reviews, and linking review spikes to release dates.</p>
"""),
    ],
)

# ============================================================ 03 IT spend
CASES["it-expenditure-powerbi"] = dict(
    says="Watch the <mark>YTD trap</mark>. Plan is a full year.",
    lede="How does a large company keep $900M of IT spend honest? This dashboard compares plan, forecast and actuals across business areas, countries and cost types, and shows where the variance comes from.",
    beats=[
        ("Q", "Question", "Where do plan, forecast and actuals drift apart?", """
<ol>
<li><b>Cost distribution:</b> how spend splits across 7 business areas, 5 IT areas (38 sub-areas), 6 regions (30 countries) and 5 cost-element groups (23 sub-groups).</li>
<li><b>Budget and forecast alignment:</b> where are the largest gaps between actual, forecast and plan, over time and geography?</li>
<li><b>Structural drivers:</b> what drives deviations in areas such as internal versus external labour, shared services and R&amp;D planning?</li>
</ol>
"""),
        ("M", "Method", "Power Query prep, a clean model, DAX measures", """
<ul>
<li><b>Append and tag.</b> Combine the two sheets (81,610 + 12,119 rows) and tag each with a dataset period, so a single click can return to the original view.</li>
<li><b>Replace nulls with 0.</b> Each ERP row fills only one of actual, forecast or plan. Dropping rows with nulls would erase the budget.</li>
<li><b>Sort months properly.</b> Add a month number and quarter, and sort by column, so Power BI doesn't order months alphabetically.</li>
<li><b>Keep the credits.</b> 1,463 negative actual rows (about −$126M) are valid chargebacks and accrual reversals. Removing them would inflate net spend.</li>
<li><b>Measure.</b> Variance is defined once as <code>Actual − Plan</code>, so negative means underspend, and used everywhere.</li>
</ul>
<p>A Python EDA notebook sits alongside the dashboard for checks that are easier in code.</p>
"""),
        ("R", "Result", "Full-year actuals land 3.77% under plan", kpis([("$900.40M", "full-year plan"), ("$890.54M", "forecast"), ("$866.41M", "actual"), ("−$33.99M", "actual vs plan (−3.77%)")]) + fig(
            columns([("Plan", 900.40, "bar-a"), ("Forecast", 890.54, "bar-c"), ("Actual", 866.41, "bar-b")], 1000, lambda v: f"${v:,.2f}M"),
            "Three bars: plan 900.40 million dollars, forecast 890.54 million, actual 866.41 million.",
            "Full-year combined view, January to December, 93,729 rows. All three are close; the story is in the drill-downs.") + """
<p>The drill-downs are where the questions live: variance by business area and region, internal versus external labour, and a clear flag on Europe shared services overspend.</p>
"""),
        ("C", "Caveat", "Plan is a full year; actuals are not", """
<p>The first version of the numbers looked alarming: actuals 38% below plan. That is a comparison of eight months of actuals against twelve months of plan. The fair like-for-like view is January to August only:</p>
""" + fig(columns([("Plan", 611.31, "bar-a"), ("Forecast", 574.82, "bar-c"), ("Actual", 555.73, "bar-b")], 700, lambda v: f"${v:,.2f}M"),
          "Three bars for January to August: plan 611.31 million dollars, forecast 574.82 million, actual 555.73 million.",
          "Year-to-date, January to August: actual is 9.09% under plan and 3.32% under forecast.") + """
<ul>
<li>Use the <b>month slicer</b>, not the dataset-period filter, for a fair year-to-date comparison.</li>
<li>Replacing nulls with 0 is safe here only because each row fills exactly one measure.</li>
<li>This is a practice dataset, so the real-world causes of the variances are not known.</li>
</ul>
"""),
    ],
)

# ============================================================ 04 Coke
_months = [510750, 484975, 483530, 494888, 673573, 903838, 1041438, 945275, 681000, 623375, 795613, 1045775]
CASES["coke-sales-analysis"] = dict(
    says="The biggest market was <mark>not</mark> the most profitable.",
    lede="Selling more units is not enough. The goal is to sell the right products, in the right regions, through the right retailers, at a healthy margin. This workbook finds where that is and isn’t happening.",
    beats=[
        ("Q", "Question", "How can sales and profitability improve across US retailers?", """
<ol>
<li><b>Where:</b> how do sales vary by retailer, region, state and brand?</li>
<li><b>When:</b> is there a seasonal pattern in sales and margin?</li>
<li><b>How well:</b> where are margins strong, and where are they weak?</li>
</ol>
<p>The data: 3,888 invoice lines from 1 January to 31 December 2021, covering 4 retailers, 5 regions, 50 states and 6 brands.</p>
"""),
        ("M", "Method", "Everything live in Excel, margins weighted", """
<ul>
<li><b>Prepare.</b> No missing values or duplicates; real dates and numbers; header frozen, filters on; a <code>Month</code> helper column. The original file stays untouched.</li>
<li><b>Aggregate.</b> <code>SUMIFS</code> for every retailer, region, brand, month and state total.</li>
<li><b>Weight the margins.</b> Operating profit divided by sales, never a simple average of row-level percentages, so big orders count in proportion.</li>
<li><b>Show.</b> A dashboard with KPI tiles and 7 charts, colour-scale heatmaps (region × brand), and an <b>Explorer</b> sheet with dropdowns for retailer, region and brand.</li>
</ul>
"""),
        ("R", "Result", "Volume and profit point in different directions", kpis([("$8.68M", "total sales"), ("$3.17M", "operating profit"), ("36.5%", "weighted margin"), ("17.15M", "units sold")]) + fig(
            pairs([("Sodapop", 50.7, 37.4), ("FizzySip", 29.8, 32.3), ("BevCo", 14.9, 42.0), ("DreamCo", 4.7, 36.6)], 60, ("Share of sales", "Operating margin")),
            "Paired bars per retailer. Sodapop: 50.7 percent of sales at 37.4 percent margin. FizzySip: 29.8 percent of sales at 32.3 percent margin. BevCo: 14.9 percent of sales at 42.0 percent margin. DreamCo: 4.7 percent at 36.6 percent.",
            "Retailers: FizzySip is the second-largest account but has the thinnest margin. BevCo is small but the most profitable.") + """
<p>The same pattern shows by region: the <b>West</b> brings in about a third of sales at the lowest margin (32.6%), while the <b>South</b> is smaller but the most profitable (42.0%). Among brands, Coca-Cola leads at 39.3% and Diet Coke trails at 33.4%.</p>
<p>Demand is seasonal, and the margin barely moves, so the swings come from volume, not profitability:</p>
""" + fig(line(_months, ["J", "F", "M", "A", "M", "J", "J", "A", "S", "O", "N", "D"], 1_200_000, lambda v: f"${v / 1e6:.2f}M", mark=(6, 11)),
          "Line chart of monthly sales in 2021. Low from January to April at about 0.5 million dollars, peaks in July and December at about 1.04 million.",
          "Monthly sales, 2021. Peaks in July (summer) and December (holidays); margin stays between 35.8% and 37.0% all year.") + """
<p><b>What I would recommend:</b> renegotiate terms with FizzySip and in the West, grow BevCo and the South, time promotions around July and December, and review Diet Coke and Sprite pricing or costs.</p>
"""),
        ("C", "Caveat", "Three oddities I left in, and flagged", """
<ul>
<li><b>Zero-sale rows.</b> Units sold has a minimum of 0, so a few rows record no sales.</li>
<li><b>Wyoming and Utah are identical,</b> down to the cent: $199,937.50 in sales and $69,359.38 in profit.</li>
<li><b>South region = BevCo.</b> The two contain exactly the same rows.</li>
</ul>
<p>I kept them as supplied so the totals tie back to the source, and recommended verifying them with the data owner before acting on any of the findings.</p>
"""),
    ],
)

# ============================================================ 05 Test automation
CASES["python-test-automation"] = dict(
    says="Push the code. The <mark>report</mark> publishes itself.",
    lede="A small, honest pytest framework: tests run on every push, an interactive Allure report is published to GitHub Pages, and each test logs what went in, what was expected and what came out.",
    live_label="Open the live Allure report",
    beats=[
        ("Q", "Question", "Can a test suite run itself and leave a report anyone can read?", """
<p>Test results that live on one laptop are easy to doubt. The goal was a loop where pushing code runs the tests, builds a readable report and puts it online, so the evidence is public and repeatable.</p>
"""),
        ("M", "Method", "pytest, Allure and GitHub Actions, with simulated CAN", fig(
            flow([("git push", "to GitHub"), ("GitHub Actions", "CI workflow"), ("pytest", "runs the tests"), ("Allure", "builds the report"), ("GitHub Pages", "publishes it")]),
            "Flow diagram: git push triggers GitHub Actions, which runs pytest, builds an Allure report and publishes it to GitHub Pages.",
            "The pipeline from push to published report. Coverage is tracked with Codecov.") + """
<ul>
<li><b>Scenarios.</b> CAN message transmission, arbitration ID validation and payload verification, using <code>python-can</code> to simulate the bus.</li>
<li><b>Structured logging.</b> Every test records Input, Expected and Actual, so a failure explains itself in the report.</li>
<li><b>Structure.</b> <code>src/</code>, <code>tests/</code> and a shared <code>conftest.py</code>, so the framework can grow.</li>
</ul>
"""),
        ("R", "Result", "A report you can click through, built without touching a button", """
<p>The Allure report is live on GitHub Pages and refreshes on every push. It is a small project, but it contains the habits that matter in validation work: automated runs, reproducible evidence, and failures that say what happened.</p>
"""),
        ("C", "Caveat", "A starting point, not a production suite", """
<ul>
<li>It is a basic introduction to pytest with Allure, and the CAN bus is <b>simulated</b>. No hardware was involved.</li>
<li>It is licensed GPL-3.0 and meant to be read and borrowed.</li>
</ul>
<p><b>Next steps listed in the repo:</b> UDS diagnostic testing, real CAN hardware integration, parallel execution, and dashboard analytics.</p>
"""),
    ],
)

# ============================================================ 06 DSA
CASES["dsa-learning"] = dict(
    says="Learning in public means <mark>showing</mark> the messy middle.",
    lede="I’m learning data structures and algorithms in Python on the way to data science, and I’m doing it in public: practice files by level, interactive note pages, and a summary report that points at what to clean up next.",
    live_label="Open the live notes",
    beats=[
        ("Q", "Question", "Can I learn DSA in public and keep myself honest?", """
<p>Writing code is one thing; being able to explain it is another. The notes pages force the second: each topic gets a dry-run table or a graph builder you can click through.</p>
"""),
        ("M", "Method", "Three levels of practice, nine note pages, one summary report", fig(
            stack([("Basics", 6, "bar-c"), ("Intermediate", 16, "bar-b"), ("Advanced", 4, "bar-a")], unit=" files"),
            "Stacked bar of 26 Python practice files: 6 basics, 16 intermediate, 4 advanced.",
            "26 practice files by level.") + """
<ul>
<li><b>Practice.</b> Basics, intermediate and advanced folders of Python files.</li>
<li><b>Notes.</b> Nine interactive pages, such as a clickable dry-run table and a graph builder.</li>
<li><b>Review.</b> A summary report lists learning coverage, topic balance, the most ready files and the best next cleanup.</li>
</ul>
"""),
        ("R", "Result", "16 themes covered so far", """
<p>Linked lists, queues, stacks, heaps, dictionaries and sets; binary search, two pointers, recursion and matrix traversal; strings, trees, graphs and prime numbers; plus object-oriented classes and hash-based grouping.</p>
"""),
        ("C", "Caveat", "A learning log, not a library", """
<ul>
<li>The files are practice, at different levels of polish. The summary report itself marks which are ready and which need cleanup.</li>
<li>Nothing here is production code. It is evidence of habit: showing up, writing it down, and fixing what is weak.</li>
</ul>
"""),
    ],
)
