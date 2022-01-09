import unittest
import random
import datetime

from portfolio.functions.find import find

class TestFind(unittest.TestCase):
    def setUp(self):
        self.data_A = [1, 2, 5, 6, 10]

        self.msg_output = 'output of find() -> expected: {target_index}, got {index}'

    def test_type(self):
        pass

    def test_raises(self):
        target = -1
        self.assertRaises(ValueError, find, data=self.data_A, target= target, low=0, high=len(self.data_A) - 1, force=True)

        target = 20
        self.assertRaises(ValueError, find, data=self.data_A, target= target, low=0, high=len(self.data_A) - 1, force=True)

    def test_output_force_set_to_true(self):
        index = self.data_A[find(data=self.data_A, target= 2, low=0, high=len(self.data_A) - 1, force=True)]
        self.assertEqual(index, self.data_A[1], self.msg_output.format(target_index=1, index=index))

    def test_output_force_set_to_false(self):
        index = self.data_A[find(data=self.data_A, target= 3, low=0, high=len(self.data_A) - 1, force=False)]
        self.assertEqual(index, self.data_A[1], self.msg_output.format(target_index= 1, index=index))

        index = self.data_A[find(data=self.data_A, target= 4, low=0, high=len(self.data_A) - 1, force=False)]
        self.assertEqual(index, self.data_A[1], self.msg_output.format(target_index= 1, index=index))

        index = self.data_A[find(data=self.data_A, target= 7, low=0, high=len(self.data_A) - 1, force=False)]
        self.assertEqual(index, self.data_A[3], self.msg_output.format(target_index= 2, index=index))

        index = self.data_A[find(data=self.data_A, target= 8, low=0, high=len(self.data_A) - 1, force=False)]
        self.assertEqual(index, self.data_A[3], self.msg_output.format(target_index= 3, index=index))

        index = self.data_A[find(data=self.data_A, target= 9, low=0, high=len(self.data_A) - 1, force=False)]
        self.assertEqual(index, self.data_A[3], self.msg_output.format(target_index= 3, index=index))

        index = self.data_A[find(data=self.data_A, target= 20, low=0, high=len(self.data_A) - 1, force=False)]
        self.assertEqual(index, self.data_A[4], self.msg_output.format(target_index=4, index=index))

    def test_output_on_random_date_force_set_to_true(self):
        msg_output = '{i} out of {n}: output of find() -> expected: {target_index}, got {index}'

        random_data = random.sample(range(-1000000, 1000000), 10000)
        random_data.sort()
        
        for i in range(0, len(random_data) - 1):
            target_index = random.randint(0, len(random_data) - 1)
            target = random_data[target_index]

            index = find(data=random_data, target= target, low=0, high=len(random_data) - 1, force=True)
            self.assertEqual(index, target_index, msg=msg_output.format(i=i, n=len(random_data)-1, target_index=target_index, index=index))
