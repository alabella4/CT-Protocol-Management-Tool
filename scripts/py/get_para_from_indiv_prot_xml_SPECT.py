# Filename: get_para_from_indiv_prot_xml.py
"""Summary: get technical parameters from individual xml protocol files (Siemens Force)


"""
# Author: Da Zhang, PhD, DABR
# Created: Thu Apr  7 20:15:48 2022
# Last-Updated: Mon Jul 25 22:44:03 2022 (-14400 Eastern Daylight Time)
# Update #:
    
import re

def get_para_from_indiv_prot_xml_Siemens_Force(sub_protocol,
                                               para_xpath,
                                               bool_verbose=True):

    """Dig out detailed scan parameter from individual protocol file

    :param prot_xml_tree: xml ET parsed from the individual protocol file, e.g., *.Child, *.Adult for Siemens CT
    :param para_xpath: xpath string for the parameter to retrieve
    :param entry_node_xpath: xpath string for the entry level node, e.g. "MlModeEntryType" for Siemens Force, which is the parent of both scan and recon nodes
    :param entry_node_id_attrib: attribute name for the ID of the entry node, in XPath format, e.g., "@EntryNo" for Siemens Force
    :param entry_node_id_value: target attribute value for the entry-node's ID
    :param sub_node_xpath: xpath string relative to the entry node, e.g., "./MlModeReconType", "./MlModeScanType"
    :param sub_node_id_attrib: attribute name for the sub-node's ID, in XPath format, e.g., "@ReconJob" for Siemens Force
    :param sub_node_id_value: target attribute value for the sub-node's ID
    :param bool_verbose: whether to print the results

    :returns: tuple containing the single parameter's tag and text, (e.tag: e.text)

    """

    sub_protocol = sub_protocol
    # select the entry node based on the entry_node_xpath, entry_node_id_attrib, and entry_node_id_value
    
    para = list(filter(lambda x: re.match(para_xpath,x), sub_protocol))[0]
    e = para.split(":",1)[1].strip()
    f = para.split(":",1)[0].strip()
    
    return_pair = (f, e)

    if bool_verbose:
        print(f, e, "\n")
            
    return return_pair

# # unit test
# import xml.etree.ElementTree as ET
# import re
# import glob
# target_prot_name_list = ["TF_CTA_ABDOMEN_UNDER_55KG_Customized (Child)", "TF_CTA_ABDOMEN_OVER_55KG (Adult)"]
# protocol_file_folder = "./prot_data_dump"
# target_prot_name = target_prot_name_list[0]
# target_prot_file_name = re.sub(r" \((Child|Adult)\)", r".\1", target_prot_name)
# indiv_prot_xml_filename1 = glob.glob(protocol_file_folder + "\\**\\" + target_prot_file_name, recursive=True)[0]

# target_prot_name = target_prot_name_list[1]
# target_prot_file_name = re.sub(r" \((Child|Adult)\)", r".\1", target_prot_name)
# indiv_prot_xml_filename2 = glob.glob(protocol_file_folder + "\\**\\" + target_prot_file_name, recursive=True)[0]


# # test functions to get single para from xml ET
# para_list5 = []
# prot_xml_tree = ET.parse(indiv_prot_xml_filename1)

# # test for topogram
# print("\n")
# for para_xpath in [".//RangeName", ".//TubePosition", ".//Voltage", ".//Current"]:
#     para = get_para_from_indiv_prot_xml_Siemens_Force(prot_xml_tree,
#                                                       para_xpath=para_xpath,
#                                                       entry_node_xpath=".//MlModeEntryType",
#                                                       entry_node_id_attrib="@EntryNo",
#                                                       entry_node_id_value="2",
#                                                       sub_node_xpath="./MlModeScanType", # MlModeReconType
#                                                       sub_node_id_attrib=None,
#                                                       sub_node_id_value=None,
#                                                       bool_verbose=True)
#     para_list5.append(para)
#     print(para_list5)

# # test for monitoring
# para_list6 = []
# for para_xpath in [".//RangeName", ".//NoOfScans"]:
#     para = get_para_from_indiv_prot_xml_Siemens_Force(prot_xml_tree,
#                                                       para_xpath=para_xpath,
#                                                       entry_node_xpath=".//MlModeEntryType",
#                                                       entry_node_id_attrib="@EntryNo",
#                                                       entry_node_id_value="4",
#                                                       sub_node_xpath="./MlModeScanType", # MlModeReconType
#                                                       sub_node_id_attrib=None,
#                                                       sub_node_id_value=None,
#                                                       bool_verbose=True)

#     para_list6.append(para)
#     print(para_list6)

# # test for scan and recon
# para_list7 = []
# for para_xpath in [".//SeriesDescription", ".//IRecStrengths"]:
#     para = get_para_from_indiv_prot_xml_Siemens_Force(prot_xml_tree,
#                                                       para_xpath=para_xpath,
#                                                       entry_node_xpath=".//MlModeEntryType",
#                                                       entry_node_id_attrib="@EntryNo",
#                                                       entry_node_id_value="3",
#                                                       sub_node_xpath="./MlModeReconType", # MlModeReconType
#                                                       sub_node_id_attrib="@ReconJob",
#                                                       sub_node_id_value="1",
#                                                       bool_verbose=True)
#     para_list7.append(para)
#     print(para_list7)
