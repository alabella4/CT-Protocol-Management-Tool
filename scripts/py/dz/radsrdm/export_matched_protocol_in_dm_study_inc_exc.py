# Filename: export_matched_protocol_in_dm_study_inc_exc.py
"""Summary: search the dose dump file from DoseMonitor for protocols with protocol names that matched the ((inc, exc),) criteria.


"""
# Author: Da Zhang, PhD, DABR
# Created: Thu May 20 18:34:45 2021
# Last-Updated: Tue Jun 29 14:48:51 2021 (-14400 Eastern Daylight Time)
#      Update #: 78

import pandas as pd
from dz.utilities.match_pattern_inc_exc import match_pattern_inc_exc
from dz.utilities.uniquify import uniquify_list_simple
# from dz.radsrdm.decompose_concat_protocol_name import truncate_concat_protocol_name

def export_matched_protocol_in_dm_study_inc_exc(input_filename,
                                                prot_inc_exc_regexp_pair_list,
                                                which_name="protocol_name",
                                                prot_name_column_override=None,
                                                device_name_field="Device",
                                                chosen_device_list=('all',),
                                                header_row_number=1,
                                                export_filepath="matched_dose_data.csv",
                                                export_type="csv",
                                                export_kwargs=None,
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
    :param chosen_device_list: the name of the device for the export to be focused on
    :param bool_verbose: whether to be verbose
    :param bool_debug: whether to show debug info
    :param header_row_number: which row contains the header of the table
    :param bool_export_data: if to export matched data
    :param export_filepath: filepath of the exported data
    :param export_type: file type of the export
    :param export_kwargs: additional parameters for the export for pandas.to_XXX
    :return: output_list, a list containing tuples for (device_name, protocol_name) or (device_name, study_description)
    :rtype: list

    """

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
            # if bool_proc_prot_name:
            #     scan_protocol_name = truncate_concat_protocol_name(scan_protocol_name, separator='|')
            for regexp_pair in prot_inc_exc_regexp_pair_list:
                inc_patterns = regexp_pair[0]
                exc_patterns = regexp_pair[1]
                if match_pattern_inc_exc(scan_protocol_name, inc_patterns, exc_patterns):
                    # a container for matching protocol names for each CT
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
    
    unique_matched_protocols = uniquify_list_simple(matched_protocol_list)
    if bool_verbose:
        print(unique_matched_protocols)

    df_match_protocol = pd.DataFrame()

    df_match_protocol_list = []
    # also match by device name in chosen_device_list
    if str.lower(first_chosen_device_name) == "all":
        if len(unique_matched_protocols) > 0:
            # use Pandas DataFrame slicing to select all exam records whose core  protocol name == target core protocol name
            for target_core_prot_name in unique_matched_protocols:
                df_match_protocol_list.append(df_dose_full[df_dose_full[prot_field] == target_core_prot_name])
    elif (len(chosen_device_list) >= 1) and (str.lower(first_chosen_device_name) != "all"):
        if len(unique_matched_protocols) > 0:

            for chosen_device_name in chosen_device_list:
                candidate_df1 = df_dose_full[df_dose_full[device_name_field] == chosen_device_name]

                for target_core_prot_name in unique_matched_protocols:
                    candidate_df2 = candidate_df1[candidate_df1[prot_field] == target_core_prot_name]
                    df_match_protocol_list.append(candidate_df2)
    else:
        raise Exception("chosen_device_list's length <= 1 or != 'all'")

    # form one DataFrame from a list of DataFrame objects, for this scanner
    df_match_protocol = pd.concat(df_match_protocol_list)

    dups_by_exam_id = df_match_protocol[df_match_protocol.duplicated(('Study ID', 'Study Date', 'Station Name'))]
    if len(dups_by_exam_id) > 0:
        print('number of duplicated exams: ', len(dups_by_exam_id), ', removed.')
    df_match_protocol.drop_duplicates(('Study ID', 'Study Date', 'Station Name'))
    if bool_verbose:
        if len(dups_by_exam_id) > 0:
            print("The following duplications were dropped.")
            print(dups_by_exam_id)

    df_output = df_match_protocol.sort_values(by=[device_name_field, prot_field])
    if bool_verbose:
        print("Exporting to ", export_filepath)
    if export_type == 'csv':
        if not export_kwargs:
            export_kwargs = {'index': False}
        df_output.to_csv(export_filepath, **export_kwargs)
    elif export_type == 'json':
        df_output.to_json(export_filepath, **export_kwargs)
    elif export_type == 'html':
        df_output.to_html(export_filepath, **export_kwargs)
    elif export_type == 'excel':
        df_output.to_excel(export_filepath, **export_kwargs)
    elif export_type == 'clipboard':
        df_output.to_string(**export_kwargs)
    elif export_type == 'string':
        return df_output.to_string(**export_kwargs)
    elif export_type == 'DataFrame':
        return df_output
    else:
        raise ValueError(
            "Possible values for 'export_type': 'csv', 'json', 'html', 'excel', 'clipboard', 'string, 'DataFrame'. ")
    return df_output
