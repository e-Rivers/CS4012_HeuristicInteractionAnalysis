from phermes import Problem
from phermes import HyperHeuristic
from typing import List, Type, Tuple
from individual import Individual
import random
import time

class GeneticModel(HyperHeuristic):

    def __init__(self, features : List[str], heuristics : List[str], maxGenerations : int, population : int):
        super().__init__(features, heuristics)
        self._generation = List[Individual]
        self._populationSize = population
        self._maxGenerations = maxGenerations
        self._geneToTest = None

    def _initGeneration(self, problemSize : int) -> None:
        random.seed(time.time())
        self._generation = [Individual("0"*problemSize) for _ in range(self._populationSize)]
        for individual in self._generation:
            individual.setRandomGenome(len(self._heuristics), problemSize)
        
        # DISPLAY THE GENERATED INDIVIDUALS
        #print(*self._generation, sep="\n")
    
    def _evaluateGeneration(self, thisGeneration : List[Individual], problem : Problem) -> List[Tuple[Individual, float]]:
        generationScores = []

        # Gets the score for each individual
        for individual in thisGeneration:
            heuristicList = []
            # Converts the genome sequence of bits into a sequence of heuristics
            for i in range(0, individual.getGenomeLen(), 2):
                heuristicList.append(self._heuristics[int(individual.getGenome()[i:i+2], 2)])
            
            problem.solveHH(heuristicList)
            generationScores.append((individual, problem.getObjValue()))
            problem.reset()
        
        # Sorts the individuals based on their score
        return sorted(generationScores, key=lambda x: x[1])
        
    ###########################
    # METHODS RELATED TO THE GENERATION EVOLUTION PROCESS
    
    """
    * METHOD 1.
    * STRONGEST INDIVIDUAL SELECTION
    *
    * This offsping generation method selects the 2 strongest parents
    * to produce 2 children, then, the 2 weakest of both all parents and all
    * children are removed. Finally, all the selected individuals are induced
    * 2 random mutations to their genomes. 
    """
    def _evolve_strongestSelection(self, parentGeneration : List[Tuple[Individual, float]], problem : Problem) -> List[Individual]:
        parent1 = parentGeneration[-1][0]
        parent2 = parentGeneration[-2][0]
        
        # The 2 strongest parents produce 2 children
        children = parent1.recombine(parent2)

        # Evaluates the children
        scoredChildren = self._evaluateGeneration(children, problem)
        
        # Adds the evaluated children to the same group as the parents for the duel
        parentGeneration.extend(scoredChildren)

        # Removes the 2 weakest individuals
        strongestIndividuals = sorted(parentGeneration, key=lambda x: x[1])[2:]
        selectedIndividuals = [individual[0] for individual in strongestIndividuals] 

        # Each remaining individual suffers a random double-mutation
        for individual in selectedIndividuals:
            individual.mutate()
            individual.mutate()
            
        return selectedIndividuals

    """
    * METHOD 2.
    * WEAKEST INDIVIDUAL SELECTION
    *
    * This offsping generation method is straightforward, as it selects the 2 
    * weakest parents to produce 2 children, then, the 2 strongest of both all 
    * parents and all children are removed. Then the weakest recombines with all
    * the others and the weakest n are selected, where n is the population's size.
    """
    def _evolve_weakestSelection(self, parentGeneration : List[Tuple[Individual, float]], problem : Problem) -> List[Individual]:
        parent1 = parentGeneration[0][0]
        parent2 = parentGeneration[1][0]

        # The 2 weakest parents produce 2 children
        children = parent1.recombine(parent2)

        # Evaluates the children
        scoredChildren = self._evaluateGeneration(children, problem)
        
        # Adds the evaluated children to the same group as the parents for the duel
        parentGeneration.extend(scoredChildren)

        # Removes the 2 strongest individuals
        weakIndividuals = sorted(parentGeneration, key=lambda x: x[1])[:-2]
        
        # Weakest recombines with the rest
        for i in range(1, len(weakIndividuals)):
            weakIndividuals.extend(self._evaluateGeneration(weakIndividuals[0][0].recombine(weakIndividuals[i][0]), problem))
        
        weakestIndividuals = sorted(weakIndividuals, key=lambda x: x[1])[:self._populationSize]
        selectedIndividuals = [individual[0] for individual in weakestIndividuals] 
        
        return selectedIndividuals
    
    """
    * METHOD 4. Lion Prides
    * This method is based on lion prides I've seen in some documentaries
    * about the African ecosystem. In these prides, the alpha male has
    * the right of reproduction with all the females. 
    * 
    * So, let us say the current generation has g individuals. This 
    * method takes the most convenient individual so far, and it 
    * recombines it with all the remaining individuals
    * in the generation. This will yield (g-1) * 2 children. The children
    * are aggressively mutated, where each gene in their genome has a
    * 50% probability of being flipped. Only the fittest g individuals 
    * are kept out of the parents and the children. 
    * 
    """
    def _evolve_lion_prides(self, parentGeneration : List[Tuple[Individual, float]], problem : Problem) -> List[Individual]:
        alpha = parentGeneration[-1][0]
        g = len(parentGeneration)
        mothers = parentGeneration[:-1]#random.sample(parentGeneration, g // 2)
        mothers = [mother[0] for mother in mothers]

        children = []
        for mother in mothers:
            c_children = alpha.recombine(mother)
            c_children[0].mutate2()
            c_children[1].mutate2()
            children += c_children

        # Evaluates the children
        scoredChildren = self._evaluateGeneration(children, problem)
        
        # Adds the evaluated children to the same group as the parents for the duel
        parentGeneration.extend(scoredChildren)
        selectedIndividualsScores = sorted(parentGeneration, key=lambda x: x[1])[len(parentGeneration) - g:]
        selectedIndividuals = [individualScore[0] for individualScore in selectedIndividualsScores]
        #print('new generation', [xd[1] for xd in selectedIndividualsScores])

        return selectedIndividuals
        


    # M A I N   E V O L U T I O N A R Y   P R O C E S S
    def solve(self, problem : Problem, target: float, evolutionMethods : List[str] = []) -> None:
        self._initGeneration(problem.getItemCount())
        print('beginning generations')

        for generationNum in range(self._maxGenerations):
            
            # Gets the score of each individual (how well do they solve the problem)
            scoredGeneration = self._evaluateGeneration(self._generation, problem)
            print(self._generation[-1])

            # Evaluates if one of the individuals has equaled or outperformed the oracle
            if round(scoredGeneration[-1][1], 3) >= target:
                print('-------------------------------------------')
                print("Optimal solution has been found!")
                if generationNum != 0:
                    print(f"Generations: {generationNum}")
                    # Prints all individuals of the generation that are optimal solutions
                    for individual in scoredGeneration:
                        heuristicList = []
                        if individual[1] >= target:
                            for i in range(0, individual[0].getGenomeLen(), 2):
                                heuristicList.append(self._heuristics[int(individual[0].getGenome()[i:i+2], 2)])
                            #print("Solution:", *heuristicList, sep=" ")
                            print(f"Score: {individual[1]} target {target}")
                            for ind in self._generation:
                                print(ind)
                            print([xd[1] for xd in self._evaluateGeneration(self._generation, problem)])
                return generationNum

            # Selects the method that will be used to create the new generation
            random.seed(time.time())
            evolutionMethod = random.choice(["strongest", "weakest"]) \
                                if len(evolutionMethods) == 0 else \
                                    random.choice(evolutionMethods)
            selectedIndividuals = List[Individual]
            if evolutionMethod == "strongest":
                selectedIndividuals = self._evolve_strongestSelection(scoredGeneration, problem)
            elif evolutionMethod == "weakest":
                selectedIndividuals = self._evolve_weakestSelection(scoredGeneration, problem)
            elif evolutionMethod == "lion_pride":
                selectedIndividuals = self._evolve_lion_prides(scoredGeneration, problem)

            # Creates the new generation
            self._generation = selectedIndividuals
        print(f"NO Optimal solution could be found in {self._maxGenerations} generations target {target}")
        for ind in self._generation:
            print(ind)
        print([xd[1] for xd in self._evaluateGeneration(self._generation, problem)])
        print("------------------------------------------------------")
        return generationNum

    
