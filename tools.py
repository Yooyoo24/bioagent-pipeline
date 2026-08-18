import requests
from langchain.tools import tool


@tool
def fetch_pdb_summary(pdb_id: str) -> str:
    """Fetches structure metadata and title for a given 4-character PDB ID (e.g. '1TUP')."""
    pdb_id = pdb_id.strip().upper()
    url = f"https://data.rcsb.org/rest/v1/core/entry/{pdb_id}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            title = data.get("struct", {}).get("title", "Unknown Title")
            deposit_date = data.get("rcsb_accession_info", {}).get("deposit_date", "N/A")
            method = data.get("exptl", [{}])[0].get("method", "N/A")
            return f"PDB ID: {pdb_id}\nTitle: {title}\nExperimental Method: {method}\nDeposit Date: {deposit_date}"
        return f"Error: PDB ID '{pdb_id}' not found."
    except Exception as e:
        return f"Failed to connect to RCSB PDB API: {str(e)}"


@tool
def fetch_uniprot_sequence(uniprot_id: str) -> str:
    """Fetches protein length, organism, and sequence preview for a given UniProt ID (e.g. 'P04637')."""
    uniprot_id = uniprot_id.strip().upper()
    url = f"https://rest.uniprot.org/uniprotkb/{uniprot_id}.json"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            protein_name = data.get("proteinDescription", {}).get("recommendedName", {}).get("fullName", {}).get(
                "value", "N/A")
            organism = data.get("organism", {}).get("scientificName", "N/A")
            seq = data.get("sequence", {}).get("value", "")
            return f"UniProt ID: {uniprot_id}\nName: {protein_name}\nOrganism: {organism}\nLength: {len(seq)} AA\nSequence Preview: {seq[:50]}..."
        return f"Error: UniProt ID '{uniprot_id}' not found."
    except Exception as e:
        return f"Failed to connect to UniProt API: {str(e)}"


@tool
def search_pubmed_abstracts(query: str) -> str:
    """Searches PubMed literature for a keyword query and returns the top relevant article titles."""
    url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {"db": "pubmed", "term": query, "retmode": "json", "retmax": 3}
    try:
        res = requests.get(url, params=params, timeout=10).json()
        id_list = res.get("esearchresult", {}).get("idlist", [])
        if not id_list:
            return f"No PubMed articles found for query: {query}"

        sum_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
        sum_params = {"db": "pubmed", "id": ",".join(id_list), "retmode": "json"}
        sum_res = requests.get(sum_url, params=sum_params, timeout=10).json()

        results = []
        for pmid in id_list:
            title = sum_res.get("result", {}).get(pmid, {}).get("title", "No Title")
            results.append(f"- [PMID: {pmid}] {title}")
        return f"Top PubMed Literature for '{query}':\n" + "\n".join(results)
    except Exception as e:
        return f"Failed to search PubMed: {str(e)}"