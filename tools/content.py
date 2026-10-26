"""All editable content for the site lives here. Run `python3 tools/build.py` from the repo root to regenerate the pages.

Rules the content follows:
  * Every number comes from the project's own README, or is labelled as an estimate.
  * No employer, job title, salary, notice period or job-search signal appears on the site.
  * A skill chip only exists if a repo (or, where labelled "course", a dated course) backs it.
"""

SITE = "https://anuj-nagar-0910.github.io"
NAME = "Anuj Nagar"
LINKEDIN = "https://www.linkedin.com/in/anuj-n-478690143/"
GITHUB = "https://github.com/Anuj-Nagar-0910"
SUBSTACK = "https://unfogit.substack.com/"
EMAIL_U, EMAIL_D = "anuj456nagar", "gmail.com"
UPDATED = "2026-10-26"

# ------------------------------------------------------------------ writing (UnFogIt)
# (date, tag, title, slug-url). Title is split at the first ": " into headline + deck.
POSTS = [
    ("2026-10-26", "Biology", "The Lilliputian Molecule: How DNA Sequencing Solved a 90-Year-Old Mystery of Mushrooms That Make People See Tiny Humans", "the-lilliputian-molecule-how-dna"),
    ("2026-10-26", "Space", "The Triple Engine: How Webb Caught Three Feeding Supermassive Black Holes Colliding in a Single Dawn-Era Galaxy", "the-triple-engine-how-webb-caught"),
    ("2026-10-26", "AI", "The Softmax Fix: How Google's Jonathan Barron Solved a Decade-Old Floating-Point Bug in Deep Learning's Core Engine", "the-softmax-fix-how-googles-jonathan"),
    ("2026-10-25", "Space", "The Magnetic Tapestry: How Sunrise III's Stratospheric Balloon Telescope Uncovered the Twisted 3D Web Powering the \"Quiet\" Sun", "the-magnetic-tapestry-how-sunrise"),
    ("2026-10-25", "AI", "The Algorithmic Mob: How Exposure to Peer Counts Drives LLM Agent Swarms into Runaway, Irreversible Herding Cascades", "the-algorithmic-mob-how-exposure"),
    ("2026-10-24", "Biology", "The Living Thermometer of Stress: How Dual-Color Bioluminescent Plants Report Hidden Disease by Shifting Their Glow Color", "the-living-thermometer-of-stress"),
    ("2026-10-24", "Biology", "The Pentagonal Lock: How Oxford Scientists Filmed Viruses Building Themselves One Molecule at a Time Without a Blueprint", "the-pentagonal-lock-how-oxford-scientists"),
    ("2026-10-24", "Space", "The Shifting Vacuum: How 2,884 Exploding Stars Reveal That Dark Energy Is Changing Over Cosmic Time", "the-shifting-vacuum-how-2884-exploding"),
    ("2026-10-23", "AI", "The Sycophancy Stamp: How Reinforcement Learning Accidentally Bakes Spineless Flattery into 741 AI Models", "the-sycophancy-stamp-how-reinforcement"),
    ("2026-10-23", "Mind", "The Line of Doubt: Why 75% of Humans Will Deny Their Own Eyes to Agree with a Room (The Asch Conformity Study)", "the-line-of-doubt-why-75-of-humans"),
    ("2026-10-23", "Quantum", "The Cultivated Qubit: How Google's Willow Processor Slashes Quantum Error Overhead 40-Fold with Magic State Cultivation", "the-cultivated-qubit-how-googles"),
    ("2026-10-23", "Biology", "The 60-Year Reset: How Direct Cell Reprogramming Erases Six Decades of Epigenetic Aging Without Stem Cell Chaos", "the-60-year-reset-how-direct-cell"),
]

