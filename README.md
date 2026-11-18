# MyoGenomics

**A computational genomics and proteomics platform focused on muscle development.**

MyoGenomics is a Python-based application designed to support the exploration and analysis of genomic and proteomic data, with a particular focus on biological processes related to muscle development.

The platform aims to provide an integrated workflow for retrieving genomic information, processing DNA sequences, translating nucleotide sequences into amino acid sequences, and visualizing biological structures in 3D.

## Key Features

- **Genomic data retrieval:** Import genomic information from external biological databases and APIs without requiring permanent local storage of large genomic files.
- **Data normalization:** Process and standardize retrieved genomic data for downstream analysis.
- **DNA sequence extraction:** Identify and isolate specific DNA sequences of interest.
- **Protein translation:** Translate nucleotide sequences into their corresponding amino acid sequences.
- **3D molecular visualization:** Visualize DNA double helices and protein structures, including tertiary structures.
- **Muscle development focus:** Provide a computational framework for exploring genomic and proteomic information relevant to muscle biology.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming language | Python |
| Web application | Streamlit |
| Bioinformatics | Biopython |
| Data processing | Pandas, NumPy |
| API communication | Requests |
| 3D visualization | stmol, py3Dmol |
| Data visualization | Plotly |

## External Data Sources

The application is designed to integrate with biological data resources, including:

- [Ensembl](https://www.ensembl.org/) — genomic information and sequence data.
- [UniProt](https://www.uniprot.org/) — protein sequences and functional annotations.
- [AlphaFold Protein Structure Database](https://alphafold.ebi.ac.uk/) — predicted protein structures.

## Project Structure

```text
mine_idea/
│
├── app.py
├── requirements.txt
├── README.md
│
└── core/
    ├── __init__.py
    ├── importer.py
    ├── api_client.py
    └── visualizer.py
```

## Installation

Clone the repository:

```bash
git clone https://github.com/PanagiwthsBUG/myogenomics-app.git
cd myogenomics-app
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## Run the Application

Start the Streamlit application:

```bash
streamlit run app.py
```

## Project Goals

MyoGenomics aims to bring together computational genomics, protein analysis, and molecular visualization in an accessible interactive environment.

Its broader objective is to facilitate the exploration of biological information associated with muscle development and provide a foundation for future bioinformatics research and analysis.

## License

License information will be added in a future version.