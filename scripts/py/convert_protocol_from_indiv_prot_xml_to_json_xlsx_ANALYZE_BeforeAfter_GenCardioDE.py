# Filename: convert_protocol_from_indiv_prot_xml_to_json_xlsx.py
"""Summary: functions for the conversion from individual CT protocol xml files to the presentable Excel file


"""
# Author: Da Zhang, PhD, DABR
# Created: Wed Apr 27 16:33:31 2022
# Last-Updated: Mon Jul 25 22:43:31 2022 (-14400 Eastern Daylight Time)
# Update #:

import xml.etree.ElementTree as ET
import pandas as pd
import xlsxwriter
import re
import glob
from get_para_from_indiv_prot_xml import get_para_from_indiv_prot_xml_Siemens_Force
import json
import os
from os import listdir
from os.path import isfile, join
import numpy as np
from convert_protocol_from_indiv_prot_xml_to_json_xlsx_Cardiac_funconly import convert_protocol_from_indiv_prot_xml_to_json_C
from convert_protocol_from_indiv_prot_xml_to_json_xlsx_Cardiac_funconly import convert_protocol_from_json_to_xlsx_C
from convert_protocol_from_indiv_prot_xml_to_json_xlsx_AB_funconly import convert_protocol_from_indiv_prot_xml_to_json_DE
from convert_protocol_from_indiv_prot_xml_to_json_xlsx_AB_funconly import convert_protocol_from_json_to_xlsx_DE

def isfloat(x):
    try:
        a = float(x)
    except (TypeError, ValueError):
        return False
    else:
        return True
 
def isint(x):
    try:
        a = float(x)
        b = int(a)
    except (TypeError, ValueError):
        return False
    else:
        return a == b

def parse_prot_pair_structure(prot_se_list1, prot_se_list2):
    """ Figure out the structure of the two protocols, which is used for creating the Excel file.

    :param prot_se_list1: list of dict, each dict being a scan or recon series, for protocol 1
    :param prot_se_list2: list of dict, each dict being a scan or recon series, for protocol 2
    :returns: tuple, containing:
    (topo_count_list,
    premonitoring_count_list,
    monitoring_count_list,
    main_scan_count_list,
    recon_per_scan_list)

    """
    
    # digest the protocol 1 and protocol 2, for their respective number of sections
    # number of topo, [prot1, prot2]
    topo_count_list = [0, 0]
    # number of premonitoring, [prot1, prot2]
    premonitoring_count_list = [0, 0]
    # number of monitoring, [prot1, prot2]
    monitoring_count_list = [0, 0]
    # of main scan, [prot1, prot2]
    main_scan_count_list = [0, 0]

    # list of recons for each major scan
    # the len of recon_per_scan_prot1 is the total number of main scans
    # each element of the recon_per_scan_prot1 is the number of recons for that main scan
    # the sum of the recon_per_scan_prot1 is the total number of recon scans
    recon_per_scan_prot1 = []
    recon_count = 0

    for i, se in enumerate(prot_se_list1):

        if ('"Topogram"' in [se[para] for para in se.keys()]) or ('"TopograM"' in [se[para] for para in se.keys()]) or ('"Topogram LAT"' in [se[para] for para in se.keys()]) or ('"Topogram AP"' in [se[para] for para in se.keys()]):
            topo_count_list[0] = topo_count_list[0] + 1
        elif '"PreMonitoring"' in [se[para] for para in se.keys()]:
            premonitoring_count_list[0] = premonitoring_count_list[0] + 1
        elif '"Monitoring"' in [se[para] for para in se.keys()]:
            monitoring_count_list[0] = monitoring_count_list[0] + 1
        elif 'ReconJob' in se.keys():
            recon_count += 1
        else:
            main_scan_count_list[0] = main_scan_count_list[0] + 1
            if main_scan_count_list[0] > 1:
                recon_per_scan_prot1.append(recon_count)
                recon_count = 0
            else:
                continue
        if i == len(prot_se_list1) - 1:
            # no more main scans, store the number of recons for the last main scans
            recon_per_scan_prot1.append(recon_count)
        else:
            continue

    recon_per_scan_prot2 = []
    recon_count = 0

    for i, se in enumerate(prot_se_list2):

        if ('"Topogram"' in [se[para] for para in se.keys()]) or ('"TopograM"' in [se[para] for para in se.keys()]) or ('"Topogram LAT"' in [se[para] for para in se.keys()]) or ('"Topogram AP"' in [se[para] for para in se.keys()]):
            topo_count_list[1] = topo_count_list[1] + 1
        elif '"PreMonitoring"' in [se[para] for para in se.keys()]:
            premonitoring_count_list[1] = premonitoring_count_list[1] + 1
        elif '"Monitoring"' in [se[para] for para in se.keys()]:
            monitoring_count_list[1] = monitoring_count_list[1] + 1
        elif 'ReconJob' in se.keys():
            recon_count += 1
        else:
            main_scan_count_list[1] = main_scan_count_list[1] + 1
            if main_scan_count_list[1] > 1:
                recon_per_scan_prot2.append(recon_count)
                recon_count = 0
            else:
                continue
        if i == len(prot_se_list2) - 1:
            # no more main scans, store the number of recons for the last main scans
            recon_per_scan_prot2.append(recon_count)
        else:
            continue

    # use recon_per_scan_list to store the number of recons for each main scan for pro1 and prot2.
    # If (m1, n1) is for scan1, and (m2, n2) is for scan2, then this list is [(m1, n1), (m2, n2), ...]
    recon_per_scan_list = []

    if len(recon_per_scan_prot1) == len(recon_per_scan_prot2):
        recon_per_scan_list = list(zip(recon_per_scan_prot1, recon_per_scan_prot2))
    elif len(recon_per_scan_prot1) > len(recon_per_scan_prot2):
        for i, recon_num_prot1 in enumerate(recon_per_scan_prot1):
            if i < len(recon_per_scan_prot2):
                recon_per_scan_list.append((recon_num_prot1, recon_per_scan_prot2[i]))
            else:
                recon_per_scan_list.append((recon_num_prot1, None))
    else: # len(recon_per_scan_prot1) < len(recon_per_scan_prot2):
        for j, recon_num_prot2 in enumerate(recon_per_scan_prot2):
            if j < len(recon_per_scan_prot1):
                recon_per_scan_list.append((recon_per_scan_prot1[j], recon_num_prot2))
            else:
                recon_per_scan_list.append((None, recon_num_prot2))
    return (topo_count_list,
            premonitoring_count_list,
            monitoring_count_list,
            main_scan_count_list,
            recon_per_scan_list)
    

