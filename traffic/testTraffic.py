import unittest
import traffic

class testTraffic(unittest.TestCase):

    def test_loadData(self):
        data = traffic.load_data(data_dir="gtsrb-small")
        num_files = [540 , 150 ,150]
        self.assertEqual(
            len(data[0]),sum(num_files)
        )
        self.assertEqual(
            data[1].count(0), num_files[0]
        )

if __name__ == "__main__":
    unittest.main()