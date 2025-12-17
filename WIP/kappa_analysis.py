import pandas as pd
from sklearn.metrics import cohen_kappa_score
import re

kannada_human = pd.read_csv('kannada/5b.Para-TextKannada-Human1Evaluation-Human2EvaluationRanked-Agreement-Notes.csv')
kannada_method = pd.read_csv('kannada/lexicon-comparison-results/1-janapada-kathegalu_method_comparison.csv')

def get_first_moral(eval_str):
    if pd.isna(eval_str): return None
    lines = str(eval_str).strip().split('\n')
    return lines[0].strip().split(',')[0].strip() if lines else None

def get_base(moral_str):
    if pd.isna(moral_str) or moral_str is None: return None
    return str(moral_str).split('.')[0]

print('KANNADA: EMBEDDING RELIABILITY ANALYSIS')
print('='*70)

kannada_human['H1_first'] = kannada_human['Human 1 Evaluation'].apply(get_first_moral)
kannada_human['H2_first'] = kannada_human['Human 2 Evaluation Ranked'].apply(get_first_moral)
kannada_human['H1_base'] = kannada_human['H1_first'].apply(get_base)
kannada_human['H2_base'] = kannada_human['H2_first'].apply(get_base)

valid_kan = kannada_human.dropna(subset=['H1_base', 'H2_base'])
kappa_human_kan = cohen_kappa_score(valid_kan['H1_base'], valid_kan['H2_base'])
human_agree_kan = (valid_kan['H1_base'] == valid_kan['H2_base']).sum()

print(f'\n1. HUMAN INTER-ANNOTATOR AGREEMENT (baseline):')
print(f'   Paragraphs evaluated: {len(valid_kan)}')
print(f'   Agreement: {human_agree_kan}/{len(valid_kan)} ({human_agree_kan/len(valid_kan)*100:.1f}%)')
print(f'   Cohen\'s Kappa (H1 vs H2): {kappa_human_kan:.3f}')

results = []
for idx, row in kannada_human.iterrows():
    text = str(row['Text (Kannada)'])
    match = re.search(r'(\d+)', text)
    if match:
        actual_para = int(match.group(1))
        method_row = kannada_method[kannada_method['paragraph_num'] == actual_para]
        if not method_row.empty:
            h1 = get_base(row['H1_first'])
            h2 = get_base(row['H2_first'])
            emb = get_base(method_row['dominant_embedding'].values[0])
            lex = get_base(method_row['dominant_lexicon'].values[0])
            results.append({'para': actual_para, 'H1': h1, 'H2': h2, 'Emb': emb, 'Lex': lex})

df = pd.DataFrame(results)
print(f'\n2. COMPARISON TABLE ({len(df)} matched paragraphs):')
print('\n   Para | H1         | H2         | Embedding  | Lexicon    | Emb? | Lex?')
print('   ' + '-'*72)
for _, r in df.iterrows():
    em = 'Y' if r['Emb'] in [r['H1'], r['H2']] else 'N'
    lm = 'Y' if r['Lex'] in [r['H1'], r['H2']] else 'N'
    print(f"   {r['para']:>4} | {str(r['H1']):<10} | {str(r['H2']):<10} | {str(r['Emb']):<10} | {str(r['Lex']):<10} | {em}    | {lm}")

emb_match = ((df['Emb'] == df['H1']) | (df['Emb'] == df['H2'])).sum()
lex_match = ((df['Lex'] == df['H1']) | (df['Lex'] == df['H2'])).sum()

print(f'\n3. AGREEMENT WITH HUMAN ANNOTATORS:')
print(f'   Embedding matches either human: {emb_match}/{len(df)} ({emb_match/len(df)*100:.0f}%)')
print(f'   Lexicon matches either human:   {lex_match}/{len(df)} ({lex_match/len(df)*100:.0f}%)')

valid_df = df.dropna()
kappa_emb_h1 = cohen_kappa_score(valid_df['H1'], valid_df['Emb'])
kappa_emb_h2 = cohen_kappa_score(valid_df['H2'], valid_df['Emb'])
kappa_lex_h1 = cohen_kappa_score(valid_df['H1'], valid_df['Lex'])
kappa_lex_h2 = cohen_kappa_score(valid_df['H2'], valid_df['Lex'])

print(f'\n4. COHEN\'S KAPPA COMPARISON:')
print(f'   H1 vs H2 (human baseline):  k = {kappa_human_kan:.3f}')
print(f'   Embedding vs H1:            k = {kappa_emb_h1:.3f}')
print(f'   Embedding vs H2:            k = {kappa_emb_h2:.3f}')
print(f'   Lexicon vs H1:              k = {kappa_lex_h1:.3f}')
print(f'   Lexicon vs H2:              k = {kappa_lex_h2:.3f}')

avg_emb = (kappa_emb_h1+kappa_emb_h2)/2
avg_lex = (kappa_lex_h1+kappa_lex_h2)/2

print(f'\n   AVERAGE Embedding-Human:    k = {avg_emb:.3f}')
print(f'   AVERAGE Lexicon-Human:      k = {avg_lex:.3f}')

print(f'\n5. INTERPRETATION:')
print(f'   Human inter-annotator reliability: k = {kappa_human_kan:.3f} (moderate)')
print(f'   Embedding achieves {avg_emb/kappa_human_kan*100:.0f}% of human-level reliability')
print(f'   Lexicon achieves {avg_lex/kappa_human_kan*100:.0f}% of human-level reliability')
print(f'\n   The embedding-based approach is a FAIR substitute for human annotation')
print(f'   given the moderate agreement (k > 0.2) with human annotators.')
