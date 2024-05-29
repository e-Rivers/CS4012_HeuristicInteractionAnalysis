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
    heuristicSpaceToExplore = 60

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

###### ANALYSIS

def dendogram_analysis(allScores_allSequences : dict, dict1 : dict, testGroup : str):
    problemInstances = pd.read_csv(f"BPP-{testGroup}.csv")
    column_values = problemInstances["INSTANCE"]

    
    # Get the array's values and make a matrix of sequences vs instances
    matrix_allScores_allSequences = np.vstack(list(allScores_allSequences.values()))

    # Create a dataframe 
    df_allScores_allSequences = pd.DataFrame(matrix_allScores_allSequences, index=allScores_allSequences.keys(), columns=column_values)

    # Rotate the dataframe in order to have the instances in the columns
    df_allScores_allSequences.transpose()
    
    # Rename from sequences to heuristics 01010101 -> "bfit", "bfit"
    #df_allScores_allSequences.rename(index=lambda x: fromGenToSeq(x, heuristics), inplace=True)

    # Get the values of the average of the evaluation of each sequence
    avg_norm = np.vstack(list(dict1.values()))

    # Update the dataframe with the average of the evaluation of each sequence
    df_allScores_allSequences['avg_norm'] = avg_norm

    ########### ANALYZING THE TOP 30 SEQUENCES WITH THE WORST PERFORMANCE ###########
    
    # Sort the dataframe
    df_sorted = df_allScores_allSequences.sort_values(by='avg_norm', ascending=True)
    
    #Delete the column with the average of the evaluation of each sequence
    df_sorted = df_sorted.drop(columns=['avg_norm'])

    # Create the clustermap with a larger figure size and specific aspect ratio
    g = sns.clustermap(df_sorted.head(30), cmap='RdYlBu_r')

    # Adjust the y-axis label size
    g.ax_heatmap.set_yticklabels(g.ax_heatmap.get_ymajorticklabels(), fontsize=6)  # Set the y-axis labels font size

    g.savefig("30_worst.png")

    ########### ANALYZING THE TOP 30 SEQUENCES WITH THE BEST PERFORMANCE ###########

    # Create the clustermap with a larger figure size and specific aspect ratio
    h = sns.clustermap(df_sorted.tail(30), cmap='RdYlBu_r')

    # Adjust the y-axis label size
    h.ax_heatmap.set_yticklabels(g.ax_heatmap.get_ymajorticklabels(), fontsize=6)  # Set the y-axis labels font size

    h.savefig("30_best.png")

    ########### ANALYZING THE TOP 30 SEQUENCES WITH MORE VARIANCE ###########
    # Calculate the standard deviation for each row
    row_std_dev = df_sorted.std(axis=1)

    # Select the top 30 rows with the highest standard deviation
    top_30_rows_indices = row_std_dev.nlargest(30).index

    # Create a new DataFrame containing only the top 30 rows
    df_top_30_rows = df_sorted.loc[top_30_rows_indices]  

    # Create the clustermap with a larger figure size and specific aspect ratio
    k = sns.clustermap(df_top_30_rows, cmap='RdYlBu_r')

    # Adjust the y-axis label size
    k.ax_heatmap.set_yticklabels(g.ax_heatmap.get_ymajorticklabels(), fontsize=6)  # Set the y-axis labels font size

    k.savefig("30_std_dev_more.png")

    ### with LESS standar deviation

    bottom_30_rows_indices = row_std_dev.nsmallest(30).index

    # Create a new DataFrame containing only the bottom 30 rows
    df_bottom_30_rows = df_sorted.loc[bottom_30_rows_indices]

    # Create the clustermap with a larger figure size and specific aspect ratio
    m = sns.clustermap(df_bottom_30_rows, cmap='RdYlBu_r')

    # Adjust the y-axis label size
    m.ax_heatmap.set_yticklabels(g.ax_heatmap.get_ymajorticklabels(), fontsize=6)  # Set the y-axis labels font size

    m.savefig("30_std_dev_less.png")

    ##################################################
    ##### SELECTING THE 30 INSTANCES WITH MORE CHANGES

    std_dev = df_sorted.std()

    # Select the top 30 columns with the greatest standard deviation
    top_30_columns = std_dev.nlargest(30).index

    # Create a new DataFrame containing only the top 30 columns
    df_top_30 = df_sorted[top_30_columns]

    ########### ANALYZING THE TOP 30 SEQUENCES WITH THE WORST PERFORMANCE ###########
    

    # Create the clustermap with a larger figure size and specific aspect ratio
    i = sns.clustermap(df_top_30.head(30), cmap='RdYlBu_r')

    # Adjust the y-axis label size
    i.ax_heatmap.set_yticklabels(g.ax_heatmap.get_ymajorticklabels(), fontsize=6)  # Set the y-axis labels font size

    i.savefig("30_worst_30_instances.png")

     ########### ANALYZING THE TOP 30 SEQUENCES WITH THE BEST PERFORMANCE ###########
    

    # Create the clustermap with a larger figure size and specific aspect ratio
    j = sns.clustermap(df_top_30.tail(30), cmap='RdYlBu_r')

    # Adjust the y-axis label size
    j.ax_heatmap.set_yticklabels(g.ax_heatmap.get_ymajorticklabels(), fontsize=6)  # Set the y-axis labels font size

    j.savefig("30_best_30_instances.png")





dendogram_analysis(allScores_allSequences,dict1, "Test I")




