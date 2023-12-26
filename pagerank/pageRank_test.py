import unittest
import pagerank 

class TestPageRank(unittest.TestCase):

    def test_transitionModel(self):

        expectedResult = {"1.html":0.05, "2.html":0.475, "3.html":0.475}
        corpusTest = {"1.html": {"2.html", "3.html"}, "2.html": {"3.html"}, "3.html": {"2.html"}}
        result = pagerank.transition_model(corpusTest,"1.html",0.85)
        self.assertEqual(result,expectedResult)



if __name__ == "__main__":
    unittest.main()