from blast2galaxy import cli
from click.testing import CliRunner

test_tool_id = 'toolshed.g2.bx.psu.edu/repos/bgruening/diamond/bg_diamond/2.0.15+galaxy0'


def test_list_tools_cli():
    runner = CliRunner()
    result = runner.invoke(cli.list_tools, terminal_width=1000)

    assert result.exit_code == 0
    assert test_tool_id in result.output


def test_blastn_cli():
    runner = CliRunner()
    params = [
        '--profile', 'blastn_barley',
        '--query', 'test_data/barley_vrs1_cds.fasta',
        '--db', 'morex_v3.all.cds',
        '--outfmt', '6'
    ]
    result = runner.invoke(cli.blastn, params, terminal_width=1000)

    assert result.exit_code == 0
    assert 'HORVU.MOREX.r3.2HG0184740.1' in result.output


def test_tblastn_cli():
    runner = CliRunner()
    params = [
        '--profile', 'tblastn_barley',
        '--query', 'test_data/barley_vrs1_prot.fasta',
        '--db', 'morex_v3.all.cds',
        '--outfmt', '6'
    ]
    result = runner.invoke(cli.tblastn, params, terminal_width=1000)

    assert result.exit_code == 0
    assert 'HORVU.MOREX.r3.2HG0184740.1' in result.output


def test_blastx_cli():
    runner = CliRunner()
    params = [
        '--profile', 'blastx_barley',
        '--query', 'test_data/barley_vrs1_cds.fasta',
        '--db', 'morex_v3.all',
        '--outfmt', '6'
    ]
    result = runner.invoke(cli.blastx, params, terminal_width=1000)

    assert result.exit_code == 0
    assert 'HORVU.MOREX.r3.2HG0184740.1' in result.output


def test_blastp_cli():
    runner = CliRunner()
    params = [
        '--profile', 'blastp_barley',
        '--query', 'test_data/barley_vrs1_prot.fasta',
        '--db', 'morex_v3.all',
        '--outfmt', '6'
    ]
    result = runner.invoke(cli.blastp, params, terminal_width=1000)

    assert result.exit_code == 0
    assert 'HORVU.MOREX.r3.2HG0184740.1' in result.output


def test_diamond_blastp_cli():
    runner = CliRunner()
    
    params = [
        '--profile', 'diamond_blastp',
        '--query', 'test_data/human_h4c1_prot.fasta',
        '--db', 'uniprot_swissprot_2023_03',
        '--outfmt', '6',
        '--fast'
    ]
    result = runner.invoke(cli.diamond_blastp, params, terminal_width=1000)

    assert result.exit_code == 0
    assert 'sp|P62803|H4_BOVIN' in result.output