import pandas as pd
from sklearn.metrics import cohen_kappa_score
import re

print("="*70)
print("KANNADA: EMBEDDING vs HUMAN COMPARISON (ALL 10 PARAGRAPHS)")
print("="*70)

# Load data
kan_human = pd.read_csv('kannada/5b.Para-TextKannada-Human1Evaluation-Human2EvaluationRanked-Agreement-Notes.csv')
kan_method = pd.read_csv('kannada/lexicon-comparison-results/1-janapada-kathegalu_method_comparison.csv')

def get_first_moral(eval_str):
    if pd.isna(eval_str): return None
    lines = str(eval_str).strip().split('\n')
    return lines[0].strip().split(',')[0].strip() if lines else None

# Manual paragraph mapping (Row 2 has no number in text - it's para 16)
para_mapping = {
    0: 81,    # Row 1
    1: 16,    # Row 2 - manually identified as paragraph 16
    2: 183,   # Row 3
    3: 160,   # Row 4
    4: 148,   # Row 5
    5: 102,   # Row 6
    6: 72,    # Row 7
    7: 41,    # Row 8
    8: 60,    # Row 9
    9: 206,   # Row 10
}

results = []
for idx, row in kan_human.iterrows():
    h1 = get_first_moral(row['Human 1 Evaluation'])
    h2 = get_first_moral(row['Human 2 Evaluation Ranked'])
    
    para_num = para_mapping.get(idx)
    if para_num:
        method_row = kan_method[kan_method['paragraph_num'] == para_num]
        if not method_row.empty:
            emb = method_row['dominant_embedding'].values[0]
            lex = method_row['dominant_lexicon'].values[0] if pd.notna(method_row['dominant_lexicon'].values[0]) else None
            results.append({
                'para': para_num,
                'H1': h1,
                'H2': h2,
                'Emb': emb,
                'Lex': lex
            })

df = pd.DataFrame(results)
print(f"\nMatched {len(df)} paragraphs:")
print(df[['para', 'H1', 'H2', 'Emb']])

# Calculate metrics
valid = df.dropna(subset=['H1', 'H2', 'Emb'])
print(f"\nValid rows for comparison: {len(valid)}")

emb_h1_exact = (valid['H1'] == valid['Emb']).sum()
emb_h2_exact = (valid['H2'] == valid['Emb']).sum()
emb_either_exact = ((valid['H1'] == valid['Emb']) | (valid['H2'] == valid['Emb'])).sum()

print(f'\nExact match (foundation.polarity):')
print(f'  Embedding matches H1: {emb_h1_exact}/{len(valid)} ({emb_h1_exact/len(valid)*100:.1f}%)')
print(f'  Embedding matches H2: {emb_h2_exact}/{len(valid)} ({emb_h2_exact/len(valid)*100:.1f}%)')
print(f'  Embedding matches either: {emb_either_exact}/{len(valid)} ({emb_either_exact/len(valid)*100:.1f}%)')

# Cohen's Kappa
h1_list = valid['H1'].tolist()
h2_list = valid['H2'].tolist()
emb_list = valid['Emb'].tolist()

print(f'\nCohens Kappa:')
kappa_h1_h2 = cohen_kappa_score(h1_list, h2_list)
print(f'  H1 vs H2 (baseline): {kappa_h1_h2:.3f}')
kappa_emb_h1 = cohen_kappa_score(emb_list, h1_list)
print(f'  Embedding vs H1: {kappa_emb_h1:.3f}')
kappa_emb_h2 = cohen_kappa_score(emb_list, h2_list)
print(f'  Embedding vs H2: {kappa_emb_h2:.3f}')

print("\n" + "="*70)
print("DETAILED COMPARISON:")
print("="*70)
for _, row in df.iterrows():
    h1_match = "✓" if row['H1'] == row['Emb'] else "✗"
    h2_match = "✓" if row['H2'] == row['Emb'] else "✗"
    print(f"Para {row['para']}: H1={row['H1']}, H2={row['H2']}, Emb={row['Emb']} | H1:{h1_match} H2:{h2_match}")

# ========================================
# TAMIL
# ========================================
print("\n\n" + "="*70)
print("TAMIL: EMBEDDING vs HUMAN COMPARISON (ALL 9 COUPLETS)")
print("="*70)

tamil_human = pd.read_csv('tamil/5b.PoemTamil-Human1Evaluation-Human2EvaluationRanked-Agreement-Notes.csv', skiprows=1)

