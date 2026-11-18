import unittest
from pathlib import Path
from codonprint import (
    analyse_sequence, clean_sequence, check_sequence, make_codons,
    count_codons, find_gc_content, compare_two_sequences, read_fasta_file
)

class TestCodonPrint(unittest.TestCase):
    def test_clean_sequence(self):
        self.assertEqual(clean_sequence(" atg\n gcc "), "ATGGCC")

    def test_valid_and_invalid_sequence(self):
        self.assertTrue(check_sequence("ATGC"))
        self.assertFalse(check_sequence("ATGX"))
        self.assertFalse(check_sequence(""))

    def test_codon_splitting(self):
        self.assertEqual(make_codons("ATGGCCG"), ["ATG", "GCC"])

    def test_codon_counting(self):
        self.assertEqual(count_codons(["ATG", "GCC", "ATG"]), {"ATG": 2, "GCC": 1})

    def test_gc_content(self):
        self.assertAlmostEqual(find_gc_content("GGCCAT"), 66.6666666, places=5)

    def test_analysis_and_knn(self):
        result = analyse_sequence("ATGGCCGCTGCAAAAGCTGCC")
        self.assertIsNotNone(result)
        self.assertIn("ml_prediction", result)
        self.assertIn("ml_votes", result)
        self.assertEqual(result["leftover"], 0)

    def test_sequence_comparison(self):
        result = compare_two_sequences("ATGGCCGCTGCA", "ATGGCTGCTGCA")
        self.assertIsNotNone(result)
        self.assertIn("ATG", result["shared"])

    def test_fasta_reader(self):
        file_path = Path(__file__).parent / "sample_sequences.fasta"
        records = read_fasta_file(str(file_path))
        self.assertEqual(len(records), 2)

if __name__ == "__main__":
    unittest.main()
