"""
Timeline Demo - Player Journey Analytics
"""
import streamlit as st
from timeline_viz import create_timeline_viz, generate_synthetic_journey, TIMELINE_PALETTE

st.set_page_config(page_title="Player Journey Timeline", layout="wide", initial_sidebar_state="collapsed")

# Custom CSS
st.markdown(f"""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    * {{
        font-family: 'Inter', sans-serif;
    }}
    
    .stApp {{
        background: {TIMELINE_PALETTE['bg']};
    }}
    
    .main-header {{
        font-size: 2.5rem;
        font-weight: 700;
        color: {TIMELINE_PALETTE['text']};
        margin-bottom: 0.5rem;
        letter-spacing: -0.02em;
    }}
    
    .sub-header {{
        font-size: 1.1rem;
        color: {TIMELINE_PALETTE['text_dim']};
        margin-bottom: 2rem;
        font-weight: 400;
    }}
    
    .metric-card {{
        background: {TIMELINE_PALETTE['surface']};
        border-radius: 12px;
        padding: 1.5rem;
        border: 1px solid {TIMELINE_PALETTE['grid']};
        backdrop-filter: blur(10px);
    }}
    
    .metric-label {{
        font-size: 0.85rem;
        color: {TIMELINE_PALETTE['text_dim']};
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 0.5rem;
    }}
    
    .metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {TIMELINE_PALETTE['text']};
    }}
    
    div[data-testid="stSelectbox"] > div {{
        background: {TIMELINE_PALETTE['surface']};
        border-radius: 8px;
        border: 1px solid {TIMELINE_PALETTE['grid']};
    }}
    
    div[data-testid="stSelectbox"] label {{
        color: {TIMELINE_PALETTE['text']} !important;
        font-weight: 600;
    }}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-header">Player Journey Analytics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">How game design affects time investment, retention, and engagement across playtime</div>', unsafe_allow_html=True)

# Generate data
df = generate_synthetic_journey(hours=100)

# Metric selector
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    metric = st.selectbox(
        'Select Metric',
        ['engagement', 'progress_time', 'dropoff', 'content_density', 'repetition'],
        format_func=lambda x: {
            'engagement': '📊 Engagement Index',
            'progress_time': '⏱️ Avg Time to Progress',
            'dropoff': '📉 Drop-off Rate',
            'content_density': '🎯 Content Density',
            'repetition': '🔁 Repetition Intensity'
        }[x]
    )

# Summary stats
with col2:
    avg_val = df[metric].mean()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Average</div>
        <div class="metric-value">{avg_val:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    peak_val = df[metric].max()
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Peak</div>
        <div class="metric-value">{peak_val:.1f}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Timeline visualization
fig = create_timeline_viz(df, metric)
st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

# Insights
st.markdown("<br>", unsafe_allow_html=True)

insights = {
    'engagement': '**Early Hook:** Strong initial engagement drops as novelty fades. Mid-game oscillation suggests content variety. Late-game decline indicates fatigue.',
    'progress_time': '**Pacing Analysis:** Time investment per milestone increases steadily. Spikes indicate difficulty walls or grinding requirements.',
    'dropoff': '**Retention Risk:** Drop-off accelerates in late game. Critical threshold around 60h where player commitment wanes.',
    'content_density': '**Content Efficiency:** High density early, declining as padding increases. Sinusoidal pattern suggests repetitive mission structure.',
    'repetition': '**Grind Detection:** Repetition intensity climbs sharply post-50h. Indicates content recycling and diminishing returns.'
}

st.markdown(f"""
<div class="metric-card">
    <div class="metric-label">Insight</div>
    <div style="color: {TIMELINE_PALETTE['text']}; font-size: 0.95rem; line-height: 1.6; margin-top: 0.5rem;">
        {insights[metric]}
    </div>
</div>
""", unsafe_allow_html=True)
