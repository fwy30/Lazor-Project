# Lazor Project
by Fan Wu (fwu30@jhu.edu), Heon Joon Lee (hlee260@jhmi.edu), Vincent Clark (vclark19@jhu.edu)
EN 540.635 Software Carpentry

The goal of this project is to use python automatically solve different levels of the Lazor game played on iOS or Android, and generate a text file with the solution.
The goal of the game is to put the block in the grid to reflect and refract the lazor beam to change the path of lazor, and finally make the lazor go through all the target points, if this is achieved, the solution is considered as successful. 

## Instructions
1. Download the 'lazor_project.py' file and make sure all bff files are in the same folder.
2. Enter the name of the .bff file that you want to solve into the code.
3. Run the code, and a text file (solution.txt) of the solution with positions of the blocks will be generated.

## Process flow
A bff file is inputted and broken down to into different blocks represented by A, B, C, X, O.

The code will process the grid, type and number of blocks available, initial lazor position and direction, and list of target points.

Information from the bff file is also used to generate a lazor class object which may calculate changes in lazor position and direction, check available positions, check and calculate interaction with A/B/C blocks, and edit the path of the lazor and movement of blocks.

Finally, the code creates and writes in a text file (solution.txt) with a visual representation for where blocks should be for the solution.

## Sample code
Output for numbered_6.bff:
'''
('The solution grid is', [[0, 0, 0, 0, 0, 0, 0], [0, 4, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 2, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0], [0, 4, 0, 1, 0, 3, 0], [0, 0, 0, 0, 0, 0, 0], [0, 3, 0, 2, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0], [0, 4, 0, 1, 0, 1, 0], [0, 0, 0, 0, 0, 0, 0]])
[Finished in 0.2s]
'''

## Note for sample
Grid will start at top left being 0, 0
Step size is by half blocks
Thus, this leads to even numbers indicating
the rows/columns between blocks, and odd numbers
intersecting blocks.

## Sample solution file
Output for solution.txt (for numbered_6.bff):
 B  o  o  
       
 A  x  x  
       
 B  o  A  
       
 A  x  o  
       
 B  o  o  

## Notes for generated solutions:

A - Reflect block

B - Opaque block

C - Refract block

X - No blocks allowed

O - Available space for block

## test time (may change a little bit depends on computer):
mad_1: 0.2s
mad_4: 0.6s
mad_7: 6.2s
tiny_5: 0.2s
yarn_5: 6.2s
dark_1: 0.1s
numbered_6: 0.2s
(note: all the test file has and only has one solution)
