import re
import requests
from requests.adapters import HTTPAdapter, Retry
re_next_link = re.compile(r'<(.+)>; rel="next"')
retries = Retry(total=5, backoff_factor=0.25, status_forcelist=[500, 502, 503, 504])
session = requests.Session()
session.mount("https://", HTTPAdapter(max_retries=retries))

def get_next_link(headers):
    if "Link" in headers:
        match = re_next_link.match(headers["Link"])
        if match:
            return match.group(1)

def get_batch(batch_url):
    while batch_url:
        response = session.get(batch_url)
        response.raise_for_status()
        total = response.headers["x-total-results"]
        yield response, total
        batch_url = get_next_link(response.headers)

url = 'https://rest.uniprot.org/uniprotkb/search?fields=accession%2Creviewed%2Cid%2Cprotein_name%2Cgene_names%2Corganism_name%2Clength%2Cxref_proteomes%2Cvirus_hosts%2Clineage_ids%2Clineage%2Corganism_id%2Cgene_primary%2Cgene_orf%2Csequence%2Cmass%2Ccc_rna_editing%2Cabsorption%2Cft_act_site%2Cft_binding%2Ccc_catalytic_activity%2Ccc_cofactor%2Cft_dna_bind%2Cph_dependence%2Ccc_pathway%2Ckinetics%2Ccc_function%2Ccc_activity_regulation%2Cec%2Credox_potential%2Crhea%2Cft_site%2Ctemp_dependence%2Ccc_interaction%2Ccc_subunit%2Cgo_c%2Cgo_p%2Cgo%2Cgo_f%2Cgo_id%2Ccc_subcellular_location%2Cft_intramem%2Cft_transmem%2Cft_topo_dom%2Cstructure_3d%2Clit_pubmed_id%2Cft_coiled%2Cft_compbias%2Ccc_domain%2Cft_domain%2Cft_motif%2Cprotein_families%2Cft_region%2Cft_repeat%2Cft_zn_fing%2Cxref_alphafolddb%2Cxref_pdb%2Cxref_smr%2Cxref_bmrb%2Cxref_pdbsum%2Cxref_pcddb%2Cxref_sasbdb%2Cxref_eggnog%2Cxref_orthodb%2Cxref_brenda%2Cxref_unipathway%2Cxref_interpro%2Cxref_pfam%2Cxref_prosite%2Cannotation_score&format=tsv&query=%28%28taxonomy_id%3A10239%29%20NOT%20%28taxonomy_id%3A131567%29%29%20AND%20%28reviewed%3Atrue%29&size=500'
progress = 0
with open('data/0_reviewed_Virus_Uniprot.tsv', 'w') as f:
    for batch, total in get_batch(url):
        lines = batch.text.splitlines()
        if not progress:
            print(lines[0], file=f)
        for line in lines[1:]:
            print(line, file=f)
        progress += len(lines[1:])
        print(f'{progress} / {total}')
