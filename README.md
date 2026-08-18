# NSW HSC Results Explorer

One-paragraph summary: what the project does and the tech (Python, pandas, Streamlit).

## Data source
NESA/Board of Studies statistics archive — what you scraped, which years/subjects. Link + note it's public data. (Pull from your data/SOURCES.md.)

## Project structure
Short tree: src/, notebooks/ (01 scrape, 02 clean, 03 eda), dashboard/, data/ (raw→interim→processed).

## How to run
1. Create venv + `pip install -r requirements.txt`
2. (Data's already scraped; note the notebooks reproduce it)
3. `streamlit run dashboard/app.py`

## Key findings
3–4 bullets from your EDA (Maths Ext 2 enrolment surge, Legal Studies decline, flat band distributions, English Standard's near-zero Band 6).