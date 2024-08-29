from blast2galaxy import cli
from click.testing import CliRunner

def test_list_tools():
    runner = CliRunner()
    result = runner.invoke(cli.list_tools)
    #print(result.exit_code)
    #print(result.output)

    assert result.exit_code == 0
    assert "ncbi_tblastn_wrapper_rye" in result.output

