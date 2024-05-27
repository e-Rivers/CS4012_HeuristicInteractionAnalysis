from typing import List

"""
Converts the genome from a bit sequence into a heuristic sequence
"""
def fromGenToSeq(genome : str, heuristics : List[str]) -> List[str]:
    heuristicList = []
    # Converts the genome sequence of bits into a sequence of heuristics
    for i in range(0, len(genome), 2):
        heuristicList.append(heuristics[int(genome[i:i+2], 2)])

    return heuristicList