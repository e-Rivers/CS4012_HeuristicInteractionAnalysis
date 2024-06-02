from geneticAll import GeneticModel
from bpp import BPP
from typing import List
from phermes import HyperHeuristic
import os
import pandas as pd
import numpy as np
import time

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
    heuristicSpaceToExplore = 10_000

    with open("time.txt", "w") as file:
        file.write(str(heuristicSpaceToExplore) + '\n')

    prueba = hyperHeuristic.solveAll(testGroup, heuristicSpaceToExplore, ["strongest"])
    #prueba = hyperHeuristic.solveAll(testGroup, heuristicSpaceToExplore)
    return prueba

def save_results_csv(allScores_allSequences : dict, dict1 : dict, testGroup : str):
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
    df_sorted.to_csv("df_sequences_instances.csv", index = True)
    
    row_names_df = pd.DataFrame(df_sorted.index, columns=['Row Names'])
    row_names_df.to_csv("index_sequences.csv", index=False)


# For BPP
start = time.time()

features = ["LENGTH", "SMALL", "LARGE"]
heuristics = ["FFIT", "BFIT", "WFIT", "AWFIT"]
gen = GeneticModel(features, heuristics, 100, 5)
dict1, allScores_allSequences, avgBins = solveHH("Test I", gen)
#solveHH("Test II", gen)
#solveHH("Training", gen)
##### IMPORTANT, CHANGE THE TEST I IF NEEDED #######
save_results_csv(allScores_allSequences,dict1, "Test I")

elapsed = time.time() - start
with open("time.txt", "w") as file:
        file.write(str(elapsed) + '\n')
