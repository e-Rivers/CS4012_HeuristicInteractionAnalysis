from genetic import GeneticModel
from bpp import BPP
from typing import List
from phermes import HyperHeuristic
import os
import pandas as pd
import numpy as np

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
    problemInstances = pd.read_csv(f"BPP-{testGroup}.csv")
    total_gens = 0
    for index, row in problemInstances.iterrows():
        filename = row["INSTANCE"]
        oracleValue = row["ORACLE"]

        problem = BPP(testGroup + "/" + filename)
        
        # EVOLUTION PROCESS GOES HERE
        #print(f"\nProblem Instance {index}")
        #print(f"\nProblem Name {filename}")
        gens = hyperHeuristic.solve(problem, oracleValue, ["lion_pride"])
        total_gens += gens
    print("total gens", total_gens)        

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
gen = GeneticModel(features, heuristics, 100, 4)
solveHH("Test I", gen)
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