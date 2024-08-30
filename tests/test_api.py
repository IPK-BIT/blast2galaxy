import blast2galaxy
import json

test_tool_id = 'toolshed.g2.bx.psu.edu/repos/bgruening/diamond/bg_diamond/2.0.15+galaxy0'
test_db_id = 'uniprot_swissprot_2023_03'


dna_seq = """>Vrs1_EU886278.1
ATGGACAAGCATCAGCTCTTTGATTCATCCAACGTGGACACGACTTTCTTCGCGGCCAATGGCACGGCGC
AGGGGGATACCAGCAAGCAGAGGGCGCGGCGCAGGCGGCGGAGGTCGGCGAGGTGCGGCGGAGGGGATGG
TGACGGTGGGGAGATGGACGGAGGAGGGGACCCCAAGAAGCGGCGGCTCACCGACGAGCAGGCCGAGATT
CTGGAGCTGAGCTTCCGGGAGGACCGCAAGCTGGAGACAGCCCGCAAGGTGTATCTGGCCGCCGAGCTCG
GGCTGGACCCCAAGCAGGTCGCCGTGTGGTTCCAGAACCGCCGCGCGCGCCACAAGAACAAGACGCTCGA
GGAGGAGTTCGCGAGGCTCAAGCACGCCCACGACGCCGCCATCCTCCACAAATGCCACCTCGAGAACGAG
CTGCTGAGGCTGAAGGAGAGACTGGGAGCGACTGAGCAGGAGGTGCGGCGCCTCAGGTCGGCAGCTGGGA
GCCACGGGGCATCTGTGGATGGCGGACACGCCGCTGGCGCCGTTGGCGTGTGCGGCGGGAGCCCGAGCTC
GTCCTTCTCGACGGGAACCTGCCAGCAGCAGCCGGGTTTCAGCGGGGCAGACGTGCTGGGGCGGGACGAT
GACCTGATGATGTGCGTCCCCGAGTGGTTTTTAGCATGA"""


protein_seq = """>sp|P62805|H4_HUMAN Histone H4 OS=Homo sapiens OX=9606 GN=H4C1 PE=1 SV=2
MSGRGKGGKGLGKGGAKRHRKVLRDNIQGITKPAIRRLARRGGVKRISGLIYEETRGVLK
VFLENVIRDAVTYTEHAKRKTVTAMDVVYALKRQGRTLYGFGG"""


def test_list_tools_api():
    tools = blast2galaxy.list_tools()
    #print(json.dumps(tools, indent=4))

    tool = False
    db = False

    if test_tool_id in tools:
        tool = True

    if test_db_id in tools[test_tool_id]['available_databases']:
        db = True

    assert (tool, db) == (True, True)



def test_blastn():
    result = blast2galaxy.blastn(
        profile = 'blastn_barley',
        query_str = dna_seq,
        db = 'morex_v3.all.cds',
        outfmt = '6'
    )

    assert 'HORVU.MOREX.r3.2HG0184740.1' in result



def test_diamond_blastp():

    # res = blast2galaxy.diamond_blastp(
    #     profile = 'diamond_blastp',
    #     query = 'query_protein.fasta',
    #     db = 'uniprot_swissprot_2023_03', # Hordeum_vulgare__BPGv2__all_BPGv2:pep
    #     outfmt = '6'
    # )

    result = blast2galaxy.diamond_blastp(
        profile = 'diamond_blastp',
        query_str = protein_seq,
        db = 'uniprot_swissprot_2023_03',
        outfmt = '6'
    )
    
    assert 'sp|P62803|H4_BOVIN' in result