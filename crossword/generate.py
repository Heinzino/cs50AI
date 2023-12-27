import sys
from queue import Queue

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword:Crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword:Crossword = crossword
        self.domains  = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self) -> None:
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for variable, setOfWord in self.domains.items():

            wordsToRemove = set()  #Delete after loop so set size doesn't change during iteration
            for value in setOfWord:
                if len(value) != variable.length:
                    wordsToRemove.add(value)
            
            self.domains[variable].difference_update(wordsToRemove)


    def revise(self, x:Variable, y:Variable):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        revision = False

        xValsToRemove = set()
        for xVal in self.domains[x]:

            if self.no_y_in_Ydomain_satisfies_constraint(xVal,y):
                xValsToRemove.add(xVal)
                revision = True

        self.domains[x].difference_update(xValsToRemove)
        return revision

    def no_y_in_Ydomain_satisfies_constraint(self,x:str,y:Variable) -> bool:
        updated_y_domain = self.domains[y].difference(set(x))
        if len(updated_y_domain == 0):
            return True
        else:
            return False

    def ac3(self, arcs:list=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        def create_Queue_with_all_arcs() -> Queue:
            return Queue([(v1,v2) for v1,v2 in self.crossword.overlaps.keys() if self.crossword.overlaps[v1,v2] is not None])

        if arcs == None:
            initial_queue = create_Queue_with_all_arcs() 
        else:
            initial_queue = Queue(arcs)

        while not initial_queue.empty():
            (x,y) = initial_queue.get()
            if self.revise(x,y):
                if len(self.domains[x] == 0): #No possible values for X to solve csp
                    return False

                neighbours = self.crossword.neighbors(x).difference(y)
                for neighbour in neighbours:
                    initial_queue.put(tuple((neighbour,x)))
        
        return True

    def assignment_complete(self, assignment:dict) -> bool:
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        return self.crossword.variables == set(assignment.keys())

    def consistent(self, assignment:dict) -> bool:
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        def no_conflicts_between_neighbouring_variables() -> bool:
            for variable in assignment.keys():
                for neighbour in self.crossword.neighbors(variable):
                    if neighbour in set(assignment.keys()):
                        overlappingCell:tuple = self.crossword.overlaps[variable,neighbour]

                        if overlappingCell:
                            overlapping_letter_is_different = (assignment[variable][overlappingCell[0]] != assignment[neighbour][overlappingCell[1]] )
                            if overlapping_letter_is_different:
                                return False
            return True

        all_values_are_distinct = len(set(assignment.values())) == len(assignment.values())

        if not all_values_are_distinct:
            return False

        for variable, value in assignment.items():
            if variable.length != len(value):
                return False
        
        return no_conflicts_between_neighbouring_variables()

    def order_domain_values(self, var:Variable, assignment:dict) -> list:
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        word_to_num_eliminations = dict()
         
        for word in self.domains[var]:
            num_eliminations = 0
            for neighbour in self.crossword.neighbors(var):
                if word in self.domains[neighbour]:
                    num_eliminations += 1

            word_to_num_eliminations[word] = num_eliminations

        return sorted(word_to_num_eliminations.keys(), key= lambda x:word_to_num_eliminations[x]) 

    def select_unassigned_variable(self, assignment:dict) -> Variable:
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        variables_not_assigned = self.crossword.variables.difference(set(assignment.keys()))

        var_to_remaining_values_in_domain = dict()
        for var in variables_not_assigned:
            var_to_remaining_values_in_domain[var] = len(self.domains[var])

        fewest_remaining_value = min(list(var_to_remaining_values_in_domain.values()))
        vars_with_fewest_remaining_values = [var for var,value in var_to_remaining_values_in_domain.items() if value == fewest_remaining_value]

        if len(vars_with_fewest_remaining_values) == 1:
            return vars_with_fewest_remaining_values[0]
        else:
            var_to_degree = dict()
            for var in vars_with_fewest_remaining_values:
                var_to_degree[var] = len(self.crossword.neighbors(var))
            
            largest_degree = max(list(var_to_degree.values()))
            vars_with_fewest_degree = [var for var,value in var_to_degree.items() if value == largest_degree]
            return vars_with_fewest_degree[-1]



    def backtrack(self, assignment:dict):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var,assignment):
            assignment[var] = value
            if self.consistent(assignment):
                result = self.backtrack(assignment)
                if result is not None:
                    return result

            assignment.pop(var)

        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
