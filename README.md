# Do Games Respect Your Time?


## The Insight

**37% of perceived game length is statistical noise.**

When you account for how many players actually reported completion times, games are dramatically shorter than they appear. Most platforms show you raw averages,this project show you confidence-weighted truth.

## What Makes This Different

This isn't a dashboard. It's data journalism.

- **Original metrics** — Confidence-adjusted time cost (not raw averages)
- **Distribution-first** — Medians over means, long-tail awareness
- **Counterfactual reasoning** — What changes when uncertainty is modeled?
- **Editorial visuals** — Annotated insights, not default charts
- **One memorable finding** — 74% of games have <10 polls (unreliable estimates)

## Key Visualizations

1. **Trust-Time Map** — The hero chart. Where confidence meets completion time.
2. **Genre Reliability Ranking** — How rankings shift when confidence is modeled.
3. **Time Respect Score Leaderboard** — Top 10 most respectful games vs bottom 10 time wasters.
4. **Illusion of Length** — Games that seem longer than they are.
5. **Sensitivity Analysis** — How insights stabilize with more data.
6. **Confidence Distribution** — The crisis of unreliable estimates.

## Files

- `app.py` — **Streamlit editorial experience (MAIN DELIVERABLE)**
- `data_engine.py` — Modular analysis engine with enhanced metrics
- `viz_engine.py` — Editorial-quality visualization engine
- `Do_Games_Respect_Your_Time.ipynb` — Publication-ready notebook
- `analysis.py` — Standalone script (generates HTML visualizations)
- `hltb_dataset.csv` — Source data ([HowLongToBeat](https://www.kaggle.com/datasets/b4n4n4p0wer/how-long-to-beat-video-game-playtime-dataset/))

## Run It

```bash
# Install dependencies
pip install -r requirements.txt

# Launch Streamlit app (PRIMARY EXPERIENCE)
streamlit run app.py

# Alternative: Jupyter notebook
jupyter notebook Do_Games_Respect_Your_Time.ipynb

# Alternative: Standalone HTML generation
python3 analysis.py
```

## Architecture

**Modular Design:**
- `data_engine.py` — Data cleaning, metrics, filtering, analysis
- `viz_engine.py` — Plotly charts with editorial styling
- `app.py` — Streamlit narrative flow (scrollytelling)

**Enhanced Metrics:**
- Confidence score (log-scaled)
- Adjusted time cost (confidence-weighted)
- Misrepresentation risk indicator
- Sensitivity analysis across thresholds
- Genre-level rank shift detection
- **Time Respect Score (TRS)** — Composite metric combining length, confidence, and genre fit

## Methodology

**Confidence Score:** `log(polls + 1)`  
**Adjusted Time Cost:** `time / confidence`  
**Misrepresentation Risk:** `1 / confidence`  
**Time Respect Score:** `0.4×Length Penalty + 0.4×Confidence + 0.2×Genre Fit`  
**Sample:** 39,514 games (after 1% outlier removal)