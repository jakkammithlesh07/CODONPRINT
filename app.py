import streamlit as st
from codonprint import analyse_sequence, compare_two_sequences, read_fasta_file

st.set_page_config(page_title="CODONPRINT", page_icon="🧬", layout="wide")

# Simple black and silver theme
st.markdown("""
<style>
.stApp {
    background-color: #111111;
    color: #eeeeee;
}
section[data-testid="stSidebar"] {
    background-color: #202020;
}
h1, h2, h3, p, label {
    color: #eeeeee;
}
.stButton button, .stDownloadButton button {
    background-color: #bfc3c7;
    color: #111111;
    border: 1px solid #eeeeee;
    border-radius: 5px;
}
.stButton button:hover, .stDownloadButton button:hover {
    background-color: #eeeeee;
    color: #111111;
    border: 1px solid #ffffff;
}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.title("CODONPRINT")
st.sidebar.write("Codon Usage Analysis")
st.sidebar.divider()
st.sidebar.write("Group 18")
st.sidebar.write("Jakkam Mithlesh")
st.sidebar.write("Ch. Nirav")
st.sidebar.write("Biotechnology")

# Main heading
st.title("🧬 CODONPRINT")
st.subheader("Codon Usage-Based Organism Classifier")
st.write("A simple tool to analyse DNA sequences and codon usage.")
st.info(
    "This is an educational project. The reference patterns and KNN results "
    "are demonstrations and are not verified organism identifications."
)
st.divider()

# Three main sections
analysis_tab, compare_tab, fasta_tab = st.tabs(
    ["Analyse DNA", "Compare Sequences", "FASTA File"]
)

# Analyse one DNA sequence
with analysis_tab:
    st.header("Analyse DNA Sequence")
    st.write("Enter a DNA sequence using A, T, G and C.")

    dna = st.text_area(
        "DNA sequence",
        placeholder="Example: ATGGCCGCTGCAAAAGCTGCC"
    )

    if st.button("Analyse DNA"):
        result = analyse_sequence(dna)

        if result is None:
            st.error("Invalid sequence. Use only A, T, G and C.")
        elif len(result["codons"]) == 0:
            st.warning("Enter at least 3 DNA bases.")
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
                    "Count": result["counts"][codon],
                    "Usage (%)": percent
                })

            st.dataframe(codon_rows, use_container_width=True)
            st.bar_chart(codon_rows, x="Codon", y="Usage (%)")

            st.subheader("Codon Fingerprint")
            st.write(result["fingerprint"])

            st.subheader("Demonstration Classification")
            st.write("Closest reference pattern:", result["closest"])
            st.write("Basic KNN prediction:", result["ml_prediction"])
            st.write("KNN votes:", result["ml_votes"])

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
            report += "Basic KNN prediction: " + result["ml_prediction"] + "\n"
            report += "Note: demonstration data only.\n"

            st.download_button(
                "Download Analysis Report",
                report,
                file_name="codonprint_report.txt"
            )

# Compare two DNA sequences
with compare_tab:
    st.header("Compare Two Sequences")
    st.write("Enter two DNA sequences to compare their codon usage.")

    first = st.text_area("First DNA sequence")
    second = st.text_area("Second DNA sequence")

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

# Read sequences from a FASTA file
with fasta_tab:
    st.header("FASTA File Analysis")
    st.write("Upload a FASTA file containing DNA sequences.")

    uploaded_file = st.file_uploader(
        "Choose a FASTA file",
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
                    st.error("This record contains invalid DNA bases.")
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
                        st.warning(
                            str(result["leftover"]) +
                            " leftover base(s) were not used."
                        )

st.divider()
st.caption("CODONPRINT | Group 18 | Codon Usage Analysis")
