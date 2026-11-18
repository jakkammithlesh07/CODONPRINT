import streamlit as st
from codonprint import analyse_sequence, compare_two_sequences, read_fasta_file

st.set_page_config(page_title="CODONPRINT | DNA Analysis", page_icon="🧬", layout="wide")

# CSS is used only for the website's appearance.
st.markdown("""
<style>
.stApp { background:#F7F2F5; color:#332735; }
.block-container { max-width:1180px; padding-top:2rem; padding-bottom:2rem; }
h1,h2,h3,p,label { color:#332735; }
.hero { background:#FFFCFE; border:1px solid #E7DCE7; border-radius:20px; padding:34px; margin-bottom:22px; }
.eyebrow { color:#805C7E; font-size:12px; font-weight:700; letter-spacing:3px; }
.brand { color:#552653; font-size:44px; font-weight:800; letter-spacing:2px; margin-top:8px; }
.tagline { color:#765F75; font-size:18px; margin-top:5px; }
.hero-note { color:#665866; font-size:14px; margin-top:16px; }
.feature { background:#FFFCFE; border:1px solid #E7DCE7; border-radius:16px; padding:19px; min-height:116px; }
.feature-no { color:#805C7E; font-size:12px; font-weight:700; letter-spacing:2px; }
.feature-title { color:#552653; font-size:18px; font-weight:700; margin-top:8px; }
.feature-text { color:#766776; font-size:13px; margin-top:4px; }
.footer { color:#806D80; text-align:center; font-size:13px; padding:26px 0 5px; }
div[data-testid="stMetric"] { background:#FFFCFE; border:1px solid #E7DCE7; border-radius:13px; padding:14px; }
div[data-testid="stTextArea"] textarea { background:#FFFCFE !important; color:#332735 !important; border:1px solid #D9C9DA !important; border-radius:10px !important; }
div[data-testid="stFileUploader"] { background:#FFFCFE; border:1px dashed #CBB8CE; border-radius:13px; padding:14px; }
.stButton>button,.stDownloadButton>button { background:#552653; color:white; border:1px solid #552653; border-radius:10px; min-height:44px; font-weight:600; }
.stButton>button:hover,.stDownloadButton>button:hover { background:#70436E; color:white; border-color:#70436E; }
div[data-testid="stTabs"] button { color:#552653; font-weight:700; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="eyebrow">GROUP 18 / PYTHON + BIOPYTHON PROJECT</div>
  <div class="brand">CODONPRINT</div>
  <div class="tagline">Codon Usage-Based Organism Classifier</div>
  <div class="hero-note">A simple workspace to explore DNA sequences, codon patterns, sequence comparisons and a basic KNN demonstration.</div>
</div>
""", unsafe_allow_html=True)

a,b,c = st.columns(3)
with a:
    st.markdown('<div class="feature"><div class="feature-no">01 / ANALYSE</div><div class="feature-title">DNA composition</div><div class="feature-text">Base counts, GC content and codon usage</div></div>', unsafe_allow_html=True)
with b:
    st.markdown('<div class="feature"><div class="feature-no">02 / CLASSIFY</div><div class="feature-title">Basic KNN</div><div class="feature-text">Compare codon features with labelled demo examples</div></div>', unsafe_allow_html=True)
with c:
    st.markdown('<div class="feature"><div class="feature-no">03 / EXPLORE</div><div class="feature-title">Sequence tools</div><div class="feature-text">Compare sequences and read FASTA records</div></div>', unsafe_allow_html=True)

st.write("")
st.info("Reference profiles and KNN training rows are small demonstration examples, not verified biological data. Predictions demonstrate the method and do not confirm an organism.")

tab1,tab2,tab3 = st.tabs(["DNA ANALYSIS","SEQUENCE COMPARISON","FASTA READER"])

