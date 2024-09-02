import sys
import json

from bioblend.galaxy.tools.inputs import inputs

from ..utils import parse_tabular_to_list_of_dict
from .. import config
from .. import errors


DEBUG = False


diamond_outfmt_fields = [
    'qseqid',
    'sseqid',
    'pident',
    'length',
    'mismatch',
    'gapopen',
    'qstart',
    'qend',
    'sstart',
    'send',
    'evalue',
    'bitscore'
]



def _set_blast_adv_opts(params, tool_inputs):

    cli_opts_to_adv_opts_mapping = {
        'gapopen': 'gapopen',
        'gapextend': 'gapextend',
        'perc_identity': 'identity_cutoff',
        'max_hsps': 'max_hsps',
        'parse_deflines': 'parse_deflines',
        'qcov_hsp_perc': 'qcov_hsp_perc',
        'window_size': 'window_size',
        'word_size': 'word_size',
        'db_gencode': 'db_gencode',
        'comp_based_stats': 'comp_based_stats',
        'threshold': 'threshold',
        'max_target_seqs': 'max_hits',
        'num_descriptions': 'max_hits',
        'num_alignments': 'max_hits'
    }

    for cli_opt, adv_opt in cli_opts_to_adv_opts_mapping.items():
        if cli_opt in params and params[cli_opt]:
            tool_inputs = tool_inputs.set_param('adv_opts|' + adv_opt, str(params[cli_opt]))


    # unspecific
    if 'ungapped' in params and params['ungapped']:
        tool_inputs = tool_inputs.set_param('adv_opts|ungapped', True)



    # blastn specific
    if 'strand' in params:
        tool_inputs = tool_inputs.set_param('adv_opts|strand', '-strand ' + params['strand'])

    if 'dust' in params and params['dust'] == 'yes':
        tool_inputs = tool_inputs.set_param('adv_opts|filter_query', True)



    # tblastn, blastp, blastx specific
    if 'matrix' in params and params['matrix']:
        tool_inputs = tool_inputs.set_param('adv_opts|matrix_gapcosts|matrix', params['matrix'])

    if 'seg' in params and params['seg'] == 'yes':
        tool_inputs = tool_inputs.set_param('adv_opts|filter_query', True)


    # blastp specific
    if 'use_sw_tback' in params and params['use_sw_tback']:
        tool_inputs = tool_inputs.set_param('adv_opts|use_sw_tback', True)


    return tool_inputs



def _get_blast_outfmt(params):
    outfmt = params['outfmt']

    if params['html']:
        outfmt = outfmt + ' -html'

    if params['outfmt'] == 'json':
        outfmt = '6'

    return outfmt



def _get_diamond_outfmt(params):
    outfmt = params['outfmt']

    if params['outfmt'] == 'json':
        outfmt = '6'

    return outfmt



def _get_diamond_sensitivity(params):
    sensitivity = None

    if params['fast']:
        sensitivity = '--fast'

    if params['faster']:
        sensitivity = '--faster'

    if params['mid_sensitive']:
        sensitivity = '--mid-sensitive'

    if params['sensitive']:
        sensitivity = '--sensitive'

    if params['more_sensitive']:
        sensitivity = '--more-sensitive'

    if params['very_sensitive']:
        sensitivity = '--very-sensitive'

    if params['ultra_sensitive']:
        sensitivity = '--ultra-sensitive'

    return sensitivity



def _get_blast_tool_inputs(params, tool_inputs):

    outfmt = _get_blast_outfmt(params)

    tool_inputs = (
        tool_inputs
        .set_param('db_opts|db_opts_selector', 'db')
        .set_param('db_opts|database', [str(params['db'])])
        .set_param('blast_type', str(params['task']))
        .set_param('output|out_format', str(outfmt))
        .set_param('evalue_cutoff', params['evalue'])
    )

    tool_inputs = _set_blast_adv_opts(params, tool_inputs)

    return tool_inputs



