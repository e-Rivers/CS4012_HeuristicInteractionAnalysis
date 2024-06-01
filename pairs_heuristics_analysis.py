import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import os
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from helperFuncs import fromGenToSeq2
import statsmodels.api as sm
from statsmodels.formula.api import ols

##20 DECISIONS

df_sequences_instances = pd.read_csv("df_sequences_instances.csv")
bit_seq = df_sequences_instances["Unnamed: 0"]
heuristics = ['FFIT-FFIT', 'FFIT-BFIT', 'FFIT-WFIT','FFIT-AWFIT',
              'BFIT-FFIT', 'BFIT-BFIT', 'BFIT-WFIT','BFIT-AWFIT',
               'WFIT-FFIT', 'WFIT-BFIT', 'WFIT-WFIT','WFIT-AWFIT',
                'AWFIT-FFIT', 'AWFIT-BFIT', 'AWFIT-WFIT','AWFIT-AWFIT']

bit_seq_transformed = bit_seq.apply(lambda x: fromGenToSeq2(x, heuristics))

df_sequences_instances["Unnamed: 0"] = bit_seq_transformed

# Define a function to calculate the proportion of each heuristic
def calculate_proportions(seq, heuristic):
    return seq.count(heuristic) / len(seq) if len(seq) > 0 else 0

# Define a function to categorize the proportion into intervals of 0.2
def categorize_proportions(proportion):
    return int(proportion / 0.2) * 0.2

# Calculate the proportion of each heuristic and add as new columns
for heuristic in heuristics:
    df_sequences_instances[f'proportion_{heuristic}'] = df_sequences_instances["Unnamed: 0"].apply(lambda x: calculate_proportions(x, heuristic))
    df_sequences_instances[f'proportion_category_{heuristic}'] = df_sequences_instances[f'proportion_{heuristic}'].apply(categorize_proportions)


# Calculate the proportion of each heuristic and add as new columns
i=0
myColors = ((0, 0.482, 1, 1), (1.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.502, 0, 0.502, 1))

for heuristic, color in zip(heuristics, myColors):
    df_sequences_instances[f'proportion_{heuristic}'] = df_sequences_instances["Unnamed: 0"].apply(lambda x: calculate_proportions(x, heuristic))
    plt.figure(figsize=(10, 6))
    plt.scatter(df_sequences_instances[f'proportion_{heuristic}'], df_sequences_instances['avg_norm'], alpha=0.5, color=color)
    plt.ylabel('Average Normalized Efficiency of Space')
    plt.xlabel(f'Proportion of {heuristic}')
    plt.title("Average Normalized Efficiency of Space")
    plt.grid(True)
    plt.savefig(f'proportions_pairs/proportion_{heuristic}.png', dpi=300.0)

# Create boxplots for each interval of 0.2 for each heuristic
for heuristic in heuristics:
    plt.figure(figsize=(10, 6))
    plt.boxplot([df_sequences_instances[df_sequences_instances[f'proportion_category_{heuristic}'] == category]['avg_norm'] for category in df_sequences_instances[f'proportion_category_{heuristic}'].unique()],
                labels=[round(category, 2) for category in df_sequences_instances[f'proportion_category_{heuristic}'].unique()])
    plt.ylabel('Average Normalized Efficiency of Space')
    plt.xlabel(f'Proportion of {heuristic}')
    plt.title("Average Normalized Efficiency of Space by Proportion Category")
    plt.grid(True)
    plt.savefig(f'proportions_pairs/boxplot_proportion_{heuristic}.png', dpi=300.0)

# Create histograms for each interval of 0.2 for each heuristic
for heuristic, color in zip(heuristics, myColors):
    ax = df_sequences_instances.hist(column=f'proportion_{heuristic}', color=color)
    plt.title(f'Histogram of Proportion of {heuristic}')
    plt.xlabel('Proportion of {heuristic}')
    plt.ylabel('Frequency')
    plt.savefig(f'proportions_pairs/histogram_proportion_{heuristic}.png', dpi=300.0)



# Save the plot
plt.savefig('histogram.png')

def calculate_proportions_last_half(seq, heuristic):
    if len(seq) == 0:
        return 0
    last_half = seq[len(seq)//2:]
    return last_half.count(heuristic) / len(last_half) if len(last_half) > 0 else 0

# Calculate the proportion of each heuristic in the last half and add as new columns
myColors = ((0, 0.482, 1, 1), (1.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.502, 0, 0.502, 1))

for heuristic, color in zip(heuristics, myColors):
    df_sequences_instances[f'proportion_{heuristic}_last_half'] = df_sequences_instances["Unnamed: 0"].apply(lambda x: calculate_proportions_last_half(x, heuristic))
    plt.figure(figsize=(10, 6))
    plt.scatter(df_sequences_instances[f'proportion_{heuristic}_last_half'], df_sequences_instances['avg_norm'], alpha=0.5, color=color)
    plt.ylabel('Average Normalized Efficiency of Space')
    plt.xlabel(f'Proportion of {heuristic} in the last half')
    plt.title("Average Normalized Efficiency of Space")
    plt.grid(True)
    plt.savefig(f'proportions_pairs/proportion_{heuristic}_last_half.png', dpi=300.0)


# Create histograms for each interval of 0.2 for each heuristic last half
for heuristic, color in zip(heuristics, myColors):
    ax = df_sequences_instances.hist(column=f'proportion_{heuristic}_last_half', color=color)
    plt.title(f'Histogram of Proportion of {heuristic} in the last half')
    plt.xlabel('Proportion of {heuristic} in the last half')
    plt.ylabel('Frequency')
    plt.savefig(f'proportions_pairs/histogram_proportion_{heuristic}_lastHalf.png', dpi=300.0)



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
                              alpha=0.01)
    
    with open('anova_tukey_pairs_20.txt', 'a') as f:
        f.write(f"ANOVA table for {choice_type} :\n")
        f.write(f"{anova_table}\n\n")
        f.write(f"Tukey HSD test results for {choice_type}:\n")
        f.write(f"{tukey}\n\n")   
    
    # Plot the results
    tukey.plot_simultaneous()
    plt.title(f'Tukey HSD Test for avg_norm by {choice_type} ')
    plt.savefig(f'proportions_pairs/boxplot_tukey/tukey_of_avg_norm_by_{choice_type}_Choice.png', dpi=300.0)
    
    # Plot the boxplot for visualization with custom colors
    palette = sns.color_palette("Set2")  # Custom colors
    plt.figure(figsize=(10, 6))
    sns.boxplot(x=choice_column, y='avg_norm', data=df_sequences_instances, palette=palette)
    plt.xlabel(f'{choice_type} ')
    plt.ylabel('Average Normalized Efficiency Utilized (avg_norm)')
    plt.title(f'Boxplot of avg_norm by {choice_type} ')
    plt.grid(True)
    plt.savefig(f'proportions_pairs/boxplot_tukey/Boxplot_of_avg_norm_by_{choice_type}_Choice.png', dpi=300.0)

# Perform tests for choices from 1 to 20/2
for choice_num in range(1, 11):
    choice_column = f'choice_{choice_num}'
    choice_type = f'Choice {choice_num}'
    df_sequences_instances[choice_column] = df_sequences_instances["Unnamed: 0"].apply(lambda x: x[choice_num - 1] if len(x) >= choice_num else None)
    df_sequences_instances = df_sequences_instances.dropna(subset=[choice_column])
    perform_tests(choice_column, choice_type)


print(df_sequences_instances['avg_norm'].max())
print(df_sequences_instances['avg_norm'].min())

