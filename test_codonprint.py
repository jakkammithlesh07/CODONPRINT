import unittest
from codonprint import clean_sequence, validate_dna, analyse_sequence, split_codons


class TestCodonPrint(unittest.TestCase):
    def test_clean_sequence(self):
        self.assertEqual(clean_sequence("atg gcc\n"), "ATGGCC")

    def test_valid_dna(self):
        self.assertTrue(validate_dna("ATGCCG"))
        self.assertFalse(validate_dna("ATGXCC"))

    def test_split_codons(self):
        self.assertEqual(split_codons("ATGGCCAA"), ["ATG", "GCC"])

    def test_gc_content(self):
        result = analyse_sequence("GGCC")
        self.assertEqual(result["gc_content"], 100.0)


if __name__ == "__main__":
    unittest.main()
