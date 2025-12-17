import pandas as pd
from sklearn.metrics import cohen_kappa_score

# Tamil
print('='*70)
print('TAMIL HUMAN ANNOTATION ANALYSIS')
print('='*70)

tam = pd.read_csv('tamil/5b.PoemTamil-Human1Evaluation-Human2EvaluationRanked-Agreement-Notes.csv', skiprows=1)

def parse_morals(eval_str):
    if pd.isna(eval_str): return []
    # Handle both newline and comma separated
    text = str(eval_str).strip()
    if '\n' in text:
        lines = text.split('\n')
    else:
        lines = [l.strip() for l in text.split(',')]
    return [l.strip() for l in lines if l.strip()]

def get_base(moral):
    if not moral: return None
    return moral.split('.')[0]

# Parse all rankings
tam['H1_all'] = tam['Human 1 Evaluation'].apply(parse_morals)
tam['H2_all'] = tam['Human 2 Evaluation Ranked'].apply(parse_morals)
tam['H1_first'] = tam['H1_all'].apply(lambda x: x[0] if x else None)
tam['H2_first'] = tam['H2_all'].apply(lambda x: x[0] if x else None)
tam['H1_base'] = tam['H1_first'].apply(get_base)
tam['H2_base'] = tam['H2_first'].apply(get_base)

print('\nPrimary Moral Comparison (first-ranked only):')
print('-'*60)
for i, row in tam.iterrows():
    text_id = f"{row['Text_Name']}-{row['Unit_ID']}"
    agree = '✓' if row['H1_first'] == row['H2_first'] else '✗'
    base_agree = '✓' if row['H1_base'] == row['H2_base'] else '✗'
    print(f"{text_id:<25}: H1={str(row['H1_first']):<18} H2={str(row['H2_first']):<18} Match:{agree} Base:{base_agree}")

# Calculate kappa on FIRST moral only (full foundation.polarity)
valid = tam.dropna(subset=['H1_first', 'H2_first'])
exact_agree = (valid['H1_first'] == valid['H2_first']).sum()
kappa_exact = cohen_kappa_score(valid['H1_first'], valid['H2_first'])

# Calculate kappa on base foundation only
valid_base = tam.dropna(subset=['H1_base', 'H2_base'])
base_agree = (valid_base['H1_base'] == valid_base['H2_base']).sum()
kappa_base = cohen_kappa_score(valid_base['H1_base'], valid_base['H2_base'])

print(f'\n--- TAMIL KAPPA RESULTS ---')
print(f'Exact match (foundation.polarity): {exact_agree}/{len(valid)} ({exact_agree/len(valid)*100:.1f}%)')
print(f"Cohen's Kappa (exact): {kappa_exact:.3f}")
print(f'Base match (foundation only): {base_agree}/{len(valid_base)} ({base_agree/len(valid_base)*100:.1f}%)')
print(f"Cohen's Kappa (base): {kappa_base:.3f}")

# Analyze overlap in top-3
print('\n--- OVERLAP ANALYSIS (Primary Disagree, Secondary/Tertiary Overlap) ---')
for i, row in tam.iterrows():
    h1_all = row['H1_all']
    h2_all = row['H2_all']
    if row['H1_first'] != row['H2_first'] and len(h1_all) > 0 and len(h2_all) > 0:
        h1_set = set(h1_all)
        h2_set = set(h2_all)
        overlap = h1_set & h2_set
        text_id = f"{row['Text_Name']}-{row['Unit_ID']}"
        print(f"{text_id}: Primary disagree ({row['H1_first']} vs {row['H2_first']})")
        print(f"   H1 top-3: {h1_all}")
        print(f"   H2 top-3: {h2_all}")
        print(f"   Overlap: {overlap if overlap else 'NONE'}")
