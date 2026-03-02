# ============================================
# UX ANALYSIS DASHBOARD
# Author: [Ton Prénom]
# Stack: Python, Pandas, Plotly
# ============================================

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# ============================================
# DATA
# ============================================

# Funnel de conversion
df_funnel = pd.DataFrame({
    'etape': ['Visiteurs', 'Navigation', 'Fiche Produit',
              'Ajout Panier', 'Checkout', 'Paiement', 'Achat Confirmé'],
    'users': [10000, 7200, 4800, 2900, 2100, 1380, 920],
    'drop_rate': [0, 28, 33, 40, 28, 34, 33]
})

# Sévérité heuristiques
df_heuristic = pd.DataFrame({
    'heuristique': [
        'Visibilité statut', 'Correspondance monde réel',
        'Liberté utilisateur', 'Cohérence standards',
        'Prévention erreurs', 'Reconnaissance vs rappel',
        'Flexibilité', 'Design minimaliste',
        'Gestion erreurs', 'Aide & documentation'
    ],
    'severite': [3, 2, 4, 3, 4, 2, 1, 3, 3, 2],
    'priorite': ['Haute', 'Moyenne', 'Critique', 'Haute', 'Critique',
                 'Moyenne', 'Faible', 'Haute', 'Haute', 'Moyenne']
})

# Matrice Impact/Effort
df_matrix = pd.DataFrame({
    'recommandation': [
        'Simplifier checkout', 'Afficher frais livraison',
        'Validation temps réel', 'Uniformiser CTA',
        'Loader visible', 'Refonte recherche',
        'Redesign fiches produit', 'Checkout one-page',
        'FAQ contextuelle', "Messages d'erreur"
    ],
    'impact': [5, 4, 4, 3, 3, 5, 4, 5, 2, 2],
    'effort': [2, 1, 2, 1, 1, 4, 3, 4, 1, 1],
    'categorie': [
        'Quick Win', 'Quick Win', 'Quick Win', 'Quick Win', 'Quick Win',
        'Projet Majeur', 'Projet Majeur', 'Projet Majeur',
        'Fill-in', 'Fill-in'
    ]
})

# Abandon par étape
df_abandon = pd.DataFrame({
    'etape': ['Recherche→Produit', 'Checkout→Paiement',
              'Panier→Checkout', 'Produit→Panier', 'Accueil→Navigation'],
    'taux_abandon': [35, 28, 18, 40, 28]
})

# Before/After simulation
df_before_after = pd.DataFrame({
    'metrique': ['Taux Conversion', 'Abandon Panier',
                 'Abandon Checkout', 'Score NPS', 'Temps Checkout (min)'],
    'avant': [0.92, 68, 28, 32, 8.5],
    'apres': [1.15, 46, 18, 47, 3.2]
})

# ============================================
# COLORS
# ============================================
colors = {
    'bg': '#0a0e1a',
    'card': '#141828',
    'accent1': '#00d4ff',
    'accent2': '#7c3aed',
    'accent3': '#10b981',
    'accent4': '#f59e0b',
    'danger': '#ef4444',
    'text': '#e2e8f0',
    'subtext': '#94a3b8'
}

cat_colors = {
    'Quick Win': colors['accent3'],
    'Projet Majeur': colors['accent2'],
    'Fill-in': colors['accent4']
}

priority_colors = {
    'Critique': colors['danger'],
    'Haute': colors['accent4'],
    'Moyenne': colors['accent1'],
    'Faible': colors['accent3']
}

# ============================================
# FIGURE
# ============================================
fig = make_subplots(
    rows=3, cols=3,
    subplot_titles=(
        '🔻 Funnel de Conversion',
        '⚠️ Sévérité des Problèmes UX',
        '📉 Taux d\'Abandon par Étape (%)',
        '🎯 Matrice Impact / Effort',
        '📊 Before / After — KPIs UX',
        '🏆 Priorités de Recommandations'
    ),
    specs=[
        [{"type": "xy"}, {"type": "xy"}, {"type": "xy"}],
        [{"type": "xy"}, {"type": "xy"}, {"type": "xy"}],
        [{"type": "xy", "colspan": 3}, None, None]
    ],
    vertical_spacing=0.14,
    horizontal_spacing=0.08
)

# --- Funnel
fig.add_trace(go.Funnel(
    y=df_funnel['etape'],
    x=df_funnel['users'],
    textinfo='value+percent initial',
    marker_color=[colors['accent3'], colors['accent1'], colors['accent1'],
                  colors['accent4'], colors['accent4'], colors['danger'], colors['danger']],
    connector=dict(line=dict(color=colors['subtext'], width=1))
), row=1, col=1)

# --- Sévérité heuristiques (Bar horizontal)
sev_colors = [priority_colors[p] for p in df_heuristic['priorite']]
fig.add_trace(go.Bar(
    y=df_heuristic['heuristique'],
    x=df_heuristic['severite'],
    orientation='h',
    marker_color=sev_colors,
    hovertemplate='%{y}<br>Sévérité: %{x}/4<extra></extra>'
), row=1, col=2)

