# CT-Protocol-Management-Tool

# CT_protocol_converter
Converter/Parser of CT raw protocol files

Structure of the repository

- ./scripts/py: python scripts for the program
- ./scripts/py/para_lookup_tbl: saved lookup tables for xml parsing

- convert_protocol_from_indiv_prot_xml_to_json_xlsx_ANALYZE_BeforeAfter_GenCardioDE - example Siemens script with several self-contained functions. Checks if protocol is general CT, dual energy, or cardiac, and parses out parameters based on the according json files. User-specific parameters should be specified in lines 1068 - 1072. If general CT protocol is identified, convert_protocol_from_indiv_prot_xml_to_json is called (from within convert_protocol_from_indiv_prot_xml_to_json_xlsx_ANALYZE_BeforeAfter_GenCardioDE). If cardiac protocol is identified, convert_protocol_from_indiv_prot_xml_to_json_xlsx_Cardiac_funconly is called. If dual energy protocol is identified, convert_protocol_from_indiv_prot_xml_to_json_xlsx_AB_funconly is called.
-   In this example, 2 directories are called to compare all protocols with the same name between the 2 directories (for example, for comparing protocols between 2 timepoints).
-   store_para_lookup_tbl_json_Siemens - generate JSON files for Siemens protocol files based on Siemens data structure


- convert_protocol_from_indiv_prot_xml_to_json_xlsx_GE - example GE script with several self-contained functions. User-specific parameters should be specified in lines 1065 - 1070. Current functionality only works for general CT, but functionality may be built for other protocol types (e.g., Cardiac).
-   In this example, 2 protocol files are called to compare parameters between the 2.
-   store_para_lookup_tbl_json_GE - generate JSON files for GE protocol files based on GE data structure

- get_para_from_indiv_prot_xml - extracts parameters from Siemens or GE files based on the called fields from the JSON files
