# Sudoku-Solver

## Use backtrack and constrain strategy to solve this problem

constrain method is simple.  
It screens for the only one possible number cells and remove all this number from all the related cells.  

## with purely numpy 9x9x9 ndarray solution

commonly, the 9x9 sudoku use 1-9 string to represent the possible numbers in each cells.  
I choose a 9 length np.array to represent all the possible numbers from index 0 to 8.  
For example:  
[1 1 1 1 1 1 1 1 1] means all 1-9 number are possible.  
[1 0 0 0 0 0 0 0 0] means only number 1 is possiblel.  
[0 1 0 1 0 1 0 1 0] means 2,4,6,8 are possible.
