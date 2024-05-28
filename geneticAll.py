from phermes import Problem
from phermes import HyperHeuristic
from typing import List, Type, Tuple, Dict
from individual import Individual
from helperFuncs import fromGenToSeq
import random
import time
from bpp import BPP
import pandas as pd
import numpy as np

class GeneticModel(HyperHeuristic):

    def __init__(self, features : List[str], heuristics : List[str], maxGenerations : int, population : int):
        super().__init__(features, heuristics)
        self._generation = List[Individual]
        self._populationSize = population
        self._maxGenerations = maxGenerations
        # Dictionary that keeps the overall evaluation of each specific individual over ALL problem instances
        self._heuristicSpaceExplored : Dict[str, float] = {}
        self._heuristicSpaceExploredAll : Dict[str, float] = {}

    def _initGeneration(self, problemSize : int) -> None:
        random.seed(time.time())
        self._generation = [Individual("0"*problemSize) for _ in range(self._populationSize)]
        for individual in self._generation:
            individual.setRandomGenome(len(self._heuristics), problemSize)
        

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
    def _evolve_strongestSelection(self, problemInstances, testGroup : str, parentGeneration : List[Tuple[Individual, float]]) -> List[Individual]:
        # Creates a sorted copy of the parent generation
        sortedParentGeneration = sorted(parentGeneration, key=lambda x: x[1]).copy()

        parent1 = sortedParentGeneration[-1][0]
        parent2 = sortedParentGeneration[-2][0]
        
        # The 2 strongest parents produce 2 children
        children = parent1.recombine(parent2)

        # Gets rid of the scores in the parent generation
        parentGeneration = [individual[0] for individual in parentGeneration]

        # Adds the evaluated children to the same group as the parents for the duel
        parentGeneration.extend(children)
        
        # Evaluates all the individuals (parents & children)
        scoredIndividuals = self._evaluateOnMultiInstance(problemInstances, testGroup, parentGeneration)
        
        # Removes the 2 weakest individuals
        selectedIndividualsScores = sorted(scoredIndividuals, key=lambda x: x[1])[2:]
        selectedIndividuals = [individual[0] for individual in selectedIndividualsScores]

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
    def _evolve_weakestSelection(self, problemInstances, testGroup : str, parentGeneration : List[Tuple[Individual, float]]) -> List[Individual]:
        # Creates a sorted copy of the parent generation
        sortedParentGeneration = sorted(parentGeneration, key=lambda x: x[1]).copy()

        parent1 = sortedParentGeneration[0][0]
        parent2 = sortedParentGeneration[1][0]

        # The 2 weakest parents produce 2 children
        children = parent1.recombine(parent2)

        # Gets rid of the scores in the parent generation
        parentGeneration = [individual[0] for individual in parentGeneration]

        # Adds the evaluated children to the same group as the parents for the duel
        parentGeneration.extend(children)
        
        # Evaluates all the individuals (parents & children)
        scoredIndividuals = self._evaluateOnMultiInstance(problemInstances, testGroup, parentGeneration)
        
        # Removes the 2 strongest individuals
        weakIndividuals = sorted(scoredIndividuals, key=lambda x: x[1])[:-2]
        
        weakChildren = []
        # Weakest recombines with the rest
        for i in range(1, len(weakIndividuals)):
            weakChildren.extend(weakIndividuals[0][0].recombine(weakIndividuals[i][0]))
        
        # Gets rid of the scores in the parent generation
        weakIndividuals = [individual[0] for individual in weakIndividuals]
        weakIndividuals.extend(weakChildren)
        
        weakIndividualsScore = self._evaluateOnMultiInstance(problemInstances, testGroup, weakIndividuals)

        weakIndividualsScore = sorted(weakIndividualsScore, key=lambda x: x[1])[:self._populationSize]
        selectedIndividuals = [individual[0] for individual in weakIndividualsScore] 
        
        return selectedIndividuals  

    """
    * METHOD 3.
    * RANDOM PARENT SELECTION
    *
    * This offsping generation method selects 2 parents randomly to produce 
    * 2 children, then, removes the 2 weakest individuals, each remaining individual suffers
    * a random triple-mutation
    
    """

    def _evolve_randomSelection(self, problemInstances, testGroup : str, parentGeneration : List[Tuple[Individual, float]]) -> List[Individual]:
        #Selects two random parents
        parent1, parent2 = random.sample([individual[0] for individual in parentGeneration], 2)
        
        # The parents produce 2 children
        children = parent1.recombine(parent2)

        # Gets rid of the scores in the parent generation
        parentGeneration = [individual[0] for individual in parentGeneration]

        # Adds the evaluated children to the same group as the parents for the duel
        parentGeneration.extend(children)
        
        # Evaluates all the individuals (parents & children)
        scoredIndividuals = self._evaluateOnMultiInstance(problemInstances, testGroup, parentGeneration)
        
        selectedIndividualsScores = sorted(scoredIndividuals, key=lambda x: x[1])[:2]
        selectedIndividuals = [individual[0] for individual in selectedIndividualsScores]

         # Each remaining individual suffers a random triple-mutation
        for individual in selectedIndividuals:
            individual.mutate()
            individual.mutate()
            individual.mutate()

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
    def _evolve_lion_prides(self, problemInstances, testGroup : str, parentGeneration : List[Tuple[Individual, float]]) -> List[Individual]:
        # Creates a sorted copy of the parent generation
        sortedParentGeneration = sorted(parentGeneration, key=lambda x: x[1]).copy()

        alpha = sortedParentGeneration[-1][0]
        g = len(sortedParentGeneration)
        mothers = sortedParentGeneration[:-1]#random.sample(sortedParentGeneration, g // 2)
        mothers = [mother[0] for mother in mothers]

        children = []
        for mother in mothers:
            c_children = alpha.recombine(mother)
            c_children[0].mutate2()
            c_children[1].mutate2()
            children += c_children

        # Gets rid of the scores in the parent generation
        parentGeneration = [individual[0] for individual in parentGeneration]

        # Adds the evaluated children to the same group as the parents for the duel
        parentGeneration.extend(children)
        
        # Evaluates all the individuals (parents & children)
        scoredIndividuals = self._evaluateOnMultiInstance(problemInstances, testGroup, parentGeneration)
        
        selectedIndividualsScores = sorted(scoredIndividuals, key=lambda x: x[1])[len(scoredIndividuals) - g:]
        selectedIndividuals = [individual[0] for individual in selectedIndividualsScores]

        return selectedIndividuals
        

    ###########################
    # METHODS RELATED TO THE EVALUATIONS PROCESS
    """
    This method is for evaluating a list of individuals against ONE single problem instance
    """
    def _evaluateOnSingleInstance(self, thisGeneration : List[Individual], problem : Problem) -> List[float]:
        generationScores = []

        # Gets the score for each individual
        for individual in thisGeneration:
            problem.solveHH(fromGenToSeq(individual.getGenome(), self._heuristics))
            generationScores.append(problem.getObjValue())
            problem.reset()

        # Sorts the individuals based on their score
        return generationScores
    
    """
    This method is for evaluating a list of individuals against MULTIPLE problem instances
    """
    def _evaluateOnMultiInstance(self, problemInstances, testGroup : str, individualsToEvaluate : List[Individual]) -> List[Tuple[Individual, float]]:
        # Separates the individuals were solved previously to the ones that are not (missing)
        individualsMissing = [i for i in individualsToEvaluate if self._heuristicSpaceExplored.get(i.getGenome(), None) is None]
        individualsEvaluated = [(i, self._heuristicSpaceExplored[i.getGenome()]) for i in individualsToEvaluate if self._heuristicSpaceExplored.get(i.getGenome(), None) is not None]

        # Creates the space where the scores of each (missing to be evaluated) individual for each problem instance will be stored
        individuals_scoresOnALLProblemInstances = np.zeros((problemInstances.shape[0], len(individualsMissing)))

        # ITERATES ON ALL PROBLEM INSTANCES
        for index, row in problemInstances.iterrows():
            problem = BPP(f"{testGroup}/{row['INSTANCE']}")
            oracleValue = row["ORACLE"]
            instance = row['INSTANCE']

            # Gets the score of each individual (how well do they solve the problem)
            individuals_scoresOnONEProblemInstance = self._evaluateOnSingleInstance(individualsMissing, problem)
            

            # Store the normalized score of each individual for each problem instance
            for i, indScore in enumerate(individuals_scoresOnONEProblemInstance):
                individuals_scoresOnALLProblemInstances[index, i] = indScore / oracleValue
            
        # Initialize an empty list to store the columns
        columns_list = []

        # Iterate over the columns and append each to the list (to get in each elemnt a list with the results of the instances)
        for i in range(individuals_scoresOnALLProblemInstances.shape[1]):
            column = individuals_scoresOnALLProblemInstances[:, i]
            columns_list.append(column)
        
        # Link the individual with all the scores gotten for each instance
        allScoresIndividuals = [(individualsMissing[i], columns_list[i]) for i in range(len(individualsMissing))]
        print(allScoresIndividuals)

        #Store in a dictionary the individual and the list of all the scores of all the instances
        for ind, allScores in allScoresIndividuals:
            self._heuristicSpaceExploredAll[ind.getGenome()] = allScores

        # Get the overall performance of each individual in all the problems
        sumOfScores = np.sum(individuals_scoresOnALLProblemInstances, axis=0)
        avgOfScores = sumOfScores / problemInstances.shape[0]

        # Links the scores to their respective individual
        scoredIndividuals = [(individualsMissing[i], avgOfScores[i]) for i in range(len(individualsMissing))]
        #print(scoredIndividuals)

        # Store the newly explored and evaluated individuals scores to avoid redundancy and keep track of the explored heuristic space
        for ind, score in scoredIndividuals:
            self._heuristicSpaceExplored[ind.getGenome()] = score

        # Adds the already evaluated individuals
        scoredIndividuals.extend(individualsEvaluated)

        return scoredIndividuals


    ###########################
    # M A I N   E V O L U T I O N A R Y   P R O C E S S
    def solveAll(self, testGroup : str, heuristicSpace : int, evolutionMethods : List[str] = []) -> None:

        problemInstances = pd.read_csv(f"BPP-{testGroup}.csv")
        problemSize = 40 if testGroup == "Test II" else 20
        self._initGeneration(problemSize)
        
        # While the minimum heuristic space hasn't been covered, keep mutating
        while len(self._heuristicSpaceExplored) < heuristicSpace:

            # Gets the evaluation of the individuals on this current generation
            thisGeneration_scoredIndividuals = self._evaluateOnMultiInstance(problemInstances, testGroup, self._generation)

            # Selects the method that will be used to create the new generation
            random.seed(time.time())
            evolutionMethod = random.choice(["strongest", "weakest", "lion_pride", "random"]) \
                                if len(evolutionMethods) == 0 else \
                                    random.choice(evolutionMethods)
            # Generate new generation
            if(evolutionMethod == "strongest"):
                self._generation = self._evolve_strongestSelection(problemInstances, testGroup, thisGeneration_scoredIndividuals)
            elif(evolutionMethod == "weakest"):
                self._generation = self._evolve_weakestSelection(problemInstances, testGroup, thisGeneration_scoredIndividuals)
            elif(evolutionMethod == "lion_pride"):
                self._generation = self._evolve_lion_prides(problemInstances, testGroup, thisGeneration_scoredIndividuals)
            elif(evolutionMethod == "random"):
                self._generation = self._evolve_randomSelection(problemInstances, testGroup, thisGeneration_scoredIndividuals)
            
        print(f"HEURISTIC SPACE EXPLORED: ", len(self._heuristicSpaceExplored))
        print("HartaEstoy",len(self._heuristicSpaceExploredAll))
        return self._heuristicSpaceExplored, self._heuristicSpaceExploredAll

        



        