from itertools import compress
import json

from .. import config

def get_available_tools_and_databases(server = 'default', blast_type = None):

    gi = config.get_galaxy_instance(server=server)

    blast_tool_ids = []
    blast_tools_databases = []
    blast_tools_databases_dict = {}

    tool_id_pattern_to_tool_type = {
        'ncbi_blastn_wrapper': 'blastn',
        'ncbi_tblastn_wrapper': 'tblastn',
        'ncbi_blastx_wrapper': 'blastx',
        'ncbi_blastp_wrapper': 'blastp',
        'bg_diamond/': 'diamond'
    }

    tool_name_by_tool_id = {}

    if blast_type:
        if blast_type in tool_id_pattern_to_tool_type.values():
            tool_id_pattern_to_tool_type_inv = {v: k for k, v in tool_id_pattern_to_tool_type.items()}
            blast_tool_ids_to_match = [ tool_id_pattern_to_tool_type_inv[blast_type] ]
        else:
            print(f'ERROR: The type `{blast_type}` is not implemented in blast2galaxy.')
            exit()
    else:
        blast_tool_ids_to_match = tool_id_pattern_to_tool_type.keys()

    tools = gi.tools.get_tools()
    for tool in tools:
        matches = [x in tool['id'] for x in blast_tool_ids_to_match]
        if any(matches):
            blast_tool_ids.append(tool['id'])
            which_tool = list(compress(blast_tool_ids_to_match, matches))[0]
            tool_name_by_tool_id[tool['id']] = tool_id_pattern_to_tool_type[which_tool]

    for blast_tool_id in blast_tool_ids:
        blast_tool_io_details = gi.tools.show_tool(blast_tool_id, io_details=True)
        blast_tool_databases = {}
        blast_tool_types = {}

        for _input in blast_tool_io_details['inputs']:

            if _input['name'] == 'blast_type':
                for _option in _input['options']:
                    blast_tool_types[_option[1]] = _option[0]

            # NCBI BLAST+
            if _input['name'] == 'db_opts':
                for _case in _input['cases']:
                    if _case['value'] == 'db':
                        for __input in _case['inputs']:
                            #print(__input)
                            if __input['name'] == 'database':
                                for _database in __input['options']:
                                    blast_tool_databases[_database[1]] = _database[0]

            # diamond
            if _input['name'] == 'ref_db_source':
                for _case in _input['cases']:
                    if _case['value'] == 'indexed':
                        for __input in _case['inputs']:
                            #print(__input)
                            if __input['name'] == 'index':
                                for _database in __input['options']:
                                    blast_tool_databases[_database[1]] = _database[0]
        
        blast_tool_entry = {'blast_tool_id': blast_tool_id, 'available_databases': blast_tool_databases, 'available_blast_types': blast_tool_types}
        blast_tools_databases.append(blast_tool_entry)
        blast_tools_databases_dict[blast_tool_id] = {
            'tool_name': tool_name_by_tool_id[blast_tool_id],
            'available_databases': blast_tool_databases.keys(),
            'available_blast_types': blast_tool_types.keys()
        }

    return blast_tool_ids, blast_tools_databases, blast_tools_databases_dict