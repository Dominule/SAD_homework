import pandas as pd
import scipy.stats as stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import seaborn as sns
import matplotlib.pyplot as plt


"""
Solution from my close friend Gemini.
"""

# 1. PŘÍPRAVA DAT
# Vytvoření DataFrame ve "dlouhém" formátu (tidy format)
data = {
    'Linie': ['ALL']*3 + ['PML']*3 + ['MYE']*3 + ['LYM']*3 + ['CML']*3,
    'Exprese': [
        7.1835, 7.19263, 7.2657,   # ALL
        7.11836, 7.23998, 7.26544, # PML
        7.55379, 7.60075, 7.4909,  # MYE
        7.3758, 7.42104, 7.30891,  # LYM
        7.16879, 7.11564, 7.12803  # CML
    ]
}

df = pd.DataFrame(data)

print("--- Základní statistika ---")
print(df.groupby('Linie')['Exprese'].describe()[['count', 'mean', 'std']])
print("\n")

# 2. STATISTICKÝ TEST: One-Way ANOVA
# Musíme rozdělit data do polí podle skupin pro funkci f_oneway
skupiny = [df[df['Linie'] == l]['Exprese'] for l in df['Linie'].unique()]

f_stat, p_value = stats.f_oneway(*skupiny)

print("--- Výsledky ANOVA ---")
print(f"F-statistika: {f_stat:.4f}")
print(f"P-hodnota:    {p_value:.6f}")

if p_value < 0.05:
    print("Závěr: Existuje statisticky významný rozdíl mezi skupinami.")
else:
    print("Závěr: Nebyl nalezen statisticky významný rozdíl.")
print("\n")

# 3. POST-HOC TEST (Tukey HSD)
# Zjistíme, KTERÉ konkrétní skupiny se od sebe liší
tukey = pairwise_tukeyhsd(endog=df['Exprese'], groups=df['Linie'], alpha=0.05)

print("--- Tukey HSD Post-hoc test ---")
print(tukey)

# 4. VIZUALIZACE
# Nastavení vzhledu grafu
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))

# Boxplot pro rozdělení
ax = sns.boxplot(x='Linie', y='Exprese', data=df, palette="Set3", showfliers=False)

# Stripplot (jitter) pro zobrazení jednotlivých bodů (protože n=3)
sns.stripplot(x='Linie', y='Exprese', data=df, color='black', size=6, alpha=0.7)

plt.title('Porovnání exprese genu TRAPPC9 v buněčných liniích', fontsize=15)
plt.ylabel('Logaritmus signálu (mRNA)', fontsize=12)
plt.xlabel('Typ tkáňové kultury', fontsize=12)

plt.savefig("plots/tissue_culture_comparison.png")
plt.show()