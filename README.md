# CS4012_FinalProject
Final Project code for exploring the relationship between heuristics using Genetic Algorithms to solve the 1D Bin Packing Problem


Our first approach was to evolve the sequence of heuristics to fit each problem instance individually. However, our final approach was to evolve the sequence of heuristics so that it fits the entire dataset of instances being used.

This way, the file ```hhprojectAll.py``` contains our final approach. In this file, there is a function called ```solveHH```, which has the variable ```heuristicSpaceToExplore = 100```. This variable indicates how many sequences will be explored, and that drives the execution time for the algorithm.

Then, to run the project from beginning to end, the steps are the following

1. Decide the amount of search space to cover.
    ```
    In file hhprojectAll.py line 69
    heuristicSpaceToExplore = 100
    ```

2. Define the evolutionary methods to be used:
   ```
   In hhproject.py line 74
    prueba = hyperHeuristic.solveAll(testGroup, heuristicSpaceToExplore, ["strongest"])
   ```
   Define the evolutionary methods to be used, which can be any subset of ["strongest", "weakest", "lion_pride", "random"]. These methods are explained in detail in the paper Section 3.4.
3. Establish the population size for the genetic algorithm.
   ```
   In hhprojectAll.py line 115
   gen = GeneticModel(features, heuristics, 100, 5)
   ```
   Replace the ```5``` with the desired population size for each generation.

4. Define the dataset to be used:
    ```
    In file hhprojectAll.py line 116
    dict1, allScores_allSequences, avgBins = solveHH("Test II", gen)
    ```
    Specify which dataset to use, can be one of ['Test II', 'Test I', 'Training']

5. Execute the program
    ```
    python hhprojectAll.py
    ```

6. Generate clustering information:
    ```
    python clustering.py
    ```

7. Generate visualizations for the best sequences, worst sequences, etc., execute the following:
    ```
    python individuals_comp.py
    ```
    Open the folder of ```./individuals_comps``` to see the heatmaps.

8. Perform ANOVA and Tukey tests. If the problem instances have 40 items (Test II), then execute:
    ```
    python proportions.py
    ```
    Otherwise, if the problem instances have 20 items (Test I, Training), then execute:
    ```
    python proportions20.py
    ```
    The results of these tests are stored in the ```proportions_heuristics``` or ```proportions20``` folders.


9. Statistical analysis of permutations of pairs of heuristics:
    ```
    python pairs_heuristics_analysis.py
    ```

    The results of this analysis are stored in the folder ```proportions_pairs```.



