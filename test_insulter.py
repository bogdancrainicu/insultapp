from unittest import TestCase
from insult_generator import Insulter


def mock_choice(sequence):
    return sequence[0]


class TestInsulter(TestCase):

    def test__generate_insult(self):
        insulter = Insulter(mock_choice)
        insult = insulter._generate_insult()

        self.assertEqual(insult, "artless bat-fowling barnacle")
