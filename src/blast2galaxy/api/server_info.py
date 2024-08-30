from itertools import compress

from .. import config
from .. import errors

def get_available_tools_and_databases(server = 'default', blast_type = None):

    gi = config.get_galaxy_instance(server=server)

    blast_tool_ids = []
    blast_tools_databases_dict = {}

    tool_id_pattern_to_tool_type = {
        'ncbi_blastn_wrapper': 'blastn',
        'ncbi_tblastn_wrapper': 'tblastn',
        'ncbi_blastx_wrapper': 'blastx',
        'ncbi_blastp_wrapper': 'blastp',
        'bg_diamond/': 'diamond'
    }

    compatible_versions = {
        'blastn': ['2.10.1+galaxy0', '2.14.1+galaxy0', '2.14.1+galaxy1'],
        'tblastn': ['2.10.1+galaxy0', '2.14.1+galaxy0', '2.14.1+galaxy1'],
        'blastx': ['2.10.1+galaxy0', '2.14.1+galaxy0', '2.14.1+galaxy1'],
        'blastp': ['2.10.1+galaxy0', '2.14.1+galaxy0', '2.14.1+galaxy1'],
        'diamond': ['2.0.15+galaxy0']
    }

    tool_name_by_tool_id = {}

    if blast_type:
        if blast_type in tool_id_pattern_to_tool_type.values():
            tool_id_pattern_to_tool_type_inv = {v: k for k, v in tool_id_pattern_to_tool_type.items()}
            blast_tool_ids_to_match = [ tool_id_pattern_to_tool_type_inv[blast_type] ]
        else:
            raise errors.Blast2galaxyError(f'The type `{blast_type}` is not implemented in blast2galaxy.')
    else:
        blast_tool_ids_to_match = tool_id_pattern_to_tool_type.keys()

    tools = gi.tools.get_tools()

    for tool in tools:
        matches = [x in tool['id'] for x in blast_tool_ids_to_match]
        if any(matches):
            which_tool = list(compress(blast_tool_ids_to_match, matches))[0]
            tool_name = tool_id_pattern_to_tool_type[which_tool]
            tool_name_by_tool_id[tool['id']] = tool_name

            if tool['version'] in compatible_versions[tool_name]:
                blast_tool_ids.append(tool['id'])

    for blast_tool_id in blast_tool_ids:
        blast_tool_details = gi.tools.show_tool(blast_tool_id, io_details=True)
        blast_tool_databases = {}

        for _input in blast_tool_details['inputs']:

            # NCBI BLAST+
            if _input['name'] == 'db_opts':
                for _case in _input['cases']:
                    if _case['value'] == 'db':
                        for __input in _case['inputs']:
                            if __input['name'] == 'database':
                                for _database in __input['options']:
                                    blast_tool_databases[_database[1]] = _database[0]

            # DIAMOND
            if _input['name'] == 'ref_db_source':
                for _case in _input['cases']:
                    if _case['value'] == 'indexed':
                        for __input in _case['inputs']:
                            if __input['name'] == 'index':
                                for _database in __input['options']:
                                    blast_tool_databases[_database[1]] = _database[0]
        

        blast_tools_databases_dict[blast_tool_id] = {
            'tool_name': tool_name_by_tool_id[blast_tool_id],
            'version': blast_tool_details['version'],
            'available_databases': blast_tool_databases
        }

    return blast_tools_databases_dict