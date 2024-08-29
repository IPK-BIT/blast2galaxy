import click
from typing import Optional
from typing_extensions import Annotated

from rich.console import Console
from rich.table import Table
from rich import box

from .api import blast_request as api

from .api.choices import ChoicesBlastType, ChoicesTaskBlastn, ChoicesTaskTblastn, ChoicesTaskBlastp, ChoicesTaskBlastx, ChoicesOutfmt, ChoicesOutfmtDiamond, ChoicesYesNo, ChoicesStrand
from .api.help_texts import HELP

from .api import server_info
from .utils import get_value


@click.group(name='blast2galaxy')
@click.version_option(package_name = 'blast2galaxy')
def cli():
    pass



@cli.command()
def show_config():
    """
    Show information about the currently available configuration loaded from a .blast2galaxy.toml file
    """
    from . import config

    try:
        config, config_toml_path = config.load_config_toml()

        table = Table(show_lines=True, box=box.SQUARE)
        table.add_column('Server ID', justify='left', style='white', no_wrap=True)
        table.add_column('Server URL', justify='left', style='white')
        table.add_column('API Key', justify='left', style='white')

        for server_id, server_config in config['servers'].items():
            table.add_row(server_id, server_config['server_url'], server_config['api_key'][:-12]+'*'*12)

        console = Console()
        console.print(f'\nShowing settings stored in the following blast2galaxy config file: {config_toml_path}')
        console.print('\n[underline]Configured Galaxy servers:')
        console.print(table)

        table = Table(show_lines=True, box=box.SQUARE)
        table.add_column('Profile ID', justify='left', style='white', no_wrap=True)
        table.add_column('Server ID', justify='left', style='white')
        table.add_column('Tool ID', justify='left', style='white')

        for profile_id, profile_config in config['profiles'].items():
            table.add_row(profile_id, profile_config['server'], profile_config['tool'])

        console = Console()
        console.print('\n[underline]Configured profiles:')
        console.print(table)
        console.print('\n')

    except Exception as e:
        print(e)





@cli.command()
@click.option('--server', help='Server-ID as in your config TOML', type=str, default='default', show_default=True)
@click.option('--type', help='Type of BLAST search', type=click.Choice(ChoicesBlastType, case_sensitive=False), default=None)
def list_tools(
        server: str = '',
        type: Optional[ChoicesBlastType | None] = None,
        **kwargs
    ):
    """
    list available and compatible BLAST+ and DIAMOND tools installed on a Galaxy server
    """
    blast_tools_databases_dict = server_info.get_available_tools_and_databases(
        server = server,
        blast_type = get_value(type)
    )

    if 'calltype' in kwargs and kwargs['calltype'] == 'api':
        return blast_tools_databases_dict

    table = Table(show_lines=True, box=box.SQUARE) # MINIMAL_DOUBLE_HEAD SQUARE
    table.add_column('Tool', justify='left', style='white', no_wrap=True)
    table.add_column('Tool ID', justify='left', style='white', no_wrap=True)
    table.add_column('Tool Version', justify='left', style='white')

    for tool_id, tool_specs in blast_tools_databases_dict.items():
        table.add_row(tool_specs['tool_name'], tool_id, tool_specs['version'])

    console = Console()
    console.print('\n[underline]Available BLAST tools and corresponding databases:\n')
    console.print(table)




@cli.command()
@click.option('--server', help='Server-ID as in your config TOML', type=str, default='default', show_default=True)
@click.option('--tool', help='Tool-ID of a tool available on the Galaxy server', type=str, required=True)
def list_dbs(
        server: str = '',
        tool: str = '',
        **kwargs
    ):
    """
    list available databases of a BLAST+ or DIAMOND tool installed on a Galaxy server
    """
    tool_id = tool

    blast_tools_databases_dict = server_info.get_available_tools_and_databases(server = server)

    if tool_id in blast_tools_databases_dict:

        if 'calltype' in kwargs and kwargs['calltype'] == 'api':
            return blast_tools_databases_dict[tool_id]['available_databases']

        table = Table(show_lines=True, box=box.SQUARE) # MINIMAL_DOUBLE_HEAD SQUARE
        table.add_column('Database ID', justify='left', style='white', no_wrap=True)
        table.add_column('Database Description', justify='left', style='white', no_wrap=True)

        for db_id, db_desc in blast_tools_databases_dict[tool_id]['available_databases'].items():
            table.add_row(db_id, db_desc)

        console = Console()
        console.print(f'\n[underline]Available databases for tool with ID `{tool_id}`:\n')
        console.print(table)

    else:
        console = Console()
        console.print(f'\n[red]ERROR: A tool with ID `{tool_id}` does not exist on the Galaxy server `{server}`.\n')





