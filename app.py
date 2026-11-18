import streamlit as st
from codonprint import analyse_sequence, compare_two_sequences, read_fasta_file

st.set_page_config(
    page_title="CODONPRINT | DNA Analysis",
    page_icon="🧬",
    layout="wide"
)

# White and blue website design
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #eef6ff 0%, #ffffff 48%);
    color: #17324d;
}
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1200px;
}
.hero {
    background: linear-gradient(120deg, #073b72, #1677c8);
    padding: 35px;
    border-radius: 22px;
    color: white;
    margin-bottom: 22px;
    box-shadow: 0 10px 30px rgba(16, 75, 130, 0.16);
}
.hero h1 {
    color: white;
    font-size: 42px;
    margin: 0;
    letter-spacing: 2px;
}
.hero p {
    color: #e5f2ff;
    font-size: 17px;
    margin-bottom: 4px;
}
.small-tag {
    color: #d7ecff;
    font-size: 13px;
    letter-spacing: 2px;
    font-weight: bold;
}
.info-card {
    background: white;
    border: 1px solid #d9eaff;
    border-radius: 16px;
    padding: 19px;
    box-shadow: 0 5px 18px rgba(30, 90, 150, 0.06);
    min-height: 105px;
}
.info-card h3 {
    color: #1769aa;
    margin: 0 0 8px 0;
    font-size: 15px;
}
.info-card p {
    color: #17324d;
    font-size: 19px;
    font-weight: 650;
    margin: 0;
}
.section-title {
    color: #104b7e;
    font-size: 24px;
    font-weight: 700;
    margin-top: 10px;
}
.stButton button, .stDownloadButton button {
    background: #1268ad;
    color: white;
    border: 0;
    border-radius: 10px;
    padding: 10px 20px;
    font-weight: 650;
}
.stButton button:hover, .stDownloadButton button:hover {
    background: #084b85;
    color: white;
    border: 0;
}
div[data-testid="stTabs"] button {
    font-weight: 650;
}
div[data-testid="stTextArea"] textarea {
    border: 1px solid #b9d7f4;
    border-radius: 12px;
}
footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("## 🧬 CODONPRINT")
st.sidebar.caption("DNA sequence analysis")
st.sidebar.markdown("---")
st.sidebar.write("**Project team**")
st.sidebar.write("Jakkam Mithlesh")
st.sidebar.write("Ch. Nirav")
st.sidebar.markdown("---")
st.sidebar.caption("Group 18 | Biotechnology")

# Main heading
st.markdown("""
<div class="hero">
    <div class="small-tag">GROUP 18 • BIOTECHNOLOGY PROJECT</div>
    <h1>🧬 CODONPRINT</h1>
    <p>Codon Usage-Based Organism Classifier</p>
    <p>Explore DNA sequences through codon patterns, GC content and simple comparisons.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="info-card">
<h3>ABOUT THIS PROJECT</h3>
<p style="font-size:15px;font-weight:400;">
CODONPRINT is a learning project for analysing DNA sequences.
It calculates base composition, GC content and codon usage.
The reference patterns and KNN output are demonstrations, not verified
scientific organism identifications.
</p>
</div>
""", unsafe_allow_html=True)

st.write("")
analysis_tab, compare_tab, fasta_tab = st.tabs(
    ["🧬  Analyse DNA", "⇄  Compare Sequences", "📁  FASTA Analysis"]
)

# Analyse one sequence
with analysis_tab:
    st.markdown('<div class="section-title">DNA Sequence Analysis</div>', unsafe_allow_html=True)
    st.write("Enter a DNA sequence to view its composition and codon pattern.")
    dna = st.text_area(
        "DNA sequence (A, T, G and C only)",
        placeholder="Example: ATGGCCGCTGCAAAAGCTGCC",
        height=130
    )

    if st.button("Analyse sequence", key="analyse"):
        result = analyse_sequence(dna)

        if result is None:
            st.error("Invalid sequence. Please use only A, T, G and C.")
        elif len(result["codons"]) == 0:
            st.warning("Please enter at least 3 DNA bases.")
        else:
            st.success("Sequence analysed successfully.")

            col1, col2, col3 = st.columns(3)
            col1.metric("Sequence length", str(result["length"]) + " bases")
            col2.metric("GC content", str(round(result["gc"], 2)) + "%")
            col3.metric("Complete codons", len(result["codons"]))

            st.markdown("#### Base composition")
            b1, b2, b3, b4 = st.columns(4)
            b1.metric("Adenine (A)", result["bases"]["A"])
            b2.metric("Thymine (T)", result["bases"]["T"])
            b3.metric("Guanine (G)", result["bases"]["G"])
            b4.metric("Cytosine (C)", result["bases"]["C"])

            st.markdown("#### Codon usage")
            codon_rows = []
            for codon in result["usage"]:
                percent = round(result["usage"][codon] * 100, 2)
                codon_rows.append({"Codon": codon, "Usage (%)": percent,
                                   "Count": result["counts"][codon]})
            st.dataframe(codon_rows, use_container_width=True, hide_index=True)
            st.bar_chart(
                {"Usage (%)": [row["Usage (%)"] for row in codon_rows]},
                x=[row["Codon"] for row in codon_rows],
                use_container_width=True
            )

            st.markdown("#### Codon fingerprint")
            st.info(result["fingerprint"])

            st.markdown("#### Demonstration classification")
            x1, x2 = st.columns(2)
            x1.metric("Closest reference pattern", result["closest"])
            x2.metric("Basic KNN prediction", result["ml_prediction"])
            with st.expander("View KNN votes"):
                st.write(result["ml_votes"])
            with st.expander("View codon counts"):
                st.write(result["counts"])
            with st.expander("What does this result mean?"):
                st.write("GC content is the percentage of G and C bases in the sequence.")
                st.write("Codon usage shows how frequently each three-base codon occurs.")
                st.write("The reference and KNN outputs use small demonstration data only.")

            if result["leftover"] > 0:
                st.warning(str(result["leftover"]) + " leftover base(s) were not included in complete codons.")

            report = "CODONPRINT ANALYSIS REPORT\n"
            report += "Sequence length: " + str(result["length"]) + "\n"
            report += "Base counts: " + str(result["bases"]) + "\n"
            report += "GC content: " + str(round(result["gc"], 2)) + "%\n"
            report += "Codon counts: " + str(result["counts"]) + "\n"
            report += "Codon fingerprint: " + result["fingerprint"] + "\n"
            report += "Closest reference pattern: " + result["closest"] + "\n"
            report += "Basic KNN prediction: " + result["ml_prediction"] + "\n"
            report += "Note: demonstration data only; not validated identification.\n"

            st.download_button(
                "⬇ Download analysis report",
                report,
                file_name="codonprint_report.txt"
            )

# Compare two sequences
with compare_tab:
    st.markdown('<div class="section-title">Compare DNA Sequences</div>', unsafe_allow_html=True)
    st.write("Enter two DNA sequences to compare their shared codons and usage.")
    left, right = st.columns(2)
    with left:
        first = st.text_area("First DNA sequence", placeholder="Enter first sequence", height=130)
    with right:
        second = st.text_area("Second DNA sequence", placeholder="Enter second sequence", height=130)

    if st.button("Compare sequences", key="compare"):
        result = compare_two_sequences(first, second)

        if result is None:
            st.error("Both sequences must contain only A, T, G and C.")
        elif result["difference"] is None:
            st.warning("No shared complete codons were found.")
        else:
            st.success("Comparison completed.")
            st.metric("Average usage difference", round(result["difference"], 4))
            st.markdown("#### Shared codons")
            st.write(", ".join(result["shared"]))
            st.caption("A smaller difference means the shared codon usage values are more similar.")

# FASTA file analysis
with fasta_tab:
    st.markdown('<div class="section-title">FASTA File Analysis</div>', unsafe_allow_html=True)
    st.write("Upload a FASTA file containing one or more DNA sequences.")
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
            st.warning("No FASTA sequences were found in this file.")
        else:
            st.success(str(len(records)) + " sequence(s) found.")
            for name, sequence in records:
                with st.expander(name, expanded=True):
                    result = analyse_sequence(sequence)
                    if result is None:
                        st.error("This record contains invalid DNA bases.")
                    elif len(result["codons"]) == 0:
                        st.warning("This record does not contain a complete codon.")
                    else:
                        c1, c2, c3 = st.columns(3)
                        c1.metric("Length", str(result["length"]) + " bases")
                        c2.metric("GC content", str(round(result["gc"], 2)) + "%")
                        c3.metric("Codons", len(result["codons"]))
                        st.write("Codon fingerprint:", result["fingerprint"])
                        st.write("Closest reference pattern:", result["closest"])
                        if result["leftover"] > 0:
                            st.caption(str(result["leftover"]) + " leftover base(s) were not used.")

st.markdown("---")
st.markdown(
    "<div style='text-align:center;color:#54718c;font-size:13px;'>"
    "CODONPRINT  |  Group 18  |  Codon Usage Analysis"
    "</div>",
    unsafe_allow_html=True
)
