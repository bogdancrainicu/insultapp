import unittest
from insult_generator import Insulter


class TestInsulter(unittest.TestCase):
    def test_insult(self):
        insulter = Insulter(self.fake_choice1)
        actual_insult = insulter.insult()
        self.assertEqual(actual_insult, "Though artless bat-fowling barnacle!")

    def test_named_insult(self):
        insulter = Insulter(self.fake_choice1)
        actual_insult = insulter.named_insult("roberto")
        self.assertEqual(actual_insult, "Roberto, though artless bat-fowling barnacle!")

    def test_named_insult_second_choice(self):
        insulter = Insulter(self.fake_choice2)
        actual_insult = insulter.named_insult("roberto")
        self.assertEqual(actual_insult, "Roberto, though foolish boil-brained bladder!")

    @staticmethod
    def fake_choice1(list_of_insults):
        return list_of_insults[0]

    @staticmethod
    def fake_choice2(list_of_insults):
        return list_of_insults[1]


if __name__ == '__main__':
    unittest.main()