tamil_human['H1_first'] = tamil_human['Human 1 Evaluation'].apply(get_first_moral)
tamil_human['H2_first'] = tamil_human['Human 2 Evaluation Ranked'].apply(get_first_moral)

text_file_map = {
    'Thirukkural': 'thirukkural',
    'Moothurai': 'moothurai', 
    'Aathichoodi': 'aathichoodi',
}

tamil_results = []
for idx, row in tamil_human.iterrows():
    text_name = row['Text_Name']
    unit_id = row['Unit_ID']
    h1 = row['H1_first']
    h2 = row['H2_first']
    
    if text_name in text_file_map:
        method_file = f"tamil/lexicon-comparison-results/{text_file_map[text_name]}_method_comparison.csv"
        try:
            method_df = pd.read_csv(method_file)
            if 'id' in method_df.columns:
                match = method_df[method_df['id'] == unit_id]
                if not match.empty:
                    emb = match['dominant_embedding'].values[0]
                    tamil_results.append({
                        'text': text_name,
                        'unit': unit_id,
                        'H1': h1,
                        'H2': h2,
                        'Emb': emb
                    })
        except Exception as e:
            print(f"Error: {e}")

tamil_df = pd.DataFrame(tamil_results)
print(f"\nMatched {len(tamil_df)} couplets:")
print(tamil_df)

valid_tamil = tamil_df.dropna(subset=['H1', 'H2', 'Emb'])
print(f"\nValid rows for comparison: {len(valid_tamil)}")

emb_h1_tamil = (valid_tamil['H1'] == valid_tamil['Emb']).sum()
emb_h2_tamil = (valid_tamil['H2'] == valid_tamil['Emb']).sum()
emb_either_tamil = ((valid_tamil['H1'] == valid_tamil['Emb']) | (valid_tamil['H2'] == valid_tamil['Emb'])).sum()

print(f'\nExact match (foundation.polarity):')
print(f'  Embedding matches H1: {emb_h1_tamil}/{len(valid_tamil)} ({emb_h1_tamil/len(valid_tamil)*100:.1f}%)')
print(f'  Embedding matches H2: {emb_h2_tamil}/{len(valid_tamil)} ({emb_h2_tamil/len(valid_tamil)*100:.1f}%)')
print(f'  Embedding matches either: {emb_either_tamil}/{len(valid_tamil)} ({emb_either_tamil/len(valid_tamil)*100:.1f}%)')

h1_tamil = valid_tamil['H1'].tolist()
h2_tamil = valid_tamil['H2'].tolist()
emb_tamil = valid_tamil['Emb'].tolist()

print(f'\nCohens Kappa:')
print(f'  H1 vs H2 (baseline): {cohen_kappa_score(h1_tamil, h2_tamil):.3f}')
print(f'  Embedding vs H1: {cohen_kappa_score(emb_tamil, h1_tamil):.3f}')
print(f'  Embedding vs H2: {cohen_kappa_score(emb_tamil, h2_tamil):.3f}')

print("\n" + "="*70)
print("SUMMARY TABLE")
print("="*70)
print(f"{'Metric':<35} {'Kannada (n=10)':<18} {'Tamil (n=9)':<15}")
print("-"*70)
print(f"{'Embedding matches H1':<35} {emb_h1_exact}/{len(valid)} ({emb_h1_exact/len(valid)*100:.1f}%){'':<8} {emb_h1_tamil}/{len(valid_tamil)} ({emb_h1_tamil/len(valid_tamil)*100:.1f}%)")
print(f"{'Embedding matches H2':<35} {emb_h2_exact}/{len(valid)} ({emb_h2_exact/len(valid)*100:.1f}%){'':<8} {emb_h2_tamil}/{len(valid_tamil)} ({emb_h2_tamil/len(valid_tamil)*100:.1f}%)")
print(f"{'Embedding matches either':<35} {emb_either_exact}/{len(valid)} ({emb_either_exact/len(valid)*100:.1f}%){'':<8} {emb_either_tamil}/{len(valid_tamil)} ({emb_either_tamil/len(valid_tamil)*100:.1f}%)")
print(f"{'Cohen κ: H1 vs H2':<35} {kappa_h1_h2:.3f}{'':<15} {cohen_kappa_score(h1_tamil, h2_tamil):.3f}")
print(f"{'Cohen κ: Emb vs H1':<35} {kappa_emb_h1:.3f}{'':<15} {cohen_kappa_score(emb_tamil, h1_tamil):.3f}")
print(f"{'Cohen κ: Emb vs H2':<35} {kappa_emb_h2:.3f}{'':<15} {cohen_kappa_score(emb_tamil, h2_tamil):.3f}")
