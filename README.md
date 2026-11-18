# CODONPRINT
### Codon Usage-Based Organism Classifier

**A Python project using Biopython and Basic Machine Learning**

**Developed by:** Jakkam Mithlesh and Ch. Nirav  
**Group 18**

CODONPRINT analyses DNA sequences using codon usage patterns. It calculates base counts, GC content, codon frequencies and codon usage. It also demonstrates a basic **K-Nearest Neighbours (KNN)** classifier using six codon-usage values as features. Biopython is used to read FASTA sequence files. A Streamlit interface provides the web application.

## Features
- Enter and validate a DNA sequence.
- Calculate base counts and GC content.
- Split DNA into complete codons and calculate codon usage.
- Display the most frequent codons.
- Compare two DNA sequences.
- Upload and read FASTA files with Biopython.
- Demonstrate KNN classification (K = 3) using codon-usage features.

## Important note about the ML data
`training_data_demo.csv` contains small illustrative training examples created to demonstrate how KNN works. These are not verified biological reference records and do not establish real organism-classification accuracy. The prediction is an educational demonstration, not a confirmed identification. A reliable scientific classifier would require a larger, documented dataset and testing on independent sequences.

## Run locally
Install the packages:
```bash
pip install -r requirements.txt
```
Run the website:
```bash
streamlit run app.py
```
Run the command-line version:
```bash
python codonprint.py
```

Keep `app.py`, `codonprint.py`, `requirements.txt`, and `training_data_demo.csv` in the repository root.
