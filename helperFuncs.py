from typing import List
import pandas as pd
"""
Converts the genome from a bit sequence into a heuristic sequence
"""
def fromGenToSeq(genome : str, heuristics : List[str]) -> List[str]:
    heuristicList = []
    # Converts the genome sequence of bits into a sequence of heuristics
    for i in range(0, len(genome), 2):
        heuristicList.append(heuristics[int(genome[i:i+2], 2)])

    return heuristicList

def fromGenToSeq2(genome : str, heuristics : List[str]) -> List[str]:
    heuristicList = []
    # Converts the genome sequence of bits into a sequence of heuristics
    for i in range(0, len(genome), 4):
        heuristicList.append(heuristics[int(genome[i:i+4], 2)])

    return heuristicList

heuristics = ['FFIT-FFIT', 'FFIT-BFIT', 'FFIT-WFIT','FFIT-AWFIT',
              'BFIT-FFIT', 'BFIT-BFIT', 'BFIT-WFIT','BFIT-AWFIT',
               'WFIT-FFIT', 'WFIT-BFIT', 'WFIT-WFIT','WFIT-AWFIT',
                'AWFIT-FFIT', 'AWFIT-BFIT', 'AWFIT-WFIT','AWFIT-AWFIT']

heuristics1 = ["FFIT", "BFIT", "WFIT", "AWFIT"]

