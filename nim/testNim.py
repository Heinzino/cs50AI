import unittest

import nim

class testNimAI(unittest.TestCase):


    def test_get_q_value(self):

        q = {((0,0,0,2), (3,2)) :-1}
        model = nim.NimAI()
        model.q = q
        self.assertEqual(
            model.get_q_value([0,0,0,2],(3,2)), -1
        )

        self.assertEqual(
            model.get_q_value([1,2,3,4], (3,2)), 0
        )

    def test_chooseactions(self):
        max_action_Qval_pair = ( (0,0) , -100)
        self.assertEqual(-100, max_action_Qval_pair[1])
        
if __name__ == "__main__":
    unittest.main()