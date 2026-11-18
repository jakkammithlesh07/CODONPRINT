# CODONPRINT
# Codon Usage-Based Organism Classifier
# Group 18
# Jakkam Mithlesh - SE25UBIT036
# Ch. Nirav - SE25UBIT031
#
# This program continues the work from Updates 2 and 3.
# It uses beginner-level Python: strings, lists, dictionaries,
# loops, if conditions, functions and file handling.

# These are the small demonstration values used in Update 3.
# They are NOT a validated scientific database.
REFERENCE = {
    "E_coli_demo": {"GCT": 0.18, "GCC": 0.26, "GCA": 0.23,
                    "GCG": 0.33, "AAA": 0.34, "AAG": 0.66},
    "Human_demo": {"GCT": 0.27, "GCC": 0.40, "GCA": 0.23,
                   "GCG": 0.10, "AAA": 0.43, "AAG": 0.57},
    "Yeast_demo": {"GCT": 0.38, "GCC": 0.22, "GCA": 0.29,
                   "GCG": 0.11, "AAA": 0.42, "AAG": 0.58}
}


# Step 1: Clean the sequence
def clean_sequence(sequence):
    sequence = sequence.upper()
    sequence = sequence.replace(" ", "")
    sequence = sequence.replace("\n", "")
    sequence = sequence.replace("\r", "")
    return sequence


# Step 2: Check that the sequence contains only DNA bases
def check_sequence(sequence):
    if len(sequence) == 0:
        return False

    for base in sequence:
        if base not in "ATGC":
            return False

    return True


# Step 3: Count A, T, G and C
def count_bases(sequence):
    counts = {"A": 0, "T": 0, "G": 0, "C": 0}

    for base in sequence:
        counts[base] = counts[base] + 1

    return counts


# Step 4: Calculate GC percentage
def find_gc_content(sequence):
    if len(sequence) == 0:
        return 0

    gc_count = sequence.count("G") + sequence.count("C")
    gc_percentage = (gc_count / len(sequence)) * 100
    return gc_percentage


# Step 5: Divide the DNA sequence into groups of three
def make_codons(sequence):
    codons = []

    for i in range(0, len(sequence) - 2, 3):
        codon = sequence[i:i + 3]
        codons.append(codon)

    return codons


# Step 6: Count how many times each codon appears
def count_codons(codons):
    counts = {}

    for codon in codons:
        if codon in counts:
            counts[codon] = counts[codon] + 1
        else:
            counts[codon] = 1

    return counts


# Step 7: Calculate the usage of each codon
def find_usage(counts, total_codons):
    usage = {}

    if total_codons == 0:
        return usage

    for codon in counts:
        usage[codon] = counts[codon] / total_codons

    return usage


# Step 8: Show the three most frequently used codons
def make_fingerprint(usage):
    ranked_codons = sorted(usage, key=usage.get, reverse=True)
    fingerprint = []

    for codon in ranked_codons[:3]:
        percent = round(usage[codon] * 100, 1)
        fingerprint.append(codon + " = " + str(percent) + "%")

    if len(fingerprint) == 0:
        return "No complete codons found"

    return ", ".join(fingerprint)


# Step 9: Compare the sequence with the demonstration reference patterns
def compare_with_references(usage):
    scores = {}

    for organism in REFERENCE:
        total_difference = 0
        number_compared = 0

        for codon in usage:
            if codon in REFERENCE[organism]:
                difference = abs(usage[codon] - REFERENCE[organism][codon])
                total_difference = total_difference + difference
                number_compared = number_compared + 1

        if number_compared > 0:
            scores[organism] = total_difference / number_compared
        else:
            scores[organism] = None

    return scores


# Step 10: Find the reference with the smallest difference
def find_closest_reference(scores):
    best_name = "No matching reference codons"
    best_score = None

    for organism in scores:
        score = scores[organism]

        if score is not None:
            if best_score is None or score < best_score:
                best_score = score
                best_name = organism

    return best_name




# Basic machine-learning section: K-Nearest Neighbours (KNN)
# The CSV contains teaching/demo rows only. Replace them with verified
# codon-usage data before making scientific organism-identification claims.
FEATURE_CODONS = ["GCT", "GCC", "GCA", "GCG", "AAA", "AAG"]


def load_training_data(filename="training_data_demo.csv"):
    import csv

    samples = []
    from pathlib import Path
    filename = Path(__file__).resolve().parent / filename
    file = open(filename, "r", newline="")
    reader = csv.DictReader(file)

    for row in reader:
        features = []
        for codon in FEATURE_CODONS:
            features.append(float(row[codon]))

        samples.append((features, row["organism"]))

    file.close()
    return samples


def make_feature_list(usage):
    features = []

    for codon in FEATURE_CODONS:
        if codon in usage:
            features.append(usage[codon])
        else:
            features.append(0.0)

    return features


def calculate_distance(first, second):
    # Euclidean distance, calculated using a simple loop.
    total = 0

    for i in range(len(first)):
        difference = first[i] - second[i]
        total = total + difference * difference

    return total ** 0.5


def predict_with_knn(features, training_samples, k=3):
    distances = []

    for sample_features, organism in training_samples:
        distance = calculate_distance(features, sample_features)
        distances.append((distance, organism))

    distances.sort()

    votes = {}
    neighbours = distances[:k]

    for distance, organism in neighbours:
        if organism in votes:
            votes[organism] = votes[organism] + 1
        else:
            votes[organism] = 1

    predicted = max(votes, key=votes.get)
    return predicted, neighbours, votes


