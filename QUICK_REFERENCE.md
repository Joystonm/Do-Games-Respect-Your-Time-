# Quick Reference Card

## 🚀 Launch

```bash
streamlit run app.py
```

## 🎯 The Core Insight

**37% of perceived game length is statistical noise**

- Median perceived: 3.5 hours
- Median adjusted: 2.2 hours
- 74% of games have <10 polls

## 📁 Key Files

| File | Purpose |
|------|---------|
| `app.py` | Streamlit editorial experience ⭐ |
| `data_engine.py` | Analysis engine |
| `viz_engine.py` | Visualization engine |
| `analysis.py` | Standalone HTML generator |
| `Do_Games_Respect_Your_Time.ipynb` | Jupyter notebook |

## 📊 Metrics

```python
Confidence Score = log(polls + 1)
Adjusted Time = time / confidence
Misrepresentation Risk = 1 / confidence
```

## 🎨 Visualizations

1. **Trust-Time Map** — Hero chart with annotated regions
2. **Genre Reliability** — Raw vs adjusted comparison
3. **Illusion Detector** — Perception gaps
4. **Sensitivity Analysis** — Threshold stability
5. **Confidence Distribution** — The crisis

## 🏆 Target Awards

- Best Storyteller
- Best Visualization
- Sherlock "Aha" Moment

## ✅ Quality Checklist

- [x] Original metrics
- [x] Distribution-first
- [x] Counterfactual reasoning
- [x] Editorial storytelling
- [x] Zero filler
- [x] Zero default styling
- [x] One memorable insight

## 📈 Key Stats

- 39,514 games analyzed
- 64 genres (min 20 games)
- Max rank shift: 17 positions
- Max perception gap: 40.8 hours

## 🔧 Dependencies

```bash
pip install pandas numpy plotly streamlit
```

## 📚 Documentation

- `README.md` — Project overview
- `UPGRADE_SUMMARY.md` — Technical details
- `JUDGES_SUMMARY.md` — Competition focus
- `CHECKLIST.md` — Completion status

## 💡 The Unforgettable Line

> Most games don't disrespect your time by being long.  
> They disrespect it by being **unmeasured**.

---

**This is research-grade data journalism, not business reporting.**
