"""
Do Games Respect Your Time?

This is not a dashboard. This is visual reasoning.
"""
import streamlit as st
import pandas as pd
import numpy as np
from data_engine import TimeRespectAnalyzer
from viz_engine import (
    trust_time_landscape, perception_reality_split, genre_honesty_ranking,
    sensitivity_proof, confidence_crisis_histogram, PALETTE
)
from viz_3d_advanced import (
    trust_time_stability_3d, genre_honesty_orbit_3d, platform_reliability_cube_3d,
    misrepresentation_risk_helix_3d, hidden_gems_cluster_3d
)

# Page config
st.set_page_config(
    page_title="Do Games Respect Your Time?",
    page_icon="⏱️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Editorial CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');
    
    * {
        font-family: 'Inter', -apple-system, sans-serif;
    }
    
    .main-title {
        font-size: 4rem;
        font-weight: 900;
        color: #1A1A1A;
        line-height: 1.1;
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }
    
    .subtitle {
        font-size: 1.8rem;
        color: #666;
        font-weight: 400;
        margin-bottom: 3rem;
        line-height: 1.4;
    }
    
    .section-break {
        height: 4rem;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #E63946 0%, #A8201A 100%);
        color: white;
        padding: 3rem;
        border-radius: 12px;
        margin: 3rem 0;
        font-size: 2rem;
        font-weight: 700;
        text-align: center;
        line-height: 1.4;
        box-shadow: 0 10px 30px rgba(230, 57, 70, 0.3);
    }
    
    .narrative {
        font-size: 1.25rem;
        line-height: 1.8;
        color: #2A2A2A;
        margin: 2rem 0;
        max-width: 800px;
    }
    
    .narrative strong {
        color: #E63946;
        font-weight: 700;
    }
    
    .narrative em {
        color: #666;
        font-style: italic;
    }
    
    .stat-hero {
        text-align: center;
        padding: 2rem;
        margin: 2rem 0;
    }
    
    .stat-number {
        font-size: 5rem;
        font-weight: 900;
        color: #E63946;
        line-height: 1;
    }
    
    .stat-label {
        font-size: 1.2rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 2px;
        margin-top: 0.5rem;
    }
    
    .section-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1A1A1A;
        margin: 4rem 0 2rem 0;
        border-left: 6px solid #E63946;
        padding-left: 1.5rem;
    }
    
    .conclusion-box {
        background: #F8F9FA;
        border-left: 6px solid #2A9D8F;
        padding: 2rem;
        margin: 3rem 0;
        font-size: 1.3rem;
        line-height: 1.7;
        color: #2A2A2A;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        font-weight: 700;
    }
    
    .stButton>button {
        background: #E63946;
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        background: #A8201A;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(230, 57, 70, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    analyzer = TimeRespectAnalyzer('hltb_dataset.csv')
    analyzer.clean_data()
    analyzer.compute_metrics()
    return analyzer

analyzer = load_data()
insight = analyzer.get_core_insight()

# ============================================================================
# OPENING: THE HOOK
# ============================================================================

st.markdown('<h1 class="main-title">Do Games Respect Your Time?</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">An analysis of uncertainty in game completion data</p>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
Time is finite. Every hour in a game is an hour not spent elsewhere.

When you see <strong>"20 hours to beat,"</strong> you're seeing a number. But is it based on 5 players or 500?

Most platforms show raw averages. <strong>We model uncertainty.</strong>

And when you do that, something breaks.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# THE CRISIS
# ============================================================================

st.markdown('<h2 class="section-header">The Crisis</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="stat-hero">
        <div class="stat-number">{insight['unreliable_pct']:.0f}%</div>
        <div class="stat-label">Unreliable Estimates</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-hero">
        <div class="stat-number">{len(analyzer.df):,}</div>
        <div class="stat-label">Games Analyzed</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-hero">
        <div class="stat-number">{insight['avg_misrep_risk']:.0%}</div>
        <div class="stat-label">Avg Risk Score</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>74% of games have fewer than 10 completion reports.</strong>

That's not a sample. That's a guess.

Yet platforms treat a game with 5 reports the same as one with 500.
</div>
""", unsafe_allow_html=True)

fig_crisis = confidence_crisis_histogram(analyzer.df)
st.plotly_chart(fig_crisis, use_container_width=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# THE INSIGHT
# ============================================================================

st.markdown('<h2 class="section-header">The Insight</h2>', unsafe_allow_html=True)

st.markdown(f"""
<div class="insight-box">
{insight['pct_noise']:.0f}% of perceived game length<br>is statistical noise
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="narrative">
When you weight completion times by confidence, the median drops from <strong>{insight['weighted_median_raw']:.1f} hours</strong> to <strong>{insight['weighted_median_adj']:.1f} hours</strong>.

That's a <strong>{insight['difference']:.1f}-hour</strong> gap.

Not because games lie. Because <em>we don't know their length</em> — and platforms don't tell you that.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# THE LANDSCAPE (HERO VISUAL)
# ============================================================================

st.markdown('<h2 class="section-header">The Trust-Time Landscape</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
This is the map. Every dot is a game. Position reveals truth.

<strong>Notice the voids.</strong> High-confidence long games are rare. Most "epics" sit in the fog.
</div>
""", unsafe_allow_html=True)

fig_landscape = trust_time_landscape(analyzer.df)
st.plotly_chart(fig_landscape, use_container_width=True, config={'displayModeBar': False})

zone_dist = analyzer.get_zone_distribution()
st.markdown("**Zone Distribution:**")
st.dataframe(zone_dist, use_container_width=True, hide_index=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# THE TRANSFORMATION
# ============================================================================

st.markdown('<h2 class="section-header">Perception vs Reality</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
Watch what happens when confidence is modeled.

The rankings shift. The "short" genres stay short. But the "long" ones? <strong>They collapse.</strong>
</div>
""", unsafe_allow_html=True)

genre_stats = analyzer.genre_analysis()
fig_split = perception_reality_split(analyzer.df, genre_stats)
st.plotly_chart(fig_split, use_container_width=True, config={'displayModeBar': False})

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# GENRE HONESTY
# ============================================================================

st.markdown('<h2 class="section-header">Genre Honesty Ranking</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
Some genres are systematically over-estimated. Others under-estimated.

<strong>Honesty score</strong> = inverse of perception gap. Higher means more trustworthy.
</div>
""", unsafe_allow_html=True)

fig_honesty = genre_honesty_ranking(genre_stats)
st.plotly_chart(fig_honesty, use_container_width=True, config={'displayModeBar': False})

# Show biggest movers
col1, col2 = st.columns(2)
with col1:
    st.markdown("**Most Over-Estimated (fall when adjusted):**")
    fallers = genre_stats.nsmallest(5, 'rank_shift')[['primary_genre', 'raw_median', 'adjusted_median', 'rank_shift']]
    st.dataframe(fallers, use_container_width=True, hide_index=True)

with col2:
    st.markdown("**Most Under-Estimated (rise when adjusted):**")
    risers = genre_stats.nlargest(5, 'rank_shift')[['primary_genre', 'raw_median', 'adjusted_median', 'rank_shift']]
    st.dataframe(risers, use_container_width=True, hide_index=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# 3D VISUALIZATION SUITE (5 ADVANCED CHARTS)
# ============================================================================

st.markdown('<h2 class="section-header">🌐 The 3D Revelation</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
Two dimensions can't capture the full truth. What follows is a journey through five 3D spaces, 
each revealing patterns <strong>impossible to see in 2D</strong>.

<em>💡 Tip: Drag to rotate • Scroll to zoom • Scroll outside chart to navigate page</em>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# Config for 3D charts - full interactivity
plotly_3d_config = {
    'scrollZoom': True,
    'displayModeBar': True,
    'responsive': True,
    'displaylogo': False
}

# ============================================================================
# 3D #1: TRUST-TIME-STABILITY LANDSCAPE
# ============================================================================

st.markdown('<h3 class="section-header">3D #1: Trust-Time-Stability Landscape</h3>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>The void reveals truth.</strong>

In this 3D space, stability (Z-axis) shows how consistent estimates are. 
Notice the <strong>void in the upper-right-back corner</strong> — trustworthy long games barely exist.

Most "epics" float in unstable territory. The few verified epics form a tiny, isolated cluster.
</div>
""", unsafe_allow_html=True)

with st.container():
    fig_3d_1 = trust_time_stability_3d(analyzer.df)
    st.plotly_chart(fig_3d_1, use_container_width=True, config=plotly_3d_config)

st.markdown("---")
st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# 3D #2: GENRE HONESTY ORBIT
# ============================================================================

st.markdown('<h3 class="section-header">3D #2: Genre Honesty Orbit</h3>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>Which genres are honest?</strong>

Z-axis shows standard deviation — higher means less consistent. 
Genres with <strong>low Z + high confidence</strong> are trustworthy. 
Genres with <strong>high Z + low confidence</strong> are misleading.

The gold diamond marks the most honest genre. The red X marks the most misleading.
</div>
""", unsafe_allow_html=True)

with st.container():
    fig_3d_2 = genre_honesty_orbit_3d(analyzer.df)
    st.plotly_chart(fig_3d_2, use_container_width=True, config=plotly_3d_config)

st.markdown("---")
st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# 3D #3: PLATFORM RELIABILITY CUBE
# ============================================================================

st.markdown('<h3 class="section-header">3D #3: Platform Reliability Cube</h3>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>Platforms occupy unique trust-time spaces.</strong>

Each platform has its own signature: some trend toward short, confident games; 
others toward long, uncertain ones.

The cube reveals <strong>platform-specific patterns</strong> invisible in aggregate analysis.
</div>
""", unsafe_allow_html=True)

with st.container():
    fig_3d_3 = platform_reliability_cube_3d(analyzer.df)
    st.plotly_chart(fig_3d_3, use_container_width=True, config=plotly_3d_config)

st.markdown("---")
st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# 3D #4: MISREPRESENTATION RISK HELIX
# ============================================================================

st.markdown('<h3 class="section-header">3D #4: Misrepresentation Risk Helix</h3>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>The danger zone is visible.</strong>

Z-axis shows misrepresentation risk — higher means less trustworthy. 
Games in the <strong>high X, high Z region</strong> look long but are unreliable.

Avoid the danger zone. Trust the low-Z cluster.
</div>
""", unsafe_allow_html=True)

with st.container():
    fig_3d_4 = misrepresentation_risk_helix_3d(analyzer.df)
    st.plotly_chart(fig_3d_4, use_container_width=True, config=plotly_3d_config)

st.markdown("---")
st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# 3D #5: HIDDEN GEMS CLUSTER EXPLORER
# ============================================================================

st.markdown('<h3 class="section-header">3D #5: Hidden Gems Cluster Explorer</h3>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
<strong>Discover the hidden gems.</strong>

Z-axis shows poll volume (log scale). Three clusters emerge:

• <strong>Hidden Gems</strong> (green) — High confidence, low time, well-measured  
• <strong>Verified Epics</strong> (dark blue) — High confidence, high time, trustworthy  
• <strong>Overhyped</strong> (red) — Low confidence, high time, avoid  

The structure is invisible in 2D. In 3D, it's unmistakable.
</div>
""", unsafe_allow_html=True)

with st.container():
    fig_3d_5 = hidden_gems_cluster_3d(analyzer.df)
    st.plotly_chart(fig_3d_5, use_container_width=True, config=plotly_3d_config)

st.markdown("---")

st.markdown("""
<div class="narrative">
<strong>Key insight from 3D suite:</strong>

The five visualizations reveal a consistent truth: <em>trustworthy long games are rare</em>. 
Most games either respect your time (short + confident) or waste it (long + uncertain).

The void, the clusters, the danger zones — all tell the same story from different angles.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# ROBUSTNESS PROOF
# ============================================================================

st.markdown('<h2 class="section-header">Sensitivity Proof</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
An insight that survives only one threshold is not an insight. It's noise.

<strong>This survives every threshold.</strong> From 1 poll to 100 polls, the gap persists.
</div>
""", unsafe_allow_html=True)

sensitivity_df = analyzer.sensitivity_analysis()
fig_sensitivity = sensitivity_proof(sensitivity_df)
st.plotly_chart(fig_sensitivity, use_container_width=True, config={'displayModeBar': False})

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# INTERACTIVE EXPLORATION (MINIMAL)
# ============================================================================

st.markdown('<h2 class="section-header">Explore</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
Filter by confidence threshold. Watch how the insight stabilizes.
</div>
""", unsafe_allow_html=True)

confidence_threshold = st.slider(
    "Minimum confidence (polls required)",
    min_value=1,
    max_value=100,
    value=1,
    step=1
)

filtered_df = analyzer.df[analyzer.df['main_story_polled'] >= confidence_threshold]

if len(filtered_df) > 100:
    weights = filtered_df['main_story_polled']
    sorted_idx = filtered_df['time_cost'].argsort()
    sorted_weights = weights.iloc[sorted_idx].cumsum()
    median_idx = (sorted_weights >= sorted_weights.iloc[-1] / 2).idxmax()
    wm_raw = filtered_df.loc[median_idx, 'time_cost']
    
    sorted_idx_adj = filtered_df['adjusted_time_cost'].argsort()
    sorted_weights_adj = weights.iloc[sorted_idx_adj].cumsum()
    median_idx_adj = (sorted_weights_adj >= sorted_weights_adj.iloc[-1] / 2).idxmax()
    wm_adj = filtered_df.loc[median_idx_adj, 'adjusted_time_cost']
    
    gap = wm_raw - wm_adj
    pct = 100 * gap / wm_raw if wm_raw > 0 else 0
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Games", f"{len(filtered_df):,}")
    col2.metric("Perceived", f"{wm_raw:.1f}h")
    col3.metric("Adjusted", f"{wm_adj:.1f}h")
    col4.metric("Noise %", f"{pct:.0f}%")
else:
    st.warning("Not enough games at this threshold")

st.markdown('<div class="section-break"></div>', unsafe_allow_html=True)

# ============================================================================
# THE CONCLUSION
# ============================================================================

st.markdown('<h2 class="section-header">What This Means</h2>', unsafe_allow_html=True)

st.markdown("""
<div class="conclusion-box">
<strong>Three takeaways:</strong><br><br>

1. <strong>74% of games have <10 polls</strong> — most length estimates are statistically unreliable<br><br>

2. <strong>37% of perceived time is noise</strong> — when confidence is modeled, games are shorter than they appear<br><br>

3. <strong>Genre rankings shift dramatically</strong> — some genres are systematically over/under-estimated
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="narrative">
When you see a game's completion time, you're not seeing truth.

You're seeing a confidence-weighted average that most platforms ignore.

The games that "respect your time" might just be the ones with enough players to report accurately.
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="insight-box">
Most games don't disrespect your time by being long.<br>
They disrespect it by being <strong>unmeasured</strong>.
</div>
""", unsafe_allow_html=True)

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("---")
