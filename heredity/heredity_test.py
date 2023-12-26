import unittest

import heredity


class heredityTest(unittest.TestCase):
    def test_jp(self):
        people = {
            "Harry": {
                "name": "Harry",
                "mother": "Lily",
                "father": "James",
                "trait": None,
            },
            "James": {"name": "James", "mother": None, "father": None, "trait": True},
            "Lily": {"name": "Lily", "mother": None, "father": None, "trait": False},
        }

        result = heredity.joint_probability(people,{"Harry"},{"James"},{"James"})
        self.assertAlmostEqual(result, 0.0026643247488)



if __name__ == "__main__":
    unittest.main()