# ------------------------------------------------------------------ projects (lab entries)
PROJECTS = [
    dict(
        slug="mf4-log-analytics", n="01", title="MF4 Log Analytics",
        short="Which processor started first, and by how many milliseconds?",
        tools=["Python", "pandas", "NumPy", "asammdf"], period="Oct 2026",
        repo="https://github.com/Anuj-Nagar-0910/mf4-log-analytics",
        live="https://anuj-nagar-0910.github.io/mf4-log-analytics/workflow.html",
        meta_title="MF4 Log Analytics: ECU Start-up Analysis in Python",
        meta_desc="A Python and pandas pipeline that reads MF4 (MDF4) recordings and checks every ECU power-up in minutes, not hours. Method, results and caveats.",
        facts=[("Period", "Built and published Oct 2026"), ("Stack", "Python, pandas, NumPy, asammdf, HTML/JS dashboard"), ("Data", "Synthetic demo recordings (no proprietary logs)"), ("Licence", "MIT, open source")],
    ),
    dict(
        slug="chatgpt-review-analysis", n="02", title="ChatGPT Review Analysis",
        short="What do 193,148 app reviews actually say?",
        tools=["Python", "TextBlob", "NLP", "Jupyter"], period="Oct 2026",
        repo="https://github.com/Anuj-Nagar-0910/Chat-Gpt-Review-Analysis",
        live=None,
        meta_title="ChatGPT Review Analysis: Sentiment on 193K Reviews",
        meta_desc="Sentiment and feature analysis of 193,148 Google Play reviews of the ChatGPT app in Python. Findings, method and the limits of a lexicon-based approach.",
        facts=[("Period", "Built Oct 2026; reviews Jul 2023 to Aug 2024"), ("Stack", "Python 3.12, pandas, TextBlob, NLTK, seaborn, scikit-learn"), ("Data", "196,727 raw reviews, 193,148 after cleaning"), ("Context", "Crio.Do DA-201, session 5")],
    ),
    dict(
        slug="it-expenditure-powerbi", n="03", title="Global IT Spend in Power BI",
        short="Where does a $900M plan drift from the forecast and the actuals?",
        tools=["Power BI", "DAX", "Power Query", "Python EDA"], period="Oct 2026",
        repo="https://github.com/Anuj-Nagar-0910/it-expenditure-analysis-powerbi",
        live=None,
        meta_title="Global IT Spend Dashboard in Power BI: Plan vs Actual",
        meta_desc="A Power BI dashboard on $900M of IT spend: plan versus forecast versus actual, variance drill-downs, DAX measures, Power Query prep and a Python EDA notebook.",
        facts=[("Period", "Built Oct 2026"), ("Stack", "Power BI Desktop, DAX, Power Query, Python notebook"), ("Data", "93,729 rows, 7 business areas, 30 countries"), ("Context", "Crio.Do DA-201, session 7")],
    ),
    dict(
        slug="coke-sales-analysis", n="04", title="Coca-Cola US Sales in Excel",
        short="Selling more is not the same as earning more.",
        tools=["Excel", "SUMIFS", "Dashboards"], period="Oct 2026",
        repo="https://github.com/Anuj-Nagar-0910/Coke-Sales-Analysis",
        live=None,
        meta_title="Coca-Cola US Retail Sales Analysis in Excel",
        meta_desc="An Excel dashboard on 3,888 invoice lines of 2021 US beverage sales: retailer, region and brand margins, seasonality and data-quality flags.",
        facts=[("Period", "Built Oct 2026; data covers 2021"), ("Stack", "Microsoft Excel: SUMIFS, conditional formatting, data validation"), ("Data", "3,888 invoice lines, 4 retailers, 50 states"), ("Context", "Crio.Do DA-201, session 4")],
    ),
    dict(
        slug="python-test-automation", n="05", title="Python Test Automation Framework",
        short="CAN tests that run, report and publish themselves on every push.",
        tools=["pytest", "Allure", "GitHub Actions", "python-can"], period="Mar 2026",
        repo="https://github.com/Anuj-Nagar-0910/python-testing-automation",
        live="https://anuj-nagar-0910.github.io/python-testing-automation/",
        meta_title="Python Test Automation with pytest, Allure and CI",
        meta_desc="A small pytest framework with Allure reports published to GitHub Pages by GitHub Actions on every push, using python-can to simulate CAN message tests.",
        facts=[("Period", "Built Mar 2026"), ("Stack", "Python 3.11, pytest, Allure, GitHub Actions, python-can"), ("Data", "Simulated CAN messages, no hardware"), ("Licence", "GPL-3.0, open source")],
    ),
    dict(
        slug="dsa-learning", n="06", title="Python DSA Learning Log",
        short="26 practice files and 9 interactive note pages, in public.",
        tools=["Python", "Algorithms", "Data structures"], period="Mar to May 2026",
        repo="https://github.com/Anuj-Nagar-0910/DSA_Learning",
        live="https://anuj-nagar-0910.github.io/DSA_Learning/",
        meta_title="Python DSA Learning Log: Notes and Practice",
        meta_desc="A public log of Python data structures and algorithms practice: 26 practice files across three levels and 9 interactive note pages.",
        facts=[("Period", "Mar to May 2026"), ("Stack", "Python, HTML/JS note pages"), ("Scope", "26 Python files, 9 note pages, 16 themes"), ("Status", "Learning log, not a library")],
    ),
]

SKETCHES = [
    ("awesome-prompts", "Jul 2025", "A small curated set of prompts for code generation, creative writing, extraction and summarisation.", "https://github.com/Anuj-Nagar-0910/awesome-prompts"),
    ("smart-dashboard-demos", "Jul 2025", "A D3.js dashboard with rolling live charts for warehouse temperature and humidity.", "https://github.com/Anuj-Nagar-0910/smart-dashboard-demos"),
    ("study-tracker", "Jul 2025", "A single-page study tracker in plain HTML and JavaScript.", "https://github.com/Anuj-Nagar-0910/study-tracker"),
    ("ollama-qdrant-demos", "Jul 2025", "Placeholder repo for a local-LLM plus vector-search idea. Early prototype, not a finished pipeline.", "https://github.com/Anuj-Nagar-0910/ollama-qdrant-demos"),
    ("langchain-n8n-pipelines", "Jul 2025", "Placeholder repo for a LangChain and n8n document-to-questions idea. Early prototype, not a finished pipeline.", "https://github.com/Anuj-Nagar-0910/langchain-n8n-pipelines"),
    ("Trending-Media-Dashboard", "Jul 2025", "An n8n automation idea for a trending-media dashboard. Early prototype.", "https://github.com/Anuj-Nagar-0910/Trending-Media-Dashboard"),
]
SKETCH_PAGES = [
    ("Interactive guide: an n8n Medium article agent", "/interactive-medium-guide.html"),
    ("Jingle research guide", "/jingle-research-guide.html"),
]

