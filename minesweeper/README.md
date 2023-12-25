PROJECT 1:

AI that plays Minesweeper.

Uses a logical sentence class that works like this
{A,B,C,D} = 1

A,B,C,D.. are the set of all cells and the number is the count of mines among those cells

The three main inferences used are:
1) If the count is 0 all cells in the set must be safe
2) If the the number of cells in the set is equal to the count of bombs. All the cells must be bombs
3) If s1 is a subset of s2 a new sentence can be inferred:
    set2 - set1 = count2 - count 1

Usage:
Requires Python(3) and Python package installer pip(3) to run:

Install requirements: $pip3 install -r requirements.txt

Run Game: $python3 runner.py