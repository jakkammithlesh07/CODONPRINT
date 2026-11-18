import streamlit as st
from codonprint import analyse_sequence, compare_two_sequences, read_fasta_file

st.set_page_config(page_title="CODONPRINT", page_icon="🧬", layout="wide")

# Simple white and light grey design
st.markdown("""
<style>
.stApp {
    background-color: #f5f6f7;
}
.block-container {
    max-width: 1100px;
    padding-top: 2rem;
}
h1, h2, h3 {
    color: #30343b;
}
</style>
""", unsafe_allow_html=True)

# Project heading
st.title("🧬 CODONPRINT")
st.subheader("Codon Usage-Based Organism Classifier")
st.write("Group 18 | Jakkam Mithlesh and Ch. Nirav")
st.write(
    "This project analyses DNA sequences using base counts, GC content "
    "and codon usage. The reference patterns and KNN results are for "
    "demonstration and are not verified organism identifications."
)

st.divider()

# Three main parts of the project
analysis_tab, compare_tab, fasta_tab = st.tabs(
    ["Analyse DNA", "Compare Sequences", "FASTA File"]
)

# 1. Analyse one DNA sequence
with analysis_tab:
    st.header("Analyse a DNA Sequence")
    dna = st.text_area(
        "Enter a DNA sequence (A, T, G and C only)",
        placeholder="Example: ATGGCCGCTGCAAAAGCTGCC"
    )

    if st.button("Analyse DNA"):
        result = analyse_sequence(dna)

        if result is None:
            st.error("Invalid sequence. Please enter only A, T, G and C.")
        elif len(result["codons"]) == 0:
            st.warning("Enter at least 3 DNA bases to make a codon.")
        else:
            st.success("Analysis completed.")

            col1, col2, col3 = st.columns(3)
            col1.metric("Sequence length", str(result["length"]) + " bases")
            col2.metric("GC content", str(round(result["gc"], 2)) + "%")
            col3.metric("Complete codons", len(result["codons"]))

            st.subheader("Base Counts")
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("A", result["bases"]["A"])
            col2.metric("T", result["bases"]["T"])
            col3.metric("G", result["bases"]["G"])
            col4.metric("C", result["bases"]["C"])

            st.subheader("Codon Usage")
            codon_rows = []

            for codon in result["usage"]:
                percent = round(result["usage"][codon] * 100, 2)
                codon_rows.append({
                    "Codon": codon,
                    "Usage (%)": percent,
                    "Count": result["counts"][codon]
                })

            st.dataframe(codon_rows, use_container_width=True, hide_index=True)
            st.bar_chart(codon_rows, x="Codon", y="Usage (%)")

            st.subheader("Codon Fingerprint")
            st.write(result["fingerprint"])

            st.subheader("Demonstration Classification")
            col1, col2 = st.columns(2)
            col1.metric("Closest reference pattern", result["closest"])
            col2.metric("Basic KNN result", result["ml_prediction"])

            with st.expander("Show KNN votes"):
                st.write(result["ml_votes"])

            with st.expander("Show codon counts"):
                st.write(result["counts"])

            if result["leftover"] > 0:
                st.warning(
                    str(result["leftover"]) +
                    " leftover base(s) were not included in complete codons."
                )

            report = "CODONPRINT ANALYSIS REPORT\n"
            report += "Sequence length: " + str(result["length"]) + "\n"
            report += "Base counts: " + str(result["bases"]) + "\n"
            report += "GC content: " + str(round(result["gc"], 2)) + "%\n"
            report += "Codon counts: " + str(result["counts"]) + "\n"
            report += "Codon fingerprint: " + result["fingerprint"] + "\n"
            report += "Closest reference pattern: " + result["closest"] + "\n"
            report += "Basic KNN result: " + result["ml_prediction"] + "\n"
            report += "Note: demonstration data only.\n"

            st.download_button(
                "Download Analysis Report",
                report,
                file_name="codonprint_report.txt"
            )

# 2. Compare two DNA sequences
with compare_tab:
    st.header("Compare Two DNA Sequences")
    first = st.text_area("First DNA sequence", key="first_sequence")
    second = st.text_area("Second DNA sequence", key="second_sequence")

    if st.button("Compare DNA"):
        result = compare_two_sequences(first, second)

        if result is None:
            st.error("Both sequences must contain only A, T, G and C.")
        elif result["difference"] is None:
            st.warning("No shared complete codons were found.")
        else:
            st.success("Comparison completed.")
            st.metric(
                "Average usage difference",
                round(result["difference"], 4)
            )
            st.write("Shared codons:", ", ".join(result["shared"]))

# 3. Read DNA sequences from a FASTA file
with fasta_tab:
    st.header("Read a FASTA File")
    uploaded_file = st.file_uploader(
        "Upload a FASTA file",
        type=["fasta", "fa", "fna", "txt"]
    )

    if uploaded_file is not None:
        file = open("uploaded_sequences.fasta", "wb")
        file.write(uploaded_file.getvalue())
        file.close()

        records = read_fasta_file("uploaded_sequences.fasta")

        if len(records) == 0:
            st.warning("No sequences were found in this file.")
        else:
            st.success(str(len(records)) + " sequence(s) found.")

            for name, sequence in records:
                st.subheader(name)
                result = analyse_sequence(sequence)

                if result is None:
                    st.error("This record contains an invalid DNA sequence.")
                elif len(result["codons"]) == 0:
                    st.warning("This record has no complete codons.")
                else:
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Length", str(result["length"]) + " bases")
                    col2.metric("GC content", str(round(result["gc"], 2)) + "%")
                    col3.metric("Codons", len(result["codons"]))
                    st.write("Codon fingerprint:", result["fingerprint"])
                    st.write("Closest reference pattern:", result["closest"])

                    if result["leftover"] > 0:
                        st.write(
                            str(result["leftover"]) +
                            " leftover base(s) were not used."
                        )

st.divider()
st.caption("CODONPRINT | Group 18 | Codon Usage Analysis")
