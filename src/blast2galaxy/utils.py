from enum import Enum

def get_value(var):
    if isinstance(var, Enum):
        return var.value
    else:
        return var


def parse_tabular_to_list_of_dict(blast_result):
    blast_result_list_of_dict = []
    blast_result_lines = blast_result.decode('utf-8').split('\n')
    for line in blast_result_lines:
        if line != "":
            line_parts = line.split("\t")
            single_blast_hit = {
                'contig': line_parts[1],
                'percentage_of_identical_matches': line_parts[2],
                'alignment_length': line_parts[3],
                'number_of_mismatches': line_parts[4],
                'number_of_gap_openings': line_parts[5],
                'start_of_alignment_in_query': line_parts[6],
                'end_of_alignment_in_query': line_parts[7],
                'start_of_alignment_in_subject': line_parts[8],
                'end_of_alignment_in_subject': line_parts[9],
                'e_value': line_parts[10],
                'bit_score': line_parts[11],
            }
            blast_result_list_of_dict.append(single_blast_hit)

    return blast_result_list_of_dict