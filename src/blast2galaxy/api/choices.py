from enum import Enum

class StrEnum(Enum):
    def __str__(self):
        return str(self.value)

class ChoicesBlastType(str, Enum):
    blastn = 'blastn'
    tblastn = 'tblastn'
    blastp = 'blastp'
    blastx = 'blastx'
    diamond = 'diamond'


class ChoicesYesNo(str, Enum):
    yes = 'yes'
    no = 'no'


class ChoicesTaskBlastn(str, StrEnum):
    megablast = 'megablast'
    blastn = 'blastn'
    blastn_short = 'blastn-short'
    dc_megablast = 'dc-megablast'


class ChoicesTaskTblastn(str, StrEnum):
    tblastn = 'tblastn'
    tblastn_fast = 'tblastn-fast'


class ChoicesTaskBlastx(str, StrEnum):
    blastx = 'blastx'
    blastx_fast = 'blastx-fast'


class ChoicesTaskBlastp(str, StrEnum):
    blastp = 'blastp'
    blastp_short = 'blastp-short'
    blastp_fast = 'blastp-fast'


class ChoicesOutfmt(str, StrEnum):
    tab_std = 'tabular-std'
    tab_ext = 'tabular-ext'
    xml = 'xml'
    pairwise_text = 'pairwise-text'
    pairwise_html = 'pairwise-html'
    query_anchored_text = 'query-anchored-text'
    query_anchored_html = 'query-anchored-html'
    flat_query_anchored_text = 'flat-query-anchored-text'
    flat_query_anchored_html = 'flat-query-anchored-html'
    json = 'json'


class ChoicesOutfmtDiamond(str, StrEnum):
    blast_pairwise = '0'
    blast_xml = '5'
    blast_tabular = '6'
    daa = '100'
    sam = '101'
    taxonomic_classification = '102'
    paf = '103'
    json = '104'
    #json = 'json'


ParamMappingOutfmt = {
    'tabular-std': '6',
    'tabular-ext': 'ext',
    'xml': '5',
    'pairwise-text': '0',
    'pairwise-html': '0 -html',
    'query-anchored-text': '2',
    'query-anchored-html': '2 -html',
    'flat-query-anchored-text': '4',
    'flat-query-anchored-html': '4 -html',
    'json': '6'
}


class ChoicesStrand(str, StrEnum):
    both = 'both'
    plus = 'plus'
    minus = 'minus'