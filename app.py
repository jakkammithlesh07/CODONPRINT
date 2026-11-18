import streamlit as st
from codonprint import analyse_sequence, compare_two_sequences, read_fasta_file

st.set_page_config(page_title="CODONPRINT", page_icon="🧬")
st.title("🧬 CODONPRINT")
st.subheader("Codon Usage-Based Organism Classifier")
st.write("Group 18 | Jakkam Mithlesh (SE25UBIT036) | Ch. Nirav (SE25UBIT031)")
st.info(
    "This is an educational project. The small reference patterns are examples "
    "and are not a validated database for confirming an organism."
)

tab1, tab2, tab3 = st.tabs(["Analyse DNA", "Compare DNA", "FASTA file"])

with tab1:
    dna = st.text_area("Enter DNA sequence (A, T, G and C only)")
    if st.button("Analyse DNA"):
        result = analyse_sequence(dna)
        if result is None:
            st.error("Invalid sequence. Please enter only A, T, G and C.")
        else:
            st.success("DNA sequence is valid")
            col1, col2 = st.columns(2)
            col1.metric("Sequence length", result["length"])
            col2.metric("GC content", str(round(result["gc"], 2)) + "%")
            st.write("**Base counts**")
            st.write(result["bases"])
            st.write("**Codons**")
            st.write(result["codons"])
            st.write("**Codon counts**")
            st.write(result["counts"])
            st.write("**Codon usage (%)**")
            for codon in result["usage"]:
                st.write(codon, ":", round(result["usage"][codon] * 100, 2), "%")
            st.write("**Codon fingerprint**")
            st.success(result["fingerprint"])
            st.write("**Reference comparison (lower score means closer)**")
            st.write(result["scores"])
            st.metric("Closest demonstration pattern", result["closest"])
            st.metric("Basic KNN demo prediction", result["ml_prediction"])
            st.write("KNN votes:", result["ml_votes"])
            if result["leftover"] > 0:
                st.warning(str(result["leftover"]) + " leftover base(s) were not included in codons.")

with tab2:
    first = st.text_area("First DNA sequence")
    second = st.text_area("Second DNA sequence")
    if st.button("Compare DNA sequences"):
        result = compare_two_sequences(first, second)
        if result is None:
            st.error("Please enter two valid DNA sequences.")
        elif result["difference"] is None:
            st.warning("No shared complete codons were found.")
        else:
            st.write("Shared codons:", result["shared"])
            st.metric("Average usage difference", round(result["difference"], 4))

with tab3:
    uploaded_file = st.file_uploader("Choose a FASTA file", type=["fasta", "fa", "fna", "txt"])
    if uploaded_file is not None:
        # Save the uploaded file temporarily so the same FASTA reader can be used.
        temporary_name = "uploaded_sequences.fasta"
        with open(temporary_name, "wb") as file:
            file.write(uploaded_file.getvalue())

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
                        st.write("Closest demonstration pattern:", result["closest"])
        except Exception as error:
            st.error("Could not read this FASTA file: " + str(error))

st.caption("CODONPRINT | Group 18 | Codon Usage Analysis")
