import io
import gzip
from Bio import SeqIO
from Bio.SeqUtils import gc_fraction

def parse_uploaded_file(uploaded_file) -> dict:
    """
    Διαβάζει ένα αρχείο (FASTA, FASTQ ή συμπιεσμένο .gz) απευθείας στη RAM
    και επιστρέφει ένα κανονικοποιημένο dictionary.
    """
    filename = uploaded_file.name.lower()
    raw_bytes = uploaded_file.read()
    
    # Αν είναι συμπιεσμένο (.gz), αποσυμπίεση μόνο στη RAM
    if filename.endswith(".gz"):
        text_stream = io.TextIOWrapper(gzip.GzipFile(fileobj=io.BytesIO(raw_bytes)), encoding="utf-8")
        clean_name = filename[:-3]
    else:
        text_stream = io.StringIO(raw_bytes.decode("utf-8"))
        clean_name = filename

    # Εντοπισμός μορφής αρχείου
    if clean_name.endswith((".fasta", ".fa", ".fna")):
        file_format = "fasta"
    elif clean_name.endswith((".fastq", ".fq")):
        file_format = "fastq"
    else:
        raise ValueError("Μη υποστηριζόμενη μορφή αρχείου. Χρησιμοποιήστε FASTA, FASTQ ή .gz.")

    # Ανάγνωση της πρώτης εγγραφής (streaming, χωρίς φόρτωση όλου του αρχείου)
    record = next(SeqIO.parse(text_stream, file_format))
    clean_seq = str(record.seq).upper().strip()

    # Κανονικοποιημένη έξοδος
    return {
        "id": record.id,
        "description": record.description,
        "sequence": clean_seq,
        "length": len(clean_seq),
        "gc_content": round(gc_fraction(record.seq) * 100, 2),
        "source": f"Local File ({file_format.upper()})"
    }