# ------------------------------------------------------------------ lab log (dated, newest first)
# kind: built | learned | wrote | next
LOG = [
    ("2026-10-26", "built", "MF4 Log Analytics goes public", "Open-sourced the pipeline and dashboard, with a synthetic demo recording so anyone can run it, plus an interactive workflow page.", "/work/mf4-log-analytics/"),
    ("2026-10-26", "built", "Global IT spend dashboard in Power BI", "Plan versus forecast versus actual on 93,729 rows, with DAX measures, Power Query prep and a Python EDA notebook.", "/work/it-expenditure-powerbi/"),
    ("2026-10-23", "wrote", "Twelve new UnFogIt explainers", "Between 23 and 26 October: dark energy, quantum error correction, plant biosensors and more. Each takes a paper too dense for headlines and says what it found, in plain words.", "/writing/"),
    ("2026-10-20", "built", "ChatGPT review analysis", "Sentiment and aspect analysis on 193,148 app reviews. Learned the hard way that star ratings and review text disagree more than you would expect.", "/work/chatgpt-review-analysis/"),
    ("2026-10-17", "built", "Coca-Cola sales dashboard in Excel", "SUMIFS, heatmaps and a dropdown explorer. The biggest market was not the most profitable one.", "/work/coke-sales-analysis/"),
    ("2026-09-24", "learned", "Power BI and Tableau", "Crio.Do course completed.", None),
    ("2026-09-02", "learned", "Data analysis with Python", "Crio.Do course completed: pandas, cleaning, exploration.", None),
    ("2026-07-15", "learned", "Intermediate Python", "Crio.Do course completed.", None),
    ("2026-06-15", "learned", "Python foundations", "Crio.Do course completed.", None),
    ("2026-05-15", "learned", "Excel foundations", "Crio.Do course completed.", None),
    ("2026-05-02", "built", "DSA learning log updated", "Nine interactive note pages and 26 practice files so far.", "/work/dsa-learning/"),
    ("2026-04-15", "learned", "SQL foundations", "Crio.Do course completed.", None),
    ("2026-03-26", "built", "pytest + Allure + CI for CAN tests", "A small framework that publishes its own report to GitHub Pages on every push.", "/work/python-test-automation/"),
    ("2025-07-05", "built", "First experiments in public", "Prompt collections, an n8n workflow idea, a D3 dashboard. Some of them are only placeholders, and they live on the Sketches shelf.", "/work/#sketches"),
]
# month-level dates are approximate for course completions: shown as month only
MONTH_ONLY = {"2026-07-15", "2026-06-15", "2026-05-15", "2026-04-15"}

BENCH = [
    ("In progress", "Finish the Crio.Do DA-201 capstone", "The data analytics programme has one big project left. It goes on this site as entry 07 when it is done."),
    ("Plan", "A second analytics project on public telemetry data", "Same habits as the MF4 work (two methods, a clear verdict, honest caveats), but on data anyone can download and check."),
    ("Plan", "A chart in every UnFogIt piece", "Pull one number out of each paper and draw it, so a reader can see the claim as well as read it."),
]

# evidence chips: (label, kind, url). kind "repo" links to a repo; "course" links to the lab log.
CHIPS = [
    ("Python", "repo", "https://github.com/Anuj-Nagar-0910/mf4-log-analytics"),
    ("pandas", "repo", "https://github.com/Anuj-Nagar-0910/mf4-log-analytics"),
    ("NumPy", "repo", "https://github.com/Anuj-Nagar-0910/mf4-log-analytics"),
    ("asammdf", "repo", "https://github.com/Anuj-Nagar-0910/mf4-log-analytics"),
    ("NLP", "repo", "https://github.com/Anuj-Nagar-0910/Chat-Gpt-Review-Analysis"),
    ("Power BI", "repo", "https://github.com/Anuj-Nagar-0910/it-expenditure-analysis-powerbi"),
    ("DAX", "repo", "https://github.com/Anuj-Nagar-0910/it-expenditure-analysis-powerbi"),
    ("Excel", "repo", "https://github.com/Anuj-Nagar-0910/Coke-Sales-Analysis"),
    ("pytest", "repo", "https://github.com/Anuj-Nagar-0910/python-testing-automation"),
    ("GitHub Actions", "repo", "https://github.com/Anuj-Nagar-0910/python-testing-automation"),
    ("D3.js", "repo", "https://github.com/Anuj-Nagar-0910/smart-dashboard-demos"),
    ("SQL", "course", "/lab-log/"),
    ("Tableau", "course", "/lab-log/"),
]