def _get_diamond_tool_inputs(params, tool_inputs):

    outfmt = _get_diamond_outfmt(params)

    methods = {
        'diamond_blastp': 'blastp',
        'diamond_blastx': 'blastx',
    }
    method_select = methods[params['tool']]

    tool_inputs = (
        tool_inputs
        .set_param('method_cond|method_select', method_select)
        .set_param('method_cond|no_self_hits', True)
        .set_param('method_cond|comp_based_stats', params['comp_based_stats'])
        .set_param('ref_db_source|db_source', 'indexed')
        .set_param('ref_db_source|index', str(params['db']))
        .set_param('matrix', params['matrix'])
        .set_param('filter_score|filter_score_select', 'evalue')
        .set_param('filter_score|evalue', params['evalue'])
        .set_param('hit_filter|hit_filter_select', 'max')
        .set_param('hit_filter|max_target_seqs', params['max_target_seqs'])
        .set_param('output_section|max_hsps', params['max_hsps'])
        .set_param('output_section|output|outfmt', outfmt)
        .set_param('output_section|output|fields', diamond_outfmt_fields)
    )

    sensitivity = _get_diamond_sensitivity(params)
    if sensitivity:
        tool_inputs = tool_inputs.set_param('sens_cond|sensitivity', sensitivity)

    return tool_inputs






def request(params):

    IS_API_CALL = True if 'calltype' in params['kwargs'] and params['kwargs']['calltype'] == 'api' else False
    JSON_OUTPUT = True if params['outfmt'] == 'json' else False
    
    gi = config.get_galaxy_instance(profile=params['profile'])

    profile = config.get_profile(profile=params['profile'])

    if 'query_str' in params['kwargs'] and params['kwargs']['query_str']:
        # use string provided by `query_str` parameter (only in API mode)
        query = params['kwargs']['query_str']
    else:
        # use file provided by `query` parameter
        try:
            with open(params['query']) as f:
                query = ''.join(f.readlines())
        except Exception as e:
            raise errors.Blast2galaxyError(f'File `{params["query"]}` provided via parameter --query could not be opened or even does not exist! ({e})')


    history_name = 'blast2galaxy'
    histories = gi.histories.get_histories(name = history_name)
    if not histories:
        gi.histories.create_history(name = history_name)
        histories = gi.histories.get_histories(name = history_name)

    history_id = histories[0]['id']

    file_name = f'blast2galaxy_query_{params["tool"]}.fasta'

    paste_content_result = gi.tools.paste_content(
        content = query,
        history_id = history_id,
        file_name = file_name
    )
    dataset_id_query = paste_content_result['outputs'][0]['id']


    tool_inputs = inputs().set_dataset_param('query', dataset_id_query, src='hda')

    if params['tool'] in ['diamond_blastp', 'diamond_blastx']:
        tool_inputs = _get_diamond_tool_inputs(params, tool_inputs)
    else:
        tool_inputs = _get_blast_tool_inputs(params, tool_inputs)



    if DEBUG:
        tool_inputs_dict = tool_inputs.to_dict()
        print(json.dumps(tool_inputs_dict, indent=4))


    try:
        run_tool_result = gi.tools.run_tool(
            history_id = history_id,
            tool_id = str(profile['tool']),
            tool_inputs = tool_inputs
        )
    except Exception as e:
        raise e

    dataset_id_result = run_tool_result['outputs'][0]['id']
    blast_result = gi.datasets.download_dataset(dataset_id_result)


    blast_result_output = ''
    WRITE_AS_BYTES = False
    if JSON_OUTPUT:
        blast_result_output = json.dumps(parse_tabular_to_list_of_dict(blast_result), indent = 4)
    else:
        try:
            blast_result_output = blast_result.decode('utf-8')
        except UnicodeDecodeError:
            WRITE_AS_BYTES = True
            blast_result_output = blast_result


    # clean up history
    gi.histories.delete_dataset(history_id = history_id, dataset_id = dataset_id_query, purge = True)
    gi.histories.delete_dataset(history_id = history_id, dataset_id = dataset_id_result, purge = True)

    # proceed with result
    if IS_API_CALL:
        return blast_result_output

    elif params['out'] == None or params['out'] == '':
        print(blast_result_output, file = sys.stdout)
    
    else:
        try:
            file_open_mode = 'w'

            if WRITE_AS_BYTES:
                file_open_mode = 'wb'

            with open(str(params['out']), file_open_mode) as f_out:
                f_out.write(blast_result_output)

        except Exception as e:
            raise errors.Blast2galaxyError(f'Could not save the result to this file: {str(params['out'])} ({e})')