def convert_protocol_from_indiv_prot_xml_to_json(topo_lookup_tbl_json_path,
                                                 scan_lookup_tbl_json_path,
                                                 scan_AB_lookup_tbl_json_path,
                                                 recon_lookup_tbl_json_path,
                                                 monitoring_scan_lookup_tbl_json_path,
                                                 target_prot_name_list,
                                                 target_prot_xml_path_list,
                                                 output_json_path):

    """ Parse convert protocol xml to json, for Siemens Force CT.
    How the localizier, premonitoring, monitoring, main scan, and recon series are based on the lookup tables as indicated by
    
    the function's parameters.
    For regular scans (non-DE, non-perfusion, non-cardiac), the look up table "scan_lookup_tbl.json" will work.
    
    The order of dictionary items appearing in the look up tables file also decide the order of parameters to be shown in each
    section of the intermediate json file and finally the Excel file.

    :param topo_lookup_tbl_json_path: path to the lookup table for the localizers.
    :param scan_lookup_tbl_json_path: path to the lookup table for the main scan.
    :param recon_lookup_tbl_json_path: path to the lookup table for the recons.
    :param monitoring_scan_lookup_tbl_json_path: path to the lookup table for the premonitoring and monitoring scans.
    :param target_prot_name_list: target protocol names.
    :param target_prot_xml_path_list: target protocol xml files to read in.
    :param output_json_path: target json path to save to.
    :returns: N/A

    """
    
    json_fname = output_json_path
#    print("loaded topo_lookup_tbl from ./para_lookup_tbl/topo_lookup_tbl.json")
    with open(topo_lookup_tbl_json_path, 'r') as fp:
        topo_lookup_tbl = json.load(fp)

#    print("loaded scan_lookup_tbl from ./para_lookup_tbl/scan_lookup_tbl.json")
    with open(scan_lookup_tbl_json_path, 'r') as fp:
        scan_lookup_tbl = json.load(fp)
        
#    print("loaded scan_lookup_tbl from ./para_lookup_tbl/scan_lookup_tbl.json")
    with open(scan_AB_lookup_tbl_json_path, 'r') as fp:
        scan_AB_lookup_tbl = json.load(fp)

#    print("loaded recon_lookup_tbl from ./para_lookup_tbl/recon_lookup_tbl.json")
    with open(recon_lookup_tbl_json_path, 'r') as fp:
        recon_lookup_tbl = json.load(fp)

#    print("loaded monitoring_scan_lookup_tbl from ./para_lookup_tbl/monitoring_scan_lookup_tbl.json")
    with open(monitoring_scan_lookup_tbl_json_path, 'r') as fp:
        monitoring_scan_lookup_tbl = json.load(fp)

    prot_pair_se_list = []
    prot_pair_dict_list = []

    for i, target_prot_name in enumerate(target_prot_name_list):

        indiv_prot_xml_path = target_prot_xml_path_list[i]

#        print("\n================================================================================\n")
#        print(indiv_prot_xml_path)

        # get the ET xml tree from the chosen individual protocol file
        prot_xml_tree = ET.parse(indiv_prot_xml_path)
        root = prot_xml_tree.getroot()
        xpath_string = ".//MlModeEntryType"
        found_entry_xml_list = root.findall(xpath_string)

        prot_se_list = []
        prot_dict_list = []

        for i, entry_xml in enumerate(found_entry_xml_list):

            # print(i, entry_xml.findtext(".//MlModeScanType/RangeName"))
            dict1 = {}
#            print("\n================================================================================\n")
            dict1["EntryNo"] = str(i+1)
            entry_node_id_value = str(i+1)

            if (entry_xml.findtext(".//MlModeScanType/RangeName") == '"Topogram"') or (entry_xml.findtext(".//MlModeScanType/RangeName") == '"TopograM"') or (entry_xml.findtext(".//MlModeScanType/RangeName") == '"Topogram LAT"') or (entry_xml.findtext(".//MlModeScanType/RangeName") == '"Topogram AP"'):

                # note: globals()[]() and locals()[]() are general ways to call a function from its string function name
                # locals(): use it if the call is in the the namespace of a script, instead of in the body of a function
                # globals(): use it if the function name is in the body of a function
                for key in topo_lookup_tbl:
                    target_func_name = topo_lookup_tbl[key][0]
                    para_dict = topo_lookup_tbl[key][1]
                    para = globals()[target_func_name](prot_xml_tree,
                                                       entry_node_id_value=entry_node_id_value,
                                                       bool_verbose=False,
                                                       **para_dict)
                    dict1[key] = para[1]

                scan_se = pd.Series(dict1)
                prot_se_list.append(scan_se)
                prot_dict_list.append(dict1)

            elif "monitoring" in entry_xml.findtext(".//MlModeScanType/RangeName").lower():

                for key in monitoring_scan_lookup_tbl:
                    target_func_name = monitoring_scan_lookup_tbl[key][0]
                    para_dict = monitoring_scan_lookup_tbl[key][1]
                    para = globals()[target_func_name](prot_xml_tree,
                                                       entry_node_id_value=entry_node_id_value,
                                                       bool_verbose=False,
                                                       **para_dict)
                    dict1[key] = para[1]

                scan_se = pd.Series(dict1)
                prot_se_list.append(scan_se)
                prot_dict_list.append(dict1)

            else:

                if entry_xml.attrib["ModeScans"] == '1':

                    for key in scan_lookup_tbl:
                        target_func_name = scan_lookup_tbl[key][0]
                        para_dict = scan_lookup_tbl[key][1]
                        para = globals()[target_func_name](prot_xml_tree,
                                                           entry_node_id_value=entry_node_id_value,
                                                           bool_verbose=False,
                                                           **para_dict)
                        dict1[key] = para[1]
                
                elif entry_xml.attrib["ModeScans"] == '2':
                    
                    for key in scan_AB_lookup_tbl:
                        target_func_name = scan_AB_lookup_tbl[key][0]
                        para_dict = scan_AB_lookup_tbl[key][1]
                        para = globals()[target_func_name](prot_xml_tree,
                                                           entry_node_id_value=entry_node_id_value,
                                                           bool_verbose=False,
                                                           **para_dict)
                        dict1[key] = para[1]

                scan_se = pd.Series(dict1)
                print(scan_se)
                prot_se_list.append(scan_se)
                prot_dict_list.append(dict1)                

                # start working on recon series for the main scan
                found_recon_xml_list = entry_xml.findall(".//MlModeReconType")

                for j, recon_xml in enumerate(found_recon_xml_list):

                    # skip the first recon, which is a quality-assurance RT recon
                    if j == 0:
                        continue

                    dict2 = {}
                    dict2["ReconJob"] = str(j)
