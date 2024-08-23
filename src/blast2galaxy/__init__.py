from typing import Optional
from typing_extensions import Annotated

import click

from .api.choices import ChoicesBlastType, ChoicesTaskBlastn, ChoicesTaskTblastn, ChoicesTaskBlastp, ChoicesTaskBlastx, ChoicesOutfmt, ChoicesOutfmtDiamond, ChoicesYesNo, ChoicesStrand
from . import cli


def __get_required_options(command):
    required_options = [
        param.name for param in command.params
        if isinstance(param, click.Option) and param.required
    ]
    return required_options


def __check_required_but_missing_params(_method, _kwargs):
    req = __get_required_options(_method)
    required_but_missing = [p for p in req if p not in _kwargs]

    if required_but_missing:
        missing_params = ', '.join(required_but_missing)
        raise ValueError(f'The following required arguments are missing: {missing_params}')


def __invoke(cli_method, _kwargs):
    __check_required_but_missing_params(cli_method, _kwargs)
    ctx = click.Context(cli_method)
    return ctx.invoke(cli_method, **_kwargs)





def list_tools(
        server: Optional[str] = 'default',
        type: Optional[ChoicesBlastType | None] = None,
    ):
    """
    list_tools

    list available and compatible BLAST+ and DIAMOND tools installed on a Galaxy server

    Arguments:
        server: Server-ID
        type: limit the list to a specific tool type (blastn, tblast, blastp, blastx, diamond)
    """
    params = locals()
    params['calltype'] = 'api'
    return __invoke(cli.list_tools, params)



def list_dbs(
        tool: str,
        server: Optional[str] = 'default'
    ):
    """
    list_dbs

    list available databases of a BLAST+ or DIAMOND tool installed on a Galaxy server

    Arguments:
        server: Server-ID
        tool: Tool-ID
    """
    params = locals()
    params['calltype'] = 'api'
    return __invoke(cli.list_dbs, params)



#def blastn(**kwargs):
#    __invoke(cli.blastn, kwargs)


def blastn(
        profile: Optional[str] = '',
        query: str = '',
        task: Optional[ChoicesTaskBlastn] = ChoicesTaskBlastn.megablast,
        db: Optional[str | None] = None,
        evalue: Optional[str] = '0.001',
        out: str = '',
        outfmt: Optional[ChoicesOutfmt] = ChoicesOutfmt.tab_std.value,
        html: Optional[bool] = False,
        dust: Optional[ChoicesYesNo] = ChoicesYesNo.yes.value,
        strand: Optional[ChoicesStrand] = ChoicesStrand.both.value,
        max_hsps: Optional[int | None] = None,
        perc_identity: Optional[float] = 0.0,
        word_size: Optional[int | None] = None,
        ungapped: Optional[bool] = False,
        parse_deflines: Optional[bool] = False,
        qcov_hsp_perc: Optional[float] = 0.0,
        window_size: Optional[int | None] = None,
        gapopen: Optional[int | None] = None,
        gapextend: Optional[int | None] = None
    ):
    """
    blastn

    search nucleotide databases using a nucleotide query

    Arguments:
        profile: the profile from .blast2galaxy.config.toml
        query: file path with your query sequence
        task: the blastn task: megablast or something
        db: the BLAST database to search in
        evalue: Expectation value cutoff
        out: Path / filename of file to store the BLAST result
        outfmt: Output format
        html: Format output as HTML document
        dust: Filter out low complexity regions (with DUST)
        strand: Query strand(s) to search against database/subject
        max_hsps: Maximum number of HSPs (alignments) to keep for any single query-subject pair
        perc_identity: Percent identity cutoff
        word_size: Word size for wordfinder algorithm
        ungapped: Perform ungapped alignment only?
        parse_deflines: Should the query and subject defline(s) be parsed?
        qcov_hsp_perc: Minimum query coverage per hsp (percentage, 0 to 100)
        window_size: Multiple hits window size: use 0 to specify 1-hit algorithm, leave blank for default
        gapopen: Cost to open a gap
        gapextend: Cost to extend a gap
    """

    params = locals()
    params['calltype'] = 'api'
    __invoke(cli.blastn, params)



