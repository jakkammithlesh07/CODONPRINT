# CODONPRINT — Group 18

**Project:** Codon Usage-Based Organism Classifier  
**Team:** Jakkam Mithlesh (SE25UBIT036) and Ch. Nirav (SE25UBIT031)

## What it does
- Cleans and validates a DNA sequence (A, T, G and C).
- Counts bases and calculates GC content.
- Splits the sequence into complete triplet codons and calculates codon usage.
- Displays a simple codon fingerprint.
- Compares codon usage with small demonstration reference patterns.
- Compares two DNA sequences and reads FASTA files.
- Includes a basic K-Nearest Neighbours (KNN) demonstration using a CSV file.
- Provides a Streamlit web interface.

## Run locally
Install Python, open a terminal in this folder, then run:

```bash
pip install -r requirements.txt
python codonprint.py
```

To launch the web app:

```bash
streamlit run app.py
```

Keep `codonprint.py`, `app.py`, and `training_data_demo.csv` together in the same folder. `sample_sequences.fasta` contains two example records for testing.

## GitHub and deployment
Upload the project files to a GitHub repository. To deploy, use Streamlit Community Cloud, select this repository and its `main` branch, and set the app file path to `app.py`. Share the hosted URL only after deployment succeeds and the app has been tested.

## Important scientific limitation
The reference values and `training_data_demo.csv` are small illustrative teaching examples, not a verified biological dataset. The KNN section demonstrates the algorithm; it does not establish scientifically reliable organism identification or validated accuracy. Do not present its output as a confirmed organism identity. A reliable classifier would require documented biological training data from multiple independent sequences and evaluation on separate test data.

## Course concepts used
The core analysis uses strings, variables, indexing and slicing, lists, dictionaries, conditionals, loops, functions and file handling. FASTA parsing uses Biopython SeqIO when available, with a simple Python fallback. KNN, Streamlit, GitHub and deployment are additional self-learning components.