#                    print("\n================================================================================\n")
                    sub_node_id_value = str(j)
                    for key in recon_lookup_tbl:
                        target_func_name = recon_lookup_tbl[key][0]
                        para_dict = recon_lookup_tbl[key][1]
                        para = globals()[target_func_name](prot_xml_tree,
                                                           entry_node_id_value=entry_node_id_value,
                                                           sub_node_id_value=sub_node_id_value,
                                                           bool_verbose=False,
                                                           **para_dict)
                        dict2[key] = para[1]

                    recon_se = pd.Series(dict2)
                    print(recon_se)
                    prot_se_list.append(recon_se.copy())
                    prot_dict_list.append(dict2.copy())

        prot_pair_se_list.append(prot_se_list)
        prot_pair_dict_list.append(prot_dict_list)

    # write the json file
    with open(json_fname, "w") as output:
#        print("Saved prot_pair_dict_list to:", json_fname)
        json.dump(prot_pair_dict_list, output, indent=4)


def convert_protocol_from_json_to_xlsx(target_prot_name_list,
                                       prot_list_json_path,
                                       output_xlsx_path=None,
                                       bool_verbose=False,
                                       bool_debug=False):
    """Convert the intermediate parsing result (json file) to the final Excel file for presentation.

    :param target_prot_name_list: target protocol names. Note: if target_prot_name_list has only one protocol, the
    Excel file will only have 2 columns: one for the names of parameters and the other for the parameters.
    :param prot_list_json_path: list of paths of json files to read from.
    :param output_xlsx_path: path of the output Excel file to save to.
    :param bool_verbose: whether printing status/progress information as the program run through its jobs.
    :param bool_debug:  wheter print out more detailed step-info for debugging
    :returns: N/A

    """

    xlsx_path = output_xlsx_path
    prot_json_path = prot_list_json_path
    
    with open(prot_json_path, "r") as input:
        prot_pair_dict_list = json.load(input)

    # add logic to handle the case of one protocol in prot_pair_dict_list
    if len(prot_pair_dict_list) == 2:
        # counter of protocols to be processed. This will be used as a flag.
        num_prot = 2
        prot_se_list1 = prot_pair_dict_list[0]
        prot_se_list2 = prot_pair_dict_list[1]
    elif len(prot_pair_dict_list) == 1:
        # counter of protocols to be processed. This will be used as a flag.
        num_prot = 1
        prot_se_list1 = prot_pair_dict_list[0]
        # this is a hack -- if there is only one protocol in the protocol list, keep using it twice
        # this will keep using the existing logic, just overwrite the column B twice
        prot_se_list2 = prot_pair_dict_list[0]
        # this is a hack -- if there is only one protocol in the protocol list, keep using it twice
        prot_pair_dict_list.append(prot_pair_dict_list[0])
        # this is a hack -- if there is only one protocol in the protocol list, keep using it twice
        target_prot_name_list.append(target_prot_name_list[0])
        
    # call parse_prot_pair_structure() to figure out the structure of the protocol file
    (topo_count_list,
     premonitoring_count_list,
     monitoring_count_list,
     main_scan_count_list,
     recon_per_scan_list) = parse_prot_pair_structure(prot_se_list1, prot_se_list2)

    winner_main_scan_banner_row_list = []
    follower_main_scan_banner_row_list = []

    exclusion_para_set = {'EntryNo',
                          'ReconJob',
                          'Window-1 Center',
                          'Window-1 Width',
                          'Window-2 Center',
                          'Window-2 Width',
                          'Syngo TaskflowIdCode',
                          'Syngo TaskflowProcessingIdCode',
                          'Syngo TaskflowProcessingIdMeaning',
                          'Comment1',
                          'Comment2'
                          }

    workbook = xlsxwriter.Workbook(xlsx_path)
    ws = workbook.add_worksheet()

    title_format = workbook.add_format({'bold': 1,
                                        'border': 1,
                                        'align': 'center',
                                        'valign': 'vcenter',
                                        'text_wrap': 1,
                                        'fg_color': '#fefae7'})

    banner_format = workbook.add_format({'bold': 1,
                                         'border': 1,
                                         'align': 'left',
                                         'valign': 'vcenter',
                                         'fg_color': '#5e9cfb'})

    topo_format = workbook.add_format({'border': 1,
                                       'align': 'center',
                                       'valign': 'vcenter',
                                       'fg_color': '#f4f5f7',
                                       })

    scan_format = workbook.add_format({'border': 1,
                                       'align': 'center',
                                       'valign': 'vcenter',
                                       'fg_color': '#fefae7',
                                       })

    recon_format = workbook.add_format({'border': 1,
                                        'align': 'center',
                                        'valign': 'vcenter',
                                        'fg_color': '#e9fcff',
                                        })

    monitoring_format = workbook.add_format({'border': 1,
                                             'align': 'center',
                                             'valign': 'vcenter',
                                             'fg_color': '#e6fcef',
                                             })

    dose_format = workbook.add_format({'border': 1,
                                       'align': 'center',
                                       'valign': 'vcenter',
                                       'fg_color': '#fdebe6',
                                       })

    topo_para_title_format = workbook.add_format({'border': 1,
                                                  'align': 'left',
                                                  'valign': 'vcenter',
                                                  'fg_color': '#f4f5f7'})

    scan_para_title_format = workbook.add_format({'border': 1,
                                                  'align': 'left',
                                                  'valign': 'vcenter',
                                                  'fg_color': '#fefae7'})

    recon_para_title_format = workbook.add_format({'border': 1,
                                                   'align': 'left',
                                                   'valign': 'vcenter',
                                                   'fg_color': '#e9fcff'})

    monitoring_para_title_format = workbook.add_format({'border': 1,
                                                        'align': 'left',
                                                        'valign': 'vcenter',
                                                        'fg_color': '#e6fcef'})

    dose_para_title_format = workbook.add_format({'border': 1,
                                                  'align': 'left',
                                                  'valign': 'vcenter',
                                                  'fg_color': '#fdebe6'})

    emphasis_format = workbook.add_format({'font_color': '#9c0006',
                                           'bold': 1})

    ws.write('A1', "Protocol Name", title_format)

    ws.set_row(0, 30)

    if num_prot == 2:
        ws.write('B1', target_prot_name_list, title_format)
        ws.write('C1', target_prot_name_list, title_format)
    elif num_prot == 1:
        ws.write('B1', target_prot_name_list, title_format)

    # the strategy should be:
    # find the winner of protocols that has the longest number of certain scans (e.g. localizer), then use it to set
    # the banner for this section of scans (e.g., localizer)
    # for main scans, the strategy is different: for each main scan, we need to count the number of recon series, the one with the most
    # recons is the winner

    if num_prot == 2:
        prot_col_letter_list = ['B', 'C'] # for prot-1 and prot-2
    elif num_prot == 1:
        prot_col_letter_list = ['B', 'B'] # for prot-1 and prot-2 -- this is a hack, just rewrite the column B with the same info

    # the counter for series processed. after they are processed, don't process them again
    # use se_processed_list as a list to hold number of processed series (se) for prot-1 (in Col B) and prot-2 (in Col C)
    se_processed_list = [0, 0]

    # ## (1) work on the localizers (topograms)
    row_winner = 1
    row_follower = 1

    winner_index = topo_count_list.index(max(topo_count_list))
    if bool_verbose:
        print("\n")
        print("Winner protocol to be processed first: ", target_prot_name_list[winner_index], "which has",
              max(topo_count_list), "localizers")

    if winner_index == 0:
        follower_index = 1
    elif winner_index == 1:
        follower_index = 0

    if max(topo_count_list) >= 1:
        # work with the winner prot in its target_col
        # i.e., for 2 protocols
        # if winner_index is 0, work on prot-1, use col-B
        # if winner_index is 1, work on prot-2, use col-C
        prot_se_list = prot_pair_dict_list[winner_index]
        target_col_letter = prot_col_letter_list[winner_index]

        # winner and follower are for filling the rows of Excel files
        # the winner_index follower_index may change based on the number of the current type of scan series, e.g., localizer series

        # update the se_processed for winner and follower
        se_processed_winner = se_processed_list[winner_index]
        se_processed_follower = se_processed_list[follower_index]

        for i, se in enumerate(prot_se_list):
            if ('"Topogram"' in [se[para] for para in se.keys()]) or ('"TopograM"' in [se[para] for para in se.keys()]) or ('"Topogram LAT"' in [se[para] for para in se.keys()]) or ('"Topogram AP"' in [se[para] for para in se.keys()]) and i >= se_processed_winner:
                row_winner += 1
                banner_str = "Localizer"
                title_cell_format = topo_para_title_format
                cell_format = topo_format
                if num_prot == 2:
                    ws.merge_range('A'+str(row_winner)+":"+'C'+str(row_winner), banner_str, banner_format)
                elif num_prot == 1:
                    ws.merge_range('A'+str(row_winner)+":"+'B'+str(row_winner), banner_str, banner_format)

                ws.write('A'+str(row_winner), banner_str, banner_format)

                se_processed_winner += 1
               # print("se_processed_winner", se_processed_winner, banner_str, "of protocol ", target_prot_name_list[winner_index], "in Column", target_col_letter, "starting from row: ", row_winner)
                se_processed_list[winner_index] = se_processed_winner

                for para in se.keys():
                    if para in exclusion_para_set:
                        continue

                    row_winner += 1
                    ws.write('A'+str(row_winner), para, title_cell_format)
                    para_value_quote_removed = se[para].replace('"', '')
                    if (re.compile('^\s*\d+\s*$').search(para_value_quote_removed)) and isint(para_value_quote_removed):
                        para_value = int(para_value_quote_removed)
                    elif (re.compile('^\s*(\d*\.\d+)|(\d+\.\d*)\s*$').search(para_value_quote_removed)) and isfloat(para_value_quote_removed):
                        para_value = float(para_value_quote_removed)
                    else:
                        para_value = para_value_quote_removed

                    ws.write(target_col_letter+str(row_winner), para_value, cell_format)
                    # done with the winner prot

        # work with the follower prot in its column
        prot_se_list = prot_pair_dict_list[follower_index]
        target_col_letter = prot_col_letter_list[follower_index]

        for j, se in enumerate(prot_se_list):
            if ('"Topogram"' in [se[para] for para in se.keys()]) or ('"TopograM"' in [se[para] for para in se.keys()]) or ('"Topogram LAT"' in [se[para] for para in se.keys()]) or ('"Topogram AP"' in [se[para] for para in se.keys()])and j >= se_processed_follower:
                row_follower += 1
                cell_format = topo_format

                se_processed_follower += 1
               # print("se_processed_follower", se_processed_follower, banner_str, "of protocol ", target_prot_name_list[follower_index], "in Column", target_col_letter, "starting from row: ", row_follower)
                se_processed_list[follower_index] = se_processed_follower

                for para in se.keys():
                    if para in exclusion_para_set:
                        continue

                    row_follower += 1

                    para_value_quote_removed = se[para].replace('"', '')
                    if (re.compile('^\s*\d+\s*$').search(para_value_quote_removed)) and isint(para_value_quote_removed):
                        para_value = int(para_value_quote_removed)
                    elif (re.compile('^\s*(\d*\.\d+)|(\d+\.\d*)\s*$').search(para_value_quote_removed)) and isfloat(para_value_quote_removed):
                        para_value = float(para_value_quote_removed)
                    else:
                        para_value = para_value_quote_removed

                    ws.write(target_col_letter+str(row_follower), para_value, cell_format)
                    # done with the follower prot

    elif max(topo_count_list) < 1:
        print("no localizers in both protocols")

    # current row number, beyond which there is no data
    current_row = max(row_winner, row_follower)

    # ## (2) work on premonitoring
    row_winner = current_row
    row_follower = current_row

    if premonitoring_count_list[0] == premonitoring_count_list[1]:
        print("Same number of premonitoring scans, keep using the existing order of winner and follower, don't change")
    else:
        winner_index = premonitoring_count_list.index(max(premonitoring_count_list))

    if winner_index == 0:
        follower_index = 1
    elif winner_index == 1:
        follower_index = 0

    if bool_verbose:
        print("\n")
        print("Winner protocol to be processed first: ", target_prot_name_list[winner_index], "which has",
              max(premonitoring_count_list), "premonitoring scans")

    if max(premonitoring_count_list) >= 1:
        # work with the winner prot in its target_col
        # i.e., for 2 protocols
        # if winner_index is 0, work on prot-1, use col-B
        # if winner_index is 1, work on prot-2, use col-C
        prot_se_list = prot_pair_dict_list[winner_index]
        target_col_letter = prot_col_letter_list[winner_index]

        # update the se_processed for winner and follower
        se_processed_winner = se_processed_list[winner_index]
        se_processed_follower = se_processed_list[follower_index]

        for i, se in enumerate(prot_se_list):
            if '"PreMonitoring"' in [se[para] for para in se.keys()] and i >= se_processed_winner:
                row_winner += 1
                banner_str = "PreMonitoring Scan"
                title_cell_format = monitoring_para_title_format
                cell_format = monitoring_format
                if num_prot == 2:
                    ws.merge_range('A'+str(row_winner)+":"+'C'+str(row_winner), banner_str, banner_format)
                elif num_prot == 1:
                    ws.merge_range('A'+str(row_winner)+":"+'B'+str(row_winner), banner_str, banner_format)
                    
                ws.write('A'+str(row_winner), banner_str, banner_format)

                se_processed_winner += 1
                se_processed_list[winner_index] = se_processed_winner

                for para in se.keys():
                    if para in exclusion_para_set:
                        continue

                    row_winner += 1
                    ws.write('A'+str(row_winner), para, title_cell_format)
                    para_value_quote_removed = se[para].replace('"', '')
                    if (re.compile('^\s*\d+\s*$').search(para_value_quote_removed)) and isint(para_value_quote_removed):
                        para_value = int(para_value_quote_removed)
                    elif (re.compile('^\s*(\d*\.\d+)|(\d+\.\d*)\s*$').search(para_value_quote_removed)) and isfloat(para_value_quote_removed):
                        para_value = float(para_value_quote_removed)
                    else:
                        para_value = para_value_quote_removed

                    ws.write(target_col_letter+str(row_winner), para_value, cell_format)
                    # done with the winner prot

        # work with the follower prot in its column
        prot_se_list = prot_pair_dict_list[follower_index]
        target_col_letter = prot_col_letter_list[follower_index]

        for j, se in enumerate(prot_se_list):
            if '"PreMonitoring"' in [se[para] for para in se.keys()] and j >= se_processed_follower:
                row_follower += 1
                cell_format = monitoring_format

                se_processed_follower += 1
                se_processed_list[follower_index] = se_processed_follower

                for para in se.keys():
                    if para in exclusion_para_set:
                        continue
                    row_follower += 1
                    para_value_quote_removed = se[para].replace('"', '')
                    if (re.compile('^\s*\d+\s*$').search(para_value_quote_removed)) and isint(para_value_quote_removed):
                        para_value = int(para_value_quote_removed)
                    elif (re.compile('^\s*(\d*\.\d+)|(\d+\.\d*)\s*$').search(para_value_quote_removed)) and isfloat(para_value_quote_removed):
                        para_value = float(para_value_quote_removed)
                    else:
                        para_value = para_value_quote_removed

                    ws.write(target_col_letter+str(row_follower), para_value, cell_format)
                    # done with the winner prot

    elif max(premonitoring_count_list) < 1:
        print("no PreMonitoring in both protocols")

    # current row number, beyond which there is no data
    current_row = max(row_winner, row_follower)

    # ## (3) work on monitoring
    row_winner = current_row
    row_follower = current_row

    if monitoring_count_list[0] == monitoring_count_list[1]:
        print("keep the order of winner and follower")
    else:
        winner_index = monitoring_count_list.index(max(monitoring_count_list))

    if winner_index == 0:
        follower_index = 1
    elif winner_index == 1:
        follower_index = 0

    if bool_verbose:
        print("\n")
        print("Winner protocol to be processed first: ", target_prot_name_list[winner_index], "which has",
              max(monitoring_count_list), "monitoring scans")

    if max(monitoring_count_list) >= 1:
        # work with the winner prot in its target_col
        # i.e., for 2 protocols
        # if winner_index is 0, work on prot-1, use col-B
        # if winner_index is 1, work on prot-2, use col-C
        prot_se_list = prot_pair_dict_list[winner_index]
        target_col_letter = prot_col_letter_list[winner_index]

        # update the se_processed for winner and follower
        se_processed_winner = se_processed_list[winner_index]
        se_processed_follower = se_processed_list[follower_index]

        for i, se in enumerate(prot_se_list):
            if '"Monitoring"' in [se[para] for para in se.keys()] and i >= se_processed_winner:
                row_winner += 1
                banner_str = "Monitoring Scan"
                title_cell_format = monitoring_para_title_format
                cell_format = monitoring_format
                if num_prot == 2:
                    ws.merge_range('A'+str(row_winner)+":"+'C'+str(row_winner), banner_str, banner_format)
                elif num_prot == 1:
                    ws.merge_range('A'+str(row_winner)+":"+'B'+str(row_winner), banner_str, banner_format)
                    
                ws.write('A'+str(row_winner), banner_str, banner_format)

                se_processed_winner += 1
                se_processed_list[winner_index] = se_processed_winner

                for para in se.keys():
                    if para in exclusion_para_set:
                        continue

                    row_winner += 1
                    ws.write('A'+str(row_winner), para, title_cell_format)
                    para_value_quote_removed = se[para].replace('"', '')
                    if (re.compile('^\s*\d+\s*$').search(para_value_quote_removed)) and isint(para_value_quote_removed):
                        para_value = int(para_value_quote_removed)
                    elif (re.compile('^\s*(\d*\.\d+)|(\d+\.\d*)\s*$').search(para_value_quote_removed)) and isfloat(para_value_quote_removed):
                        para_value = float(para_value_quote_removed)
                    else:
                        para_value = para_value_quote_removed

                    ws.write(target_col_letter+str(row_winner), para_value, cell_format)
                    # done with the winner prot

        # work with the follower prot in its column
        prot_se_list = prot_pair_dict_list[follower_index]
        target_col_letter = prot_col_letter_list[follower_index]

        for j, se in enumerate(prot_se_list):
            if '"Monitoring"' in [se[para] for para in se.keys()] and j >= se_processed_follower:
                row_follower += 1
                cell_format = monitoring_format

                se_processed_follower += 1
                se_processed_list[follower_index] = se_processed_follower

                for para in se.keys():
                    if para in exclusion_para_set:
                        continue

                    row_follower += 1
                    para_value_quote_removed = se[para].replace('"', '')
                    if (re.compile('^\s*\d+\s*$').search(para_value_quote_removed)) and isint(para_value_quote_removed):
                        para_value = int(para_value_quote_removed)
                    elif (re.compile('^\s*(\d*\.\d+)|(\d+\.\d*)\s*$').search(para_value_quote_removed)) and isfloat(para_value_quote_removed):
                        para_value = float(para_value_quote_removed)
                    else:
                        para_value = para_value_quote_removed

                    ws.write(target_col_letter+str(row_follower), para_value, cell_format)
                    # done with the winner prot

    elif max(monitoring_count_list) < 1:
        print("no Monitoring in both protocols")

    # current row number, beyond which there is no data

    # ## (4) work on main scan and recons

    try:
        assert (max(main_scan_count_list) >= 1)
    except Exception as e:
        print(e)
        print("There is no main scan or recon in both protocols")

    current_row = max(row_winner, row_follower)

    processed_winner_main_scan_count = 0
    processed_follower_main_scan_count = 0

    for l in recon_per_scan_list:

        row_winner = current_row
        row_follower = current_row

        if bool_verbose:
            print("\n")
            print("Working on main scans and their recons now.")
            print("current recon_per_scan_list: ", l)
            print("row_winner", row_winner)
            print("row_follower", row_follower)

        try:
            assert (len(l) == 2)
        except Exception as e:
            print(e)
            print("This program does not support more than two protocols yet!")

        if None in l:
            follower_index = l.index(None)
            jplus = -1
        else:
            follower_index = l.index(min(l))
            jplus = l[follower_index]

        if follower_index == 0:
            winner_index = 1
        elif follower_index == 1:
            winner_index = 0

        # work on winner prot first
        prot_se_list = prot_pair_dict_list[winner_index]
        target_col_letter = prot_col_letter_list[winner_index]

        # update the se_processed for winner and follower
        se_processed_winner = se_processed_list[winner_index]
        se_processed_follower = se_processed_list[follower_index]

        if bool_verbose:
            print("\n")
            print("Working on main scan section for winner protocol: ", target_prot_name_list[winner_index], "in Column ", target_col_letter, "starting from row: ", row_winner)

        for i in range(se_processed_winner, se_processed_winner+l[winner_index]+1):

            se = prot_se_list[i]

            if i >= se_processed_winner:
                if 'ReconJob' in se.keys():
                    row_winner += 1
                    if bool_debug:
                        print("row_winner", row_winner)
                    banner_str = "Recon No."+se['ReconJob']
                    title_cell_format = recon_para_title_format
                    cell_format = recon_format
                    if num_prot == 2:
                        ws.merge_range('A'+str(row_winner)+":"+'C'+str(row_winner), banner_str, banner_format)
                    elif num_prot == 1:
                        ws.merge_range('A'+str(row_winner)+":"+'B'+str(row_winner), banner_str, banner_format)
                        
                    ws.write('A'+str(row_winner), banner_str, banner_format)

                    se_processed_winner += 1
                    se_processed_list[winner_index] = se_processed_winner

                    for para in se.keys():
                        if para in exclusion_para_set:
                            continue

                        row_winner += 1
                        if bool_debug:
                            print("row_winner", row_winner)

                        ws.write('A'+str(row_winner), para, title_cell_format)
                        para_value_quote_removed = se[para].replace('"', '')
                        if (re.compile('^\s*\d+\s*$').search(para_value_quote_removed)) and isint(para_value_quote_removed):
                            para_value = int(para_value_quote_removed)
                        elif (re.compile('^\s*(\d*\.\d+)|(\d+\.\d*)\s*$').search(para_value_quote_removed)) and isfloat(para_value_quote_removed):
                            para_value = float(para_value_quote_removed)
                        else:
                            para_value = para_value_quote_removed

                        ws.write(target_col_letter+str(row_winner), para_value, cell_format)
                        # done with the winner prot

                elif ('Topogram' in " ".join([se[para] for para in se.keys()])) or ('TopograM' in " ".join([se[para] for para in se.keys()])) or ('PreMonitoring' in " ".join([se[para] for para in se.keys()])) or ('Bolus Trigger Level' in se.keys()) or ('Monitoring' in " ".join([se[para] for para in se.keys()])) or ('Test Bolus' in " ".join([se[para] for para in se.keys()])):
                    continue
                else: # this is a main scan
                    row_winner += 1
                    if bool_debug:
                        print("row_winner", row_winner)

                    banner_str = "Main Scan"
                    title_cell_format = scan_para_title_format
                    cell_format = scan_format
                    winner_main_scan_banner_row_list.append(row_winner)
                    if num_prot == 2:
                        ws.merge_range('A'+str(row_winner)+":"+'C'+str(row_winner), banner_str, banner_format)
                    elif num_prot == 1:
                        ws.merge_range('A'+str(row_winner)+":"+'B'+str(row_winner), banner_str, banner_format)
                        
                    ws.write('A'+str(row_winner), banner_str, banner_format)

                    se_processed_winner += 1
                    se_processed_list[winner_index] = se_processed_winner

                    for para in se.keys():
                        if para in exclusion_para_set:
                            continue

                        row_winner += 1
                        if bool_debug:
                            print("row_winner", row_winner)

                        ws.write('A'+str(row_winner), para, title_cell_format)
                        para_value_quote_removed = se[para].replace('"', '')
                        if (re.compile('^\s*\d+\s*$').search(para_value_quote_removed)) and isint(para_value_quote_removed):
                            para_value = int(para_value_quote_removed)
                        elif (re.compile('^\s*(\d*\.\d+)|(\d+\.\d*)\s*$').search(para_value_quote_removed)) and isfloat(para_value_quote_removed):
                            para_value = float(para_value_quote_removed)
                        else:
                            para_value = para_value_quote_removed

                        ws.write(target_col_letter+str(row_winner), para_value, cell_format)
                        # done with the winner prot

                    processed_winner_main_scan_count += 1

            else:
                continue

        # work with the follower prot in its column
        prot_se_list = prot_pair_dict_list[follower_index]
        target_col_letter = prot_col_letter_list[follower_index]

        if bool_verbose:
            print("\n")
            print("Working on main scan section for follower protocol: ", target_prot_name_list[follower_index], "in Column ", target_col_letter, "starting from row: ", row_follower)

        for j in range(se_processed_follower, se_processed_follower+jplus+1):
            se = prot_se_list[j]

            if j >= se_processed_follower:
                if 'ReconJob' in se.keys():
                    row_follower += 1
                    if bool_debug:
                        print("row_follower", row_follower)
                    cell_format = recon_format

                    se_processed_follower += 1
                    se_processed_list[follower_index] = se_processed_follower

                    for para in se.keys():
                        if para in exclusion_para_set:
                            continue

                        row_follower += 1
                        if bool_debug:
                            print("row_follower", row_follower)

                        para_value_quote_removed = se[para].replace('"', '')
                        if (re.compile('^\s*\d+\s*$').search(para_value_quote_removed)) and isint(para_value_quote_removed):
                            para_value = int(para_value_quote_removed)
                        elif (re.compile('^\s*(\d*\.\d+)|(\d+\.\d*)\s*$').search(para_value_quote_removed)) and isfloat(para_value_quote_removed):
                            para_value = float(para_value_quote_removed)
                        else:
                            para_value = para_value_quote_removed

                        ws.write(target_col_letter+str(row_follower), para_value, cell_format)
                        # done with the winner prot

                elif ('Topogram' in " ".join([se[para] for para in se.keys()])) or ('TopograM' in " ".join([se[para] for para in se.keys()])) or ('PreMonitoring' in " ".join([se[para] for para in se.keys()])) or ('Bolus Trigger Level' in se.keys()) or ('Monitoring' in " ".join([se[para] for para in se.keys()])) or ('Test Bolus' in " ".join([se[para] for para in se.keys()])):
                    continue
                else: # this is a main scan
                    row_follower += 1
                    if bool_debug:
                        print("row_follower", row_follower)

                    cell_format = scan_format
                    follower_main_scan_banner_row_list.append(row_follower)

                    se_processed_follower += 1
                    se_processed_list[follower_index] = se_processed_follower

                    for para in se.keys():
                        if para in exclusion_para_set:
                            continue

                        row_follower += 1
                        if bool_debug:
                            print("row_follower", row_follower)

                        para_value_quote_removed = se[para].replace('"', '')
                        if (re.compile('^\s*\d+\s*$').search(para_value_quote_removed)) and isint(para_value_quote_removed):
                            para_value = int(para_value_quote_removed)
                        elif (re.compile('^\s*(\d*\.\d+)|(\d+\.\d*)\s*$').search(para_value_quote_removed)) and isfloat(para_value_quote_removed):
                            para_value = float(para_value_quote_removed)
                        else:
                            para_value = para_value_quote_removed

                        ws.write(target_col_letter+str(row_follower), para_value, cell_format)
                        # done with the follower prot

                    processed_follower_main_scan_count += 1
            else:
                continue

        # current row number, beyond which there is no data
        current_row = max(row_winner, row_follower)

    # start row counter for the dose section
    i = current_row

    i += 1
    banner_str = 'Dose Info'
    if num_prot == 2:
        ws.merge_range('A'+str(i)+":"+'C'+str(i), banner_str, banner_format)
    elif num_prot == 1:
        ws.merge_range('A'+str(i)+":"+'B'+str(i), banner_str, banner_format)

    i += 1
    ws.write('A'+str(i), 'CTDIvol (mGy)', dose_para_title_format)
    ws.write('B'+str(i), '', dose_format)
    if num_prot == 2:
        ws.write('C'+str(i), '', dose_format)

    i += 1
    ws.write('A'+str(i), 'DLP (mGy*cm)', dose_para_title_format)
    ws.write('B'+str(i), '', dose_format)
    if num_prot == 2:
        ws.write('C'+str(i), '', dose_format)


    i += 1
    ws.write('A'+str(i), 'Eff. Dose (mSv)', dose_para_title_format)
    ws.write('B'+str(i), '', dose_format)
    if num_prot == 2:
        ws.write('C'+str(i), '', dose_format)


    i += 1
    ws.write('A'+str(i), 'Dose Notification (CTDIv)', dose_para_title_format)
    ws.write('B'+str(i), '', dose_format)
    if num_prot == 2:
        ws.write('C'+str(i), '', dose_format)


    i += 1
    ws.write('A'+str(i), 'Dose Notification (DLP)', dose_para_title_format)
    ws.write('B'+str(i), '', dose_format)
    if num_prot == 2:
        ws.write('C'+str(i), '', dose_format)

    ws.set_column('A:A', 40)
    ws.set_column('B:B', 60)

    if num_prot == 2:
        ws.set_column('C:C', 60)

        ws.conditional_format("C2:C1000",
                              {'type':'formula',
                               'criteria': '=$C2<>$B2',
                               'format': emphasis_format
                               })

        ws.conditional_format("B2:B1000",
                              {'type':'formula',
                               'criteria': '=$B2<>$C2',
                               'format': emphasis_format
                               })

    workbook.close()

