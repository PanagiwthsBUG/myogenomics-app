import streamlit as st
from Bio.Seq import Seq
import streamlit.components.v1 as components

from core.importer import parse_uploaded_file
from core.api_client import MUSCLE_GENES, fetch_gene_from_ensembl, fetch_uniprot_id, fetch_alphafold_pdb
from core.visualizer import create_dna_double_helix, create_protein_3d_view

st.set_page_config(page_title="MyoGenomics 3D Explorer", layout="wide")

st.title("🧬 MyoGenomics: Ανάλυση Γονιδιώματος & 3D Πρωτεομική")
st.markdown("Εισαγωγή γονιδιωματικών δεδομένων, απομόνωση αλληλουχιών και τρισδιάστατη οπτικοποίηση πρωτεϊνών μυϊκής ανάπτυξης.")

# --- ΠΛΕΥΡΙΚΗ ΜΠΑΡΑ (SIDEBAR): ΕΙΣΑΓΩΓΗ ΔΕΔΟΜΕΝΩΝ ---
st.sidebar.header("1. Πηγή Δεδομένων")
data_source = st.sidebar.radio("Επιλέξτε τρόπο εισαγωγής:", ["Αναζήτηση μέσω APIs (Μυϊκή Ανάπτυξη)", "Ανέβασμα Τοπικού Αρχείου (FASTA/FASTQ)"])

normalized_data = None
selected_gene_symbol = None

if data_source == "Αναζήτηση μέσω APIs (Μυϊκή Ανάπτυξη)":
    gene_choice = st.sidebar.selectbox("Επιλέξτε Γονίδιο Στόχο:", list(MUSCLE_GENES.keys()))
    selected_gene_symbol = MUSCLE_GENES[gene_choice]
    
    if st.sidebar.button("Φόρτωση από Ensembl API"):
        with st.spinner(f"Ανάκτηση δεδομένων για το γονίδιο {selected_gene_symbol}..."):
            try:
                normalized_data = fetch_gene_from_ensembl(selected_gene_symbol)
                st.session_state["data"] = normalized_data
                st.session_state["gene_symbol"] = selected_gene_symbol
            except Exception as e:
                st.sidebar.error(f"Σφάλμα API: {e}")

else:
    uploaded_file = st.sidebar.file_uploader("Ανεβάστε αρχείο (.fasta, .fastq, .gz)", type=["fasta", "fa", "fastq", "fq", "gz"])
    if uploaded_file is not None:
        with st.spinner("Κανονικοποίηση αρχείου στη μνήμη RAM..."):
            try:
                normalized_data = parse_uploaded_file(uploaded_file)
                st.session_state["data"] = normalized_data
                st.session_state["gene_symbol"] = None
            except Exception as e:
                st.sidebar.error(f"Σφάλμα ανάγνωσης: {e}")

# --- ΚΥΡΙΩΣ ΟΘΟΝΗ ---
if "data" in st.session_state:
    data = st.session_state["data"]
    
    # Εμφάνιση Κανονικοποιημένων Μεταδεδομένων
    st.subheader("2. Κανονικοποιημένα Δεδομένα Εισόδου (Normalized View)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Αναγνωριστικό (ID)", data["id"])
    col2.metric("Συνολικό Μήκος (bp)", f"{data['length']:,}")
    col3.metric("Περιεκτικότητα GC", f"{data['gc_content']}%")
    col4.metric("Πηγή", data["source"])

    # Απομόνωση Τμήματος Αλληλουχίας
    st.subheader("3. Απομόνωση Τμήματος Αλληλουχίας (Slicing)")
    max_len = data["length"]
    default_end = min(300, max_len)
    
    start_pos, end_pos = st.slider(
        "Επιλέξτε το εύρος νουκλεοτιδίων προς απομόνωση:",
        min_value=0, max_value=max_len, value=(0, default_end)
    )
    
    isolated_dna = data["sequence"][start_pos:end_pos]
    st.text_area("Απομονωμένη Αλληλουχία DNA (5' -> 3'):", isolated_dna, height=100)

    # Μεταγραφή & Μετάφραση σε Αμινοξέα
    dna_obj = Seq(isolated_dna)
    # Περικοπή ώστε το μήκος να είναι πολλαπλάσιο του 3 για καθαρή μετάφραση
    trim_len = len(dna_obj) - (len(dna_obj) % 3)
    mrna_seq = dna_obj[:trim_len].transcribe()
    protein_seq = dna_obj[:trim_len].translate()

    with st.expander("Προβολή Μεταγραφής (mRNA) & Μετάφρασης (Αμινοξέα)"):
        st.write("**mRNA Αλληλουχία:**")
        st.code(str(mrna_seq))
        st.write("**Αλυσίδα Αμινοξέων (1-letter code):**")
        st.code(str(protein_seq))

    # --- ΤΡΙΣΔΙΑΣΤΑΤΗ ΟΠΤΙΚΟΠΟΙΗΣΗ ---
    st.subheader("4. Τρισδιάστατη Οπτικοποίηση (3D Visualization)")
    tab1, tab2 = st.tabs(["🧬 3D Διπλή Έλικα DNA (Επιλεγμένο Τμήμα)", "🥩 3D Δομή Πρωτεΐνης (AlphaFold)"])

    with tab1:
        if len(isolated_dna) > 0:
            helix_fig = create_dna_double_helix(isolated_dna)
            st.plotly_chart(helix_fig, use_container_width=True)
        else:
            st.warning("Επιλέξτε ένα έγκυρο εύρος βάσεων.")

    with tab2:
        gene_sym = st.session_state.get("gene_symbol")
        if gene_sym:
            with st.spinner(f"Αναζήτηση πρωτεΐνης στο UniProt και λήψη 3D δομής από AlphaFold για {gene_sym}..."):
                uniprot_info = fetch_uniprot_id(gene_sym)
                if uniprot_info:
                    st.info(f"**Πρωτεΐνη:** {uniprot_info['protein_name']} | **UniProt ID:** `{uniprot_info['uniprot_id']}`")
                    pdb_data = fetch_alphafold_pdb(uniprot_info["uniprot_id"])
                    if pdb_data:
                        style_choice = st.selectbox("Στυλ Απεικόνισης 3D Μοντέλου:", ["cartoon", "stick", "sphere"])
                        viewer = create_protein_3d_view(pdb_data, style=style_choice)
                        components.html(viewer._make_html(), height=520, width=820)

                        
                        st.write("**Πλήρης Πρωτεϊνική Αλληλουχία (UniProt Reference):**")
                        st.code(uniprot_info["aa_sequence"])
                    else:
                        st.error("Δεν βρέθηκε διαθέσιμο 3D μοντέλο στο AlphaFold.")
                else:
                    st.warning("Δεν βρέθηκε αντιστοίχιση στο UniProt.")
        else:
            st.info("Για την 3D προβολή πρωτεΐνης μέσω AlphaFold, επιλέξτε ένα γονίδιο από τα APIs στην αριστερή μπάρα (ή στην επόμενη έκδοση θα προσθέσουμε αντιστοίχιση μέσω BLAST για άγνωστα αρχεία FASTA).")