def tblastn(
        profile: str = '',
        query: str = '',
        task: Optional[ChoicesTaskTblastn] = ChoicesTaskTblastn.tblastn,
        db: Optional[str] = None,
        evalue: Optional[str] = '0.001',
        out: str = '',
        outfmt: Optional[ChoicesOutfmt] = ChoicesOutfmt.tab_std.value,
        html: Optional[bool] = False,
        seg: Optional[ChoicesYesNo] = ChoicesYesNo.yes.value,
        db_gencode: Optional[int] = None,
        matrix: Optional[str] = None,
        max_target_seqs: Optional[int] = None,
        num_descriptions: Optional[int] = None,
        num_alignments: Optional[int] = None,
        threshold: Optional[float] = None,
        max_hsps: Optional[int] = None,
        word_size: Optional[int] = None,
        ungapped: Optional[bool] = False,
        parse_deflines: Optional[bool] = False,
        qcov_hsp_perc: Optional[float] = 0.0,
        window_size: Optional[int] = None,
        gapopen: Optional[int] = None,
        gapextend: Optional[int] = None,
        comp_based_stats: Optional[str] = '2',
    ):
    """
    tblastn

    search translated nucleotide databases using a protein query

    Arguments:
        profile: the profile from .blast2galaxy.config.toml
        query: file path with your query sequence
        task: the blastn task: megablast or something
        db: the BLAST database to search in
        evalue: Expectation value cutoff
        out: Path / filename of file to store the BLAST result
        outfmt: Output format
        html: Format output as HTML document
        seg: Filter out low complexity regions (with SEG)
        db_gencode: Genetic code to use to translate database/subjects (see user manual for details)
        matrix: Scoring matrix name (normally BLOSUM62)
        max_target_seqs: Maximum number of aligned sequences to keep (value of 5 or more is recommended) Default = 500
        num_descriptions: Number of database sequences to show one-line descriptions for. Not applicable for outfmt > 4. Default = 500 * Incompatible with:  max_target_seqs
        num_alignments: Number of database sequences to show alignments for. Default = 250 * Incompatible with:  max_target_seqs
        threshold: Minimum word score such that the word is added to the BLAST lookup table
        max_hsps: Maximum number of HSPs (alignments) to keep for any single query-subject pair
        word_size: Word size for wordfinder algorithm
        ungapped: Perform ungapped alignment only?
        parse_deflines: Should the query and subject defline(s) be parsed?
        qcov_hsp_perc: Minimum query coverage per hsp (percentage, 0 to 100)
        window_size: Multiple hits window size: use 0 to specify 1-hit algorithm, leave blank for default
        gapopen: Cost to open a gap
        gapextend: Cost to extend a gap
        comp_based_stats: Use composition-based statistics: D or d: default (equivalent to 2 ); 0 or F or f: No composition-based statistics; 1: Composition-based statistics as in NAR 29:2994-3005, 2001; 2 or T or t : Composition-based score adjustment as in Bioinformatics 21:902-911, 2005, conditioned on sequence properties; 3: Composition-based score adjustment as in Bioinformatics 21:902-911, 2005, unconditionally
    """

    params = locals()
    params['calltype'] = 'api'
    __invoke(cli.tblastn, params)




