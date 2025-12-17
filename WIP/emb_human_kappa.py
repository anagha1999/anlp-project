import pandas as pd
from sklearn.metrics import cohen_kappa_score
import re

# Load human annotations
kan_human = pd.read_csv('kannada/5b.Para-TextKannada-Human1Evaluation-Human2EvaluationRanked-Agreement-Notes.csv')
kan_method = pd.read_csv('kannada/lexicon-comparison-results/1-janapada-kathegalu_method_comparison.csv')

def get_first_moral(eval_str):
    if pd.isna(eval_str): return None
    lines = str(eval_str).strip().split('\n')
    return lines[0].strip().split(',')[0].strip() if lines else None

def get_base(moral_str):
    if pd.isna(moral_str) or moral_str is None: return None
    return str(moral_str).split('.')[0]

# Parse human annotations
kan_human['H1_first'] = kan_human['Human 1 Evaluation'].apply(get_first_moral)
kan_human['H2_first'] = kan_human['Human 2 Evaluation Ranked'].apply(get_first_moral)
kan_human['H1_base'] = kan_human['H1_first'].apply(get_base)
kan_human['H2_base'] = kan_human['H2_first'].apply(get_base)

# Match paragraphs to embedding results
results = []
for idx, row in kan_human.iterrows():
    text = str(row['Text (Kannada)'])
    match = re.search(r'(\d+)', text)
    if match:
        actual_para = int(match.group(1))
        method_row = kan_method[kan_method['paragraph_num'] == actual_para]
        if not method_row.empty:
            h1 = row['H1_first']
            h2 = row['H2_first']
            h1_base = get_base(h1)
            h2_base = get_base(h2)
            emb = method_row['dominant_embedding'].values[0]
            emb_base = get_base(emb)
            lex = method_row['dominant_lexicon'].values[0]
            lex_base = get_base(lex)
            results.append({
                'para': actual_para, 
                'H1': h1, 'H2': h2, 
                'H1_base': h1_base, 'H2_base': h2_base,
                'Emb': emb, 'Emb_base': emb_base,
                'Lex': lex, 'Lex_base': lex_base
            })

df = pd.DataFrame(results)

print('MATCHED PARAGRAPHS:')
print(df[['para', 'H1', 'H2', 'Emb', 'Lex']])

print('\n' + '='*70)
print('EMBEDDING vs HUMAN COMPARISON')
print('='*70)

# Exact match (full foundation.polarity)
valid = df.dropna(subset=['H1', 'H2', 'Emb'])
emb_h1_exact = (valid['H1'] == valid['Emb']).sum()
emb_h2_exact = (valid['H2'] == valid['Emb']).sum()
emb_either_exact = ((valid['H1'] == valid['Emb']) | (valid['H2'] == valid['Emb'])).sum()

print(f'\nExact match (foundation.polarity):')
print(f'  Embedding matches H1: {emb_h1_exact}/{len(valid)} ({emb_h1_exact/len(valid)*100:.1f}%)')
print(f'  Embedding matches H2: {emb_h2_exact}/{len(valid)} ({emb_h2_exact/len(valid)*100:.1f}%)')
print(f'  Embedding matches either: {emb_either_exact}/{len(valid)} ({emb_either_exact/len(valid)*100:.1f}%)')

# Base match (foundation only)
valid_base = df.dropna(subset=['H1_base', 'H2_base', 'Emb_base'])
emb_h1_base = (valid_base['H1_base'] == valid_base['Emb_base']).sum()
emb_h2_base = (valid_base['H2_base'] == valid_base['Emb_base']).sum()
emb_either_base = ((valid_base['H1_base'] == valid_base['Emb_base']) | (valid_base['H2_base'] == valid_base['Emb_base'])).sum()

print(f'\nBase match (foundation only):')
print(f'  Embedding matches H1: {emb_h1_base}/{len(valid_base)} ({emb_h1_base/len(valid_base)*100:.1f}%)')
print(f'  Embedding matches H2: {emb_h2_base}/{len(valid_base)} ({emb_h2_base/len(valid_base)*100:.1f}%)')
print(f'  Embedding matches either: {emb_either_base}/{len(valid_base)} ({emb_either_base/len(valid_base)*100:.1f}%)')

# Cohen's Kappa
print(f'\nCohens Kappa:')
try:
    kappa_h1_h2 = cohen_kappa_score(valid['H1'], valid['H2'])
    print(f'  H1 vs H2 (baseline): {kappa_h1_h2:.3f}')
except Exception as e:
    print(f'  H1 vs H2: could not calculate - {e}')

try:
    kappa_emb_h1 = cohen_kappa_score(valid['H1'], valid['Emb'])
    print(f'  Embedding vs H1: {kappa_emb_h1:.3f}')
except Exception as e:
    print(f'  Embedding vs H1: could not calculate - {e}')

try:
    kappa_emb_h2 = cohen_kappa_score(valid['H2'], valid['Emb'])
    print(f'  Embedding vs H2: {kappa_emb_h2:.3f}')
except Exception as e:
    print(f'  Embedding vs H2: could not calculate - {e}')

# Note about sample
print('\n' + '='*70)
print('NOTE: These 10 paragraphs were selected from DISAGREEMENT cases')
print('between lexicon and embedding methods, so this is a biased sample.')
print('='*70)
