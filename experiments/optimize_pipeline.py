"""
Optimized Pipeline: Include S*O, S*D, O*D interaction features
and polynomial features to help capture RPN = S x O x D structure.
"""

import os
import json
import warnings
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.cluster.hierarchy import dendrogram, linkage, fcluster
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score, RepeatedKFold
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_percentage_error
import xgboost as xgb
import shap

warnings.filterwarnings('ignore')
np.random.seed(42)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'cubesat_fmea_dataset.csv')
FIG_DIR = os.path.join(BASE_DIR, '..', 'artigo', 'figuras')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

DPI = 300
RANDOM_STATE = 42

print("=" * 60)
print("CubeSat FMEA RPN Estimation — Optimized Pipeline")
print("=" * 60)

# ============================================================
# STAGE 1: Load and engineer features
# ============================================================
print("\n[STAGE 1] Loading data and engineering features...")

df = pd.read_csv(DATA_PATH)
print(f"  Dataset: {len(df)} failure modes")

le_sub = LabelEncoder()
le_phase = LabelEncoder()
le_comp = LabelEncoder()

df['subsystem_enc'] = le_sub.fit_transform(df['subsystem'])
df['phase_enc'] = le_phase.fit_transform(df['mission_phase'])
df['comptype_enc'] = le_comp.fit_transform(df['component_type'])

# Interaction features (key: helps model learn multiplicative RPN structure)
df['S_x_O'] = df['S'] * df['O']
df['S_x_D'] = df['S'] * df['D']
df['O_x_D'] = df['O'] * df['D']

feature_cols = ['S', 'O', 'D', 'S_x_O', 'S_x_D', 'O_x_D',
                'subsystem_enc', 'phase_enc', 'comptype_enc']
feature_names = ['Severity', 'Occurrence', 'Detection', 'S×O', 'S×D', 'O×D',
                 'Subsystem', 'Mission Phase', 'Component Type']

X = df[feature_cols].values
y = df['RPN'].values

X_train, X_test, y_train, y_test, idx_train, idx_test = train_test_split(
    X, y, np.arange(len(df)), test_size=0.2, random_state=RANDOM_STATE
)
print(f"  Features: {len(feature_cols)} (including interaction terms)")
print(f"  Train: {len(X_train)}, Test: {len(X_test)}")

# ============================================================
# STAGE 2: Train models
# ============================================================
print("\n[STAGE 2] Training models...")

# XGBoost with broader grid
param_grid = {
    'n_estimators': [200, 300, 500],
    'max_depth': [3, 5, 7, 9],
    'learning_rate': [0.01, 0.05, 0.1],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0],
    'min_child_weight': [1, 3],
    'reg_alpha': [0, 0.1],
    'reg_lambda': [1, 2],
}

xgb_model = xgb.XGBRegressor(
    objective='reg:squarederror',
    random_state=RANDOM_STATE,
    n_jobs=-1
)

grid = GridSearchCV(
    xgb_model, param_grid,
    cv=5, scoring='r2', n_jobs=-1, verbose=0
)
grid.fit(X_train, y_train)
best_xgb = grid.best_estimator_
print(f"  XGBoost best params: {grid.best_params_}")

y_pred_xgb_test = best_xgb.predict(X_test)
y_pred_xgb_train = best_xgb.predict(X_train)

# Linear Regression
lr = LinearRegression()
lr.fit(X_train, y_train)
y_pred_lr_test = lr.predict(X_test)

# Random Forest
rf = RandomForestRegressor(n_estimators=300, max_depth=9, random_state=RANDOM_STATE, n_jobs=-1)
rf.fit(X_train, y_train)
y_pred_rf_test = rf.predict(X_test)

# ============================================================
# STAGE 3: Evaluate
# ============================================================
print("\n[STAGE 3] Model evaluation...")

def eval_model(y_true, y_pred, name):
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    print(f"  {name:20s} | R²={r2:.4f} | RMSE={rmse:.2f} | MAPE={mape:.2f}%")
    return {'model': name, 'R2': round(r2, 4), 'RMSE': round(rmse, 2), 'MAPE_pct': round(mape, 2)}

results = []
print("  --- Test set ---")
results.append(eval_model(y_test, y_pred_xgb_test, "XGBoost"))
results.append(eval_model(y_test, y_pred_lr_test, "Linear Regression"))
results.append(eval_model(y_test, y_pred_rf_test, "Random Forest"))

print("\n  --- Train set (XGBoost) ---")
eval_model(y_train, y_pred_xgb_train, "XGBoost (train)")

