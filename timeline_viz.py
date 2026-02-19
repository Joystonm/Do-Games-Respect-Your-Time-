"""
Premium Timeline Visualization - Player Journey Analytics
Research-grade temporal engagement modeling
"""
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline

TIMELINE_PALETTE = {
    'bg': '#1a1d23',
    'surface': '#252932',
    'text': '#e8eaed',
    'text_dim': '#9aa0a6',
    'accent': '#8ab4f8',
    'warning': '#ffa726',
    'danger': '#ef5350',
    'success': '#66bb6a',
    'grid': '#3c4043'
}

def generate_synthetic_journey(hours=100, seed=42):
    """Generate realistic player journey data"""
    np.random.seed(seed)
    x = np.linspace(0, hours, 50)
    
    # Base engagement curve with phases
    early = np.exp(-x/10) * 30 + 70
    mid = 60 + 10 * np.sin(x/15)
    late = 50 - x/10
    engagement = np.where(x < 20, early, np.where(x < 60, mid, late))
    engagement = np.clip(engagement + np.random.normal(0, 3, len(x)), 20, 100)
    
    # Metrics
    progress_time = 2 + (x/20) + np.random.normal(0, 0.3, len(x))
    dropoff = 5 + (x/5) + np.where(x > 40, (x-40)/2, 0) + np.random.normal(0, 2, len(x))
    content_density = 70 - (x/3) + 10*np.sin(x/10) + np.random.normal(0, 4, len(x))
    repetition = 20 + (x/2) + np.where(x > 50, (x-50)*0.8, 0) + np.random.normal(0, 3, len(x))
    
    return pd.DataFrame({
        'hours': x,
        'engagement': engagement,
        'progress_time': np.clip(progress_time, 0.5, 10),
        'dropoff': np.clip(dropoff, 0, 50),
        'content_density': np.clip(content_density, 20, 100),
        'repetition': np.clip(repetition, 10, 80)
    })

def smooth_curve(x, y, points=200):
    """Smooth curve interpolation"""
    if len(x) < 4:
        return x, y
    x_smooth = np.linspace(x.min(), x.max(), points)
    spl = make_interp_spline(x, y, k=3)
    y_smooth = spl(x_smooth)
    return x_smooth, y_smooth

def create_timeline_viz(df=None, selected_metric='engagement'):
    """Premium timeline visualization"""
    if df is None:
        df = generate_synthetic_journey()
    
    metrics = {
        'engagement': {'label': 'Engagement Index', 'color': TIMELINE_PALETTE['accent'], 'suffix': '%'},
        'progress_time': {'label': 'Avg Time to Progress', 'color': TIMELINE_PALETTE['warning'], 'suffix': 'h'},
        'dropoff': {'label': 'Drop-off Rate', 'color': TIMELINE_PALETTE['danger'], 'suffix': '%'},
        'content_density': {'label': 'Content Density', 'color': TIMELINE_PALETTE['success'], 'suffix': '%'},
        'repetition': {'label': 'Repetition Intensity', 'color': '#ab47bc', 'suffix': '%'}
    }
    
    metric_info = metrics[selected_metric]
    x_smooth, y_smooth = smooth_curve(df['hours'].values, df[selected_metric].values)
    
    fig = go.Figure()
    
    # Phase backgrounds
    phases = [
        {'range': [0, 20], 'label': 'Early Game', 'color': 'rgba(138,180,248,0.08)'},
        {'range': [20, 60], 'label': 'Mid Game', 'color': 'rgba(255,167,38,0.08)'},
        {'range': [60, 80], 'label': 'Late Game', 'color': 'rgba(239,83,80,0.08)'},
        {'range': [80, 100], 'label': 'Post-Game', 'color': 'rgba(171,71,188,0.08)'}
    ]
    
    for phase in phases:
        fig.add_vrect(
            x0=phase['range'][0], x1=phase['range'][1],
            fillcolor=phase['color'], layer='below',
            line_width=0, annotation_text=phase['label'],
            annotation_position='top left',
            annotation=dict(font_size=10, font_color=TIMELINE_PALETTE['text_dim'])
        )
    
    # Main line with glow
    fig.add_trace(go.Scatter(
        x=x_smooth, y=y_smooth,
        mode='lines',
        line=dict(color=metric_info['color'], width=4, shape='spline'),
        fill='tozeroy',
        fillcolor=f"rgba{tuple(list(bytes.fromhex(metric_info['color'][1:])) + [0.15])}",
        name=metric_info['label'],
        hovertemplate='<b>%{x:.1f}h</b><br>%{y:.1f}' + metric_info['suffix'] + '<extra></extra>'
    ))
    
    # Glow effect
    fig.add_trace(go.Scatter(
        x=x_smooth, y=y_smooth,
        mode='lines',
        line=dict(color=metric_info['color'], width=12, shape='spline'),
        opacity=0.2,
        showlegend=False,
        hoverinfo='skip'
    ))
    
    # Critical points annotation
    peaks = df.nlargest(2, selected_metric)
    valleys = df.nsmallest(2, selected_metric)
    
    for _, point in peaks.iterrows():
        fig.add_annotation(
            x=point['hours'], y=point[selected_metric],
            text='Peak',
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowwidth=1.5,
            arrowcolor=TIMELINE_PALETTE['text_dim'],
            ax=0, ay=-40,
            font=dict(size=10, color=TIMELINE_PALETTE['text']),
            bgcolor=TIMELINE_PALETTE['surface'],
            borderpad=4
        )
    
    fig.update_layout(
        plot_bgcolor=TIMELINE_PALETTE['bg'],
        paper_bgcolor=TIMELINE_PALETTE['bg'],
        font=dict(family='Inter, sans-serif', color=TIMELINE_PALETTE['text']),
        xaxis=dict(
            title='Total Playtime (Hours)',
            gridcolor=TIMELINE_PALETTE['grid'],
            showgrid=True,
            zeroline=False,
            title_font=dict(size=13, color=TIMELINE_PALETTE['text_dim'])
        ),
        yaxis=dict(
            title=metric_info['label'],
            gridcolor=TIMELINE_PALETTE['grid'],
            showgrid=True,
            zeroline=False,
            title_font=dict(size=13, color=TIMELINE_PALETTE['text_dim'])
        ),
        hovermode='x unified',
        hoverlabel=dict(
            bgcolor=TIMELINE_PALETTE['surface'],
            font_size=12,
            font_family='Inter, sans-serif'
        ),
        margin=dict(l=60, r=40, t=40, b=60),
        height=500,
        showlegend=False
    )
    
    return fig
