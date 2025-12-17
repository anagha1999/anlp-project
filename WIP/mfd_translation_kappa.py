from sklearn.metrics import cohen_kappa_score
import numpy as np

print("="*70)
print("MFD TRANSLATION EVALUATION - Cohen's Kappa")
print("="*70)

# KANNADA: Semantic equivalence coding based on evaluation table
# 1 = semantically equivalent (share root, morphological variant, or identical)
# 0 = different meaning/interpretation

# Human 1 vs Human 2 (do they give equivalent translations?)
kannada_h1_h2 = [
    1,  # prejudicing - morphological variant (poorvagraha variants)
    1,  # curses - identical root (shaapa)
    1,  # honest - identical
    1,  # blood - identical  
    0,  # double - different (dupatta vs dwiguna)
    1,  # sympathizers - same root (sahānubhūti)
    1,  # repenting - same root (pashchattapa)
    0,  # repulses - different (disgust vs magnetic force)
    1,  # vomiting - same root (vaanti)
    0,  # heresies - different (traitors vs delusions)
]

# Sarvam AI vs Human 1
kannada_mt_h1 = [
    1,  # prejudicing - morphological match
    1,  # curses - identical
    1,  # honest - identical  
    1,  # blood - identical
    0,  # double - MT=betrayal, H1=dupatta (different)
    1,  # sympathizers - same root
    1,  # repenting - same root (noun vs verb phrase)
    0,  # repulses - MT=retreat, H1=disgust (different)
    1,  # vomiting - identical
    0,  # heresies - MT=apostasy, H1=traitors (different)
]

# Sarvam AI vs Human 2
kannada_mt_h2 = [
    1,  # prejudicing - identical
    1,  # curses - morphological (singular vs plural)
    1,  # honest - identical
    1,  # blood - identical
    0,  # double - MT=betrayal, H2=duplicate (different)
    1,  # sympathizers - same root
    1,  # repenting - same root
    0,  # repulses - MT=retreat, H2=magnetic (different)
    1,  # vomiting - morphological
    0,  # heresies - MT=apostasy, H2=delusion (different)
]

# TAMIL: Semantic equivalence coding
tamil_h1_h2 = [
    0,  # compassion - H1=mercy(இறக்கம்), H2=compassion(கருணை) - different nuance
    0,  # harm - H1=suffering, H2=abstract harm - different
    1,  # equality - identical
    1,  # cheat - morphological variants
    1,  # team player - identical
    0,  # traitor - H1=traitor, H2=lack of integrity - different
    1,  # respect - identical
    1,  # disrespect - identical
    1,  # sanctity - identical (spacing difference only)
    1,  # impurity - H1=H2=asuththam (both humans agree)
]

tamil_mt_h1 = [
    0,  # compassion - MT=karuna, H1=mercy (different)
    0,  # harm - MT=theengu, H1=suffering (different)
    1,  # equality - identical
    1,  # cheat - morphological
    1,  # team player - near identical
    1,  # traitor - identical
    1,  # respect - identical
    1,  # disrespect - identical
    1,  # sanctity - identical
    0,  # impurity - MT=maasu, H1=asuththam (different)
]

tamil_mt_h2 = [
    1,  # compassion - MT=H2=karuna
    1,  # harm - MT=H2=theengu  
    1,  # equality - identical
    1,  # cheat - morphological
    1,  # team player - identical
    0,  # traitor - H2=lack of integrity (different)
    1,  # respect - identical
    1,  # disrespect - identical
    1,  # sanctity - identical
    0,  # impurity - MT=maasu, H2=asuththam (different)
]

# Calculate agreement percentages
kan_h1_h2 = sum(kannada_h1_h2) / len(kannada_h1_h2) * 100
kan_mt_h1 = sum(kannada_mt_h1) / len(kannada_mt_h1) * 100
kan_mt_h2 = sum(kannada_mt_h2) / len(kannada_mt_h2) * 100

tam_h1_h2 = sum(tamil_h1_h2) / len(tamil_h1_h2) * 100
tam_mt_h1 = sum(tamil_mt_h1) / len(tamil_mt_h1) * 100
tam_mt_h2 = sum(tamil_mt_h2) / len(tamil_mt_h2) * 100

# Cohen's Kappa
kappa_kan_h1_h2 = cohen_kappa_score(kannada_h1_h2, kannada_mt_h1)  # H1-H2 pattern vs MT-H1 pattern
kappa_kan_mt = cohen_kappa_score(kannada_mt_h1, kannada_mt_h2)  # MT consistency with both humans

kappa_tam_h1_h2 = cohen_kappa_score(tamil_h1_h2, tamil_mt_h1)
kappa_tam_mt = cohen_kappa_score(tamil_mt_h1, tamil_mt_h2)

# More meaningful kappa: agreement on which words are "hard" vs "easy"
kappa_kan_pattern = cohen_kappa_score(kannada_h1_h2, kannada_mt_h1)
kappa_tam_pattern = cohen_kappa_score(tamil_h1_h2, tamil_mt_h1)

print("\nKANNADA (n=10 MFD words):")
print(f"  Human 1 vs Human 2 agreement:  {kan_h1_h2:.0f}% (7/10)")
print(f"  Sarvam AI vs Human 1:          {kan_mt_h1:.0f}% (7/10)")
print(f"  Sarvam AI vs Human 2:          {kan_mt_h2:.0f}% (7/10)")
print(f"  Cohen's κ (MT-H1 vs MT-H2):    {kappa_kan_mt:.3f}")

print("\nTAMIL (n=10 MFD words):")
print(f"  Human 1 vs Human 2 agreement:  {tam_h1_h2:.0f}% (7/10)")
print(f"  Sarvam AI vs Human 1:          {tam_mt_h1:.0f}% (7/10)")  
print(f"  Sarvam AI vs Human 2:          {tam_mt_h2:.0f}% (8/10)")
print(f"  Cohen's κ (MT-H1 vs MT-H2):    {kappa_tam_mt:.3f}")

print("\n" + "="*70)
print("SUMMARY TABLE")
print("="*70)
print(f"\n{'Metric':<30} {'Kannada':<15} {'Tamil':<15}")
print("-"*60)
print(f"{'H1 vs H2 agreement':<30} {kan_h1_h2:.0f}%{'':<12} {tam_h1_h2:.0f}%")
print(f"{'Sarvam AI vs H1':<30} {kan_mt_h1:.0f}%{'':<12} {tam_mt_h1:.0f}%")
print(f"{'Sarvam AI vs H2':<30} {kan_mt_h2:.0f}%{'':<12} {tam_mt_h2:.0f}%")
print(f"{'κ (MT pattern consistency)':<30} {kappa_kan_mt:.3f}{'':<12} {kappa_tam_mt:.3f}")

print("\n" + "="*70)
print("KEY FINDING")
print("="*70)
print("""
Sarvam AI achieves 70% semantic equivalence with human translators for 
both Kannada and Tamil MFD terms—matching the 70% inter-annotator 
agreement between the two human translators. This indicates that MT 
performance is comparable to human translation variability for moral 
vocabulary, with disagreements concentrated on polysemous terms 
(double, repulses, heresies) and culturally-nuanced concepts.
""")
