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




if __name__ == "__main__":
    unittest.main()