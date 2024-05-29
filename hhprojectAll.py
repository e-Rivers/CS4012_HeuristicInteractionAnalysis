from geneticAll import GeneticModel
from bpp import BPP
from typing import List
from phermes import HyperHeuristic
import os
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from helperFuncs import fromGenToSeq


def characterize(domain : str, folder : str, features : List[str]):
    """
      Characterizes the instances contained in a folder.
    """
    text = ""
    files = os.listdir(folder)
    files.sort()
    text += "INSTANCE\t" + "\t".join(features) + "\r\n"
    for file in files:    
        if domain == "KP":
            problem = KP(folder + "/" + file)
        elif domain == "BPP":
            problem = BPP(folder + "/" + file)
        elif domain == "VCP":
            problem = VCP(folder + "/" + file)
        elif domain == "FFP":
            problem = FFP(folder + "/" + file)
        else:
            raise Exception("Problem domain '" + domain + "' is not recognized by the system.") 
        text += file + "\t"

        for f in features:
            text += str(round(problem.getFeature(f), 3)) + "\t"
        text += "\r\n"  
    print(text)

def solve(domain : str, folder : str, heuristics : List[str]):
    text = ""
    files = os.listdir(folder)
    files.sort()
    text += "INSTANCE\t" + "\t".join(heuristics) + "\r\n"  
    for i in range(len(files)):    
        text += files[i] + "\t"   
        for h in heuristics:
            if domain == "KP":
                problem = KP(folder + "/" + files[i])
            elif domain == "BPP":
                problem = BPP(folder + "/" + files[i])
            elif domain == "VCP":
                problem = VCP(folder + "/" + files[i])
            elif domain == "FFP":
                np.random.seed(i)
                problem = FFP(folder + "/" + files[i])
            else:
                raise Exception("Problem domain '" + domain + "' is not recognized by the system.")      
            problem.solve(h)
            text += str(round(problem.getObjValue(), 3)) + "\t"
        text += "\r\n"  
    print(text)

def solveHH(testGroup : str, hyperHeuristic : HyperHeuristic):
    heuristicSpaceToExplore = 40 if testGroup == "Test II" else 20
    heuristicSpaceToExplore = int((len(hyperHeuristic.getHeuristics())**heuristicSpaceToExplore)*0.25)

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
    # WARNING, TAKE EXTREME CAUTION IF YOU WANT TO USE THE REAL HEURISTIC SPACE, IF SO, COMMENT THE LINE BELOW AND MAY GOD HELP YOU... RIP  # 
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! #
    heuristicSpaceToExplore = 100000

    prueba = hyperHeuristic.solveAll(testGroup, heuristicSpaceToExplore)
    return prueba

# Trains and tests a KNN hyper-heuristic on any of the given problem domains.
# To test it, uncomment the corresponding code.

"""
# For KP
features = ["WEIGHT", "PROFIT", "CORRELATION"]
heuristics = ["DEF", "MAXP", "MAXPW", "MINW", "MARK"]
hh = KNNHH(features, heuristics, 3)
hh.train("Instances/KP/KP-Training.csv")
solveHH("KP", "Instances/KP/Test I", hh)
"""

# For BPP
features = ["LENGTH", "SMALL", "LARGE"]
heuristics = ["FFIT", "BFIT", "WFIT", "AWFIT"]
gen = GeneticModel(features, heuristics, 100, 3)
dict1, allScores_allSequences = solveHH("Test I", gen)
#solveHH("Test II", gen)
#solveHH("Training", gen)

"""
features = ["DENSITY", "MAX_DEG", "MIN_DEG"]
heuristics = ["DEF", "DEG", "COL_DEG", "UNCOL_DEG"]
hh = KNNHH(features, heuristics, 3)
hh.train("Instances/VCP/VCP-Training.csv")
solveHH("VCP", "Instances/VCP/Test I", hh)
"""

"""
features = ["DENSITY", "MAX_DEG", "MIN_DEG", "COST"]
heuristics = ["DEF", "DEG", "RISK_DEG"]
hh = KNNHH(features, heuristics, 3)
hh.train("Instances/FFP/FFP-Training.csv")
solveHH("FFP", "Instances/FFP/Test I", hh)
"""

###### ANALYSIS ######

def clustermap_analysis(df, filename):
    g = sns.clustermap(df, cmap='RdYlBu_r')
    g.ax_heatmap.set_yticklabels(g.ax_heatmap.get_ymajorticklabels(), fontsize=6)
    g.savefig(filename)

def dendogram_analysis(allScores_allSequences : dict, dict1 : dict, testGroup : str):
    problemInstances = pd.read_csv(f"BPP-{testGroup}.csv")
    column_values = problemInstances["INSTANCE"]

    # Generate a dataframe with sequences as rows and instances as columns
    matrix_allScores_allSequences = np.vstack(list(allScores_allSequences.values()))
    df_allScores_allSequences = pd.DataFrame(matrix_allScores_allSequences, index=allScores_allSequences.keys(), columns=column_values)
    df_allScores_allSequences.transpose()

    # Rename from sequences to heuristics 01010101 -> "bfit", "bfit"
    #df_allScores_allSequences.rename(index=lambda x: fromGenToSeq(x, heuristics), inplace=True)

    # add the avg score for each sequence to the dataframe in order to sort it
    avg_norm = np.vstack(list(dict1.values()))
    df_allScores_allSequences['avg_norm'] = avg_norm

    # sort the dataframe
    df_sorted = df_allScores_allSequences.sort_values(by='avg_norm', ascending=True)

    # delete the column, because we are not analysing the average yet
    df_sorted_without_avg = df_sorted.drop(columns=['avg_norm'])

    # analyze the 30 sequences with BEST and WORST average
    clustermap_analysis(df_sorted_without_avg.head(30), "30_worst.png")
    clustermap_analysis(df_sorted_without_avg.tail(30), "30_best.png")

    # calculate standard deviation and visualize the 30 sequences with more variance
    row_std_dev = df_sorted.std(axis=1)
    top_30_rows_indices = row_std_dev.nlargest(30).index
    df_top_30_rows = df_sorted.loc[top_30_rows_indices]  
    clustermap_analysis(df_top_30_rows, "30_std_dev_more.png")

    # visualize the 30 sequences with less variance
    bottom_30_rows_indices = row_std_dev.nsmallest(30).index
    df_bottom_30_rows = df_sorted.loc[bottom_30_rows_indices]
    clustermap_analysis(df_bottom_30_rows, "30_std_dev_less.png")

    # visualize only the 30 instances with more variance
    std_dev = df_sorted.std()
    top_30_columns = std_dev.nlargest(30).index
    df_top_30 = df_sorted[top_30_columns]

    # visualize only the 30 instances with less variance
    std_dev = df_sorted.std()
    bottom_30_columns = std_dev.nsmallest(30).index
    df_bottom_30 = df_sorted[bottom_30_columns]    

    clustermap_analysis(df_top_30.head(30), "30_worst_30_instances.png")
    clustermap_analysis(df_top_30.tail(30), "30_best_30_instances.png")
    clustermap_analysis(df_bottom_30.head(30), "30_worst_30_instances_less.png")
    clustermap_analysis(df_bottom_30.tail(30), "30_best_30_instances_less.png")


dendogram_analysis(allScores_allSequences,dict1, "Test I")




