######################
###### ANALYSIS ######
######################
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from helperFuncs import fromGenToSeq
from sklearn.cluster import KMeans
from kneed import KneeLocator
from sklearn.decomposition import PCA
from matplotlib.lines import Line2D
import os


def clustermap_analysis(df, filename):

    g = sns.clustermap(df, cmap="RdYlBu_r", cbar_kws={'label': 'Color Scale', 'ticks': [df.min().min(), df.max().max()], 'orientation': 'vertical', 'fontsize': 14})
    y_labels = g.dendrogram_row.reordered_ind
    y_labels_df = pd.DataFrame({'y_labels': [df.index[i] for i in y_labels]})
    
    g.ax_heatmap.set_yticklabels(g.ax_heatmap.get_ymajorticklabels(), fontsize=19)
    g.ax_heatmap.set_xticklabels([])  # Remove x-axis labels

    g.savefig(filename)
    y_labels_df.to_csv(os.path.join('labels', f'y_ls_{filename[:-4]}.csv'))
    

def dendogram_analysis(df_sorted):

    # delete the column, because we are not analysing the average yet
    print(df_sorted)
    df_sorted_without_avg = df_sorted.drop(columns=['avg_norm', 'Unnamed: 0', 'opened_bins', 'closed_bins'])
    #df_sorted_without_avg = df_sorted.drop(columns=['avg_norm', 'Unnamed: 0'])

    pattern = r'Hard([A-Z]{2,3})_.*?(\d{3})\.bpp'

    # Use the str.extract method to apply the pattern to the column names
    new_columns = df_sorted_without_avg.columns.str.extract(pattern)

    # Combine the extracted parts to form the new column names
    df_sorted_without_avg.columns = new_columns[0] + '_' + new_columns[1]

    # analyze the 30 sequences with BEST and WORST average
    clustermap_analysis(df_sorted_without_avg.head(30), "30_worst.png")
    clustermap_analysis(df_sorted_without_avg.tail(30), "30_best.png")

    print(df_sequences_instances)

    # calculate standard deviation and visualize the 30 sequences with more variance
    row_std_dev = df_sorted_without_avg.std(axis=1)
    top_30_rows_indices = row_std_dev.nlargest(30).index
    df_top_30_rows = df_sorted_without_avg.loc[top_30_rows_indices]  
    clustermap_analysis(df_top_30_rows, "30_std_dev_more.png")

    # visualize the 30 sequences with less variance
    bottom_30_rows_indices = row_std_dev.nsmallest(30).index
    df_bottom_30_rows = df_sorted_without_avg.loc[bottom_30_rows_indices]
    clustermap_analysis(df_bottom_30_rows, "30_std_dev_less.png")

    # visualize only the 30 instances with more variance
    std_dev = df_sorted_without_avg.std()
    top_30_columns = std_dev.nlargest(30).index
    df_top_30 = df_sorted_without_avg[top_30_columns]

    # visualize only the 30 instances with less variance
    std_dev = df_sorted_without_avg.std()
    bottom_30_columns = std_dev.nsmallest(30).index
    df_bottom_30 = df_sorted_without_avg[bottom_30_columns]    

    clustermap_analysis(df_top_30.head(30), "30_worst_30_instances.png")
    clustermap_analysis(df_top_30.tail(30), "30_best_30_instances.png")
    clustermap_analysis(df_bottom_30.head(30), "30_worst_30_instances_less.png")
    clustermap_analysis(df_bottom_30.tail(30), "30_best_30_instances_less.png")


def cluster_sequences(df_sequences_instances):
    # 
    df_sequences_instances = df_sequences_instances.drop(columns=['avg_norm'])

    kmeans_kwargs = {
     "init": "random",
     "n_init": 10,
     "max_iter": 300,
     "random_state": 0,
    }

    # A list holds the SSE values for each k
    sse = []
    for k in range(1, 20):
        kmeans = KMeans(n_clusters=k, **kmeans_kwargs)
        kmeans.fit(df_sequences_instances)
        sse.append(kmeans.inertia_)
    
    #Select the number of clusters
    kl = KneeLocator(
        range(1, 20), sse, curve="convex", direction="decreasing"
    )
    cluster_number = int(kl.elbow)

    pca = PCA(n_components=2)
    principalComponents = pca.fit_transform(df_sequences_instances)
    principalDf = pd.DataFrame(data = principalComponents                    
             , columns = ['pc_1', 'pc_2'])
    
    # clustering using k-means

    kmeans = KMeans(n_clusters=cluster_number, **kmeans_kwargs)
    kmeans.fit(df_sequences_instances)

    df_sequences_instances["clusters"] = kmeans.labels_

    ## plot pca
    df_target = pd.DataFrame(kmeans.labels_, columns = ['target'])
    finalDf = pd.concat([principalDf,df_target], axis = 1)

    
    colors = [
    'red', 'green', 'blue', 'cyan', 'magenta', 'yellow', 'black', 'white', 'gray', 'orange',
    'purple', 'pink', 'brown', 'lime', 'olive', 'maroon', 'navy', 'teal', 'aqua', 'silver',
    'gold', 'beige', 'coral', 'crimson', 'darkblue', 'darkcyan', 'darkgreen', 'darkkhaki', 'darkmagenta', 'darkorange'
    ]
    finalDf['c'] = finalDf.target.map({0:colors[0], 1:colors[1], 2:colors[2], 3:colors[3], 4:colors[4],
                                       5:colors[5], 6:colors[6], 7:colors[7],8:colors[8], 9:colors[9],
                                       10:colors[10], 11:colors[11], 12:colors[12],13:colors[13], 14:colors[14],
                                       15:colors[15], 16:colors[16], 17:colors[17],18:colors[18], 19:colors[19],
                                       })


    fig, ax = plt.subplots(1, figsize=(8,8))
    # plot data
    plt.scatter(finalDf.pc_1, finalDf.pc_2, c=finalDf.c, alpha = 0.6, s=10)
    plt.title('PCA 2D\n', loc='left', fontsize=22)
    plt.xlabel('PC_1')
    plt.ylabel('PC_2')

    df_sequences_instances.to_csv("df_sequences_instances_clusters.csv", index = False)
    
df_sequences_instances = pd.read_csv("df_sequences_instances_Exp4.csv")
print("HOLA")

#cluster_sequences(df_sequences_instances)

dendogram_analysis(df_sequences_instances)


