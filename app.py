import streamlit as st
from codonprint import analyse_sequence, compare_two_sequences, read_fasta_file

# Page setup
st.set_page_config(
    page_title="CODONPRINT | DNA Analysis",
    page_icon="🧬",
    layout="wide"
)

# Simple page styling
st.markdown("""
<style>
    .main {background-color: #f7fafc;}
    .block-container {padding-top: 2rem; padding-bottom: 2rem;}
    h1, h2, h3 {color: #123047;}
    .stButton button {
        background-color: #087f8c;
        color: white;
        border-radius: 8px;
        border: 0;
        padding: 0.55rem 1.1rem;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("🧬 CODONPRINT")
st.subheader("Codon Usage-Based Organism Classifier")
st.write("A simple DNA sequence analysis project | Group 18")
st.caption("Jakkam Mithlesh (SE25UBIT036)  •  Ch. Nirav (SE25UBIT031)")
st.divider()

# Sidebar information
with st.sidebar:
    st.header("About CODONPRINT")
    st.write(
        "CODONPRINT studies DNA sequences by counting bases, "
        "calculating GC content and analysing codon usage."
    )
    st.write("**Tools included**")
    st.write("- DNA sequence analysis")
    st.write("- Two-sequence comparison")
    st.write("- FASTA file reading")
    st.write("- Demonstration KNN prediction")
    st.divider()
    st.caption("Built using Python and Streamlit.")

st.info(
    "Learning-project note: the included reference patterns and KNN training "
    "rows are small demonstration examples. They are not a validated scientific "
    "database and must not be treated as confirmed organism identification."
)

# Main sections
analyse_tab, compare_tab, fasta_tab = st.tabs(
    ["🧬 Analyse DNA", "↔️ Compare Sequences", "📁 FASTA Upload"]
)

with analyse_tab:
    st.header("DNA Sequence Analysis")
    st.write("Enter a DNA sequence using only A, T, G and C.")

    dna = st.text_area(
        "DNA sequence",
        placeholder="Example: ATGGCCGCTGCAAAAGCTGCC",
        height=130
    )

    if st.button("Analyse Sequence", key="analyse_button"):
        result = analyse_sequence(dna)

        if result is None:
            st.error("Invalid sequence. Please enter a non-empty sequence containing only A, T, G and C.")
        elif len(result["codons"]) == 0:
            st.warning("The sequence is valid, but it does not contain one complete codon (3 bases).")
        else:
            st.success("Sequence analysed successfully.")

            metric1, metric2, metric3 = st.columns(3)
            metric1.metric("Sequence length", result["length"], "bases")
            metric2.metric("GC content", str(round(result["gc"], 2)) + "%")
            metric3.metric("Complete codons", len(result["codons"]))

            st.subheader("Base composition")
            st.bar_chart({"Number of bases": result["bases"]})

            st.subheader("Codon usage")
            usage_percent = {}
            for codon in result["usage"]:
                usage_percent[codon] = round(result["usage"][codon] * 100, 2)
            st.bar_chart({"Usage (%)": usage_percent})

            st.subheader("Analysis details")
            detail1, detail2 = st.columns(2)
            with detail1:
                st.write("**Base counts**")
                st.write(result["bases"])
                st.write("**Codon counts**")
                st.write(result["counts"])
            with detail2:
                st.write("**Codon fingerprint (top three)**")
                st.write(result["fingerprint"])
                st.write("**Codon usage (%)**")
                for codon in usage_percent:
                    st.write(codon + ": " + str(usage_percent[codon]) + "%")

            st.subheader("Demonstration classification")
            st.write("**Closest reference pattern:**", result["closest"])
            st.write("**Basic KNN demo prediction:**", result["ml_prediction"])
            st.write("**KNN votes:**")
            st.write(result["ml_votes"])

            score_rows = []
            for organism in result["scores"]:
                score = result["scores"][organism]
                if score is not None:
                    score_rows.append({
                        "Reference pattern": organism,
                        "Average difference": round(score, 4)
                    })
            if score_rows:
                st.write("Lower difference means a closer match to the example pattern.")
                st.dataframe(score_rows, use_container_width=True)

            if result["leftover"] > 0:
                st.warning(
                    str(result["leftover"]) +
                    " leftover base(s) were not included in complete codons."
                )

            # Simple text report that can be downloaded
            report = "CODONPRINT DNA ANALYSIS\n"
            report += "Sequence length: " + str(result["length"]) + "\n"
            report += "GC content: " + str(round(result["gc"], 2)) + "%\n"
            report += "Base counts: " + str(result["bases"]) + "\n"
            report += "Codon counts: " + str(result["counts"]) + "\n"
            report += "Codon fingerprint: " + result["fingerprint"] + "\n"
            report += "Closest demonstration pattern: " + result["closest"] + "\n"
            report += "KNN demo prediction: " + result["ml_prediction"] + "\n"
            report += "Note: example data only; not validated organism identification.\n"

            st.download_button(
                "Download Analysis Report",
                data=report,
                file_name="codonprint_analysis.txt",
                mime="text/plain"
            )

with compare_tab:
    st.header("Compare Two DNA Sequences")
    st.write("Enter two sequences to compare their shared codons and usage.")

    first = st.text_area("First DNA sequence", key="first_sequence")
    second = st.text_area("Second DNA sequence", key="second_sequence")

    if st.button("Compare Sequences", key="compare_button"):
        result = compare_two_sequences(first, second)

        if result is None:
            st.error("Please enter two valid DNA sequences using A, T, G and C only.")
        elif result["difference"] is None:
            st.warning("No shared complete codons were found.")
        else:
            st.success("Comparison completed.")
            col1, col2 = st.columns(2)
            col1.metric("Shared codons", len(result["shared"]))
            col2.metric("Average usage difference", round(result["difference"], 4))
            st.write("**Shared codons:**", ", ".join(result["shared"]))

with fasta_tab:
    st.header("Analyse FASTA File")
    st.write("Upload a FASTA file containing one or more DNA sequences.")
    uploaded_file = st.file_uploader(
        "Choose a FASTA file",
        type=["fasta", "fa", "fna", "txt"]
    )

    if uploaded_file is not None:
        temporary_name = "uploaded_sequences.fasta"
        with open(temporary_name, "wb") as file:
            file.write(uploaded_file.getvalue())

        try:
            records = read_fasta_file(temporary_name)
            st.success(str(len(records)) + " sequence(s) found.")

            if len(records) == 0:
                st.warning("No FASTA records were found. Check that each sequence has a header beginning with >.")

            for name, sequence in records:
                with st.expander(name):
                    result = analyse_sequence(sequence)
                    if result is None:
                        st.error("This record contains invalid DNA characters.")
                    elif len(result["codons"]) == 0:
                        st.warning("No complete codons found in this record.")
                    else:
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Length", result["length"], "bases")
                        col2.metric("GC content", str(round(result["gc"], 2)) + "%")
                        col3.metric("Complete codons", len(result["codons"]))
                        st.write("**Codon fingerprint:**", result["fingerprint"])
                        st.write("**Closest demonstration pattern:**", result["closest"])
        except Exception:
            st.error("The FASTA file could not be read. Please check its format and try again.")

st.divider()
st.caption("CODONPRINT | Group 18 | Codon Usage Analysis")
