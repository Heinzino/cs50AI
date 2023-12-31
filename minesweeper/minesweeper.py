import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self) -> set:
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        num_cells = len(self.cells)
        if(num_cells == self.count and num_cells > 0):
            return self.cells
        else:
            return set()

    def known_safes(self) -> set:
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if(self.count == 0 and len(self.cells) > 0):
            return self.cells
        else:
            return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            if self.count > 0:
                self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge:list[Sentence] = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def make_new_sentence_with_cell(self,cell:tuple,count:int) -> Sentence:
        valid_neighbours = set()
        initialX, initialY = cell

        # Loop over all cells within one row and column
        for i in range(initialX - 1, initialX + 2):
            for j in range(initialY - 1, initialY  + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                elif (i,j) in self.mines:
                    count-=1
                    continue
                elif (i,j) in self.safes:
                    continue
                else:
                    inBounds:bool = 0 <=i< self.height and 0 <= j < self.width
                    if inBounds:
                        valid_neighbours.add((i,j))
        
        newSentence = Sentence(cells=valid_neighbours,count=count)
        return newSentence

    def removeEmptyKnowledge(self):
        emptyKnowledge = Sentence(cells=set(),count=0)
        self.knowledge[:] = [sentence for sentence in self.knowledge if sentence != emptyKnowledge]

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        #1
        self.moves_made.add(cell)
        #2
        self.mark_safe(cell)
        #3
        newSentence:Sentence = self.make_new_sentence_with_cell(cell,count)
        self.knowledge.append(newSentence)

        new_inference_can_be_made = True
        while(new_inference_can_be_made):
            new_inference_can_be_made = False
                
            mines_to_mark = set() #remove after loop to not cause errors while looping through set
            safes_to_mark = set()            

            #4
            for sentence in self.knowledge:
                mines_to_mark = mines_to_mark.union((sentence.known_mines()))
                safes_to_mark = safes_to_mark.union((sentence.known_safes()))

            if mines_to_mark: #If empty skip
                for mine_to_mark in mines_to_mark:
                    self.mark_mine(mine_to_mark)
                    new_inference_can_be_made = True
            
            if safes_to_mark:
                for safes in safes_to_mark:
                    self.mark_safe(safes)
                    new_inference_can_be_made = True
            
            self.removeEmptyKnowledge() #Before subset inference is made so that empty set is a subset doesnt' cause infinite loop

            #5
            for sentence in self.knowledge:
                for anotherSentence in self.knowledge:
                    if sentence != anotherSentence and sentence.cells.issubset(anotherSentence.cells):
                        sentenceToInfer = Sentence(cells=anotherSentence.cells.difference(sentence.cells),
                                                   count=anotherSentence.count - sentence.count)
                        if sentenceToInfer not in self.knowledge:
                            self.knowledge.append(sentenceToInfer)
                            new_inference_can_be_made=True

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe_cell in self.safes:
            if safe_cell not in self.moves_made:
                return safe_cell
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        randI = random.randrange(self.height)
        randJ = random.randrange(self.width)
        randomMove = (randI,randJ)
        random_moves_tried = set()
        num_valid_random_moves = (self.width*self.height) - len(self.mines) - len(self.safes)

        if(num_valid_random_moves <= 0):
            return None
        else:
            while(randomMove in random_moves_tried or randomMove in self.mines or randomMove in self.moves_made):
                random_moves_tried.add(randomMove)
                randI = random.randrange(self.height)
                randJ = random.randrange(self.width)
                randomMove = (randI,randJ)
            
            return randomMove 