def blastp(
        profile: str = '',
        query: str = '',
        task: Optional[ChoicesTaskBlastp] = ChoicesTaskBlastp.blastp,
        db: Optional[str] = None,
        evalue: Optional[str] = '0.001',
        out: str = '',
        outfmt: Optional[ChoicesOutfmt] = ChoicesOutfmt.tab_std.value,
        html: Optional[bool] = False,
        seg: Optional[ChoicesYesNo] = ChoicesYesNo.yes.value,
        matrix: Optional[str] = None,
        max_target_seqs: Optional[int] = None,
        num_descriptions: Optional[int] = None,
        num_alignments: Optional[int] = None,
        threshold: Optional[float] = None,
        max_hsps: Optional[int] = None,
        word_size: Optional[int] = None,
        ungapped: Optional[bool] = False,
        parse_deflines: Optional[bool] = False,
        qcov_hsp_perc: Optional[float] = 0.0,
        window_size: Optional[int] = None,
        gapopen: Optional[int] = None,
        gapextend: Optional[int] = None,
        comp_based_stats: Optional[str] = '2',
        use_sw_tback: Optional[bool] = False
    ):
    """
    blastp

    search protein databases using a protein query

    Arguments:
        profile: the profile from .blast2galaxy.config.toml
        query: file path with your query sequence
        task: the blastn task: megablast or something
        db: the BLAST database to search in
        evalue: Expectation value cutoff
        out: Path / filename of file to store the BLAST result
        outfmt: Output format
        html: Format output as HTML document
        seg: Filter out low complexity regions (with SEG)
        matrix: Scoring matrix name (normally BLOSUM62)
        max_target_seqs: Maximum number of aligned sequences to keep (value of 5 or more is recommended) Default = 500
        num_descriptions: Number of database sequences to show one-line descriptions for. Not applicable for outfmt > 4. Default = 500 * Incompatible with:  max_target_seqs
        num_alignments: Number of database sequences to show alignments for. Default = 250 * Incompatible with:  max_target_seqs
        threshold: Minimum word score such that the word is added to the BLAST lookup table
        max_hsps: Maximum number of HSPs (alignments) to keep for any single query-subject pair
        word_size: Word size for wordfinder algorithm
        ungapped: Perform ungapped alignment only?
        parse_deflines: Should the query and subject defline(s) be parsed?
        qcov_hsp_perc: Minimum query coverage per hsp (percentage, 0 to 100)
        window_size: Multiple hits window size: use 0 to specify 1-hit algorithm, leave blank for default
        gapopen: Cost to open a gap
        gapextend: Cost to extend a gap
        comp_based_stats: Use composition-based statistics: D or d: default (equivalent to 2 ); 0 or F or f: No composition-based statistics; 1: Composition-based statistics as in NAR 29:2994-3005, 2001; 2 or T or t : Composition-based score adjustment as in Bioinformatics 21:902-911, 2005, conditioned on sequence properties; 3: Composition-based score adjustment as in Bioinformatics 21:902-911, 2005, unconditionally
        use_sw_tback: Compute locally optimal Smith-Waterman alignments?
    """

    params = locals()
    params['calltype'] = 'api'
    __invoke(cli.blastp, params)