def classify_with_knn(usage, filename="training_data_demo.csv"):
    training_samples = load_training_data(filename)
    features = make_feature_list(usage)
    predicted, neighbours, votes = predict_with_knn(features, training_samples)
    return predicted, neighbours, votes


# Main analysis function: joins all the steps above
def analyse_sequence(sequence):
    sequence = clean_sequence(sequence)

    if check_sequence(sequence) == False:
        return None

    bases = count_bases(sequence)
    gc = find_gc_content(sequence)
    codons = make_codons(sequence)
    counts = count_codons(codons)
    usage = find_usage(counts, len(codons))
    fingerprint = make_fingerprint(usage)
    scores = compare_with_references(usage)
    closest = find_closest_reference(scores)

    ml_prediction, ml_neighbours, ml_votes = classify_with_knn(usage)

    result = {
        "sequence": sequence,
        "length": len(sequence),
        "bases": bases,
        "gc": gc,
        "codons": codons,
        "leftover": len(sequence) % 3,
        "counts": counts,
        "usage": usage,
        "fingerprint": fingerprint,
        "scores": scores,
        "closest": closest,
        "ml_prediction": ml_prediction,
        "ml_neighbours": ml_neighbours,
        "ml_votes": ml_votes
    }

    return result


# Compare the codon usage of two DNA sequences
def compare_two_sequences(first, second):
    first_result = analyse_sequence(first)
    second_result = analyse_sequence(second)

    if first_result is None or second_result is None:
        return None

    shared_codons = []

    for codon in first_result["usage"]:
        if codon in second_result["usage"]:
            shared_codons.append(codon)

    if len(shared_codons) == 0:
        return {"shared": [], "difference": None}

    total_difference = 0

    for codon in shared_codons:
        difference = abs(
            first_result["usage"][codon] - second_result["usage"][codon]
        )
        total_difference = total_difference + difference

    average_difference = total_difference / len(shared_codons)

    return {
        "shared": shared_codons,
        "difference": average_difference
    }


# Read FASTA using Biopython if installed; otherwise use basic Python.
def read_fasta_file(filename):
    try:
        from Bio import SeqIO

        records = []
        for record in SeqIO.parse(filename, "fasta"):
            records.append((record.id, str(record.seq)))
        return records

    except ImportError:
        records = []
        current_name = ""
        current_sequence = ""

        file = open(filename, "r")
        for line in file:
            line = line.strip()

            if line.startswith(">"):
                if current_name != "":
                    records.append((current_name, current_sequence))

                current_name = line[1:]
                current_sequence = ""
            else:
                current_sequence = current_sequence + line

        file.close()

        if current_name != "":
            records.append((current_name, current_sequence))

        return records


# Display the result in the terminal
def show_result(result):
    print("\nDNA sequence is valid")
    print("Sequence length:", result["length"])
    print("Base counts:", result["bases"])
    print("GC content:", round(result["gc"], 2), "%")
    print("Codons:", result["codons"])
    print("Codon counts:", result["counts"])

    print("\nCodon usage:")
    for codon in result["usage"]:
        percent = round(result["usage"][codon] * 100, 2)
        print(codon, ":", percent, "%")

    print("\nCodon fingerprint:", result["fingerprint"])

    print("\nReference comparison:")
    for organism in result["scores"]:
        score = result["scores"][organism]
        if score is None:
            print(organism, ": no shared codons")
        else:
            print(organism, ":", round(score, 4))

    print("Closest demonstration pattern (similarity):", result["closest"])
    print("KNN demo prediction:", result["ml_prediction"])
    print("KNN neighbour votes:", result["ml_votes"])
    print("Note: reference values are examples, not validated organism data.")

    if result["leftover"] > 0:
        print("Leftover bases not used:", result["leftover"])


# Menu for using the program
def main():
    while True:
        print("\n========== CODONPRINT ==========")
        print("1. Analyse one DNA sequence")
        print("2. Compare two DNA sequences")
        print("3. Read a FASTA file")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            sequence = input("Enter DNA sequence: ")
            result = analyse_sequence(sequence)

            if result is None:
                print("Invalid DNA sequence. Enter only A, T, G and C.")
            else:
                show_result(result)

        elif choice == "2":
            first = input("Enter first DNA sequence: ")
            second = input("Enter second DNA sequence: ")
            result = compare_two_sequences(first, second)

            if result is None:
                print("Both sequences must contain only A, T, G and C.")
            elif result["difference"] is None:
                print("No shared complete codons were found.")
            else:
                print("Shared codons:", result["shared"])
                print("Average usage difference:",
                      round(result["difference"], 4))

        elif choice == "3":
            filename = input("Enter FASTA file name: ")

            try:
                records = read_fasta_file(filename)

                if len(records) == 0:
                    print("No sequences found in the FASTA file.")

                for name, sequence in records:
                    print("\nSequence name:", name)
                    result = analyse_sequence(sequence)

                    if result is None:
                        print("This FASTA record has an invalid DNA sequence.")
                    else:
                        show_result(result)

            except FileNotFoundError:
                print("File not found. Keep it in the same folder as this program.")

        elif choice == "4":
            print("Thank you for using CODONPRINT.")
            break

        else:
            print("Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()
