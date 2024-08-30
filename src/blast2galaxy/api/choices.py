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

ChoicesOutfmt = ['0', '2', '4', '5', '6', 'ext', 'json']

class ChoicesOutfmtDiamond(str, StrEnum):
    blast_pairwise = '0'
    blast_xml = '5'
    blast_tabular = '6'
    daa = '100'
    sam = '101'
    taxonomic_classification = '102'
    #paf = '103'
    #json = '104'


class ChoicesStrand(str, StrEnum):
    both = 'both'
    plus = 'plus'
    minus = 'minus'