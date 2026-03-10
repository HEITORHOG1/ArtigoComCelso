"""
Pipeline: XGBoost + SHAP + Hierarchical Clustering for CubeSat FMEA RPN Estimation
Authors: Goncalves, Pereira, Pereira (2026)
IEEE Access submission
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
from scipy.spatial.distance import pdist
from sklearn.model_selection import train_test_split, GridSearchCV, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_percentage_error
import xgboost as xgb
import shap

warnings.filterwarnings('ignore')
np.random.seed(42)

# --- Paths ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, '..', 'data', 'cubesat_fmea_dataset.csv')
FIG_DIR = os.path.join(BASE_DIR, '..', 'artigo', 'figuras')
RESULTS_DIR = os.path.join(BASE_DIR, 'results')
os.makedirs(FIG_DIR, exist_ok=True)
os.makedirs(RESULTS_DIR, exist_ok=True)

# --- Configuration ---
DPI = 300
RANDOM_STATE = 42
CV_FOLDS = 5
TEST_SIZE = 0.2

print("=" * 60)
print("CubeSat FMEA RPN Estimation Pipeline")
print("=" * 60)

# ============================================================
# STAGE 1: Load and preprocess data
# ============================================================
print("\n[STAGE 1] Loading and preprocessing data...")

df = pd.read_csv(DATA_PATH)
print(f"  Dataset loaded: {len(df)} failure modes")
print(f"  Subsystems: {df['subsystem'].value_counts().to_dict()}")
print(f"  RPN range: {df['RPN'].min()} - {df['RPN'].max()}")

# Encode categorical features
le_subsystem = LabelEncoder()
le_phase = LabelEncoder()
le_comptype = LabelEncoder()

df['subsystem_enc'] = le_subsystem.fit_transform(df['subsystem'])
df['mission_phase_enc'] = le_phase.fit_transform(df['mission_phase'])
df['component_type_enc'] = le_comptype.fit_transform(df['component_type'])

# Feature matrix and target
feature_cols = ['S', 'O', 'D', 'subsystem_enc', 'mission_phase_enc', 'component_type_enc']
X = df[feature_cols].values
y = df['RPN'].values

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE
)
print(f"  Train: {len(X_train)}, Test: {len(X_test)}")

# ============================================================
# STAGE 2: Train models
# ============================================================
print("\n[STAGE 2] Training models...")

# --- 2a: XGBoost with GridSearchCV ---
print("  Training XGBoost with GridSearchCV...")
param_grid = {
    'n_estimators': [100, 200, 300],
    'max_depth': [3, 5, 7],
    'learning_rate': [0.05, 0.1, 0.2],
    'subsample': [0.8, 1.0],
    'colsample_bytree': [0.8, 1.0],
}

xgb_model = xgb.XGBRegressor(
    objective='reg:squarederror',
    random_state=RANDOM_STATE,
    n_jobs=-1
)

grid_search = GridSearchCV(
    xgb_model, param_grid,
    cv=CV_FOLDS,
    scoring='r2',
    n_jobs=-1,
    verbose=0
)
grid_search.fit(X_train, y_train)

best_xgb = grid_search.best_estimator_
print(f"  Best params: {grid_search.best_params_}")

# XGBoost predictions
y_pred_xgb_train = best_xgb.predict(X_train)
y_pred_xgb_test = best_xgb.predict(X_test)

# --- 2b: Linear Regression baseline ---
print("  Training Linear Regression baseline...")
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
y_pred_lr_test = lr_model.predict(X_test)

# --- 2c: Random Forest baseline ---
print("  Training Random Forest baseline...")
rf_model = RandomForestRegressor(
    n_estimators=200, max_depth=7, random_state=RANDOM_STATE, n_jobs=-1
)
rf_model.fit(X_train, y_train)
y_pred_rf_test = rf_model.predict(X_test)

# ============================================================
# STAGE 3: Evaluate models
# ============================================================
print("\n[STAGE 3] Evaluating models...")

def evaluate(y_true, y_pred, name):
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mape = mean_absolute_percentage_error(y_true, y_pred) * 100
    print(f"  {name:20s} | R²={r2:.4f} | RMSE={rmse:.2f} | MAPE={mape:.2f}%")
    return {'model': name, 'R2': round(r2, 4), 'RMSE': round(rmse, 2), 'MAPE': round(mape, 2)}

results = []
results.append(evaluate(y_test, y_pred_xgb_test, "XGBoost"))
results.append(evaluate(y_test, y_pred_lr_test, "Linear Regression"))
results.append(evaluate(y_test, y_pred_rf_test, "Random Forest"))

# Cross-validation R² for XGBoost
cv_scores = cross_val_score(best_xgb, X, y, cv=CV_FOLDS, scoring='r2')
print(f"\n  XGBoost {CV_FOLDS}-fold CV R²: {cv_scores.mean():.4f} ± {cv_scores.std():.4f}")

# Save results
results_df = pd.DataFrame(results)
results_df.to_csv(os.path.join(RESULTS_DIR, 'model_comparison.csv'), index=False)
print(f"  Results saved to results/model_comparison.csv")

# ============================================================
# STAGE 4: SHAP analysis
# ============================================================
print("\n[STAGE 4] SHAP explainability analysis...")

feature_names = ['Severity', 'Occurrence', 'Detection', 'Subsystem', 'Mission Phase', 'Component Type']
X_df = pd.DataFrame(X, columns=feature_names)

explainer = shap.TreeExplainer(best_xgb)
shap_values = explainer.shap_values(X_df)

# Fig 3: SHAP Summary Plot
print("  Generating SHAP Summary Plot (Fig. 3)...")
plt.figure(figsize=(7, 5))
shap.summary_plot(shap_values, X_df, show=False, plot_size=None)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig3_shap_summary.png'), dpi=DPI, bbox_inches='tight')
plt.close()

# Fig 4: SHAP Dependence Plot (Severity, colored by Subsystem)
print("  Generating SHAP Dependence Plot (Fig. 4)...")
plt.figure(figsize=(7, 5))
shap.dependence_plot(
    'Severity', shap_values, X_df,
    interaction_index='Subsystem',
    show=False
)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig4_shap_dependence.png'), dpi=DPI, bbox_inches='tight')
plt.close()

# SHAP importance per subsystem
print("  Computing SHAP importance per subsystem...")
shap_per_subsystem = {}
subsystem_names = le_subsystem.classes_
for i, sub in enumerate(subsystem_names):
    mask = df['subsystem_enc'].values == i
    if mask.sum() > 0:
        mean_abs_shap = np.abs(shap_values[mask]).mean(axis=0)
        top_feature_idx = np.argmax(mean_abs_shap[:3])  # Only S, O, D
        feature_map = {0: 'Severity', 1: 'Occurrence', 2: 'Detection'}
        shap_per_subsystem[sub] = {
            'dominant_factor': feature_map[top_feature_idx],
            'mean_shap_S': round(float(mean_abs_shap[0]), 2),
            'mean_shap_O': round(float(mean_abs_shap[1]), 2),
            'mean_shap_D': round(float(mean_abs_shap[2]), 2),
        }
        print(f"    {sub}: dominant={feature_map[top_feature_idx]} "
              f"(S={mean_abs_shap[0]:.2f}, O={mean_abs_shap[1]:.2f}, D={mean_abs_shap[2]:.2f})")

with open(os.path.join(RESULTS_DIR, 'shap_per_subsystem.json'), 'w') as f:
    json.dump(shap_per_subsystem, f, indent=2)

# ============================================================
# STAGE 5: Hierarchical clustering
# ============================================================
print("\n[STAGE 5] Hierarchical clustering...")

from sklearn.preprocessing import StandardScaler

cluster_features = df[['S', 'O', 'D', 'RPN']].values
scaler = StandardScaler()
cluster_features_norm = scaler.fit_transform(cluster_features)

# Ward linkage
Z = linkage(cluster_features_norm, method='ward')

# Fig 5: Dendrogram
print("  Generating dendrogram (Fig. 5)...")
plt.figure(figsize=(10, 5))
dendrogram(Z, truncate_mode='lastp', p=30, leaf_rotation=90, leaf_font_size=8,
           color_threshold=0.7 * max(Z[:, 2]))
plt.xlabel('Failure Mode Index')
plt.ylabel('Ward Distance')
plt.title('Hierarchical Clustering Dendrogram')
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig5_dendrogram.png'), dpi=DPI, bbox_inches='tight')
plt.close()

# Cut into 3 clusters
labels = fcluster(Z, t=3, criterion='maxclust')
df['cluster'] = labels

# Cluster profiles
print("  Cluster profiles:")
cluster_profiles = []
for c in sorted(df['cluster'].unique()):
    mask = df['cluster'] == c
    cluster_data = df[mask]
    rpn_mean = cluster_data['RPN'].mean()
    rpn_min = cluster_data['RPN'].min()
    rpn_max = cluster_data['RPN'].max()
    count = mask.sum()
    dominant_sub = cluster_data['subsystem'].mode().iloc[0]
    s_mean = cluster_data['S'].mean()
    o_mean = cluster_data['O'].mean()
    d_mean = cluster_data['D'].mean()

    risk_level = 'High' if rpn_mean > 350 else ('Intermediate' if rpn_mean > 180 else 'Low')

    profile = {
        'cluster': int(c),
        'risk_level': risk_level,
        'count': int(count),
        'RPN_mean': round(rpn_mean, 1),
        'RPN_min': int(rpn_min),
        'RPN_max': int(rpn_max),
        'S_mean': round(s_mean, 1),
        'O_mean': round(o_mean, 1),
        'D_mean': round(d_mean, 1),
        'dominant_subsystem': dominant_sub,
        'subsystems': cluster_data['subsystem'].value_counts().to_dict()
    }
    cluster_profiles.append(profile)
    print(f"    Cluster {c} ({risk_level}): n={count}, RPN={rpn_min}-{rpn_max} "
          f"(mean={rpn_mean:.0f}), S={s_mean:.1f}, O={o_mean:.1f}, D={d_mean:.1f}")

with open(os.path.join(RESULTS_DIR, 'cluster_profiles.json'), 'w') as f:
    json.dump(cluster_profiles, f, indent=2)

# ============================================================
# STAGE 6: Generate remaining figures
# ============================================================
print("\n[STAGE 6] Generating figures...")

# Fig 2: Boxplot RPN by subsystem
print("  Generating RPN boxplot (Fig. 2)...")
plt.figure(figsize=(7, 5))
order = df.groupby('subsystem')['RPN'].median().sort_values(ascending=False).index
sns.boxplot(data=df, x='subsystem', y='RPN', order=order, palette='Set2')
plt.xlabel('Subsystem')
plt.ylabel('Risk Priority Number (RPN)')
plt.title('RPN Distribution by CubeSat Subsystem')
plt.xticks(rotation=0)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig2_rpn_boxplot.png'), dpi=DPI, bbox_inches='tight')
plt.close()

# Fig 6: Scatter plot predicted vs actual
print("  Generating predicted vs actual scatter (Fig. 6)...")
y_pred_all = best_xgb.predict(X)
plt.figure(figsize=(6, 6))
plt.scatter(y, y_pred_all, alpha=0.6, edgecolors='k', linewidth=0.5, s=40)
min_val = min(y.min(), y_pred_all.min()) - 20
max_val = max(y.max(), y_pred_all.max()) + 20
plt.plot([min_val, max_val], [min_val, max_val], 'r--', linewidth=1.5, label='Perfect prediction')
plt.xlabel('Actual RPN')
plt.ylabel('Predicted RPN')
plt.title('XGBoost: Predicted vs. Actual RPN')
plt.legend()
plt.xlim(min_val, max_val)
plt.ylim(min_val, max_val)
plt.tight_layout()
plt.savefig(os.path.join(FIG_DIR, 'fig6_predicted_vs_actual.png'), dpi=DPI, bbox_inches='tight')
plt.close()

# ============================================================
# SUMMARY
# ============================================================
print("\n" + "=" * 60)
print("PIPELINE COMPLETE")
print("=" * 60)
print(f"\nDataset: {len(df)} failure modes across {df['subsystem'].nunique()} subsystems")
print(f"\nModel performance (test set):")
for r in results:
    print(f"  {r['model']:20s} | R²={r['R2']:.4f} | RMSE={r['RMSE']:.2f} | MAPE={r['MAPE']:.2f}%")
print(f"\nXGBoost {CV_FOLDS}-fold CV: R²={cv_scores.mean():.4f} ± {cv_scores.std():.4f}")
print(f"\nClusters: {len(cluster_profiles)}")
for cp in cluster_profiles:
    print(f"  Cluster {cp['cluster']} ({cp['risk_level']}): "
          f"n={cp['count']}, RPN={cp['RPN_min']}-{cp['RPN_max']}")
print(f"\nFigures saved to: {FIG_DIR}")
print(f"Results saved to: {RESULTS_DIR}")