with tab1:
    st.markdown("## Analyse a DNA sequence")
    st.write("Enter a sequence using A, T, G and C.")
    dna = st.text_area("DNA sequence", placeholder="Example: ATGGCCGCTGCAAAAGCTGCC", height=120)
    if st.button("Analyse DNA", key="analyse_button", use_container_width=True):
        result = analyse_sequence(dna)
        if result is None:
            st.error("Invalid sequence. Please use only A, T, G and C.")
        elif len(result["codons"]) == 0:
            st.warning("Enter at least 3 DNA bases to make a complete codon.")
        else:
            st.success("Analysis completed.")
            st.markdown("### Sequence overview")
            x,y,z = st.columns(3)
            x.metric("Sequence length", str(result["length"])+" bases")
            y.metric("GC content", str(round(result["gc"],2))+"%")
            z.metric("Complete codons", len(result["codons"]))
            st.markdown("### Base composition")
            x,y,z,w = st.columns(4)
            x.metric("A",result["bases"]["A"]); y.metric("T",result["bases"]["T"])
            z.metric("G",result["bases"]["G"]); w.metric("C",result["bases"]["C"])
            st.markdown("### Codon usage")
            rows = []
            for codon in result["usage"]:
                rows.append({"Codon":codon,"Count":result["counts"][codon],"Usage (%)":round(result["usage"][codon]*100,2)})
            st.dataframe(rows,use_container_width=True,hide_index=True)
            st.bar_chart(rows,x="Codon",y="Usage (%)")
            st.markdown("### Codon fingerprint")
            st.success(result["fingerprint"])
            st.markdown("### Basic machine-learning result")
            x,y = st.columns(2)
            x.metric("Closest reference pattern",result["closest"])
            y.metric("KNN demonstration prediction",result["ml_prediction"])
            with st.expander("How did KNN vote?"):
                st.write("KNN votes:",result["ml_votes"])
                st.write("Nearest examples (distance, label):",result["ml_neighbours"])
                st.caption("K = 3: the three closest demonstration rows are used for majority voting.")
            with st.expander("See codon counts"):
                st.write(result["counts"])
            if result["leftover"] > 0:
                st.warning(str(result["leftover"])+" base(s) at the end do not form a complete codon.")
            report = "CODONPRINT / DNA ANALYSIS REPORT\n"
            report += "Sequence length: "+str(result["length"])+"\n"
            report += "Base counts: "+str(result["bases"])+"\n"
            report += "GC content: "+str(round(result["gc"],2))+"%\n"
            report += "Codon counts: "+str(result["counts"])+"\n"
            report += "Codon fingerprint: "+result["fingerprint"]+"\n"
            report += "Closest reference pattern: "+result["closest"]+"\n"
            report += "KNN demonstration prediction: "+result["ml_prediction"]+"\n"
            report += "Note: demonstration data only.\n"
            st.download_button("Download analysis report",report,file_name="codonprint_report.txt",use_container_width=True)

with tab2:
    st.markdown("## Compare two DNA sequences")
    st.write("Enter two sequences to compare their shared codons.")
    first = st.text_area("First sequence",key="first_sequence",placeholder="Enter the first DNA sequence")
    second = st.text_area("Second sequence",key="second_sequence",placeholder="Enter the second DNA sequence")
    if st.button("Compare sequences",key="compare_button",use_container_width=True):
        result = compare_two_sequences(first,second)
        if result is None:
            st.error("Both sequences must contain only A, T, G and C.")
        elif result["difference"] is None:
            st.warning("No shared complete codons were found.")
        else:
            st.success("Comparison completed.")
            st.metric("Average usage difference",round(result["difference"],4))
            st.write("Shared codons:",", ".join(result["shared"]))

with tab3:
    st.markdown("## Read a FASTA file")
    st.write("Upload a FASTA file containing one or more DNA sequences.")
    uploaded = st.file_uploader("Choose a FASTA file",type=["fasta","fa","fna","txt"])
    if uploaded is not None:
        file = open("uploaded_sequences.fasta","wb")
        file.write(uploaded.getvalue())
        file.close()
        records = read_fasta_file("uploaded_sequences.fasta")
        if len(records) == 0:
            st.warning("No sequences were found in this file.")
        else:
            st.success(str(len(records))+" sequence(s) found.")
            for name,sequence in records:
                with st.expander(name,expanded=True):
                    result = analyse_sequence(sequence)
                    if result is None:
                        st.error("This record contains an invalid DNA sequence.")
                    elif len(result["codons"]) == 0:
                        st.warning("This record has no complete codons.")
                    else:
                        x,y,z = st.columns(3)
                        x.metric("Length",str(result["length"])+" bases")
                        y.metric("GC content",str(round(result["gc"],2))+"%")
                        z.metric("Codons",len(result["codons"]))
                        st.write("Codon fingerprint:",result["fingerprint"])
                        st.write("Closest reference pattern:",result["closest"])
                        st.write("KNN demonstration prediction:",result["ml_prediction"])
                        if result["leftover"] > 0:
                            st.caption(str(result["leftover"])+" leftover base(s) were not used.")

st.markdown('<div class="footer">CODONPRINT | GROUP 18 | CODON USAGE ANALYSIS<br>Jakkam Mithlesh | Ch. Nirav</div>',unsafe_allow_html=True)
