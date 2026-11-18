import streamlit as st
import pandas as pd
from codonprint import analyse_sequence, compare_two_sequences, read_fasta_file

# ---------------------------------------------------------
# CODONPRINT | Streamlit interface
# The analysis functions remain in codonprint.py.
# ---------------------------------------------------------

st.set_page_config(
    page_title="CODONPRINT | Codon Usage Analysis",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# White and blue visual theme
st.markdown("""
<style>
    :root {
        --blue: #1769aa;
        --deep-blue: #123b63;
        --pale-blue: #edf6ff;
        --line: #d8e6f3;
        --ink: #18324b;
        --muted: #61758a;
    }

    .stApp {
        background: #f7faff;
        color: var(--ink);
    }

    [data-testid="stHeader"] {
        background: rgba(247, 250, 255, 0.92);
    }

    [data-testid="stSidebar"] {
        background: #ffffff;
        border-right: 1px solid var(--line);
    }

    [data-testid="stSidebar"] * {
        color: var(--ink);
    }

    .block-container {
        max-width: 1240px;
        padding-top: 2rem;
        padding-bottom: 2.5rem;
    }

    h1, h2, h3 {
        color: var(--deep-blue) !important;
        letter-spacing: -0.02em;
    }

    p, label, li {
        color: var(--ink);
    }

    .hero {
        background: linear-gradient(115deg, #ffffff 0%, #edf6ff 100%);
        border: 1px solid #d7e8f8;
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 22px;
    }

    .eyebrow {
        color: #1769aa;
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.13em;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .hero-title {
        color: #123b63;
        font-size: clamp(2rem, 4vw, 3.1rem);
        font-weight: 800;
        line-height: 1.08;
        margin: 0;
    }

    .hero-subtitle {
        color: #526d86;
        font-size: 1.02rem;
        margin-top: 10px;
        margin-bottom: 14px;
    }

    .hero-meta {
        color: #61758a;
        font-size: 0.86rem;
    }

    .section-kicker {
        color: #1769aa;
        font-size: 0.76rem;
        font-weight: 800;
        letter-spacing: 0.11em;
        text-transform: uppercase;
        margin-bottom: 4px;
    }

    .info-card {
        background: #ffffff;
        border: 1px solid #dce8f3;
        border-radius: 14px;
        padding: 16px 18px;
        min-height: 100px;
    }

    .info-card-title {
        color: #1769aa;
        font-size: 0.8rem;
        font-weight: 750;
        margin-bottom: 6px;
    }

    .info-card-text {
        color: #526d86;
        font-size: 0.91rem;
        line-height: 1.45;
    }

    .stButton > button, .stDownloadButton > button {
        background: #1769aa;
        color: #ffffff;
        border: 1px solid #1769aa;
        border-radius: 9px;
        font-weight: 650;
        min-height: 2.65rem;
        transition: all 0.15s ease;
    }

    .stButton > button:hover, .stDownloadButton > button:hover {
        background: #12558b;
        border-color: #12558b;
        color: #ffffff;
    }

    .stTextArea textarea, .stTextInput input {
        background: #ffffff;
        border: 1px solid #cbdbea;
        border-radius: 9px;
        color: #18324b;
    }

    [data-testid="stMetric"] {
        background: #ffffff;
        border: 1px solid #dce8f3;
        border-radius: 13px;
        padding: 14px 16px;
    }

    [data-testid="stMetricLabel"] {
        color: #61758a;
    }

    [data-testid="stMetricValue"] {
        color: #123b63;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #d8e6f3;
    }

    .stTabs [data-baseweb="tab"] {
        background: #ffffff;
        border: 1px solid #d8e6f3;
        border-radius: 9px 9px 0 0;
        color: #35536e;
        padding: 10px 16px;
    }

    .stTabs [aria-selected="true"] {
        background: #eaf4ff !important;
        color: #12558b !important;
        border-bottom: 2px solid #1769aa !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    .footer {
        border-top: 1px solid #d8e6f3;
        margin-top: 30px;
        padding-top: 16px;
        color: #71859a;
        font-size: 0.82rem;
        text-align: center;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)


def show_sequence_summary(result):
    """Display the main sequence statistics."""
    first, second, third, fourth = st.columns(4)
    first.metric("Sequence length", result["length"], "bases")
    second.metric("GC content", str(round(result["gc"], 2)) + "%")
    third.metric("Complete codons", len(result["codons"]))
    fourth.metric("Unused bases", result["leftover"])


def make_analysis_report(result):
    """Create a plain-text report for download."""
    report = "CODONPRINT | CODON USAGE ANALYSIS\n"
    report += "=" * 42 + "\n"
    report += "Sequence length: " + str(result["length"]) + " bases\n"
    report += "GC content: " + str(round(result["gc"], 2)) + "%\n"
    report += "Base counts: " + str(result["bases"]) + "\n"
    report += "Codon counts: " + str(result["counts"]) + "\n"
    report += "Codon fingerprint: " + result["fingerprint"] + "\n"
    report += "Closest demonstration pattern: " + result["closest"] + "\n"
    report += "KNN demo prediction: " + result["ml_prediction"] + "\n"
    report += "KNN demo votes: " + str(result["ml_votes"]) + "\n"
    report += "\nIMPORTANT: The reference patterns and training rows are small "
    report += "demonstration examples, not a validated scientific database.\n"
    return report


# Sidebar
with st.sidebar:
    st.markdown("## 🧬 CODONPRINT")
    st.caption("DNA sequence analysis")
    st.divider()
    st.markdown("**PROJECT TEAM**")
    st.write("Jakkam Mithlesh")
    st.caption("SE25UBIT036")
    st.write("Ch. Nirav")
    st.caption("SE25UBIT031")
    st.divider()
    st.markdown("**ANALYSIS TOOLS**")
    st.write("• DNA sequence analysis")
    st.write("• Codon usage and GC content")
    st.write("• Reference-pattern comparison")
    st.write("• Basic KNN demonstration")
    st.write("• Two-sequence comparison")
    st.write("• FASTA file analysis")
    st.divider()
    st.caption("Built with Python and Streamlit")


# Hero header
st.markdown("""
<div class="hero">
    <div class="eyebrow">Group 18 · Biotechnology project</div>
    <div class="hero-title">🧬 CODONPRINT</div>
    <div class="hero-subtitle">Codon Usage-Based Organism Classifier</div>
    <div class="hero-meta">Explore DNA composition, codon patterns and sequence differences in one workspace.</div>
</div>
""", unsafe_allow_html=True)

# Feature overview
card1, card2, card3 = st.columns(3)
with card1:
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">01 · SEQUENCE ANALYSIS</div>
        <div class="info-card-text">Check DNA bases, GC percentage, codon counts and codon usage.</div>
    </div>
    """, unsafe_allow_html=True)
with card2:
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">02 · COMPARISON</div>
        <div class="info-card-text">Compare two sequences using their shared codons and usage difference.</div>
    </div>
    """, unsafe_allow_html=True)
with card3:
    st.markdown("""
    <div class="info-card">
        <div class="info-card-title">03 · FASTA WORKSPACE</div>
        <div class="info-card-text">Upload a FASTA file and inspect each DNA record separately.</div>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.info(
    "Educational project note: reference patterns and KNN training rows are "
    "small demonstration examples. Results are not validated organism "
    "identifications and should not be used as scientific confirmation."
)

# Main navigation
analyse_tab, compare_tab, fasta_tab = st.tabs([
    "🧬  Analyse DNA",
    "↔️  Compare sequences",
    "📁  FASTA analysis"
])


# ---------------------------------------------------------
# TAB 1: DNA ANALYSIS
# ---------------------------------------------------------
with analyse_tab:
    st.markdown('<div class="section-kicker">DNA WORKSPACE</div>', unsafe_allow_html=True)
    st.header("Analyse a DNA sequence")
    st.write("Paste a DNA sequence below. Only the bases A, T, G and C are accepted.")

    with st.container():
        dna = st.text_area(
            "DNA sequence",
            placeholder="Example: ATGGCCGCTGCAAAAGCTGCC",
            height=145,
            key="analysis_dna"
        )
        analyse_clicked = st.button(
            "Analyse sequence  →",
            key="analyse_button",
            use_container_width=True
        )

    if analyse_clicked:
        result = analyse_sequence(dna)

        if result is None:
            st.error("Sequence not valid. Enter a non-empty sequence containing only A, T, G and C.")
        elif len(result["codons"]) == 0:
            st.warning("The DNA sequence is valid, but it needs at least 3 bases to form one complete codon.")
        else:
            st.success("Sequence analysis completed.")
            show_sequence_summary(result)

            st.markdown("### Sequence composition")
            base_col, codon_col = st.columns(2)

            with base_col:
                st.markdown("**Base composition**")
                base_data = pd.DataFrame({
                    "DNA base": list(result["bases"].keys()),
                    "Count": list(result["bases"].values())
                }).set_index("DNA base")
                st.bar_chart(base_data, use_container_width=True)

            with codon_col:
                st.markdown("**Codon usage (%)**")
                usage_percent = {}
                for codon in result["usage"]:
                    usage_percent[codon] = round(result["usage"][codon] * 100, 2)
                usage_data = pd.DataFrame({
                    "Codon": list(usage_percent.keys()),
                    "Usage (%)": list(usage_percent.values())
                }).set_index("Codon")
                st.bar_chart(usage_data, use_container_width=True)

            st.markdown("### Codon analysis")
            st.markdown(
                '<div class="info-card"><div class="info-card-title">CODON FINGERPRINT</div>'
                '<div class="info-card-text">' + result["fingerprint"] +
                '</div></div>',
                unsafe_allow_html=True
            )

            with st.expander("View base counts, codon counts and usage table"):
                detail_left, detail_right = st.columns(2)
                with detail_left:
                    st.markdown("**Base counts**")
                    st.json(result["bases"])
                    st.markdown("**Codon counts**")
                    st.json(result["counts"])
                with detail_right:
                    st.markdown("**Codon usage (%)**")
                    usage_table = []
                    for codon in result["usage"]:
                        usage_table.append({
                            "Codon": codon,
                            "Count": result["counts"][codon],
                            "Usage (%)": round(result["usage"][codon] * 100, 2)
                        })
                    st.dataframe(usage_table, hide_index=True, use_container_width=True)

            st.markdown("### Demonstration classification")
            class_left, class_right = st.columns(2)
            with class_left:
                st.metric("Closest reference pattern", result["closest"])
            with class_right:
                st.metric("Basic KNN demo prediction", result["ml_prediction"])

            vote_col, score_col = st.columns(2)
            with vote_col:
                st.markdown("**KNN votes**")
                st.json(result["ml_votes"])
            with score_col:
                st.markdown("**Reference-pattern differences**")
                score_rows = []
                for organism in result["scores"]:
                    score = result["scores"][organism]
                    if score is not None:
                        score_rows.append({
                            "Reference pattern": organism,
                            "Average difference": round(score, 4)
                        })
                if score_rows:
                    st.dataframe(score_rows, hide_index=True, use_container_width=True)
                else:
                    st.caption("No matching reference codons were found.")

            if result["leftover"] > 0:
                st.warning(
                    str(result["leftover"]) +
                    " leftover base(s) were not included in complete codons."
                )

            st.download_button(
                "⬇ Download analysis report",
                data=make_analysis_report(result),
                file_name="codonprint_analysis.txt",
                mime="text/plain",
                use_container_width=True
            )


# ---------------------------------------------------------
# TAB 2: COMPARE TWO SEQUENCES
# ---------------------------------------------------------
with compare_tab:
    st.markdown('<div class="section-kicker">COMPARISON WORKSPACE</div>', unsafe_allow_html=True)
    st.header("Compare two DNA sequences")
    st.write("Enter two valid DNA sequences to compare their shared codons and average usage difference.")

    first_col, second_col = st.columns(2)
    with first_col:
        first = st.text_area(
            "Sequence 1",
            placeholder="Enter first DNA sequence",
            height=150,
            key="first_sequence"
        )
    with second_col:
        second = st.text_area(
            "Sequence 2",
            placeholder="Enter second DNA sequence",
            height=150,
            key="second_sequence"
        )

    if st.button("Compare sequences  →", key="compare_button", use_container_width=True):
        comparison = compare_two_sequences(first, second)

        if comparison is None:
            st.error("Please enter two valid DNA sequences using A, T, G and C only.")
        elif comparison["difference"] is None:
            st.warning("No shared complete codons were found in these sequences.")
        else:
            st.success("Sequence comparison completed.")
            metric_a, metric_b = st.columns(2)
            metric_a.metric("Shared codons", len(comparison["shared"]))
            metric_b.metric("Average usage difference", round(comparison["difference"], 4))
            st.markdown("**Codons present in both sequences**")
            st.write(", ".join(comparison["shared"]))
            st.caption("A smaller average difference indicates more similar usage among the shared codons.")


# ---------------------------------------------------------
# TAB 3: FASTA FILE ANALYSIS
# ---------------------------------------------------------
with fasta_tab:
    st.markdown('<div class="section-kicker">MULTI-SEQUENCE WORKSPACE</div>', unsafe_allow_html=True)
    st.header("Analyse a FASTA file")
    st.write("Upload a FASTA file containing one or more DNA sequences.")

    uploaded_file = st.file_uploader(
        "Choose a FASTA file",
        type=["fasta", "fa", "fna", "txt"],
        help="Supported file types: .fasta, .fa, .fna and .txt"
    )

    if uploaded_file is not None:
        temporary_name = "uploaded_sequences.fasta"
        with open(temporary_name, "wb") as file:
            file.write(uploaded_file.getvalue())

        try:
            records = read_fasta_file(temporary_name)

            if len(records) == 0:
                st.warning("No FASTA records were found. Each sequence should begin with a header starting with >.")
            else:
                st.success(str(len(records)) + " sequence(s) found in the uploaded file.")

                for name, sequence in records:
                    with st.expander("🧬 " + name, expanded=True):
                        result = analyse_sequence(sequence)

                        if result is None:
                            st.error("This record contains invalid DNA characters. Only A, T, G and C are accepted.")
                        elif len(result["codons"]) == 0:
                            st.warning("This record has no complete codons to analyse.")
                        else:
                            show_sequence_summary(result)
                            st.markdown("**Codon fingerprint:** " + result["fingerprint"])
                            st.markdown("**Closest demonstration pattern:** " + result["closest"])
                            if result["leftover"] > 0:
                                st.caption(
                                    str(result["leftover"]) +
                                    " leftover base(s) were not included in complete codons."
                                )

        except Exception:
            st.error("The FASTA file could not be read. Please check its format and try again.")


# Footer
st.markdown("""
<div class="footer">
    <strong>CODONPRINT</strong> &nbsp;|&nbsp; Group 18 &nbsp;|&nbsp; Codon Usage Analysis
    <br><span>Jakkam Mithlesh · Ch. Nirav</span>
</div>
""", unsafe_allow_html=True)