############## USER INPUT DATA BELOW #################################################################
path1 = 'UserProtocols_2020-06'
path2 = 'UserProtocols_2022-02-09'
protocol_file_folder = "./Siemens_Force"
json_path = "\\json_path\\"
output_path = "\\output_path\\"
######################################################################################################

path1prefix = protocol_file_folder + '\\' + path1
path2prefix = protocol_file_folder + '\\' + path2
target_prot_name_list = [path1, path2]

target_prot_xml_path_list = [0,0]
onlyprots = []

for i, target_prot_name in enumerate(target_prot_name_list):
    target_prot_file_name = re.sub(r" \((Child|Adult)\)", r".\1", target_prot_name)
    mypath = protocol_file_folder + "\\" + target_prot_file_name
    onlyfiles = [os.path.join(dirpath,f) for (dirpath, dirnames, filenames) in os.walk(mypath) for f in filenames]
    onlyprots.append([x for x in onlyfiles if any(sub in x for sub in ['.Adult','.Child'])])

onlyprots_1 = onlyprots[0]
onlyprots_2 = onlyprots[1]
onlyprotnames_1 = []
onlyprotnames_2 = []

for x in onlyprots_1:
    onlyprotnames_1.append(x.removeprefix(path1prefix))
for x in onlyprots_2:
    onlyprotnames_2.append(x.removeprefix(path2prefix))

