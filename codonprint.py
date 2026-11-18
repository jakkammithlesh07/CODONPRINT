REFERENCE = {
    "E_coli": {"GCT": 0.18, "GCC": 0.26, "GCA": 0.23, "GCG": 0.33,
               "AAA": 0.34, "AAG": 0.66},
    "Human": {"GCT": 0.27, "GCC": 0.40, "GCA": 0.23, "GCG": 0.10,
              "AAA": 0.43, "AAG": 0.57},
    "Yeast": {"GCT": 0.38, "GCC": 0.22, "GCA": 0.29, "GCG": 0.11,
              "AAA": 0.42, "AAG": 0.58}
}


def clean_sequence(sequence):
    return "".join(sequence.upper().split())


def validate_dna(sequence):
    if not sequence:
        return False
    for base in sequence:
        if base not in "ATGC":
            return False
    return True


def split_codons(sequence):
    codons = []
    for i in range(0, len(sequence) - 2, 3):
        codons.append(sequence[i:i + 3])
    return codons


def analyse_sequence(sequence):
    sequence = clean_sequence(sequence)
    bases = {"A": 0, "T": 0, "G": 0, "C": 0}
    for base in sequence:
        bases[base] += 1

    gc_content = 0
    if len(sequence) > 0:
        gc_content = ((bases["G"] + bases["C"]) / len(sequence)) * 100

    codons = split_codons(sequence)
    counts = {}
    for codon in codons:
        if codon in counts:
            counts[codon] += 1
        else:
            counts[codon] = 1

    usage = {}
    total = len(codons)
    if total > 0:
        for codon in counts:
            usage[codon] = counts[codon] / total

    top_codons = sorted(counts.items(), key=lambda item: item[1], reverse=True)[:3]

    return {
        "length": len(sequence),
        "base_counts": bases,
        "gc_content": gc_content,
        "total_codons": total,
        "codon_counts": counts,
        "codon_usage": usage,
        "top_codons": top_codons
    }


def closest_reference(usage):
    best_name = "No reference match"
    best_score = None

    for organism in REFERENCE:
        differences = []
        for codon in usage:
            if codon in REFERENCE[organism]:
                differences.append(abs(usage[codon] - REFERENCE[organism][codon]))

        if differences:
            score = sum(differences) / len(differences)
            if best_score is None or score < best_score:
                best_score = score
                best_name = organism

    if best_score is None:
        return best_name, 0.0
    return best_name, best_score


def compare_sequences(first, second):
    first_usage = analyse_sequence(first)["codon_usage"]
    second_usage = analyse_sequence(second)["codon_usage"]

    shared = sorted(set(first_usage) & set(second_usage))
    if not shared:
        average_difference = 0.0
    else:
        differences = []
        for codon in shared:
            differences.append(abs(first_usage[codon] - second_usage[codon]))
        average_difference = sum(differences) / len(differences)

    return {
        "shared_codons": shared,
        "average_difference": average_difference
    }


def read_fasta(content):
    records = []
    name = None
    sequence_parts = []

    for line in content.splitlines():
        line = line.strip()
        if not line:
            continue
        if line.startswith(">"):
            if name is not None:
                records.append((name, "".join(sequence_parts)))
            name = line[1:].strip() or "Unnamed sequence"
            sequence_parts = []
        else:
            sequence_parts.append(line)

    if name is not None:
        records.append((name, "".join(sequence_parts)))

    return records
