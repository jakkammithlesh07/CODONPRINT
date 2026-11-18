import streamlit as st
from codonprint import (
    clean_sequence, validate_dna, analyse_sequence,
    compare_sequences, read_fasta, closest_reference
)

st.set_page_config(page_title="CODONPRINT", page_icon="🧬", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #3b241b; color: #ffffff; }
[data-testid="stHeader"] { background: rgba(0,0,0,0); }
h1, h2, h3, p, label, span, div { color: #ffffff; }
.stTextInput input, .stTextArea textarea {
    background-color: #f5eee8 !important;
    color: #24150f !important;
}
.stButton button {
    background-color: #8b5a3c;
    color: white;
    border: 1px solid #d8b49a;
}
.stButton button:hover { background-color: #a87552; color: white; }
[data-testid="stDataFrame"] { color: #24150f; }
</style>
""", unsafe_allow_html=True)

st.title("🧬 CODONPRINT")
st.caption("Codon Usage-Based Organism Classifier | Basic ML Project")
st.write("Analyse DNA sequences using base composition and codon usage patterns.")

tab1, tab2, tab3 = st.tabs(["Single sequence", "Compare sequences", "FASTA file"])

with tab1:
    sequence = st.text_area("Enter DNA sequence", placeholder="Example: ATGGCCGCTGCAAAAGCTGCC", height=120)
    if st.button("Analyse sequence"):
        cleaned = clean_sequence(sequence)
        if not validate_dna(cleaned):
            st.error("Invalid DNA sequence. Please use only A, T, G and C.")
        else:
            result = analyse_sequence(cleaned)
            st.subheader("Analysis results")
            c1, c2, c3 = st.columns(3)
            c1.metric("Sequence length", result["length"])
            c2.metric("GC content", f'{result["gc_content"]:.2f}%')
            c3.metric("Total codons", result["total_codons"])
            st.write("**Base counts**", result["base_counts"])
            st.write("**Codon counts**", result["codon_counts"])
            st.write("**Codon usage (%)**", {k: round(v * 100, 2) for k, v in result["codon_usage"].items()})
            st.write("**Top codons (fingerprint)**", result["top_codons"])
            name, score = closest_reference(result["codon_usage"])
            st.info(f"Closest demo reference pattern: {name} (difference score: {score:.4f})")
            st.caption("Reference patterns are simplified demonstration values, not validated biological identification.")

with tab2:
    first = st.text_area("First DNA sequence", key="seq1", height=100)
    second = st.text_area("Second DNA sequence", key="seq2", height=100)
    if st.button("Compare sequences"):
        a, b = clean_sequence(first), clean_sequence(second)
        if not validate_dna(a) or not validate_dna(b):
            st.error("Both sequences must contain only A, T, G and C.")
        else:
            result = compare_sequences(a, b)
            st.write("**Shared codons:**", result["shared_codons"])
            st.write("**Average usage difference:**", round(result["average_difference"], 4))
            st.caption("A lower difference means the codon usage patterns are more similar.")

with tab3:
    uploaded = st.file_uploader("Upload a FASTA file", type=["fasta", "fa", "fna", "txt"])
    if uploaded is not None:
        try:
            content = uploaded.getvalue().decode("utf-8")
            records = read_fasta(content)
            if not records:
                st.warning("No FASTA sequences were found.")
            for name, sequence in records:
                cleaned = clean_sequence(sequence)
                st.subheader(name)
                if not validate_dna(cleaned):
                    st.error("This record contains invalid DNA characters.")
                    continue
                result = analyse_sequence(cleaned)
                st.write(f'Length: {result["length"]} | GC content: {result["gc_content"]:.2f}% | Codons: {result["total_codons"]}')
                st.write("Top codons:", result["top_codons"])
        except Exception as error:
            st.error(f"Could not read this FASTA file: {error}")

st.divider()
st.caption("CODONPRINT | Group 18")
