import blast2galaxy
import json

test_tool_id = 'toolshed.g2.bx.psu.edu/repos/bgruening/diamond/bg_diamond/2.0.15+galaxy0'
test_db_id = 'uniprot_swissprot_2023_03'

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