def blastx(
        profile: str = '',
        query: str = '',
        task: Optional[ChoicesTaskBlastx] = ChoicesTaskBlastx.blastx,
        db: Optional[str] = None,
        evalue: Optional[str] = '0.001',
        out: str = '',
        outfmt: Optional[ChoicesOutfmt] = ChoicesOutfmt.tab_std.value,
        html: Optional[bool] = False,
        seg: Optional[ChoicesYesNo] = ChoicesYesNo.yes.value,
        matrix: Optional[str] = None,
        max_target_seqs: Optional[int] = None,
        num_descriptions: Optional[int] = None,
        num_alignments: Optional[int] = None,
        threshold: Optional[float] = None,
        max_hsps: Optional[int] = None,
        word_size: Optional[int] = None,
        ungapped: Optional[bool] = False,
        parse_deflines: Optional[bool] = False,
        qcov_hsp_perc: Optional[float] = 0.0,
        window_size: Optional[int] = None,
        gapopen: Optional[int] = None,
        gapextend: Optional[int] = None,
        comp_based_stats: Optional[str] = '2',
    ):
    """
    blastx

    search protein databases using a translated nucleotide query

    Arguments:
        profile: the profile from .blast2galaxy.config.toml
        query: file path with your query sequence
        task: the blastn task: megablast or something
        db: the BLAST database to search in
        evalue: Expectation value cutoff
        out: Path / filename of file to store the BLAST result
        outfmt: Output format
        html: Format output as HTML document
        seg: Filter out low complexity regions (with SEG)
        matrix: Scoring matrix name (normally BLOSUM62)
        max_target_seqs: Maximum number of aligned sequences to keep (value of 5 or more is recommended) Default = 500
        num_descriptions: Number of database sequences to show one-line descriptions for. Not applicable for outfmt > 4. Default = 500 * Incompatible with:  max_target_seqs
        num_alignments: Number of database sequences to show alignments for. Default = 250 * Incompatible with:  max_target_seqs
        threshold: Minimum word score such that the word is added to the BLAST lookup table
        max_hsps: Maximum number of HSPs (alignments) to keep for any single query-subject pair
        word_size: Word size for wordfinder algorithm
        ungapped: Perform ungapped alignment only?
        parse_deflines: Should the query and subject defline(s) be parsed?
        qcov_hsp_perc: Minimum query coverage per hsp (percentage, 0 to 100)
        window_size: Multiple hits window size: use 0 to specify 1-hit algorithm, leave blank for default
        gapopen: Cost to open a gap
        gapextend: Cost to extend a gap
        comp_based_stats: Use composition-based statistics: D or d: default (equivalent to 2 ); 0 or F or f: No composition-based statistics; 1: Composition-based statistics as in NAR 29:2994-3005, 2001; 2 or T or t : Composition-based score adjustment as in Bioinformatics 21:902-911, 2005, conditioned on sequence properties; 3: Composition-based score adjustment as in Bioinformatics 21:902-911, 2005, unconditionally
    """

    params = locals()
    params['calltype'] = 'api'
    __invoke(cli.blastx, params)




def diamond_blastp(
        profile: str = '',
        query: str = '',
        task: Optional[ChoicesTaskBlastp] = ChoicesTaskBlastp.blastp,
        db: Optional[str] = None,
        evalue: Optional[str] = '0.001',
        out: str = '',
        outfmt: Optional[ChoicesOutfmtDiamond] = ChoicesOutfmtDiamond.blast_pairwise.value,
        faster: Optional[bool] = False,
        fast: Optional[bool] = False,
        mid_sensitive: Optional[bool] = False,
        sensitive: Optional[bool] = False,
        more_sensitive: Optional[bool] = False,
        very_sensitive: Optional[bool] = False,
        ultra_sensitive: Optional[bool] = False,
        strand: Optional[ChoicesStrand] = ChoicesStrand.both.value,
        matrix: Optional[str] = 'BLOSUM62',
        max_target_seqs: Optional[int] = None,
        max_hsps: Optional[int] = None,
        window: Optional[int] = None,
        gapopen: Optional[int] = None,
        gapextend: Optional[int] = None,
        comp_based_stats: Optional[str] = '1',
    ):
    """
    diamond_blastp

    search protein databases using a protein query with DIAMOND

    Arguments:
        profile: the profile from .blast2galaxy.config.toml
        query: file path with your query sequence
        task: the blastn task: megablast or something
        db: the BLAST database to search in
        evalue: Expectation value cutoff
        out: Path / filename of file to store the BLAST result
        outfmt: Output format
        faster: faster mode
        fast: fast mode
        mid_sensitive: mid_sensitive mode
        sensitive: sensitive mode
        more_sensitive: more_sensitive mode
        very_sensitive: very_sensitive mode
        ultra_sensitive: ultra_sensitive mode
        strand: Query strand(s) to search against database/subject
        matrix: Scoring matrix name (normally BLOSUM62)
        max_target_seqs: Maximum number of aligned sequences to keep (value of 5 or more is recommended) Default = 500
        max_hsps: Maximum number of HSPs (alignments) to keep for any single query-subject pair
        window: Multiple hits window size: use 0 to specify 1-hit algorithm, leave blank for default
        gapopen: Cost to open a gap
        gapextend: Cost to extend a gap
        comp_based_stats: Use composition-based statistics: D or d: default (equivalent to 2 ); 0 or F or f: No composition-based statistics; 1: Composition-based statistics as in NAR 29:2994-3005, 2001; 2 or T or t : Composition-based score adjustment as in Bioinformatics 21:902-911, 2005, conditioned on sequence properties; 3: Composition-based score adjustment as in Bioinformatics 21:902-911, 2005, unconditionally
    """
    params = locals()
    params['calltype'] = 'api'
    __invoke(cli.diamond_blastp, params)