# Repeated k-fold CV
rkf = RepeatedKFold(n_splits=5, n_repeats=3, random_state=RANDOM_STATE)
cv_scores = cross_val_score(best_xgb, X, y, cv=rkf, scoring='r2')
print(f"\n  XGBoost Repeated 5-fold CV (3 repeats): R²={cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(RESULTS_DIR, 'model_comparison.csv'), index=False)

# Save summary
summary = {
    'dataset_size': len(df),
    'n_subsystems': int(df['subsystem'].nunique()),
    'n_features': len(feature_cols),
    'test_size': len(X_test),
    'train_size': len(X_train),
    'xgb_best_params': grid.best_params_,
    'xgb_test_r2': results[0]['R2'],
    'xgb_test_rmse': results[0]['RMSE'],
    'xgb_test_mape': results[0]['MAPE_pct'],
    'xgb_cv_r2_mean': round(cv_scores.mean(), 4),
    'xgb_cv_r2_std': round(cv_scores.std(), 4),
}
with open(os.path.join(RESULTS_DIR, 'summary.json'), 'w') as f:
    json.dump(summary, f, indent=2)

# ============================================================
# STAGE 4: SHAP
# ============================================================
print("\n[STAGE 4] SHAP analysis...")

X_df = pd.DataFrame(X, columns=feature_names)
explainer = shap.TreeExplainer(best_xgb)
shap_values = explainer.shap_values(X_df)

# Fig 3
print("  Fig. 3: SHAP Summary Plot...")
plt.figure(figsize=(7, 5))
shap.summary_plot(shap_values, X_df, show=False, plot_size=None)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig3_shap_summary.png'), dpi=DPI, bbox_inches='tight')
plt.close()

# Fig 4
print("  Fig. 4: SHAP Dependence Plot (Severity)...")
plt.figure(figsize=(7, 5))
shap.dependence_plot('Severity', shap_values, X_df, interaction_index='Subsystem', show=False)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig4_shap_dependence.png'), dpi=DPI, bbox_inches='tight')
plt.close()

# SHAP per subsystem
shap_per_sub = {}
for i, sub in enumerate(le_sub.classes_):
    mask = df['subsystem_enc'].values == i
    if mask.sum() > 0:
        ms = np.abs(shap_values[mask]).mean(axis=0)
        # Only compare S, O, D (indices 0, 1, 2)
        top = np.argmax(ms[:3])
        fmap = {0: 'Severity', 1: 'Occurrence', 2: 'Detection'}
        shap_per_sub[sub] = {
            'dominant_factor': fmap[top],
            'S': round(float(ms[0]), 2),
            'O': round(float(ms[1]), 2),
            'D': round(float(ms[2]), 2),
        }
        print(f"    {sub}: dominant={fmap[top]} (S={ms[0]:.1f}, O={ms[1]:.1f}, D={ms[2]:.1f})")

with open(os.path.join(RESULTS_DIR, 'shap_per_subsystem.json'), 'w') as f:
    json.dump(shap_per_sub, f, indent=2)

# ============================================================
# STAGE 5: Clustering
# ============================================================
print("\n[STAGE 5] Hierarchical clustering...")

scaler = StandardScaler()
cf = scaler.fit_transform(df[['S', 'O', 'D', 'RPN']].values)
Z = linkage(cf, method='ward')

# Fig 5
plt.figure(figsize=(10, 5))
dendrogram(Z, truncate_mode='lastp', p=30, leaf_rotation=90, leaf_font_size=8,
           color_threshold=0.7 * max(Z[:, 2]))
plt.xlabel('Failure Mode Index')
plt.ylabel('Ward Distance')
plt.title('Hierarchical Clustering Dendrogram')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig5_dendrogram.png'), dpi=DPI, bbox_inches='tight')
plt.close()

labels = fcluster(Z, t=3, criterion='maxclust')
df['cluster'] = labels

profiles = []
for c in sorted(df['cluster'].unique()):
    cd = df[df['cluster'] == c]
    rpn_m = cd['RPN'].mean()
    risk = 'High' if rpn_m > 350 else ('Intermediate' if rpn_m > 180 else 'Low')
    p = {
        'cluster': int(c), 'risk_level': risk, 'count': int(len(cd)),
        'RPN_mean': round(rpn_m, 1), 'RPN_min': int(cd['RPN'].min()),
        'RPN_max': int(cd['RPN'].max()),
        'S_mean': round(cd['S'].mean(), 1), 'O_mean': round(cd['O'].mean(), 1),
        'D_mean': round(cd['D'].mean(), 1),
        'subsystems': cd['subsystem'].value_counts().to_dict()
    }
    profiles.append(p)
    print(f"  Cluster {c} ({risk}): n={len(cd)}, RPN={p['RPN_min']}-{p['RPN_max']} (mean={rpn_m:.0f})")

with open(os.path.join(RESULTS_DIR, 'cluster_profiles.json'), 'w') as f:
    json.dump(profiles, f, indent=2)

# ============================================================
# STAGE 6: Remaining figures
# ============================================================
print("\n[STAGE 6] Remaining figures...")

# Fig 2
plt.figure(figsize=(7, 5))
order = df.groupby('subsystem')['RPN'].median().sort_values(ascending=False).index
sns.boxplot(data=df, x='subsystem', y='RPN', order=order, palette='Set2')
plt.xlabel('Subsystem')
plt.ylabel('Risk Priority Number (RPN)')
plt.title('RPN Distribution by CubeSat Subsystem')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig2_rpn_boxplot.png'), dpi=DPI, bbox_inches='tight')
plt.close()

# Fig 6
y_pred_all = best_xgb.predict(X)
plt.figure(figsize=(6, 6))
plt.scatter(y, y_pred_all, alpha=0.6, edgecolors='k', linewidth=0.5, s=40, c='steelblue')
mn = min(y.min(), y_pred_all.min()) - 20
mx = max(y.max(), y_pred_all.max()) + 20
plt.plot([mn, mx], [mn, mx], 'r--', lw=1.5, label='Perfect prediction')
plt.xlabel('Actual RPN')
plt.ylabel('Predicted RPN')
plt.title('XGBoost: Predicted vs. Actual RPN')
plt.legend()
plt.xlim(mn, mx)
plt.ylim(mn, mx)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig6_predicted_vs_actual.png'), dpi=DPI, bbox_inches='tight')
plt.close()

print("\n" + "=" * 60)
print("OPTIMIZED PIPELINE COMPLETE")
print("=" * 60)
print(f"\nModel comparison (test set):")
for r in results:
    print(f"  {r['model']:20s} | R²={r['R2']:.4f} | RMSE={r['RMSE']} | MAPE={r['MAPE_pct']}%")
print(f"\nXGBoost CV: R²={cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
print(f"\n5 figures saved to: {FIG_DIR}")
