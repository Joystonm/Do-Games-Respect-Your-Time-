import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Load data
df = pd.read_csv('hltb_dataset.csv')

# Core cleaning: keep only games with main_story data
df = df[df['type'] == 'game'].copy()
df = df[df['main_story_polled'].notna() & (df['main_story_polled'] > 0)].copy()
df = df[df['main_story'].notna() & (df['main_story'] > 0)].copy()

# Confidence score
df['confidence_score'] = np.log(df['main_story_polled'] + 1)

# Time cost
df['time_cost'] = df['main_story']

# Adjusted time cost
df['adjusted_time_cost'] = df['time_cost'] / df['confidence_score']

# Genre normalization
df['primary_genre'] = df['genres'].fillna('Unknown').str.split(',').str[0].str.strip()

# Remove extreme outliers (>99th percentile time)
time_99 = df['time_cost'].quantile(0.99)
df_clean = df[df['time_cost'] <= time_99].copy()

# Confidence tiers
df_clean['confidence_tier'] = pd.cut(df_clean['main_story_polled'], 
                                      bins=[0, 10, 50, 200, np.inf],
                                      labels=['Low (<10)', 'Medium (10-50)', 'High (50-200)', 'Very High (>200)'])

print(f"Total games: {len(df)}")
print(f"After cleaning: {len(df_clean)}")
print(f"Sample loss: {len(df) - len(df_clean)} ({100*(len(df)-len(df_clean))/len(df):.1f}%)")

# Genre analysis
genre_stats = df_clean.groupby('primary_genre').agg({
    'time_cost': ['median', 'count'],
    'confidence_score': 'median',
    'adjusted_time_cost': 'median',
    'main_story_polled': 'sum'
}).round(2)

genre_stats.columns = ['raw_median_hours', 'game_count', 'median_confidence', 'adjusted_median_hours', 'total_polls']
genre_stats = genre_stats[genre_stats['game_count'] >= 20].sort_values('adjusted_median_hours')

# Calculate ranking shift
genre_stats['raw_rank'] = genre_stats['raw_median_hours'].rank()
genre_stats['adjusted_rank'] = genre_stats['adjusted_median_hours'].rank()
genre_stats['rank_shift'] = genre_stats['raw_rank'] - genre_stats['adjusted_rank']

print("\n=== TOP GENRES BY ADJUSTED TIME ===")
print(genre_stats.head(10))

# 1. TRUST-TIME MAP (Hero Chart)
fig1 = go.Figure()

# Define regions
high_conf = df_clean['confidence_score'] > 3.5
low_time = df_clean['time_cost'] < 15
high_time = df_clean['time_cost'] > 40

# Sample for visualization (too many points)
sample = df_clean.sample(min(5000, len(df_clean)), random_state=42)

fig1.add_trace(go.Scatter(
    x=sample['time_cost'],
    y=sample['confidence_score'],
    mode='markers',
    marker=dict(
        size=np.sqrt(sample['main_story_polled'])/2,
        color=sample['confidence_score'],
        colorscale='Viridis',
        opacity=0.6,
        line=dict(width=0)
    ),
    text=sample['name'],
    hovertemplate='%{text}<br>Hours: %{x:.1f}<br>Confidence: %{y:.2f}<extra></extra>',
    showlegend=False
))

# Annotations
fig1.add_annotation(x=10, y=5, text="<b>Reliable Value</b><br>High confidence, low time",
                    showarrow=False, bgcolor="rgba(0,255,0,0.1)", font=dict(size=11))
fig1.add_annotation(x=80, y=2, text="<b>Questionable Grind</b><br>Long but uncertain",
                    showarrow=False, bgcolor="rgba(255,0,0,0.1)", font=dict(size=11))
fig1.add_annotation(x=50, y=1.5, text="<b>Statistical Mirage</b><br>Few reports, unreliable",
                    showarrow=False, bgcolor="rgba(255,255,0,0.1)", font=dict(size=11))

fig1.update_layout(
    title="The Trust-Time Map: Where Confidence Meets Completion",
    xaxis_title="Main Story Hours",
    yaxis_title="Confidence Score (log polls)",
    template="plotly_white",
    height=600,
    font=dict(size=12)
)

fig1.write_html('trust_time_map.html')

# 2. GENRE RELIABILITY RANKING
top_genres = genre_stats.head(15).sort_values('raw_median_hours')

fig2 = go.Figure()

fig2.add_trace(go.Bar(
    y=top_genres.index,
    x=top_genres['raw_median_hours'],
    name='Raw Median',
    orientation='h',
    marker=dict(color='lightgray')
))

fig2.add_trace(go.Bar(
    y=top_genres.index,
    x=top_genres['adjusted_median_hours'],
    name='Confidence-Adjusted',
    orientation='h',
    marker=dict(color='steelblue')
))

fig2.update_layout(
    title="Genre Rankings: How Confidence Changes Truth",
    xaxis_title="Hours to Complete",
    yaxis_title="",
    barmode='group',
    template="plotly_white",
    height=600,
    font=dict(size=12)
)

fig2.write_html('genre_reliability.html')

# 3. ILLUSION OF LENGTH
illusion_games = df_clean[df_clean['main_story_polled'] < 20].copy()
illusion_games['perceived_vs_adjusted'] = illusion_games['time_cost'] - illusion_games['adjusted_time_cost']
illusion_games = illusion_games.nlargest(20, 'perceived_vs_adjusted')

fig3 = go.Figure()

fig3.add_trace(go.Scatter(
    x=illusion_games['time_cost'],
    y=illusion_games['adjusted_time_cost'],
    mode='markers+text',
    marker=dict(size=12, color='red'),
    text=illusion_games['name'].str[:20],
    textposition='top center',
    textfont=dict(size=8)
))

fig3.add_trace(go.Scatter(
    x=[0, 100],
    y=[0, 100],
    mode='lines',
    line=dict(dash='dash', color='gray'),
    name='Perfect accuracy'
))

fig3.update_layout(
    title="The Illusion of Length: Games That Seem Longer Than They Are",
    xaxis_title="Perceived Time (raw hours)",
    yaxis_title="Adjusted Time (confidence-weighted)",
    template="plotly_white",
    height=600,
    font=dict(size=12)
)

fig3.write_html('illusion_of_length.html')

# Summary stats
print("\n=== KEY INSIGHT ===")
median_raw = df_clean['time_cost'].median()
median_adjusted = df_clean['adjusted_time_cost'].median()
print(f"Median raw time: {median_raw:.1f} hours")
print(f"Median adjusted time: {median_adjusted:.1f} hours")
print(f"Difference: {median_raw - median_adjusted:.1f} hours ({100*(median_raw-median_adjusted)/median_raw:.1f}%)")

# Misrepresentation risk
low_conf_games = df_clean[df_clean['main_story_polled'] < 10]
print(f"\nGames with <10 polls (high risk): {len(low_conf_games)} ({100*len(low_conf_games)/len(df_clean):.1f}%)")

print("\n✓ Analysis complete. Generated 3 visualizations.")