@cli.command()
@click.option('--profile', default='default', show_default=True, help = HELP.profile, type=str)
@click.option('--query', required = True, help = HELP.query, type=str)
@click.option('--task', help=HELP.task, type=click.Choice(ChoicesTaskBlastn, case_sensitive=False), default=ChoicesTaskBlastn.megablast.value, show_default=True)
@click.option('--db', required=True, help=HELP.db, type=str)
@click.option('--evalue', help = HELP.evalue, default='0.001', show_default=True)
@click.option('--out', required = True, help = HELP.out, type=str)
@click.option('--outfmt', help=HELP.outfmt, type=str, default=ChoicesOutfmt.tab_std.value, show_default=True)
@click.option('--html', help=HELP.html, is_flag=True)
@click.option('--dust', help=HELP.dust, type=click.Choice(ChoicesYesNo, case_sensitive=False), default=ChoicesYesNo.yes.value, show_default=True)
@click.option('--strand', help=HELP.strand, type=click.Choice(ChoicesStrand, case_sensitive=False), default=ChoicesStrand.both.value, show_default=True)
@click.option('--max_hsps', help=HELP.max_hsps, type=int)
@click.option('--perc_identity', help=HELP.perc_identity, type=click.FloatRange(0.0, 100.0), default=0.0, show_default=True)
@click.option('--word_size', help=HELP.word_size, type=click.IntRange(2))
@click.option('--ungapped', help=HELP.ungapped, is_flag=True)
@click.option('--parse_deflines', help=HELP.parse_deflines, is_flag=True)
@click.option('--qcov_hsp_perc', help=HELP.qcov_hsp_perc, type=click.FloatRange(0.0, 100.0), default=0.0, show_default=True)
@click.option('--window_size', help=HELP.window_size, type=click.IntRange(1))
@click.option('--gapopen', help=HELP.gapopen, type=click.IntRange(0))
@click.option('--gapextend', help=HELP.gapextend, type=click.IntRange(0))
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
    search nucleotide databases using a nucleotide query
    """

    """
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
    params['tool'] = 'blastn'
    api.request(params=params)












@cli.command()
@click.option('--profile', default='default', show_default=True, help = HELP.profile, type=str)
@click.option('--query', required = True, help = HELP.query, type=str)
@click.option('--task', help=HELP.task, type=click.Choice(ChoicesTaskTblastn, case_sensitive=False), default=ChoicesTaskTblastn.tblastn.value, show_default=True)
@click.option('--db', required=True, help=HELP.db, type=str)
@click.option('--evalue', help = HELP.evalue, default='0.001', show_default=True)
@click.option('--out', required = True, help = HELP.out, type=str)
@click.option('--outfmt', help=HELP.outfmt, type=str, default=ChoicesOutfmt.tab_std.value, show_default=True)
@click.option('--html', help=HELP.html, is_flag=True)
@click.option('--seg', help=HELP.seg, type=click.Choice(ChoicesYesNo, case_sensitive=False), default=ChoicesYesNo.yes.value, show_default=True)
@click.option('--db_gencode', help=HELP.db_gencode, type=int, default=1, show_default=True)
@click.option('--matrix', help = HELP.matrix, type=str)
@click.option('--max_target_seqs', help = HELP.max_target_seqs, type=click.IntRange(1), default=500, show_default=True)
@click.option('--num_descriptions', help = HELP.num_descriptions, type=click.IntRange(0), default=500, show_default=True)
@click.option('--num_alignments', help = HELP.num_alignments, type=click.IntRange(0), default=250, show_default=True)
@click.option('--threshold', help = HELP.threshold, type=click.FloatRange(0.0))
@click.option('--max_hsps', help=HELP.max_hsps, type=int)
@click.option('--word_size', help=HELP.word_size, type=click.IntRange(2))
@click.option('--ungapped', help=HELP.ungapped, is_flag=True)
@click.option('--parse_deflines', help=HELP.parse_deflines, is_flag=True)
@click.option('--qcov_hsp_perc', help=HELP.qcov_hsp_perc, type=click.FloatRange(0.0, 100.0), default=0.0, show_default=True)
@click.option('--window_size', help=HELP.window_size, type=click.IntRange(1))
@click.option('--gapopen', help=HELP.gapopen, type=click.IntRange(0))
@click.option('--gapextend', help=HELP.gapextend, type=click.IntRange(0))
@click.option('--comp_based_stats', help = HELP.comp_based_stats, type=str, default='2', show_default=True)
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
    search translated nucleotide databases using a protein query
    """

    """
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
    params['tool'] = 'tblastn'
    api.request(params=params)





