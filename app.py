import streamlit as st
from codonprint import analyse_sequence, compare_two_sequences, read_fasta_file

# Page settings
st.set_page_config(
    page_title="CODONPRINT | DNA Analysis",
    page_icon="🧬",
    layout="wide"
)

# White and light grey design
st.markdown("""
<style>
.stApp {
    background: #f4f6f8;
    color: #202936;
}
.block-container {
    max-width: 1180px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}
h1, h2, h3 {
    color: #202936;
}
.hero {
    background: white;
    padding: 30px;
    border: 1px solid #e2e6eb;
    border-radius: 16px;
    margin-bottom: 18px;
}
.hero-tag {
    color: #657386;
    font-size: 13px;
    letter-spacing: 2px;
    font-weight: bold;
}
.hero-title {
    color: #202936;
    font-size: 38px;
    font-weight: 800;
    margin: 8px 0 4px 0;
}
.hero-subtitle {
    color: #64748b;
    font-size: 17px;
}
.info-card {
    background: white;
    border: 1px solid #e2e6eb;
    border-radius: 12px;
    padding: 18px;
    min-height: 105px;
}
.info-number {
    color: #202936;
    font-size: 25px;
    font-weight: bold;
}
.info-label {
    color: #718096;
    font-size: 13px;
}
.section-card {
    background: white;
    border: 1px solid #e2e6eb;
    border-radius: 12px;
    padding: 20px;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e2e6eb;
    padding: 14px;
    border-radius: 10px;
}
.stButton > button, .stDownloadButton > button {
    border-radius: 8px;
    font-weight: 600;
    min-height: 42px;
}
div[data-testid="stTabs"] button {
    font-weight: 600;
}
.footer {
    color: #7b8794;
    text-align: center;
    padding: 18px 0 4px 0;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="hero">
    <div class="hero-tag">GROUP 18 · BIOINFORMATICS PROJECT</div>
    <div class="hero-title">🧬 CODONPRINT</div>
    <div class="hero-subtitle">Codon Usage-Based Organism Classifier</div>
    <p style="color:#64748b; margin-bottom:0;">
        Explore DNA composition, codon usage and sequence similarity
        through a simple analysis workspace.
    </p>
</div>
""", unsafe_allow_html=True)

# Project information
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="info-card">
        <div class="info-number">01</div>
        <div class="info-label">Analyse DNA composition</div>
    </div>
    """, unsafe_allow_html=True)
with col2:
    st.markdown("""
    <div class="info-card">
        <div class="info-number">02</div>
        <div class="info-label">Compare codon usage</div>
    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="info-card">
        <div class="info-number">03</div>
        <div class="info-label">Read FASTA sequences</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.info(
    "Educational project: the reference patterns and KNN training rows "
    "are demonstration examples, not verified biological data."
)

# Main work areas
analysis_tab, compare_tab, fasta_tab = st.tabs(
    ["  Analyse DNA  ", "  Compare Sequences  ", "  FASTA File  "]
)

