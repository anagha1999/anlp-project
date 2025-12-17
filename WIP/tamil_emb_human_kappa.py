import pandas as pd
from sklearn.metrics import cohen_kappa_score
import re

# Load Tamil human annotations (skip first row which is empty)
tamil_human = pd.read_csv('tamil/5b.PoemTamil-Human1Evaluation-Human2EvaluationRanked-Agreement-Notes.csv', skiprows=1)

print("Tamil Human Annotations:")
print(tamil_human.columns.tolist())
print(tamil_human.head())

def get_first_moral(eval_str):
    """Extract primary (first-ranked) moral from evaluation string"""
    if pd.isna(eval_str): return None
    lines = str(eval_str).strip().split('\n')
    first_line = lines[0].strip() if lines else None
    if first_line:
        # Handle comma-separated format too
        return first_line.split(',')[0].strip()
    return None

# Parse human annotations
tamil_human['H1_first'] = tamil_human['Human 1 Evaluation'].apply(get_first_moral)
tamil_human['H2_first'] = tamil_human['Human 2 Evaluation Ranked'].apply(get_first_moral)

print("\nParsed first morals:")
print(tamil_human[['Text_Name', 'Unit_ID', 'H1_first', 'H2_first']])

# Load all method comparison files and match
text_file_map = {
    'Thirukkural': 'thirukkural',
    'Moothurai': 'moothurai', 
    'Aathichoodi': 'aathichoodi',
    'Konraiventhan': 'konraiventhan',
    'Nalvazhi': 'nalvazhi',
    'Ulakaneethi': 'ulakaneethi',
    'Vivekacinthamani': 'vivekacinthamani'
}

results = []
for idx, row in tamil_human.iterrows():
    text_name = row['Text_Name']
    unit_id = row['Unit_ID']
    h1 = row['H1_first']
    h2 = row['H2_first']
    
    if text_name in text_file_map:
        method_file = f"tamil/lexicon-comparison-results/{text_file_map[text_name]}_method_comparison.csv"
        try:
            method_df = pd.read_csv(method_file)
            # Find matching unit - column might be 'couplet_num' or 'verse_num' etc.
            id_col = None
            for col in ['couplet_num', 'verse_num', 'unit_num', 'line_num']:
                if col in method_df.columns:
                    id_col = col
                    break
            
            # Try 'id' column first, then others
            id_col = None
            for col in ['id', 'couplet_num', 'verse_num', 'unit_num', 'line_num']:
                if col in method_df.columns:
                    id_col = col
                    break
            
            if id_col:
                match = method_df[method_df[id_col] == unit_id]
                if not match.empty:
                    emb = match['dominant_embedding'].values[0]
                    lex = match['dominant_lexicon'].values[0] if 'dominant_lexicon' in match.columns else None
                    results.append({
                        'text': text_name,
                        'unit': unit_id,
                        'H1': h1,
                        'H2': h2,
                        'Emb': emb,
                        'Lex': lex
                    })
        except Exception as e:
            print(f"Error loading {method_file}: {e}")

df = pd.DataFrame(results)
print("\n" + "="*70)
print("MATCHED UNITS:")
print("="*70)
print(df)

print("\n" + "="*70)
print("TAMIL: EMBEDDING vs HUMAN COMPARISON")
print("="*70)

# Exact match (full foundation.polarity)
valid = df.dropna(subset=['H1', 'H2', 'Emb'])
if len(valid) > 0:
    emb_h1_exact = (valid['H1'] == valid['Emb']).sum()
    emb_h2_exact = (valid['H2'] == valid['Emb']).sum()
    emb_either_exact = ((valid['H1'] == valid['Emb']) | (valid['H2'] == valid['Emb'])).sum()
    
    print(f'\nExact match (foundation.polarity):')
    print(f'  Embedding matches H1: {emb_h1_exact}/{len(valid)} ({emb_h1_exact/len(valid)*100:.1f}%)')
    print(f'  Embedding matches H2: {emb_h2_exact}/{len(valid)} ({emb_h2_exact/len(valid)*100:.1f}%)')
    print(f'  Embedding matches either: {emb_either_exact}/{len(valid)} ({emb_either_exact/len(valid)*100:.1f}%)')
    
    # Cohen's Kappa
    print(f'\nCohens Kappa:')
    h1_list = valid['H1'].tolist()
    h2_list = valid['H2'].tolist()
    emb_list = valid['Emb'].tolist()
    
    try:
        kappa_h1_h2 = cohen_kappa_score(h1_list, h2_list)
        print(f'  H1 vs H2 (baseline): {kappa_h1_h2:.3f}')
    except:
        print('  H1 vs H2: Cannot compute (insufficient data)')
    
    try:
        kappa_emb_h1 = cohen_kappa_score(emb_list, h1_list)
        print(f'  Embedding vs H1: {kappa_emb_h1:.3f}')
    except:
        print('  Embedding vs H1: Cannot compute')
    
    try:
        kappa_emb_h2 = cohen_kappa_score(emb_list, h2_list)
        print(f'  Embedding vs H2: {kappa_emb_h2:.3f}')
    except:
        print('  Embedding vs H2: Cannot compute')
else:
    print("No valid matches found")

# Show detailed comparison
print("\n" + "="*70)
print("DETAILED COMPARISON:")
print("="*70)
for _, row in df.iterrows():
    h1_match = "✓" if row['H1'] == row['Emb'] else "✗"
    h2_match = "✓" if row['H2'] == row['Emb'] else "✗"
    print(f"{row['text']} {row['unit']}: H1={row['H1']}, H2={row['H2']}, Emb={row['Emb']} | H1:{h1_match} H2:{h2_match}")