@cli.command()
@click.option('--profile', default='default', show_default=True, help = HELP.profile, type=str)
@click.option('--query', required = True, help = HELP.query, type=str)
@click.option('--task', help=HELP.task, type=click.Choice(ChoicesTaskBlastp, case_sensitive=False), default=ChoicesTaskBlastp.blastp.value, show_default=True)
@click.option('--db', required=True, help=HELP.db, type=str)
@click.option('--evalue', help = HELP.evalue, default='0.001', show_default=True)
@click.option('--out', required = True, help = HELP.out, type=str)
@click.option('--outfmt', help=HELP.outfmt, type=str, default=ChoicesOutfmt.tab_std.value, show_default=True)
@click.option('--html', help=HELP.html, is_flag=True)
@click.option('--seg', help=HELP.seg, type=click.Choice(ChoicesYesNo, case_sensitive=False), default=ChoicesYesNo.yes.value, show_default=True)
@click.option('--matrix', help = HELP.matrix, type=str)
@click.option('--max_target_seqs', help = HELP.max_target_seqs, type=click.IntRange(1), default=500, show_default=True)
@click.option('--num_descriptions', help = HELP.num_descriptions, type=click.IntRange(0), default=500, show_default=True)
@click.option('--num_alignments', help = HELP.num_alignments, type=click.IntRange(0), default=250, show_default=True)
@click.option('--threshold', help = HELP.threshold, type=click.FloatRange(0.0))
@click.option('--max_hsps', help=HELP.max_hsps, type=int)
@click.option('--word_size', help=HELP.word_size, type=click.IntRange(2))
@click.option('--ungapped', help=HELP.ungapped, is_flag=True)
@click.option('--parse_deflines', help=HELP.parse_deflines, is_flag=True)
@click.option('--qcov_hsp_perc', help=HELP.qcov_hsp_perc, type=click.FloatRange(0.0, 100.0), default=0.0, show_default=True)
@click.option('--window_size', help=HELP.window_size, type=click.IntRange(1))
@click.option('--gapopen', help=HELP.gapopen, type=click.IntRange(0))
@click.option('--gapextend', help=HELP.gapextend, type=click.IntRange(0))
@click.option('--comp_based_stats', help = HELP.comp_based_stats, type=str, default='2', show_default=True)
@click.option('--use_sw_tback', help=HELP.use_sw_tback, is_flag=True)
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
    search protein databases using a protein query
    """

    """
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
    params['tool'] = 'blastp'
    api.request(params=params)






@cli.command()
@click.option('--profile', default='default', show_default=True, help = HELP.profile, type=str)
@click.option('--query', required = True, help = HELP.query, type=str)
@click.option('--task', help=HELP.task, type=click.Choice(ChoicesTaskBlastx, case_sensitive=False), default=ChoicesTaskBlastx.blastx.value, show_default=True)
@click.option('--db', required=True, help=HELP.db, type=str)
@click.option('--evalue', help = HELP.evalue, default='0.001', show_default=True)
@click.option('--out', required = True, help = HELP.out, type=str)
@click.option('--outfmt', help=HELP.outfmt, type=str, default=ChoicesOutfmt.tab_std.value, show_default=True)
@click.option('--html', help=HELP.html, is_flag=True)
@click.option('--seg', help=HELP.seg, type=click.Choice(ChoicesYesNo, case_sensitive=False), default=ChoicesYesNo.yes.value, show_default=True)
@click.option('--matrix', help = HELP.matrix, type=str)
@click.option('--max_target_seqs', help = HELP.max_target_seqs, type=click.IntRange(1), default=500, show_default=True)
@click.option('--num_descriptions', help = HELP.num_descriptions, type=click.IntRange(0), default=500, show_default=True)
@click.option('--num_alignments', help = HELP.num_alignments, type=click.IntRange(0), default=250, show_default=True)
@click.option('--threshold', help = HELP.threshold, type=click.FloatRange(0.0))
@click.option('--max_hsps', help=HELP.max_hsps, type=int)
@click.option('--word_size', help=HELP.word_size, type=click.IntRange(2))
@click.option('--ungapped', help=HELP.ungapped, is_flag=True)
@click.option('--parse_deflines', help=HELP.parse_deflines, is_flag=True)
@click.option('--qcov_hsp_perc', help=HELP.qcov_hsp_perc, type=click.FloatRange(0.0, 100.0), default=0.0, show_default=True)
@click.option('--window_size', help=HELP.window_size, type=click.IntRange(1))
@click.option('--gapopen', help=HELP.gapopen, type=click.IntRange(0))
@click.option('--gapextend', help=HELP.gapextend, type=click.IntRange(0))
@click.option('--comp_based_stats', help = HELP.comp_based_stats, type=str, default='2', show_default=True)
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
    search protein databases using a translated nucleotide query
    """

    """
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
    params['tool'] = 'blastx'
    api.request(params=params)