# --- Taux d'abandon
fig.add_trace(go.Bar(
    y=df_abandon['etape'],
    x=df_abandon['taux_abandon'],
    orientation='h',
    marker_color=colors['danger'],
    hovertemplate='%{y}<br>Abandon: %{x}%<extra></extra>'
), row=1, col=3)

# --- Matrice Impact/Effort (Scatter)
for cat, color in cat_colors.items():
    mask = df_matrix['categorie'] == cat
    fig.add_trace(go.Scatter(
        x=df_matrix[mask]['effort'],
        y=df_matrix[mask]['impact'],
        mode='markers+text',
        name=cat,
        text=df_matrix[mask]['recommandation'],
        textposition='top center',
        textfont=dict(size=8, color=colors['text']),
        marker=dict(size=16, color=color, opacity=0.9,
                    line=dict(width=2, color='white')),
        hovertemplate='%{text}<br>Impact: %{y}/5<br>Effort: %{x}/5<extra></extra>'
    ), row=2, col=1)

# Lignes de référence matrice
fig.add_hline(y=3, line_dash='dot', line_color=colors['subtext'], opacity=0.5, row=2, col=1)
fig.add_vline(x=2.5, line_dash='dot', line_color=colors['subtext'], opacity=0.5, row=2, col=1)

# --- Before/After
metriques_norm = df_before_after['metrique']
fig.add_trace(go.Bar(
    name='Avant optimisation',
    x=metriques_norm,
    y=df_before_after['avant'],
    marker_color=colors['danger'],
    opacity=0.8
), row=2, col=2)

fig.add_trace(go.Bar(
    name='Après optimisation',
    x=metriques_norm,
    y=df_before_after['apres'],
    marker_color=colors['accent3'],
    opacity=0.8
), row=2, col=2)

# --- Recommandations par priorité (Donut)
priority_counts = df_heuristic['priorite'].value_counts()
fig.add_trace(go.Pie(
    labels=priority_counts.index,
    values=priority_counts.values,
    hole=0.55,
    marker_colors=[priority_colors.get(p, colors['subtext']) for p in priority_counts.index],
    hovertemplate='%{label}: %{value} problèmes<extra></extra>'
), row=2, col=3)

# --- Timeline d'implémentation (Gantt simplifié)
gantt_data = [
    ('Semaine 1-2', 'Quick Wins CTA & Frais livraison', 1, 2, 'Quick Win'),
    ('Semaine 2-3', 'Validation formulaires', 2, 3, 'Quick Win'),
    ('Semaine 3-4', 'Simplification Checkout', 3, 4, 'Quick Win'),
    ('Semaine 4-6', 'Redesign fiches produit', 4, 6, 'Projet Majeur'),
    ('Semaine 5-8', 'Refonte moteur recherche', 5, 8, 'Projet Majeur'),
    ('Semaine 6-10', 'Checkout one-page', 6, 10, 'Projet Majeur'),
]

for task_label, task_name, start, end, cat in gantt_data:
    fig.add_trace(go.Bar(
        x=[end - start],
        y=[task_name],
        base=[start],
        orientation='h',
        marker_color=cat_colors[cat],
        hovertemplate=f'{task_name}<br>Semaines {start}–{end}<extra></extra>',
        showlegend=False
    ), row=3, col=1)

# ============================================
# LAYOUT
# ============================================
fig.update_layout(
    title=dict(
        text='🎨 UX Analysis Dashboard — Optimisation Parcours d\'Achat 2024',
        font=dict(size=26, color=colors['text'], family='Inter'),
        x=0.5, xanchor='center'
    ),
    paper_bgcolor=colors['bg'],
    plot_bgcolor=colors['card'],
    font=dict(color=colors['text'], family='Inter'),
    height=1200,
    barmode='group',
    showlegend=True,
    legend=dict(
        bgcolor=colors['card'],
        bordercolor=colors['accent1'],
        borderwidth=1,
        font=dict(size=10)
    ),
    margin=dict(t=100, b=40, l=40, r=40)
)

for annotation in fig['layout']['annotations']:
    annotation['font'] = dict(size=12, color=colors['accent1'])

fig.update_xaxes(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)')
fig.update_yaxes(gridcolor='rgba(255,255,255,0.05)', linecolor='rgba(255,255,255,0.1)',
                 tickfont=dict(size=9))

fig.update_xaxes(title_text='Effort (1=Faible → 5=Élevé)', row=2, col=1)
fig.update_yaxes(title_text='Impact (1=Faible → 5=Élevé)', row=2, col=1)
fig.update_xaxes(title_text='Semaine', row=3, col=1)

fig.write_html("dashboard/ux_dashboard.html")
fig.write_image("dashboard/ux_dashboard.png", width=1400, height=1200, scale=2)

print("✅ UX Dashboard exporté : ux_dashboard.html & ux_dashboard.png")
