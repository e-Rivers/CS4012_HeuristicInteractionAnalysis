import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import os
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from helperFuncs import fromGenToSeq
import statsmodels.api as sm
from statsmodels.formula.api import ols

##40 DECISIONS

df_sequences_instances = pd.read_csv("df_sequences_instances.csv")
bit_seq = df_sequences_instances["Unnamed: 0"]
heuristics = ["FFIT", "BFIT", "WFIT", "AWFIT"]
bit_seq_transformed = bit_seq.apply(lambda x: fromGenToSeq(x, heuristics))

df_sequences_instances["Unnamed: 0"] = bit_seq_transformed

# Define a function to calculate the proportion of each heuristic
def calculate_proportions(seq, heuristic):
    return seq.count(heuristic) / len(seq) if len(seq) > 0 else 0

# Calculate the proportion of each heuristic and add as new columns
for heuristic in heuristics:
    df_sequences_instances[f'proportion_{heuristic}'] = df_sequences_instances["Unnamed: 0"].apply(lambda x: calculate_proportions(x, heuristic))
    plt.figure(figsize=(10, 6))
    plt.scatter(df_sequences_instances[f'proportion_{heuristic}'], df_sequences_instances['avg_norm'], alpha=0.5)
    plt.ylabel('Average Normalized Efficiency of Space')
    plt.xlabel(f'Proportion of {heuristic}')
    plt.title("Average Normalized Efficiency of Space")
    plt.grid(True)
    plt.savefig(f'proportions_heuristics/proportion_{heuristic}.png', dpi=300.0)


def calculate_proportions_last_half(seq, heuristic):
    if len(seq) == 0:
        return 0
    last_half = seq[len(seq)//2:]
    return last_half.count(heuristic) / len(last_half) if len(last_half) > 0 else 0



# Calculate the proportion of each heuristic in the last half and add as new columns
for heuristic in heuristics:
    df_sequences_instances[f'proportion_{heuristic}_last_half'] = df_sequences_instances["Unnamed: 0"].apply(lambda x: calculate_proportions_last_half(x, heuristic))
    plt.figure(figsize=(10, 6))
    plt.scatter(df_sequences_instances[f'proportion_{heuristic}_last_half'], df_sequences_instances['avg_norm'], alpha=0.5)
    plt.ylabel('Average Normalized Efficiency of Space')
    plt.xlabel(f'Proportion of {heuristic} in the last half')
    plt.title("Average Normalized Efficiency of Space")
    plt.grid(True)
    plt.savefig(f'proportions_heuristics/proportion_{heuristic}_last_half.png', dpi=300.0)




####BOX PLOT AND TUKEY

def perform_tests(choice_column, choice_type):
    # Perform ANOVA test
    model = ols(f'avg_norm ~ {choice_column}', data=df_sequences_instances).fit()
    anova_table = sm.stats.anova_lm(model, typ=2)
    print(f"ANOVA table for {choice_type} :")
    print(anova_table)
    
    # Perform Tukey's HSD test
    tukey = pairwise_tukeyhsd(endog=df_sequences_instances['avg_norm'],
                              groups=df_sequences_instances[choice_column],
                              alpha=0.05)
    print(f"Tukey HSD test results for {choice_type}:")
    print(tukey)
    
    # Plot the results
    tukey.plot_simultaneous()
    plt.title(f'Tukey HSD Test for avg_norm by {choice_type} ')
    plt.savefig(f'proportions_heuristics/boxplot_tukey/tukey_of_avg_norm_by_{choice_type}_Choice.png', dpi=300.0)
    
    # Plot the boxplot for visualization with custom colors
    palette = sns.color_palette("Set2")  # Custom colors
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=choice_column, y='avg_norm', data=df_sequences_instances, palette=palette)
    plt.xlabel(f'{choice_type} ')
    plt.ylabel('Average Normalized Efficiency Utilized (avg_norm)')
    plt.title(f'Boxplot of avg_norm by {choice_type} ')
    plt.grid(True)
    plt.savefig(f'proportions_heuristics/boxplot_tukey/Boxplot_of_avg_norm_by_{choice_type}_Choice.png', dpi=300.0)

# Perform tests for choices from 1 to 40
for choice_num in range(1, 41):
    choice_column = f'choice_{choice_num}'
    choice_type = f'Choice {choice_num}'
    df_sequences_instances[choice_column] = df_sequences_instances["Unnamed: 0"].apply(lambda x: x[choice_num - 1] if len(x) >= choice_num else None)
    df_sequences_instances = df_sequences_instances.dropna(subset=[choice_column])
    perform_tests(choice_column, choice_type)