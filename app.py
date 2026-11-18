import streamlit as st
from codonprint import analyse_sequence, compare_two_sequences, read_fasta_file

# Page setup
st.set_page_config(
    page_title="CODONPRINT / DNA Analysis",
    page_icon="🧬",
    layout="wide"
)

# Simple styling for the website
st.markdown("""
<style>
.stApp {
    background-color: #f7f3ed;
    color: #292522;
}
.block-container {
    max-width: 1120px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}
h1, h2, h3, p, label {
    color: #292522;
}
.hero {
    background: #fffdf9;
    border: 1px solid #e6ddd1;
    border-radius: 18px;
    padding: 32px;
    margin-bottom: 22px;
}
.eyebrow {
    color: #946b55;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 3px;
}
.brand {
    color: #382b2c;
    font-size: 42px;
    font-weight: 800;
    letter-spacing: 1px;
    margin: 8px 0 0 0;
}
.tagline {
    color: #806c63;
    font-size: 17px;
    margin-top: 4px;
}
.hero-note {
    color: #655b55;
    font-size: 14px;
    margin-top: 16px;
}
.feature {
    background: #fffdf9;
    border: 1px solid #e6ddd1;
    border-radius: 14px;
    padding: 18px;
    min-height: 112px;
}
.feature-no {
    color: #a56e58;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
}
.feature-title {
    color: #382b2c;
    font-size: 17px;
    font-weight: 700;
    margin-top: 8px;
}
.feature-text {
    color: #806c63;
    font-size: 13px;
    margin-top: 3px;
}
.panel {
    background: #fffdf9;
    border: 1px solid #e6ddd1;
    border-radius: 14px;
    padding: 20px;
}
.footer {
    color: #8a786e;
    text-align: center;
    font-size: 13px;
    padding: 25px 0 5px 0;
}
div[data-testid="stMetric"] {
    background: #fffdf9;
    border: 1px solid #e6ddd1;
    border-radius: 12px;
    padding: 14px;
}
div[data-testid="stTextArea"] textarea {
    background-color: #fffdf9 !important;
    color: #292522 !important;
    border: 1px solid #d8c9bb !important;
    border-radius: 10px !important;
}
div[data-testid="stFileUploader"] {
    background: #fffdf9;
    border: 1px dashed #cbb8a8;
    border-radius: 12px;
    padding: 14px;
}
.stButton > button, .stDownloadButton > button {
    background: #6f454b;
    color: white;
    border: 1px solid #6f454b;
    border-radius: 9px;
    min-height: 44px;
    font-weight: 600;
}
.stButton > button:hover, .stDownloadButton > button:hover {
    background: #52343a;
    color: white;
    border-color: #52343a;
}
div[data-testid="stTabs"] button {
    color: #6f454b;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

# Website heading
st.markdown("""
<div class="hero">
    <div class="eyebrow">GROUP 18 / PYTHON + BIOPYTHON PROJECT</div>
    <div class="brand">CODONPRINT</div>
    <div class="tagline">Codon Usage-Based Organism Classifier</div>
    <div class="hero-note">
        A simple workspace to explore DNA sequences, codon patterns
        and sequence comparisons.
    </div>
</div>
""", unsafe_allow_html=True)

# Three main features
one, two, three = st.columns(3)

with one:
    st.markdown("""
    <div class="feature">
        <div class="feature-no">01 / ANALYSE</div>
        <div class="feature-title">DNA composition</div>
        <div class="feature-text">Base counts, GC content and codon usage</div>
    </div>
    """, unsafe_allow_html=True)

with two:
    st.markdown("""
    <div class="feature">
        <div class="feature-no">02 / COMPARE</div>
        <div class="feature-title">Sequence patterns</div>
        <div class="feature-text">Compare the codon usage of two sequences</div>
    </div>
    """, unsafe_allow_html=True)

with three:
    st.markdown("""
    <div class="feature">
        <div class="feature-no">03 / UPLOAD</div>
        <div class="feature-title">FASTA reader</div>
        <div class="feature-text">Read and analyse sequence records</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.caption(
    "Note: Reference patterns and KNN training rows are small demonstration "
    "examples. They are not verified biological data."
)

# Work sections
analyse_tab, compare_tab, fasta_tab = st.tabs(
    ["DNA ANALYSIS", "SEQUENCE COMPARISON", "FASTA READER"]
)

# DNA analysis
with analyse_tab:
    st.markdown("## Analyse a DNA sequence")
    st.write("Enter a sequence using A, T, G and C.")

    dna = st.text_area(
        "DNA sequence",
        placeholder="Example: ATGGCCGCTGCAAAAGCTGCC",
        height=120
    )

    if st.button("Analyse DNA", key="analyse_button", use_container_width=True):
        result = analyse_sequence(dna)

        if result is None:
            st.error("Invalid sequence. Please use only A, T, G and C.")
        elif len(result["codons"]) == 0:
            st.warning("Enter at least 3 DNA bases to make a complete codon.")
        else:
            st.success("Analysis completed.")

            st.markdown("### Sequence overview")
            a, b, c = st.columns(3)
            a.metric("Sequence length", str(result["length"]) + " bases")
            b.metric("GC content", str(round(result["gc"], 2)) + "%")
            c.metric("Complete codons", len(result["codons"]))

            st.markdown("### Base composition")
            a, b, c, d = st.columns(4)
            a.metric("A", result["bases"]["A"])
            b.metric("T", result["bases"]["T"])
            c.metric("G", result["bases"]["G"])
            d.metric("C", result["bases"]["C"])

            st.markdown("### Codon usage")
            codon_rows = []

            for codon in result["usage"]:
                codon_rows.append({
                    "Codon": codon,
                    "Count": result["counts"][codon],
                    "Usage (%)": round(result["usage"][codon] * 100, 2)
                })

            st.dataframe(codon_rows, use_container_width=True, hide_index=True)
            st.bar_chart(codon_rows, x="Codon", y="Usage (%)")

            st.markdown("### Codon fingerprint")
            st.markdown(
                '<div class="panel">' + result["fingerprint"] + '</div>',
                unsafe_allow_html=True
            )

            st.markdown("### Demonstration results")
            a, b = st.columns(2)
            a.metric("Closest reference pattern", result["closest"])
            b.metric("Basic KNN result", result["ml_prediction"])

            with st.expander("See KNN votes"):
                st.write(result["ml_votes"])

            with st.expander("See codon counts"):
                st.write(result["counts"])

            if result["leftover"] > 0:
                st.warning(
                    str(result["leftover"]) +
                    " base(s) at the end do not form a complete codon."
                )

            report = "CODONPRINT / DNA ANALYSIS REPORT\n"
            report += "Sequence length: " + str(result["length"]) + "\n"
            report += "Base counts: " + str(result["bases"]) + "\n"
            report += "GC content: " + str(round(result["gc"], 2)) + "%\n"
            report += "Codon counts: " + str(result["counts"]) + "\n"
            report += "Codon fingerprint: " + result["fingerprint"] + "\n"
            report += "Closest reference pattern: " + result["closest"] + "\n"
            report += "Basic KNN result: " + result["ml_prediction"] + "\n"
            report += "Note: demonstration data only.\n"

            st.download_button(
                "Download analysis report",
                report,
                file_name="codonprint_report.txt",
                use_container_width=True
            )

# Compare two sequences
with compare_tab:
    st.markdown("## Compare two DNA sequences")
    st.write("Enter two DNA sequences to compare their shared codons.")

    first = st.text_area(
        "First sequence",
        key="first_sequence",
        placeholder="Enter the first DNA sequence"
    )
    second = st.text_area(
        "Second sequence",
        key="second_sequence",
        placeholder="Enter the second DNA sequence"
    )

    if st.button("Compare sequences", key="compare_button", use_container_width=True):
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

# FASTA file reader
with fasta_tab:
    st.markdown("## Read a FASTA file")
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
                        a, b, c = st.columns(3)
                        a.metric("Length", str(result["length"]) + " bases")
                        b.metric("GC content", str(round(result["gc"], 2)) + "%")
                        c.metric("Codons", len(result["codons"]))
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
    CODONPRINT / GROUP 18 / CODON USAGE ANALYSIS
    <br>
    Jakkam Mithlesh / Ch. Nirav
</div>
""", unsafe_allow_html=True)