@cli.command()
@click.option('--profile', default='default', show_default=True, help = HELP.profile, type=str)
@click.option('--query', required = True, help = HELP.query, type=str)
@click.option('--task', help=HELP.task, type=click.Choice(ChoicesTaskBlastp, case_sensitive=False), default=ChoicesTaskBlastp.blastp.value, show_default=True)
@click.option('--db', required=True, help=HELP.db, type=str)
@click.option('--evalue', help = HELP.evalue, default='0.001', show_default=True)
@click.option('--out', required = True, help = HELP.out, type=str)
@click.option('--outfmt', help=HELP.outfmt, type=str, default=ChoicesOutfmtDiamond.blast_pairwise.value, show_default=True)
@click.option('--faster', is_flag=True)
@click.option('--fast', is_flag=True)
@click.option('--mid-sensitive', is_flag=True)
@click.option('--sensitive', is_flag=True)
@click.option('--more-sensitive', is_flag=True)
@click.option('--very-sensitive', is_flag=True)
@click.option('--ultra-sensitive', is_flag=True)
@click.option('--strand', help=HELP.strand, type=click.Choice(ChoicesStrand, case_sensitive=False), default=ChoicesStrand.both.value, show_default=True)
@click.option('--matrix', help = HELP.matrix, type=str, default='BLOSUM62', show_default=True)
@click.option('--max-target-seqs', help = HELP.max_target_seqs, type=click.IntRange(1), default=500, show_default=True)
#@click.option('--threshold', help = HELP.threshold, type=click.FloatRange(0.0))
@click.option('--max-hsps', help=HELP.max_hsps, type=int)
#@click.option('--ungapped', help=HELP.ungapped, is_flag=True)
@click.option('--window', help=HELP.window_size, type=click.IntRange(1))
@click.option('--gapopen', help=HELP.gapopen, type=click.IntRange(0))
@click.option('--gapextend', help=HELP.gapextend, type=click.IntRange(0))
@click.option('--comp-based-stats', help = HELP.comp_based_stats, type=str, default='1', show_default=True)
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
    search protein databases using a protein query with DIAMOND
    """

    """
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
    params['tool'] = 'diamond_blastp'
    api.request(params=params)









@cli.command()
@click.option('--profile', default='default', show_default=True, help = HELP.profile, type=str)
@click.option('--query', required = True, help = HELP.query, type=str)
@click.option('--task', help=HELP.task, type=click.Choice(ChoicesTaskBlastp, case_sensitive=False), default=ChoicesTaskBlastp.blastp.value, show_default=True)
@click.option('--db', required=True, help=HELP.db, type=str)
@click.option('--evalue', help = HELP.evalue, default='0.001', show_default=True)
@click.option('--out', required = True, help = HELP.out, type=str)
@click.option('--outfmt', help=HELP.outfmt, type=str, default=ChoicesOutfmtDiamond.blast_pairwise.value, show_default=True)
@click.option('--faster', is_flag=True)
@click.option('--fast', is_flag=True)
@click.option('--mid-sensitive', is_flag=True)
@click.option('--sensitive', is_flag=True)
@click.option('--more-sensitive', is_flag=True)
@click.option('--very-sensitive', is_flag=True)
@click.option('--ultra-sensitive', is_flag=True)
@click.option('--strand', help=HELP.strand, type=click.Choice(ChoicesStrand, case_sensitive=False), default=ChoicesStrand.both.value, show_default=True)
@click.option('--matrix', help = HELP.matrix, type=str, default='BLOSUM62', show_default=True)
@click.option('--max-target-seqs', help = HELP.max_target_seqs, type=click.IntRange(1), default=500, show_default=True)
@click.option('--max-hsps', help=HELP.max_hsps, type=int)
@click.option('--window', help=HELP.window_size, type=click.IntRange(1))
@click.option('--gapopen', help=HELP.gapopen, type=click.IntRange(0))
@click.option('--gapextend', help=HELP.gapextend, type=click.IntRange(0))
@click.option('--comp-based-stats', help = HELP.comp_based_stats, type=str, default='1', show_default=True)
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
    search protein databases using a translated nucleotide query with DIAMOND
    """

    """
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
    params['tool'] = 'diamond_blastx'
    api.request(params=params)