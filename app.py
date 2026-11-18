import streamlit as st
from codonprint import analyse_sequence, compare_two_sequences, read_fasta_file

st.set_page_config(page_title="CODONPRINT", page_icon="🧬", layout="wide")
st.title("🧬 CODONPRINT")
st.subheader("Codon Usage-Based Organism Classifier")
st.write("A Python project using Biopython and basic machine learning.")
st.write("**Developed by:** Jakkam Mithlesh and Ch. Nirav  |  **Group 18**")
st.info("CODONPRINT analyses DNA sequences, calculates codon usage and demonstrates classification using a simple K-Nearest Neighbours (KNN) model.")
st.caption("The included training examples are demonstration data, not a validated biological dataset. Predictions are educational and should not be treated as confirmed organism identification.")

tab1, tab2, tab3 = st.tabs(["Analyse DNA", "Compare DNA", "FASTA file"])

with tab1:
    dna = st.text_area("Enter DNA sequence (A, T, G and C only)", height=130)
    if st.button("Analyse DNA", type="primary"):
        result = analyse_sequence(dna)
        if result is None:
            st.error("Invalid sequence. Please enter only A, T, G and C.")
        else:
            st.success("DNA sequence is valid")
            col1, col2, col3 = st.columns(3)
            col1.metric("Sequence length", result["length"])
            col2.metric("GC content", f"{result['gc']:.2f}%")
            col3.metric("Complete codons", len(result["codons"]))
            st.write("**Base counts**", result["bases"])
            st.write("**Codon counts**", result["counts"])
            st.write("**Codon usage (%)**")
            usage_rows = [{"Codon": codon, "Usage (%)": round(value * 100, 2)} for codon, value in result["usage"].items()]
            st.dataframe(usage_rows, use_container_width=True, hide_index=True)
            st.write("**Codon fingerprint**")
            st.success(result["fingerprint"])
            st.write("**Closest demonstration reference pattern**", result["closest"])
            st.write("**Basic ML result (KNN, K = 3)**")
            st.metric("Predicted demo label", result["ml_prediction"])
            st.write("KNN neighbour votes:", result["ml_votes"])
            if result["leftover"] > 0:
                st.warning(f"{result['leftover']} leftover base(s) were not included in complete codons.")

with tab2:
    first = st.text_area("First DNA sequence", key="first_sequence")
    second = st.text_area("Second DNA sequence", key="second_sequence")
    if st.button("Compare DNA sequences"):
        result = compare_two_sequences(first, second)
        if result is None:
            st.error("Please enter two valid DNA sequences.")
        elif result["difference"] is None:
            st.warning("No shared complete codons were found.")
        else:
            st.write("Shared codons:", ", ".join(result["shared"]))
            st.metric("Average usage difference", round(result["difference"], 4))

with tab3:
    uploaded_file = st.file_uploader("Choose a FASTA file", type=["fasta", "fa", "fna", "txt"])
    if uploaded_file is not None:
        import tempfile
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".fasta", delete=False) as temporary_file:
            temporary_file.write(uploaded_file.getvalue())
            temporary_name = temporary_file.name
        try:
            records = read_fasta_file(temporary_name)
            st.write("Sequences found:", len(records))
            for name, sequence in records:
                with st.expander(name):
                    result = analyse_sequence(sequence)
                    if result is None:
                        st.error("Invalid DNA sequence in this record.")
                    else:
                        st.write("Length:", result["length"])
                        st.write("GC content:", round(result["gc"], 2), "%")
                        st.write("Codon fingerprint:", result["fingerprint"])
                        st.write("KNN demo prediction:", result["ml_prediction"])
        except Exception as error:
            st.error("Could not read this FASTA file: " + str(error))
        finally:
            import os
            os.unlink(temporary_name)

st.caption("CODONPRINT | Group 18")
