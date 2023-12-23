import unittest

from degrees import shortest_path, load_data, names

class TestShortestPath(unittest.TestCase):

    def setUp(self):
        load_data("small")

    def test_source_connected_to_target(self):
        result = shortest_path("193", "158")
        expected_path = [
            ('104257','102'),
            ('112384','158')
        ]
        self.assertEqual(result, expected_path)

    def test_no_connection_returns_None(self):
        result = shortest_path("914612", "102")
        self.assertIsNone(result)

    def test_source_and_target_are_the_same(self):
        result = shortest_path("193", "193")
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()