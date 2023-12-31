import unittest

import tictactoe
from tictactoe import initial_state, X, EMPTY, O

class TestTicTacToe(unittest.TestCase):

    def test_next_turn_player(self):
        result = tictactoe.player([[X,O,X],
                                  [O,X,X],
                                  [O,EMPTY,EMPTY]])
        
        self.assertEqual(result,O)

        result = tictactoe.player([[X,O,X],
                                  [O,X,O],
                                  [EMPTY,EMPTY,EMPTY]])
        self.assertEqual(result,X)

        result = tictactoe.player(initial_state())
        self.assertEqual(result,X)

        result = tictactoe.player([[EMPTY,O,X],
                                    [O,O,X],
                                    [EMPTY,X,X]])

        self.assertEqual(result,EMPTY)


    def test_actions_returns_set_of_all_possible_moves(self):

        result = tictactoe.actions(initial_state())
        expectedResult = set([(x,y) for x in range(3) for y in range(3)])
        self.assertEqual(expectedResult,result)

        result = tictactoe.actions([[X,O,X],
                                    [O,O,X],
                                    [O,X,X]])
        self.assertEqual(result, None)

        result = tictactoe.actions([[X,O,X],
                                    [O,X,EMPTY],
                                    [EMPTY,EMPTY,EMPTY]])
        expectedResult = set([(1,2), (2,0),(2,1),(2,2)])
        self.assertEqual(result,expectedResult)

        result = tictactoe.actions([[EMPTY,O,X],
                                    [O,O,X],
                                    [EMPTY,X,X]])

        self.assertEqual(result,EMPTY)

    def test_winner(self):

        result = tictactoe.winner([[X,X,X],
                                   [O,O,X],
                                   [O,EMPTY,EMPTY]])
        self.assertEqual(result,X)

        result = tictactoe.winner([[O,X,X],
                                   [O,X,X],
                                   [O,EMPTY,EMPTY]])
        self.assertEqual(result,O)

        result = tictactoe.winner([[O,O,X],
                                   [O,X,X],
                                   [X,EMPTY,EMPTY]])
        self.assertEqual(result,X)

        result = tictactoe.winner([[O,O,X],
                                   [X,O,X],
                                   [X,X,O]])
        self.assertEqual(result,O)

        result = tictactoe.winner([[X,O,X],
                                   [X,O,O],
                                   [X,X,O]])
        self.assertEqual(result,X)

        result = tictactoe.winner([[X,O,X],
                                   [X,O,O],
                                   [O,X,X]])
        self.assertEqual(result,None)

        result = tictactoe.winner(initial_state())
        self.assertEqual(result,None)

    def test_terminal(self):

        result = tictactoe.terminal([[X,O,X],
                                   [X,O,O],
                                   [X,X,O]])
        self.assertEqual(result,True)

        result = tictactoe.terminal([[X,O,X],
                                   [X,O,O],
                                   [O,X,X]])
        self.assertEqual(result,True)

        result = tictactoe.terminal(initial_state())
        self.assertEqual(result,False)

        result = tictactoe.terminal([[X,O,X],
                                    [O,X,O],
                                    [O,X,O]])
        self.assertEqual(result,True)

        result = tictactoe.terminal([[X,O,X],
                                    [O,EMPTY,O],
                                    [O,X,O]])
        self.assertEqual(result,False)

        result = tictactoe.terminal([[EMPTY,O,X],
                                        [O,O,X],
                                    [EMPTY,X,X]])

        self.assertEqual(result,True)


    def test_result_return_new_board_with_applied_action(self):

        with self.assertRaises(ValueError):
            tictactoe.result(initial_state(), EMPTY)

        with self.assertRaises(ValueError):
            tictactoe.result(initial_state(), "Hello")

        with self.assertRaises(ValueError):
            tictactoe.result(initial_state(), 5)

        with self.assertRaises(ValueError):
            tictactoe.result([[X, X, X],
                            [O, O, X],
                            [EMPTY, EMPTY, EMPTY]], (1, 2))

        with self.assertRaises(ValueError):
            tictactoe.result([[X, X, O],
                            [O, O, X],
                            [EMPTY, EMPTY, EMPTY]], (1, 2))

        result = tictactoe.result([[X,X,O],
                                   [O,O,X],
                                   [EMPTY,EMPTY,EMPTY]], (2,2))
        self.assertEqual(result,[[X,X,O],
                                 [O,O,X],
                                 [EMPTY,EMPTY,X]])

    def test_utility(self):

        result = tictactoe.utility([[O,O,X],
                                   [X,O,X],
                                   [X,X,O]])
        self.assertEqual(result,-1)

        result = tictactoe.utility([[X,O,X],
                                   [X,O,O],
                                   [X,X,O]])
        self.assertEqual(result,1)

        result = tictactoe.utility([[X,O,X],
                                   [X,O,O],
                                   [O,X,X]])
        self.assertEqual(result,0)
    
    def test_minimax(self):


        result = tictactoe.minimax([[X,O,EMPTY],
                                   [EMPTY,EMPTY,EMPTY],
                                   [EMPTY,EMPTY,EMPTY]])
        self.assertEqual(result,(1,1))
        
        result = tictactoe.minimax([[EMPTY,X,O],
                                    [O,X,X],
                                    [X,EMPTY,O]])
        self.assertEqual(result,(2,1))

        result = tictactoe.minimax([[O,X,O],
                                    [O,X,X],
                                    [X,O,X]])
        self.assertEqual(result,None)
        
        
if __name__ == "__main__":
    unittest.main()