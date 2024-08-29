from blast2galaxy import cli
from click.testing import CliRunner
import shutil

test_tool_id = 'toolshed.g2.bx.psu.edu/repos/bgruening/diamond/bg_diamond/2.0.15+galaxy0'

def test_list_tools_cli():
    runner = CliRunner()
    result = runner.invoke(cli.list_tools, terminal_width=1000)
    #print(result.exit_code)
    #print(result.output)
    assert result.exit_code == 0
    assert test_tool_id in result.output