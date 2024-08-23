import os
from pathlib import Path
from enum import Enum
from typing import Optional
import json

from bioblend.galaxy import GalaxyInstance
from bioblend.galaxy.tools.inputs import inputs

from .choices import ChoicesTaskBlastn, ChoicesOutfmt, ParamMappingOutfmt, ChoicesYesNo, ChoicesStrand
from ..utils import get_value, parse_tabular_to_list_of_dict
from .. import config


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


def blastn(
        profile: str = '',
        query: str = '',
        task: Optional[ChoicesTaskBlastn] = ChoicesTaskBlastn.megablast,
        db: Optional[str | None] = None,
        evalue: Optional[str] = '0.001',
        out: str = '',
        outfmt: Optional[ChoicesOutfmt] = ChoicesOutfmt.tab_std,
        html: Optional[bool] = False,
        dust: Optional[ChoicesYesNo] = ChoicesYesNo.yes,
        strand: Optional[ChoicesStrand] = ChoicesStrand.both,
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
    print('test')


def __blastn(
        profile: str = 'default',
        query: str = '',
        task: Optional[ChoicesTaskBlastn] = ChoicesTaskBlastn.megablast,
        db: Optional[str] = None,
        evalue: Optional[str] = '0.001',
        out: str = '',
        outfmt: Optional[ChoicesOutfmt] = ChoicesOutfmt.tab_std.value,
        html: Optional[bool] = False,
        dust: Optional[ChoicesYesNo] = ChoicesYesNo.yes.value,
        strand: Optional[ChoicesStrand] = ChoicesStrand.both.value,
        max_hsps: Optional[int] = None,
        perc_identity: Optional[float] = 0.0,
        word_size: Optional[int] = None,
        ungapped: Optional[bool] = False,
        parse_deflines: Optional[bool] = False,
        qcov_hsp_perc: Optional[float] = 0.0,
        window_size: Optional[int] = None,
        gapopen: Optional[int] = None,
        gapextend: Optional[int] = None
    ):

    
    # print("################ Do a BLASTN!")
    # print('profile = ', profile)
    # print("=== Params ===")
    # print('query = ', query)
    # print('task = ', get_value(task))
    # print('db = ', db)
    # print('evalue = ', evalue)
    # #print('outfmt = ', ParamMappingOutfmt[outfmt])
    # print('outfmt = ', outfmt)
    # print('html = ', html)
    # print('dust = ', get_value(dust))
    # print('strand = ', get_value(strand))
    # print('max_hsps = ', max_hsps)
    # print('perc_identity = ', perc_identity)
    # print('word_size = ', word_size)
    # print('ungapped = ', ungapped)
    # print('parse_deflines = ', parse_deflines)
    # print('qcov_hsp_perc = ', qcov_hsp_perc)
    # print('window_size = ', window_size)
    # print('gapopen = ', gapopen)
    # print('gapextend = ', gapextend)
    
    #exit()

    #result = blastn_request(locals())
    #print(result)
    blastn_request(locals())




def _set_adv_opts(params, tool_inputs):

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




def _get_diamond_tool_inputs(params, tool_inputs):

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
        .set_param('output_section|output|outfmt', params['outfmt'])
        .set_param('output_section|output|fields', diamond_outfmt_fields)
    )

    sensitivity = _get_diamond_sensitivity(params)
    if sensitivity:
        tool_inputs = tool_inputs.set_param('sens_cond|sensitivity', sensitivity)

    return tool_inputs






def request(params):
    print('... PERFORM BLAST ...')
    print(params)

    #exit()
    
    JSON_OUTPUT = False
    
    gi = config.get_galaxy_instance(profile=params['profile'])

    profile = config.get_profile(profile=params['profile'])


    try:
        with open(params['query']) as f:
            QUERY = ''.join(f.readlines())
    except:
        print(f'ERROR: File `{params["query"]}` provided via parameter --query could not be opened or even does not exist!')
        exit()


    outfmt = ''
    try: 
        ChoicesOutfmt(params['outfmt'])
    except ValueError:
        outfmt = params['outfmt']
        if 'html' in params and params['html']:
            outfmt = outfmt + ' -html'
    else:
        outfmt = ParamMappingOutfmt[params['outfmt']]

    if params['outfmt'] == 'json':
        JSON_OUTPUT = True
        outfmt = ParamMappingOutfmt['tabular-std']



    #histories = gi.histories.get_histories()
    #history_id = histories[0]['id']

    #history_name = config['history_name']
    history_name = 'blast2galaxy_test_dev'
    histories = gi.histories.get_histories(name = history_name)
    if not histories:
        gi.histories.create_history(name = history_name)
        histories = gi.histories.get_histories(name = history_name)

    history_id = histories[0]['id']

    file_name = f'blast2galaxy_query_{params["tool"]}.fasta'

    paste_content_result = gi.tools.paste_content(
        content = QUERY,
        history_id = history_id,
        file_name = file_name
    )
    dataset_id_query = paste_content_result['outputs'][0]['id']



    if params['tool'] in ['diamond_blastp', 'diamond_blastx']:
        tool_inputs = inputs().set_dataset_param('query', dataset_id_query, src='hda')
        tool_inputs = _get_diamond_tool_inputs(params, tool_inputs)
    else:
        tool_inputs = (
            inputs()
            .set_dataset_param('query', dataset_id_query, src='hda')
            .set_param('db_opts|db_opts_selector', 'db')
            .set_param('db_opts|database', [str(params['db'])])
            .set_param('blast_type', str(params['task']))
            .set_param('output|out_format', str(outfmt))
            .set_param('evalue_cutoff', params['evalue'])
        )

        tool_inputs = _set_adv_opts(params, tool_inputs)


    
    tool_inputs_dict = tool_inputs.to_dict()
    print('='*150)
    print(json.dumps(tool_inputs_dict, indent=4))
    print('+ tool_id = ', profile['tool'])
    print('+ history_id = ', history_id)
    print('='*150)

    #exit()


    run_tool_result = gi.tools.run_tool(
        history_id = history_id,
        tool_id = str(profile['tool']),
        tool_inputs = tool_inputs
    )

    dataset_id_result = run_tool_result['outputs'][0]['id']
    blast_result = gi.datasets.download_dataset(dataset_id_result)


    blast_result_output = ''
    if JSON_OUTPUT:
        blast_result_output = json.dumps( parse_tabular_to_list_of_dict(blast_result), indent = 4)
    else:
        blast_result_output = blast_result.decode('utf-8')


    try:
        with open(str(params['out']), 'w+') as f_out:
            f_out.write(blast_result_output)
    except Exception as e:
        print('ERROR: Could not save the result to ', params['out'])
        print('ERROR MESSAGE from Exception: ', e)
        return False


    # clean up history
    gi.histories.delete_dataset(history_id = history_id, dataset_id = dataset_id_query, purge = True)
    gi.histories.delete_dataset(history_id = history_id, dataset_id = dataset_id_result, purge = True)
