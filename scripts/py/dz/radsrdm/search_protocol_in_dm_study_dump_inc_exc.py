# Filename: search_protocol_in_dm_study_dump_inc_exc.py
"""Summary: 
Search the dose dump file from DoseMonitor for protocols on each scanner that satisfy the searching criteria.

"""
# Author: Da Zhang, PhD, DABR
# Created: Wed Apr 21 13:03:23 2021
# Last-Updated: Tue Jun 29 14:14:46 2021 (-14400 Eastern Daylight Time)
#      Update #: 99

import pandas as pd
from dz.utilities.match_pattern_inc_exc import match_pattern_inc_exc
from dz.utilities.uniquify import uniquify_list_count_occurrence
from dz.radsrdm.decompose_concat_protocol_name import truncate_concat_protocol_name

def search_protocol_in_dm_study_dump_inc_exc(input_filename,
                                             prot_inc_exc_regexp_pair_list,
                                             which_name="protocol_name",
                                             prot_name_column_override=None,
                                             device_name_field="Device",
                                             chosen_device_list=('all',),
                                             header_row_number=5,
                                             bool_verbose=False,
                                             bool_debug=False):
    """    Search through the DoseMonitor study level dump file (csv) for matching protocol names based on the searching rule (inc_patterns, exc_patterns).

    :param input_filename: file name for the study level dose dump (excel).
    :param prot_inc_exc_regexp_pair_list: a list of (inc, exc) pairs, i.e., ((inc1, exc1), (inc2, exc2), ...)
           inc_patterns: a string containing regexp patterns (separated by ";") for inclusion check
           exc_patterns: a string containing regexp patterns (separated by ";") for exclusion check
    :param which_name: which name to match against: 'protocol_name', 'study_description', 'mapped_protocol_name', or 'ordered_procedure'
    :param prot_name_column_override: override the name of the column used for matching, as specified by the logic behind which_name
    :param device_name_field: the field that stores the device name of each scanner, by default being "Device" in DoseMonitor dumps
    :param bool_verbose: whether to be verbose
    :param bool_debug: whether to show debug info
    :param header_row_number: which row contains the header of the table (1st row in Excel is row "0" in pandas)
    :return: output_list, a list containing tuples for (device_name, protocol_name) or (device_name, study_description)
    :rtype: list

    """

    bool_proc_prot_name = False
    if not prot_name_column_override:
        if which_name == "protocol_name":
            prot_field = "Protocol"
            # for DM dump, "Protocol" is formed by concatenating multiple series names behind the scan protocol name
            # the true scan protocol name needs to be truncated from this long string
        elif which_name == "study_description":
            prot_field = "Description"
        elif which_name == "mapped_protocol_name":
            prot_field = "Procedure Meaning"
        elif which_name == "ordered_procedure":
            prot_field = "Requested Procedure Description"
        else:
            raise(ValueError, "which_name should be either 'protocol_name', 'study_description', 'mapped_protocol_name', or 'ordered_procedure'.")
    elif isinstance(prot_name_column_override, str):
        if len(prot_name_column_override) > 0:
            prot_field = prot_name_column_override
        else:
            raise(ValueError, "prot_name_column_override cannot be an empty string.")
    # read the DoseMonitor study level dump file
    df_dose_full = pd.read_csv(input_filename, header=header_row_number)
    title_row = list(df_dose_full.columns)
    if bool_debug:
        print("Title row:")
        print(title_row)

    output_list = []
    matched_protocol_list = []

    first_chosen_device_name = chosen_device_list[0] # to test 'all'
    
    for idx, row in df_dose_full.iterrows():
        device_name = row[device_name_field]
        scan_protocol_name = row[prot_field]
        if isinstance(scan_protocol_name, str):
            if bool_proc_prot_name:
                scan_protocol_name = truncate_concat_protocol_name(scan_protocol_name, separator='|')
            for regexp_pair in prot_inc_exc_regexp_pair_list:
                inc_patterns = regexp_pair[0]
                exc_patterns = regexp_pair[1]
                if match_pattern_inc_exc(scan_protocol_name, inc_patterns, exc_patterns):
                    # a container for matching protocol names for each device
                    output_list.append((device_name, scan_protocol_name))
                    matched_protocol_list.append(scan_protocol_name)
                    continue

    if len(chosen_device_list) > 1 or first_chosen_device_name != 'all':
        new_output_list = []
        new_matched_protocol_list = []
        for (device_name, scan_protocol_name) in output_list:
            if device_name in chosen_device_list:
                new_output_list.append((device_name, scan_protocol_name))
                new_matched_protocol_list.append(scan_protocol_name)

        output_list = new_output_list
        matched_protocol_list = new_matched_protocol_list

    unique_matched_protocols_stat = uniquify_list_count_occurrence(output_list)

    output_row_list = []
    total_matched_exams = 0
    for key in unique_matched_protocols_stat:
        output_row = [key[0], unique_matched_protocols_stat[key], key[1]]
        total_matched_exams += unique_matched_protocols_stat[key]
        output_row_list.append(output_row)

    # sort according to (1) device_name; (2) # of exams; (3) protocol name
    output_row_list.sort(key=lambda x : x[2])
    output_row_list.sort(key=lambda x : x[1], reverse=True)
    output_row_list.sort(key=lambda x : x[0])

    if bool_verbose:
        print("Found protocol names [%i]: " % total_matched_exams)
        for s in output_row_list:
            print(*s, sep='\t')

    return output_row_list
