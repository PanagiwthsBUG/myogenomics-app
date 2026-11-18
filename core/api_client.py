import requests
from Bio.SeqUtils import gc_fraction
from Bio.Seq import Seq

MUSCLE_GENES = {
    "MSTN (Μυοστατίνη - Αναστολέας μυϊκής ανάπτυξης)": "MSTN",
    "ACTN3 (Αλφα-ακτινίνη-3 - Πρωτεΐνη ταχείας συστολής)": "ACTN3",
    "MYOD1 (Μυογενής παράγοντας διαφοροποίησης 1)": "MYOD1",
    "IGF1 (Ινσουλινόμορφος αυξητικός παράγοντας 1)": "IGF1"
}

def fetch_gene_from_ensembl(gene_symbol: str) -> dict:
    """Βήμα 1: Ανάκτηση DNA αλληλουχίας από το Ensembl REST API."""
    base_url = "https://" + "rest." + "ensembl.org"
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    
    lookup_url = f"{base_url}/lookup/symbol/homo_sapiens/{gene_symbol}"
    res = requests.get(lookup_url, params={"content-type": "application/json"}, headers=headers, timeout=15)
    res.raise_for_status()
    
    gene_info = res.json()
    ensembl_id = gene_info["id"]

    seq_url = f"{base_url}/sequence/id/{ensembl_id}"
    seq_res = requests.get(seq_url, params={"content-type": "application/json"}, headers=headers, timeout=15)
    seq_res.raise_for_status()
    
    seq_data = seq_res.json()
    clean_seq = seq_data["seq"].upper()

    return {
        "id": f"{gene_symbol} ({ensembl_id})",
        "description": gene_info.get("description", "Human Gene"),
        "sequence": clean_seq,
        "length": len(clean_seq),
        "gc_content": round(gc_fraction(Seq(clean_seq)) * 100, 2),
        "source": "Ensembl REST API"
    }

def fetch_uniprot_id(gene_symbol: str) -> dict:
    """Βήμα 2: Εύρεση του UniProt ID και πληροφοριών πρωτεΐνης."""
    base_url = "https://" + "rest." + "uniprot.org/uniprotkb/search"
    params = {
        "query": f"gene_exact:{gene_symbol} AND organism_id:9606 AND reviewed:true",
        "format": "json",
        "size": 1
    }
    headers = {"Accept": "application/json"}
    
    res = requests.get(base_url, params=params, headers=headers, timeout=15)
    res.raise_for_status()
    results = res.json().get("results", [])
    
    if not results:
        return None
        
    entry = next(iter(results))
    uniprot_id = entry["primaryAccession"]
    protein_name = entry.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get("value", gene_symbol)
    sequence = entry.get("sequence", {}).get("value", "")
    
    return {
        "uniprot_id": uniprot_id,
        "protein_name": protein_name,
        "aa_sequence": sequence
    }

def fetch_alphafold_pdb(uniprot_id: str) -> str:
    """Βήμα 3: Λήψη του 3D μοντέλου (.pdb) απευθείας από το AlphaFold DB API."""
    base_url = "https://" + "alphafold." + "ebi.ac.uk/files"
    for version in ["v4", "v6", "v3"]:
        pdb_url = f"{base_url}/AF-{uniprot_id}-F1-model_{version}.pdb"
        res = requests.get(pdb_url, timeout=15)
        if res.status_code == 200 and res.text.strip():
            return res.text
    return None