def diamond_blastx(
        profile: str = '',
        query: str = '',
        task: Optional[ChoicesTaskBlastp] = ChoicesTaskBlastp.blastp,
        db: Optional[str] = None,
        evalue: Optional[str] = '0.001',
        out: str = '',
        outfmt: Optional[ChoicesOutfmtDiamond] = ChoicesOutfmtDiamond.blast_pairwise.value,
        faster: Optional[bool] = False,
        fast: Optional[bool] = False,
        mid_sensitive: Optional[bool] = False,
        sensitive: Optional[bool] = False,
        more_sensitive: Optional[bool] = False,
        very_sensitive: Optional[bool] = False,
        ultra_sensitive: Optional[bool] = False,
        strand: Optional[ChoicesStrand] = ChoicesStrand.both.value,
        matrix: Optional[str] = 'BLOSUM62',
        max_target_seqs: Optional[int] = None,
        max_hsps: Optional[int] = None,
        window: Optional[int] = None,
        gapopen: Optional[int] = None,
        gapextend: Optional[int] = None,
        comp_based_stats: Optional[str] = '1',
    ):
    """
    diamond_blastx

    search protein databases using a translated nucleotide query with DIAMOND
    
    Arguments:
        profile: the profile from .blast2galaxy.config.toml
        query: file path with your query sequence
        task: the blastn task: megablast or something
        db: the BLAST database to search in
        evalue: Expectation value cutoff
        out: Path / filename of file to store the BLAST result
        outfmt: Output format
        faster: faster mode
        fast: fast mode
        mid_sensitive: mid_sensitive mode
        sensitive: sensitive mode
        more_sensitive: more_sensitive mode
        very_sensitive: very_sensitive mode
        ultra_sensitive: ultra_sensitive mode
        strand: Query strand(s) to search against database/subject
        matrix: Scoring matrix name (normally BLOSUM62)
        max_target_seqs: Maximum number of aligned sequences to keep (value of 5 or more is recommended) Default = 500
        max_hsps: Maximum number of HSPs (alignments) to keep for any single query-subject pair
        window: Multiple hits window size: use 0 to specify 1-hit algorithm, leave blank for default
        gapopen: Cost to open a gap
        gapextend: Cost to extend a gap
        comp_based_stats: Use composition-based statistics: D or d: default (equivalent to 2 ); 0 or F or f: No composition-based statistics; 1: Composition-based statistics as in NAR 29:2994-3005, 2001; 2 or T or t : Composition-based score adjustment as in Bioinformatics 21:902-911, 2005, conditioned on sequence properties; 3: Composition-based score adjustment as in Bioinformatics 21:902-911, 2005, unconditionally
    """
    params = locals()
    params['calltype'] = 'api'
    __invoke(cli.diamond_blastx, params)





__all__ = ['list_tools', 'list_dbs', 'blastn', 'tblastn', 'blastp', 'blastx', 'diamond_blastp', 'diamond_blastx']