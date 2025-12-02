#!/usr/bin/env python3
"""
Execute Cross-Cultural Statistical Analysis
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import spearmanr
from scipy.spatial.distance import jensenshannon

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

print("="*70)
print("CROSS-CULTURAL STATISTICAL ANALYSIS")
print("="*70)

# Step 1: Load data
print("\n[1/7] Loading data...")
english_summary = pd.read_csv('phase3_outputs/aesops_moral_summary.csv', index_col=0)
thirukkural_summary = pd.read_csv('phase3_outputs/thirukkural_moral_summary.csv', index_col=0)
aathichudi_summary = pd.read_csv('phase3_outputs/aathichudi_moral_summary.csv', index_col=0)

comparison_df = pd.DataFrame({
    'English_Aesop': english_summary['0'],
    'Tamil_Thirukkural': thirukkural_summary['0'],
    'Tamil_Aathichudi': aathichudi_summary['0']
})

print("\nMoral Foundation Average Scores:")
print(comparison_df.round(4))
print("✓ Data loaded")

# Step 2: Spearman Rank Correlation
print("\n[2/7] Calculating Spearman correlations...")
print("\n" + "="*70)
print("SPEARMAN RANK CORRELATION ANALYSIS")
print("="*70)

comparisons = [
    ('English_Aesop', 'Tamil_Thirukkural'),
    ('English_Aesop', 'Tamil_Aathichudi'),
    ('Tamil_Thirukkural', 'Tamil_Aathichudi')
]

spearman_results = []

for col1, col2 in comparisons:
    rho, pval = spearmanr(comparison_df[col1], comparison_df[col2])
    spearman_results.append({
        'Comparison': f'{col1} vs {col2}',
        'Spearman_ρ': rho,
        'p-value': pval,
        'Significant': 'Yes' if pval < 0.05 else 'No'
    })

    print(f"\n{col1}")
    print(f"  vs")
    print(f"{col2}")
    print(f"  Spearman ρ = {rho:.4f}")
    print(f"  p-value = {pval:.4f}")

    if pval < 0.001:
        sig_str = "***"
    elif pval < 0.01:
        sig_str = "**"
    elif pval < 0.05:
        sig_str = "*"
    else:
        sig_str = "ns"
    print(f"  Significance: {sig_str}")

    if rho > 0.7:
        print(f"  Interpretation: STRONG positive correlation")
    elif rho > 0.4:
        print(f"  Interpretation: MODERATE positive correlation")
    elif rho > 0.0:
        print(f"  Interpretation: WEAK positive correlation")
    else:
        print(f"  Interpretation: NEGATIVE correlation")

spearman_df = pd.DataFrame(spearman_results)
print("\n✓ Spearman analysis complete")

# Step 3: Rankings visualization
print("\n[3/7] Generating rankings heatmap...")
rankings = pd.DataFrame({
    'English': comparison_df['English_Aesop'].rank(ascending=False).astype(int),
    'Tamil_Thirukkural': comparison_df['Tamil_Thirukkural'].rank(ascending=False).astype(int),
    'Tamil_Aathichudi': comparison_df['Tamil_Aathichudi'].rank(ascending=False).astype(int)
}, index=comparison_df.index)

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(rankings.T, annot=True, fmt='d', cmap='YlOrRd_r',
            cbar_kws={'label': 'Rank (1=highest)'}, ax=ax)
ax.set_title('Moral Foundation Rankings Across Cultures', fontsize=14, fontweight='bold')
ax.set_xlabel('Moral Foundation', fontsize=11)
ax.set_ylabel('Culture/Text', fontsize=11)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('phase3_outputs/cross_cultural_rankings_heatmap.png', dpi=300)
plt.close()
print("✓ Saved: cross_cultural_rankings_heatmap.png")

# Step 4: Jensen-Shannon Divergence
print("\n[4/7] Calculating Jensen-Shannon Divergence...")
print("\n" + "="*70)
print("JENSEN-SHANNON DIVERGENCE (JSD) ANALYSIS")
print("="*70)

def normalize_distribution(scores):
    scores = scores - scores.min() + 1e-10
    return scores / scores.sum()

dist_english = normalize_distribution(comparison_df['English_Aesop'])
dist_thirukkural = normalize_distribution(comparison_df['Tamil_Thirukkural'])
dist_aathichudi = normalize_distribution(comparison_df['Tamil_Aathichudi'])

jsd_results = []
pairs = [
    ('English_Aesop', dist_english, 'Tamil_Thirukkural', dist_thirukkural),
    ('English_Aesop', dist_english, 'Tamil_Aathichudi', dist_aathichudi),
    ('Tamil_Thirukkural', dist_thirukkural, 'Tamil_Aathichudi', dist_aathichudi)
]

for name1, dist1, name2, dist2 in pairs:
    jsd = jensenshannon(dist1, dist2)
    jsd_results.append({
        'Comparison': f'{name1} vs {name2}',
        'JSD': jsd,
        'Similarity': 1 - jsd
    })

    print(f"\n{name1}")
    print(f"  vs")
    print(f"{name2}")
    print(f"  JSD = {jsd:.4f}")
    print(f"  Similarity = {1-jsd:.4f}")

    if jsd < 0.1:
        print(f"  Interpretation: VERY SIMILAR distributions")
    elif jsd < 0.3:
        print(f"  Interpretation: MODERATELY DIFFERENT distributions")
    else:
        print(f"  Interpretation: VERY DIFFERENT distributions")

jsd_df = pd.DataFrame(jsd_results)
print("\n✓ JSD analysis complete")

# Step 5: Distribution comparison plots
print("\n[5/7] Generating distribution comparison plots...")
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

axes[0].bar(range(len(dist_english)), dist_english, color='steelblue', alpha=0.7)
axes[0].set_title('English (Aesop)', fontsize=12, fontweight='bold')
axes[0].set_xlabel('Moral Foundation', fontsize=10)
axes[0].set_ylabel('Normalized Probability', fontsize=10)
axes[0].set_xticks(range(len(dist_english)))
axes[0].set_xticklabels(comparison_df.index, rotation=45, ha='right', fontsize=8)
axes[0].grid(axis='y', alpha=0.3)

axes[1].bar(range(len(dist_thirukkural)), dist_thirukkural, color='coral', alpha=0.7)
axes[1].set_title('Tamil (Thirukkural)', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Moral Foundation', fontsize=10)
axes[1].set_ylabel('Normalized Probability', fontsize=10)
axes[1].set_xticks(range(len(dist_thirukkural)))
axes[1].set_xticklabels(comparison_df.index, rotation=45, ha='right', fontsize=8)
axes[1].grid(axis='y', alpha=0.3)

axes[2].bar(range(len(dist_aathichudi)), dist_aathichudi, color='lightgreen', alpha=0.7)
axes[2].set_title('Tamil (Aathichudi)', fontsize=12, fontweight='bold')
axes[2].set_xlabel('Moral Foundation', fontsize=10)
axes[2].set_ylabel('Normalized Probability', fontsize=10)
axes[2].set_xticks(range(len(dist_aathichudi)))
axes[2].set_xticklabels(comparison_df.index, rotation=45, ha='right', fontsize=8)
axes[2].grid(axis='y', alpha=0.3)

plt.suptitle('Moral Value Probability Distributions Across Cultures',
             fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('phase3_outputs/moral_distributions_comparison.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: moral_distributions_comparison.png")

# Step 6: Save statistics
print("\n[6/7] Saving statistics to CSV...")
combined_results = pd.DataFrame({
    'Comparison': spearman_df['Comparison'],
    'Spearman_ρ': spearman_df['Spearman_ρ'],
    'Spearman_p': spearman_df['p-value'],
    'JSD': jsd_df['JSD'],
    'Similarity': jsd_df['Similarity']
})

combined_results.to_csv('phase3_outputs/cross_cultural_statistics.csv', index=False)
print("✓ Saved: cross_cultural_statistics.csv")

# Step 7: Comprehensive summary figure
print("\n[7/7] Creating comprehensive summary visualization...")
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# 1. Original comparison bars
ax1 = fig.add_subplot(gs[0, :])
x = np.arange(len(comparison_df))
width = 0.25
ax1.bar(x - width, comparison_df['English_Aesop'], width, label='English', alpha=0.8, color='steelblue')
ax1.bar(x, comparison_df['Tamil_Thirukkural'], width, label='Tamil (Thiru)', alpha=0.8, color='coral')
ax1.bar(x + width, comparison_df['Tamil_Aathichudi'], width, label='Tamil (Aathi)', alpha=0.8, color='lightgreen')
ax1.set_xticks(x)
ax1.set_xticklabels(comparison_df.index, rotation=45, ha='right')
ax1.set_ylabel('Average Similarity Score')
ax1.set_title('Cross-Cultural Moral Foundation Comparison', fontweight='bold')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# 2. Spearman correlation matrix
ax2 = fig.add_subplot(gs[1, 0])
corr_matrix = comparison_df.corr(method='spearman')
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm',
            center=0.5, vmin=0, vmax=1, ax=ax2, cbar_kws={'label': 'Spearman ρ'})
ax2.set_title('Spearman Rank Correlations', fontweight='bold')

# 3. JSD heatmap
ax3 = fig.add_subplot(gs[1, 1])
jsd_matrix = np.array([
    [0, jsd_results[0]['JSD'], jsd_results[1]['JSD']],
    [jsd_results[0]['JSD'], 0, jsd_results[2]['JSD']],
    [jsd_results[1]['JSD'], jsd_results[2]['JSD'], 0]
])
labels = ['English', 'Thiru', 'Aathi']
sns.heatmap(jsd_matrix, annot=True, fmt='.3f', cmap='YlOrRd',
            xticklabels=labels, yticklabels=labels, ax=ax3,
            cbar_kws={'label': 'JSD (lower=more similar)'})
ax3.set_title('Jensen-Shannon Divergence', fontweight='bold')

# 4. Top differences
ax4 = fig.add_subplot(gs[2, :])
diff_thirukkural = comparison_df['Tamil_Thirukkural'] - comparison_df['English_Aesop']
top_diffs = diff_thirukkural.abs().sort_values(ascending=False).head(5)
colors = ['coral' if diff_thirukkural[m] > 0 else 'steelblue' for m in top_diffs.index]
ax4.barh(range(len(top_diffs)), [diff_thirukkural[m] for m in top_diffs.index], color=colors, alpha=0.7)
ax4.set_yticks(range(len(top_diffs)))
ax4.set_yticklabels(top_diffs.index)
ax4.set_xlabel('Difference (Tamil - English)')
ax4.set_title('Top 5 Cultural Differences (Positive=Tamil emphasizes more)', fontweight='bold')
ax4.axvline(0, color='black', linewidth=0.8)
ax4.grid(axis='x', alpha=0.3)

plt.savefig('phase3_outputs/cross_cultural_comprehensive_summary.png', dpi=300, bbox_inches='tight')
plt.close()
print("✓ Saved: cross_cultural_comprehensive_summary.png")

# Final summary
print("\n" + "="*70)
print("KEY FINDINGS")
print("="*70)

diff_thirukkural = comparison_df['Tamil_Thirukkural'] - comparison_df['English_Aesop']
print("\nMorals MORE emphasized in Tamil:")
for moral, diff in diff_thirukkural.sort_values(ascending=False).head(3).items():
    eng_val = comparison_df.loc[moral, 'English_Aesop']
    tam_val = comparison_df.loc[moral, 'Tamil_Thirukkural']
    print(f"  {moral:20s}: +{diff:.3f}  (Eng: {eng_val:.3f} → Tamil: {tam_val:.3f})")

print("\n" + "="*70)
print("✓ CROSS-CULTURAL STATISTICAL ANALYSIS COMPLETE")
print("="*70)
print("\nGenerated files:")
print("  - phase3_outputs/cross_cultural_statistics.csv")
print("  - phase3_outputs/cross_cultural_rankings_heatmap.png")
print("  - phase3_outputs/moral_distributions_comparison.png")
print("  - phase3_outputs/cross_cultural_comprehensive_summary.png")
