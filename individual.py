from typing import Tuple
import time
import random

class Individual:

    def __init__(self, genome : str):
        self._genome = genome 
        
    def setRandomGenome(self, geneVariations : int, genomeLength : int) -> None:
        random.seed(time.time())
        self._genome = ""
        for _ in range(genomeLength):
            # Chooses a random gene and encodes it as binary
            choice = random.randrange(geneVariations)
            bitEncodedGene = bin(choice)[2:] if choice > 1 else "0"+bin(choice)[2:]
            self._genome += bitEncodedGene
        
    def mutate(self) -> None:
        random.seed(time.time())
        selectedGene = random.randrange(self.getGenomeLen())
        modifiedBit = str(int(not int(self._genome[selectedGene])))
        self._genome = self._genome[:selectedGene] + modifiedBit + self._genome[selectedGene+1:]
    
    def recombine(self, mateIndividual):
        random.seed(time.time())
        slicingSection = random.randrange(self.getGenomeLen())
        child1 = Individual(self._split(0,slicingSection) + mateIndividual._split(slicingSection, mateIndividual.getGenomeLen()))
        child2 = Individual(mateIndividual._split(0,slicingSection) + self._split(slicingSection, self.getGenomeLen()))
        return [child1, child2]

    def getGenomeLen(self) -> int:
        return len(self._genome)

    def getGenome(self) -> str:
        return self._genome
    
    def _split(self, firstCut : int, secondCut : int) -> str:
        return self._genome[firstCut : secondCut]

    def __str__(self):
        return self._genome