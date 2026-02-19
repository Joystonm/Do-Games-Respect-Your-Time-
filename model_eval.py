"""
Model Evaluation - Time Respect Prediction Analysis
Research-grade ML performance visualization
"""
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split

MODEL_PALETTE = {
    'bg': '#0f1419',
    'surface': '#1a1f2e',
    'grid': '#2a3441',
    'text': '#e8eaed',
    'text_dim': '#9aa0a6',
    'logistic': '#66bb6a',
    'gradient': '#8ab4f8',
    'baseline': '#9aa0a6',
    'positive': '#66bb6a',
    'negative': '#ef5350'
}

def prepare_model_data(df):
    """Prepare features for time respect prediction"""
    # Create binary target: high time respect (top 30%)
    threshold = df['time_respect_score'].quantile(0.70) if 'time_respect_score' in df.columns else df['confidence_score'].quantile(0.70)
    
    if 'time_respect_score' in df.columns:
        y = (df['time_respect_score'] >= threshold).astype(int)
    else:
        y = (df['confidence_score'] >= threshold).astype(int)
    
    # Feature engineering
    features = pd.DataFrame({
        'time_efficiency': 1 / (df['main_story'] + 1),
        'content_density': np.log1p(df['main_story_polled']),
        'repetition_rate': df.get('main_extras', df['main_story']) / (df['main_story'] + 1),
        'completion_rate': np.clip(df['main_story_polled'] / df['main_story_polled'].median(), 0, 2),
        'dropoff_risk': df['main_story'] / 50
    })
    
    # Handle missing values
    features = features.fillna(features.median())
    
    return features, y

def train_models(X, y):
    """Train prediction models and compute ROC curves"""
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Logistic Regression
    lr = LogisticRegression(random_state=42, max_iter=1000)
    lr.fit(X_train, y_train)
    lr_probs = lr.predict_proba(X_test)[:, 1]
    lr_fpr, lr_tpr, _ = roc_curve(y_test, lr_probs)
    lr_auc = auc(lr_fpr, lr_tpr)
    
    # Gradient Boosting
    gb = GradientBoostingClassifier(random_state=42, n_estimators=100)
    gb.fit(X_train, y_train)
    gb_probs = gb.predict_proba(X_test)[:, 1]
    gb_fpr, gb_tpr, _ = roc_curve(y_test, gb_probs)
    gb_auc = auc(gb_fpr, gb_tpr)
    
    return {
        'logistic': {'fpr': lr_fpr, 'tpr': lr_tpr, 'auc': lr_auc, 'model': lr},
        'gradient': {'fpr': gb_fpr, 'tpr': gb_tpr, 'auc': gb_auc, 'model': gb}
    }

def create_roc_curve(results):
    """Create ROC curve visualization"""
    fig = go.Figure()
    
    # Gradient Boosting
    fig.add_trace(go.Scatter(
        x=results['gradient']['fpr'],
        y=results['gradient']['tpr'],
        mode='lines',
        name=f"Gradient Boosting (AUC={results['gradient']['auc']:.3f})",
        line=dict(color=MODEL_PALETTE['gradient'], width=3),
        hovertemplate='FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra></extra>'
    ))
    
    # Logistic Regression
    fig.add_trace(go.Scatter(
        x=results['logistic']['fpr'],
        y=results['logistic']['tpr'],
        mode='lines',
        name=f"Logistic Regression (AUC={results['logistic']['auc']:.3f})",
        line=dict(color=MODEL_PALETTE['logistic'], width=3),
        hovertemplate='FPR: %{x:.3f}<br>TPR: %{y:.3f}<extra></extra>'
    ))
    
    # Random baseline
    fig.add_trace(go.Scatter(
        x=[0, 1],
        y=[0, 1],
        mode='lines',
        name='Random Baseline',
        line=dict(color=MODEL_PALETTE['baseline'], width=2, dash='dash'),
        hoverinfo='skip'
    ))
    
    fig.update_layout(
        plot_bgcolor=MODEL_PALETTE['bg'],
        paper_bgcolor=MODEL_PALETTE['bg'],
        font=dict(family='Inter, sans-serif', color=MODEL_PALETTE['text'], size=12),
        xaxis=dict(
            title='False Positive Rate',
            gridcolor=MODEL_PALETTE['grid'],
            gridwidth=1,
            showgrid=True,
            zeroline=False,
            range=[0, 1],
            title_font=dict(size=13)
        ),
        yaxis=dict(
            title='True Positive Rate',
            gridcolor=MODEL_PALETTE['grid'],
            gridwidth=1,
            showgrid=True,
            zeroline=False,
            range=[0, 1],
            title_font=dict(size=13)
        ),
        legend=dict(
            orientation='v',
            yanchor='bottom',
            y=0.02,
            xanchor='right',
            x=0.98,
            bgcolor='rgba(0,0,0,0.3)',
            bordercolor=MODEL_PALETTE['grid'],
            borderwidth=1,
            font=dict(size=11)
        ),
        margin=dict(l=60, r=20, t=20, b=60),
        height=450,
        hovermode='closest'
    )
    
    return fig

def get_feature_importance(model, feature_names):
    """Extract feature importance/coefficients"""
    if hasattr(model, 'coef_'):
        importance = model.coef_[0]
    elif hasattr(model, 'feature_importances_'):
        importance = model.feature_importances_
    else:
        importance = np.ones(len(feature_names))
    
    # Normalize to percentages
    abs_importance = np.abs(importance)
    pct_importance = 100 * abs_importance / abs_importance.sum()
    
    return pd.DataFrame({
        'feature': feature_names,
        'coefficient': importance,
        'importance': pct_importance,
        'impact': ['Positive' if x > 0 else 'Negative' for x in importance]
    }).sort_values('importance', ascending=False)

def create_feature_importance_viz(importance_df):
    """Create feature importance horizontal bar chart"""
    fig = go.Figure()
    
    colors = [MODEL_PALETTE['positive'] if imp > 0 else MODEL_PALETTE['negative'] 
              for imp in importance_df['coefficient']]
    
    fig.add_trace(go.Bar(
        y=importance_df['feature'],
        x=importance_df['importance'],
        orientation='h',
        marker=dict(color=colors, opacity=0.8),
        text=[f"{val:.1f}%" for val in importance_df['importance']],
        textposition='outside',
        hovertemplate='<b>%{y}</b><br>Importance: %{x:.1f}%<extra></extra>'
    ))
    
    fig.update_layout(
        plot_bgcolor=MODEL_PALETTE['bg'],
        paper_bgcolor=MODEL_PALETTE['bg'],
        font=dict(family='Inter, sans-serif', color=MODEL_PALETTE['text'], size=12),
        xaxis=dict(
            title='Importance (%)',
            gridcolor=MODEL_PALETTE['grid'],
            gridwidth=1,
            showgrid=True,
            zeroline=False,
            title_font=dict(size=13)
        ),
        yaxis=dict(
            title='',
            showgrid=False,
            tickfont=dict(size=12)
        ),
        margin=dict(l=150, r=80, t=20, b=60),
        height=450,
        showlegend=False
    )
    
    return fig