inbothyears = list(set(onlyprotnames_2).intersection(onlyprotnames_1))
notin2022 = list(set(onlyprotnames_2).difference(onlyprotnames_1))
notin2023 = list(set(onlyprotnames_1).difference(onlyprotnames_2))
tot_2022 = len(onlyprotnames_1)
tot_2023 = len(onlyprotnames_2)

for x in inbothyears:
    
    target_prot_xml_path_list[0] = glob.glob(protocol_file_folder + '\\' + target_prot_name_list[0] + "\\**\\" + x, recursive=True)[0]
    target_prot_xml_path_list[1] = glob.glob(protocol_file_folder + '\\' + target_prot_name_list[1] + "\\**\\" + x, recursive=True)[0]
    common_prot_name = x.split('\\')[0] + x.split('\\')[1].replace('.','')
    output_json_path = protocol_file_folder + json_path + common_prot_name + '.json'
    output_json_path = re.sub('_\.', '.', output_json_path)
    
    prot_list_json_path = output_json_path
    xlsx_path = protocol_file_folder + output_path + common_prot_name + '.xlsx'

    xlsx_path = re.sub('_\.', '.', xlsx_path)
    
    if 'Cardiac' in x:
        
        topo_lookup_tbl_json_path = "./para_lookup_tbl/Siemens/topo_lookup_tbl.json"
        scan_lookup_tbl_json_path = "./para_lookup_tbl/Siemens/scan_lookup_tbl.json"
        scan_AB_lookup_tbl_json_path = "./para_lookup_tbl/Siemens/scan_AB_lookup_tbl.json"
        recon_lookup_tbl_json_path = "./para_lookup_tbl/Siemens/recon_lookup_tbl.json"
        bolus_lookup_tbl_json_path = "./para_lookup_tbl/Siemens/bolus_lookup_tbl.json"
        monitoring_scan_lookup_tbl_json_path = "./para_lookup_tbl/Siemens/monitoring_C_scan_lookup_tbl.json"

        if 1:
            convert_protocol_from_indiv_prot_xml_to_json_C(topo_lookup_tbl_json_path,
                                                           scan_lookup_tbl_json_path,
                                                           scan_AB_lookup_tbl_json_path,
                                                           recon_lookup_tbl_json_path,
                                                           bolus_lookup_tbl_json_path,
                                                           monitoring_scan_lookup_tbl_json_path,
                                                           target_prot_name_list,
                                                           target_prot_xml_path_list,
                                                           output_json_path)
      
            convert_protocol_from_json_to_xlsx_C(x,
                                                 prot_list_json_path,
                                                 output_xlsx_path=xlsx_path,
                                                 bool_verbose=False,
                                                 bool_debug=False)

    else:
        
        topo_lookup_tbl_json_path = "./para_lookup_tbl/Siemens/topo_lookup_tbl.json"
        scan_lookup_tbl_json_path = "./para_lookup_tbl/Siemens/scan_lookup_tbl.json"
        scan_AB_lookup_tbl_json_path = "./para_lookup_tbl/Siemens/scan_AB_lookup_tbl.json"        
        recon_lookup_tbl_json_path = "./para_lookup_tbl/Siemens/recon_lookup_tbl.json"
        monitoring_scan_lookup_tbl_json_path = "./para_lookup_tbl/Siemens/monitoring_scan_lookup_tbl.json"
    
        if 1:
            convert_protocol_from_indiv_prot_xml_to_json(topo_lookup_tbl_json_path,
                                                         scan_lookup_tbl_json_path,
                                                         scan_AB_lookup_tbl_json_path,
                                                         recon_lookup_tbl_json_path,
                                                         monitoring_scan_lookup_tbl_json_path,
                                                         target_prot_name_list,
                                                         target_prot_xml_path_list,
                                                         output_json_path)
      
            convert_protocol_from_json_to_xlsx(x,
                                               prot_list_json_path,
                                               output_xlsx_path=xlsx_path,
                                               bool_verbose=False,
                                               bool_debug=False)