# Understanding Heuristics: A Bioinformatics-Inspired Analysis of Heuristic Interactions for Efficient Bin Packing Problem Solving
## Archives Description

Our first approach was to generate sequences of heuristics tailored for each problem instance individually. The main files for that purpose are:

:warning: _These two first files were not used for the final approach, but they served to conduct the initial experiments_
* ```hhproject.py``` which invokes the Genetic Algorithm (GA) to generate sequences for each instance of the problem.
* ```genetic.py``` which holds the GA Hyper-Heuristic (HH) to generate the sequences (works by defining a certain number of generations)

However, we changed to approach to study more general patterns across all instances, as such, the generated sequences were now tested for all instances. This required certain modifications that differed from the original files provided, thus, we created a modified version to make these experiments for ALL problem instances, leaving us with the files:
* ```hhprojectAll.py``` which invokes the GA one single time and passes all problem instance of a certain problem set (either Test I or Test II) 
* ```geneticAll.py``` contains a modified version of the GA in which the fitness function is tested with all instances of the problems.
<br />

The rest of the files serve the following purposes:
* ```individual.py``` Defines the Individual class, its genome and mutations, which is essentially, the encoded sequence of heuristics as a binary string.
* ```bpp.py``` Bin Packing Problem (BPP) definition. We modified it to add a reset function, to reset the instance stats; also added a method to return the bin usage data.
* ```phermes.py``` Parent classes for HH and Problem (these were not modified).
* ```clustering.py``` Defines the clusters of sequences and instances, and generates the dendrograms to depict them.
* ```individuals_comp.py``` Creates the heatmaps comparing groups of 30 sequences by coloring the genes (low-level heuristics).
* ```helperFuncs.py``` Contains useful functions used accross many files (e.g. convert the genome from a bit-string into a heuristic list).
* ```pairs_heuristics_analysis.py``` Performs the analysis and displays the plots (histograms, boxplots, tukeys) for pairwise comparison of heuristics.
* ```proportions.py``` Analysis of proportions of each heuristic within the sequence, specially the last half while plotting the corresponding tukey and boxplots.
* ```proportions20.py``` The same as ```proportions.py```, but tailored for sequences of length 20 (20 items to pack).

<br />

## Code Execution Process


Then, to run the project from beginning to end, the steps are the following.

1. First, set the hyper-parameters for the GA model:
   * Decide the amount of heuristic space to explore. This variable indicates how many sequences will be generated, and that drives the execution time for the algorithm.
    ```
    In file hhprojectAll.py line 69
    heuristicSpaceToExplore = 100
    ```
    * Define the evolutionary methods to be used, which can be any subset of ["strongest", "weakest", "lion_pride", "random"]. These methods are explained in detail in the paper Section 3.4:
   ```
   In hhproject.py line 74
    prueba = hyperHeuristic.solveAll(testGroup, heuristicSpaceToExplore, ["strongest"])
   ```
   * Establish the population size, which is the number of individuals on each generation (Replace the ```5``` with the desired population size for each generation).
   ```
   In hhprojectAll.py line 115
   gen = GeneticModel(features, heuristics, 100, 5)
   ```
   
   * Define the dataset to be used, which can be one of ['Test II', 'Test I', 'Training'] (this will determine the length of the genome):
    ```
    In file hhprojectAll.py line 116
    dict1, allScores_allSequences, avgBins = solveHH("Test II", gen)
    ```

2. Execute the program (this is the main one):
    ```
    python hhprojectAll.py
    ```

3. Generate clustering information:
    ```
    python clustering.py
    ```

4. Generate visualizations for the best sequences, worst sequences, etc., execute the following:
    ```
    python individuals_comp.py
    ```
    Open the folder of ```./individuals_comps``` to see the heatmaps.

5. Perform ANOVA and Tukey tests. If the problem instances have 40 items (Test II), then execute:
    ```
    python proportions.py
    ```
    Otherwise, if the problem instances have 20 items (Test I, Training), then execute:
    ```
    python proportions20.py
    ```
    The results of these tests are stored in the ```proportions_heuristics``` or ```proportions20``` folders.


6. Statistical analysis of permutations of pairs of heuristics:
    ```
    python pairs_heuristics_analysis.py
    ```
    The results of this analysis are stored in the folder ```proportions_pairs```.



