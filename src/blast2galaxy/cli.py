import click
from typing import Optional
from typing_extensions import Annotated

from .api import blast_request as api

from .api.choices import ChoicesBlastType, ChoicesTaskBlastn, ChoicesTaskTblastn, ChoicesTaskBlastp, ChoicesTaskBlastx, ChoicesOutfmt, ChoicesOutfmtDiamond, ChoicesYesNo, ChoicesStrand
from .api.help_texts import HELP

from .api import server_info
from .utils import get_value




@click.group(name='blast2galaxy')
def cli():
    """Main entrypoint."""




#@cli.command()
#@click.option("-d", "--debug", help="Include debug output.")
#def build(debug):
#    """Build production assets."""





@cli.command()
def show_config():
    from rich.console import Console
    from rich.table import Table
    from rich import box

    from . import config

    try:
        config_toml_path = config.get_config_toml_path()
        config = config.load_config_toml()

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
            table.add_row(profile_id, profile_config['server'], profile_config['tool_id'])

        console = Console()
        console.print('\n[underline]Configured profiles:')
        console.print(table)
        console.print('\n')

    except Exception as e:
        print(e)





# @cli.command()
# def test_rich():
#     from rich.console import Console
#     from rich.table import Table

#     table = Table()

#     table.add_column("Released", justify="right", style="cyan", no_wrap=True)
#     table.add_column("Title", style="magenta")
#     table.add_column("Box Office", justify="right", style="green")

#     table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
#     table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
#     table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
#     table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

#     console = Console()
#     console.print(table)




# @cli.command()
# def test_config():
#     from . import config
#     test = config.get_profile(profile='univec')
#     print(test)





@cli.command()
@click.option('--server', help='Server-ID as in your config TOML', type=str, default='default', show_default=True)
@click.option('--type', help='Type of BLAST search', type=click.Choice(ChoicesBlastType, case_sensitive=False))
def list_tools(
        server: str = '',
        type: Optional[ChoicesBlastType | None] = None,
    ):
    from rich.console import Console
    from rich.table import Table
    from rich import box

    blast_tool_ids, blast_tools_databases, blast_tools_databases_dict = server_info.get_available_tools_and_databases(
        server = server,
        blast_type = get_value(type)
    )

    table = Table(show_lines=True, box=box.SQUARE) # MINIMAL_DOUBLE_HEAD SQUARE
    table.add_column('Tool', justify='left', style='white', no_wrap=True)
    table.add_column('Tool ID', justify='left', style='white', no_wrap=True)
    table.add_column('Available databases', justify='left', style='white')

    for tool_id, tool_specs in blast_tools_databases_dict.items():
        dbs = ', '.join(list(tool_specs['available_databases']))
        table.add_row(tool_specs['tool_name'], tool_id, dbs)

    console = Console()
    console.print('\n[underline]Available BLAST tools and corresponding databases:\n')
    console.print(table)







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
        profile: str = '',
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

    blastn for searching nucleotide query sequence in a nucleotides BLAST database

    Arguments:
        profile: the profile from .blast2galaxy.config.toml
        query: file path with your query sequence
        task: the blastn task: megablast or something
        db: the BLAST database to search in
        evalue: todo
        out: todo
        outfmt: todo
        html: todo
        dust: todo
        strand: todo
        max_hsps: todo
        perc_identity: todo
        word_size: todo
        ungapped: todo
        parse_deflines: todo
        qcov_hsp_perc: todo
        window_size: todo
        gapopen: todo
        gapextend: todo
    """


    params = locals()
    params['tool'] = 'blastn'
    #print(params)
    #print(type(params))
    #exit()

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

    params = locals()
    params['tool'] = 'tblastn'
    #print(params)
    #print(type(params))
    #exit()

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

    params = locals()
    params['tool'] = 'blastp'
    #print(params)
    #print(type(params))
    #exit()

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

    params = locals()
    params['tool'] = 'blastx'
    #print(params)
    #print(type(params))
    #exit()

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
        #threshold: Optional[float] = None,
        max_hsps: Optional[int] = None,
        #ungapped: Optional[bool] = False,
        window: Optional[int] = None,
        gapopen: Optional[int] = None,
        gapextend: Optional[int] = None,
        comp_based_stats: Optional[str] = '1',
    ):

    params = locals()
    params['tool'] = 'diamond_blastp'
    #print(params)
    #print(type(params))
    #exit()

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
        #threshold: Optional[float] = None,
        max_hsps: Optional[int] = None,
        #ungapped: Optional[bool] = False,
        window: Optional[int] = None,
        gapopen: Optional[int] = None,
        gapextend: Optional[int] = None,
        comp_based_stats: Optional[str] = '1',
    ):

    params = locals()
    params['tool'] = 'diamond_blastx'
    #print(params)
    #print(type(params))
    #exit()

    api.request(params=params)











#if __name__ == "__main__":
#   cli() 