import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import os

df_sequences_instances = pd.read_csv("df_sequences_instances.csv")

for filename in os.listdir('labels'):
    y_labels_df = pd.read_csv(os.path.join('labels', F"{filename}"))


    y_labels_series = y_labels_df['y_labels']

    bit_series = df_sequences_instances.iloc[y_labels_df['y_labels']]['Unnamed: 0']
    bit_strings = list(bit_series)[::-1]

    # Convert bit strings to a 2D numpy array
    bit_matrix = np.array([list(map(int, list(bit_string))) for bit_string in bit_strings])


    gene_matrix = np.zeros((bit_matrix.shape[0], bit_matrix.shape[1] // 2))
    for i in range(bit_matrix.shape[0]):
        row = bit_matrix[i]
        for j in range(0, row.shape[0], 2):
            binary = str(row[j]) + str(row[j + 1])
            num = int(binary, 2)
            gene_matrix[i][j // 2] = num


    #print(gene_matrix)
    bgene_matrix = np.full(gene_matrix.shape, fill_value='', dtype='object')

    for i in range(gene_matrix.shape[0]):
        bin_str_row = ''
        for ind, val in enumerate(gene_matrix[i]):
            bin_str = bin(int(val))[2:].rjust(2, '0')
            #print(bin_str, i, ind)
            bgene_matrix[i, ind] = bin_str
            #print(bin_str)
            
    #print(bit_matrix.shape)
    #print(gene_matrix.shape)

    # Plotting the binary matrix
    plt.figure(figsize=(12, 8))
    bgene_matrix_df = pd.DataFrame(bgene_matrix)
    #print(bgene_matrix_df)

    myColors = ((0, 0.482, 1, 1), (1.0, 0.0, 0.0, 1.0), (0.0, 0.0, 0.0, 1.0), (0.502, 0, 0.502, 1))
    cmap = LinearSegmentedColormap.from_list('Custom', myColors, len(myColors))


    ax = sns.heatmap(gene_matrix, 
                annot=bgene_matrix_df, 
                xticklabels=range(1, len(gene_matrix[0]) + 1), 
                yticklabels=list(y_labels_series), fmt='', cmap=cmap)

    # Manually specify colorbar labelling after it's been generated
    colorbar = ax.collections[0].colorbar
    colorbar.set_ticks([0.375, 1.125, 1.875, 2.625])
    colorbar.set_ticklabels(['FFIT (00)', 'BFIT (01)', 'WFIT (10)', 'AWFIT (11)'])

    #plt.title(f"{filename[5:-4]}")
    plt.xlabel("Heuristic Position")
    plt.ylabel("Bit String id")
    plt.savefig(os.path.join('individuals_comps', f'{filename[5:-4]}.png'), dpi=500.0)
