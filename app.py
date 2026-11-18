import streamlit as st
from codonprint import analyse_sequence, compare_two_sequences, read_fasta_file

st.set_page_config(page_title="CODONPRINT", page_icon="🧬")

# Simple white and blue design
st.markdown("""
<style>
.stApp {background-color: #f5f9ff;}
h1, h2, h3 {color: #174b7a;}
.stButton button {background-color: #1769aa; color: white;}
</style>
""", unsafe_allow_html=True)

st.title("🧬 CODONPRINT")
st.subheader("Codon Usage-Based Organism Classifier")
st.write("Group 18 | Jakkam Mithlesh and Ch. Nirav")
st.info("This is an educational project. Reference patterns and KNN results use small demo data and are not confirmed scientific organism identifications.")

st.sidebar.title("CODONPRINT")
st.sidebar.write("DNA sequence analysis")
st.sidebar.write("Group 18")
st.sidebar.write("Jakkam Mithlesh")
st.sidebar.write("Ch. Nirav")

analysis_tab, compare_tab, fasta_tab = st.tabs(
    ["Analyse DNA", "Compare DNA", "FASTA File"]
)

# 1. Analyse one DNA sequence
with analysis_tab:
    st.header("Analyse a DNA sequence")
    dna = st.text_area("Enter DNA sequence (A, T, G and C only)")

    if st.button("Analyse DNA"):
        result = analyse_sequence(dna)

        if result is None:
            st.error("Invalid sequence. Enter only A, T, G and C.")
        elif len(result["codons"]) == 0:
            st.warning("Enter at least 3 DNA bases to make a codon.")
        else:
            st.success("Analysis completed.")
            st.write("Sequence length:", result["length"])
            st.write("Base counts:", result["bases"])
            st.write("GC content:", round(result["gc"], 2), "%")
            st.write("Codon counts:", result["counts"])
            st.write("Codon usage:")

            for codon in result["usage"]:
                percent = round(result["usage"][codon] * 100, 2)
                st.write(codon, ":", percent, "%")

            st.write("Codon fingerprint:", result["fingerprint"])
            st.subheader("Demo classification")
            st.write("Closest reference pattern:", result["closest"])
            st.write("Basic KNN prediction:", result["ml_prediction"])
            st.write("KNN votes:", result["ml_votes"])

            if result["leftover"] > 0:
                st.warning(str(result["leftover"]) + " leftover base(s) were not used.")

            report = "CODONPRINT ANALYSIS REPORT\n"
            report += "Sequence length: " + str(result["length"]) + "\n"
            report += "Base counts: " + str(result["bases"]) + "\n"
            report += "GC content: " + str(round(result["gc"], 2)) + "%\n"
            report += "Codon counts: " + str(result["counts"]) + "\n"
            report += "Codon fingerprint: " + result["fingerprint"] + "\n"
            report += "Closest reference: " + result["closest"] + "\n"
            report += "KNN demo prediction: " + result["ml_prediction"] + "\n"

            st.download_button(
                "Download report",
                report,
                file_name="codonprint_report.txt"
            )

# 2. Compare two DNA sequences
with compare_tab:
    st.header("Compare two DNA sequences")
    first = st.text_area("Enter first DNA sequence", key="first")
    second = st.text_area("Enter second DNA sequence", key="second")

    if st.button("Compare DNA"):
        result = compare_two_sequences(first, second)

        if result is None:
            st.error("Both sequences must contain only A, T, G and C.")
        elif result["difference"] is None:
            st.warning("No shared codons found.")
        else:
            st.write("Shared codons:", result["shared"])
            st.write("Average usage difference:", round(result["difference"], 4))

# 3. Read a FASTA file
with fasta_tab:
    st.header("Analyse a FASTA file")
    uploaded_file = st.file_uploader("Upload a FASTA file", type=["fasta", "fa", "fna", "txt"])

    if uploaded_file is not None:
        file = open("uploaded_sequences.fasta", "wb")
        file.write(uploaded_file.getvalue())
        file.close()

        records = read_fasta_file("uploaded_sequences.fasta")

        if len(records) == 0:
            st.warning("No FASTA sequences found.")
        else:
            for name, sequence in records:
                st.subheader(name)
                result = analyse_sequence(sequence)

                if result is None:
                    st.error("This record has invalid DNA bases.")
                else:
                    st.write("Sequence length:", result["length"])
                    st.write("GC content:", round(result["gc"], 2), "%")
                    st.write("Codon fingerprint:", result["fingerprint"])
                    st.write("Closest reference pattern:", result["closest"])

                    if result["leftover"] > 0:
                        st.write("Unused bases:", result["leftover"])

st.markdown("---")
st.caption("CODONPRINT | Group 18 | Codon Usage Analysis")