# --------------------------------------------------
# 1. Analyse one DNA sequence
# --------------------------------------------------
with analysis_tab:
    st.markdown("## DNA Sequence Analysis")
    st.write("Enter a DNA sequence to view its base composition and codon usage.")

    dna = st.text_area(
        "DNA sequence (A, T, G and C only)",
        placeholder="Example: ATGGCCGCTGCAAAAGCTGCC",
        height=130
    )

    if st.button("Analyse Sequence", key="analyse_button", use_container_width=True):
        result = analyse_sequence(dna)

        if result is None:
            st.error("Invalid sequence. Please use only A, T, G and C.")
        elif len(result["codons"]) == 0:
            st.warning("Please enter at least 3 DNA bases.")
        else:
            st.success("Sequence analysis completed.")

            st.markdown("### Sequence Summary")
            col1, col2, col3 = st.columns(3)
            col1.metric("Sequence Length", str(result["length"]) + " bases")
            col2.metric("GC Content", str(round(result["gc"], 2)) + "%")
            col3.metric("Complete Codons", len(result["codons"]))

            st.markdown("### Base Composition")
            a, b, c, d = st.columns(4)
            a.metric("Adenine (A)", result["bases"]["A"])
            b.metric("Thymine (T)", result["bases"]["T"])
            c.metric("Guanine (G)", result["bases"]["G"])
            d.metric("Cytosine (C)", result["bases"]["C"])

            st.markdown("### Codon Usage")
            codon_rows = []

            for codon in result["usage"]:
                percent = round(result["usage"][codon] * 100, 2)
                codon_rows.append({
                    "Codon": codon,
                    "Count": result["counts"][codon],
                    "Usage (%)": percent
                })

            st.dataframe(
                codon_rows,
                use_container_width=True,
                hide_index=True
            )
            st.bar_chart(codon_rows, x="Codon", y="Usage (%)")

            st.markdown("### Codon Fingerprint")
            st.markdown(
                '<div class="section-card">' + result["fingerprint"] + '</div>',
                unsafe_allow_html=True
            )

            st.markdown("### Demonstration Classification")
            col1, col2 = st.columns(2)
            col1.metric("Closest Reference Pattern", result["closest"])
            col2.metric("Basic KNN Result", result["ml_prediction"])

            with st.expander("View KNN votes"):
                st.write(result["ml_votes"])

            with st.expander("View codon counts"):
                st.write(result["counts"])

            if result["leftover"] > 0:
                st.warning(
                    str(result["leftover"]) +
                    " leftover base(s) were not included in complete codons."
                )

            # Create a simple text report for download
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
                file_name="codonprint_report.txt",
                use_container_width=True
            )

# --------------------------------------------------
# 2. Compare two DNA sequences
# --------------------------------------------------
with compare_tab:
    st.markdown("## Compare Two DNA Sequences")
    st.write("Enter two sequences to compare their shared codons and usage.")

    first = st.text_area(
        "First DNA sequence",
        key="first_sequence",
        placeholder="Enter the first sequence"
    )
    second = st.text_area(
        "Second DNA sequence",
        key="second_sequence",
        placeholder="Enter the second sequence"
    )

    if st.button("Compare Sequences", key="compare_button", use_container_width=True):
        result = compare_two_sequences(first, second)

        if result is None:
            st.error("Both sequences must contain only A, T, G and C.")
        elif result["difference"] is None:
            st.warning("No shared complete codons were found.")
        else:
            st.success("Sequence comparison completed.")
            st.metric(
                "Average Usage Difference",
                round(result["difference"], 4)
            )
            st.write("Shared codons:", ", ".join(result["shared"]))

# --------------------------------------------------
# 3. Read a FASTA file
# --------------------------------------------------
with fasta_tab:
    st.markdown("## FASTA File Analysis")
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
            st.warning("No sequences were found in this file.")
        else:
            st.success(str(len(records)) + " sequence(s) found.")

            for name, sequence in records:
                with st.expander(name, expanded=True):
                    result = analyse_sequence(sequence)

                    if result is None:
                        st.error("This record contains an invalid DNA sequence.")
                    elif len(result["codons"]) == 0:
                        st.warning("This record has no complete codons.")
                    else:
                        col1, col2, col3 = st.columns(3)
                        col1.metric("Length", str(result["length"]) + " bases")
                        col2.metric("GC Content", str(round(result["gc"], 2)) + "%")
                        col3.metric("Codons", len(result["codons"]))

                        st.write("Codon fingerprint:", result["fingerprint"])
                        st.write("Closest reference pattern:", result["closest"])

                        if result["leftover"] > 0:
                            st.caption(
                                str(result["leftover"]) +
                                " leftover base(s) were not used."
                            )

# Footer
st.markdown("""
<div class="footer">
    CODONPRINT &nbsp; | &nbsp; Group 18 &nbsp; | &nbsp; Codon Usage Analysis
    <br>
    Jakkam Mithlesh · Ch. Nirav
</div>
""", unsafe_allow_html=True)
