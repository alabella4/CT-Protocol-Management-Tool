# Filename: store_para_lookup_tbl_json.py
"""Summary: store parameter lookup tables to json files
Structure of the 

"""
# Author: Da Zhang, PhD, DABR
# Created: Fri Apr 22 16:57:14 2022
# Last-Updated: Mon Aug 22 14:10:06 2022 (-14400 Eastern Daylight Time)
# Update #: 

#CHANGE LOOKUP TABLE
# ONE TABLE, TUBE A AND TUBE B FOR ONLY RELEVANT DIFFERENT PARAMETERS
# KV, MAS, FILTER(?)

import json

topo_lookup_tbl = {"Range": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^RangeName"}),

                   "Tube Position (Angle)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^AngleType:"}),

                   "kVp": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^Voltage:"}),

                   "mA": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^Current:"}),
                   
                   "Kernel": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^Kernel:"}),
                   
                   "Series Description": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^SeriesDescription:"})
                   }

scan_lookup_tbl = {"Range": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^RangeName"}),
                   # "Scan Mode": ("calculate_scan_para_Siemens_Force", {}),
                   "Reference kVp": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^AutokVVoltage:"}),
                   
                   "kVp": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^Voltage:"}),
                   
                   "Qref mAs": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^AECReferenceMAs:"}),
                   
                   "Eff. mAs": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^EffectiveMAs:"}),
                   
                   "Auto kV Mode": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^AutokV:"}),
                   
                   # "Auto kV Tissue": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//AutokVOptiCriteria",
                   #                                                                   "entry_node_xpath": ".//MlModeEntryType",
                   #                                                                   "entry_node_id_attrib": "@EntryNo",
                   #                                                                   "sub_node_xpath": "./MlModeScanType",
                   #                                                                   "sub_node_id_attrib": "@ModeScan",
                   #                                                                   "sub_node_id_value": "A"}),
                   # "Auto kV Min": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//AutokVVoltageMin",
                   #                                                                "entry_node_xpath": ".//MlModeEntryType",
                   #                                                                "entry_node_id_attrib": "@EntryNo",
                   #                                                                "sub_node_xpath": "./MlModeScanType",
                   #                                                                "sub_node_id_attrib": "@ModeScan",
                   #                                                                "sub_node_id_value": "A"}),
                   # "Auto kV Max": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//AutokVVoltageMax",
                   #                                                                "entry_node_xpath": ".//MlModeEntryType",
                   #                                                                "entry_node_id_attrib": "@EntryNo",
                   #                                                                "sub_node_xpath": "./MlModeScanType",
                   #                                                                "sub_node_id_attrib": "@ModeScan",
                   #                                                                "sub_node_id_value": "A"}),
                   "Dose Modulation On/Off": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^DoseModulationType:"}),
                   
                   "Dose Modulation": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^AECDoseModulationType:"}),
                   
                   "Rotation Time (s)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^RotTime:"}),
                   
                   "Delay Time (s)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^StartDelay:"}),
                   
                   "Pitch": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^PitchFactor:"}),
                   
                   "Slice No (Nominal)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^SlicesPerScan:"}),
                   
                   "Slice No (Actual)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^NoOfSlicesAfterFusing:"}),
                   
                   "Slice Width (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^SliceDetector:"}),
                   
                   "Table Feed/Rotation (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^SpiralFeedRot:"}),
                   
                   "Scan FOV (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^FOV:"}),
                   
                   # "Max recon FOV for TF (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//FoVMaxFlashTotal",
                   #                                                                              "entry_node_xpath": ".//MlModeEntryType",
                   #                                                                              "entry_node_id_attrib": "@EntryNo",
                   #                                                                              "sub_node_xpath": "./MlModeScanType",
                   #                                                                              "sub_node_id_attrib": "@ModeScan",
                   #                                                                              "sub_node_id_value": "A"}),
                   }

recon_lookup_tbl = {"Series Description": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^SeriesDescription:"}),
                    
                    "Slice Thickness (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^SliceEffective:"}),
                    
                    "Slice Increment (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^SliceEffectiveTiltCorrected:"}),
                    
                    "Kernel": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^Kernel:"}),
                    
                    "Window Name": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^Window"}),
                    
                    # "Window-1 Center": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//Window1Center",
                    #                                                                    "entry_node_xpath": ".//MlModeEntryType",
                    #                                                                    "entry_node_id_attrib": "@EntryNo",
                    #                                                                    "sub_node_xpath": "./MlModeReconType",
                    #                                                                    "sub_node_id_attrib": "@ReconJob"}),
                    # "Window-1 Width": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//Window1Width",
                    #                                                                   "entry_node_xpath": ".//MlModeEntryType",
                    #                                                                   "entry_node_id_attrib": "@EntryNo",
                    #                                                                   "sub_node_xpath": "./MlModeReconType",
                    #                                                                   "sub_node_id_attrib": "@ReconJob"}),
                    # "Window-2 Center": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//Window2Center",
                    #                                                                    "entry_node_xpath": ".//MlModeEntryType",
                    #                                                                    "entry_node_id_attrib": "@EntryNo",
                    #                                                                    "sub_node_xpath": "./MlModeReconType",
                    #                                                                    "sub_node_id_attrib": "@ReconJob"}),
                    # "Window-2 Width": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//Window2Width",
                    #                                                                   "entry_node_xpath": ".//MlModeEntryType",
                    #                                                                   "entry_node_id_attrib": "@EntryNo",
                    #                                                                   "sub_node_xpath": "./MlModeReconType",
                    #                                                                   "sub_node_id_attrib": "@ReconJob"}),
                    "Iter.Recon Type": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^ReconMode"}),
                    
                    "Iter.Recon Strength": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^ImageReconType:"}),
                    
                    "Hor FOV for Recon (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^FoVHorLength:"}),
                    
                    "Vert FOV for Recon (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^FoVVertLength:"}),
                    
                    "Transfer1": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^Transfer1:"}),
                    
                    "Transfer2": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^Transfer2:"}),
                    
                    "Transfer3": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": "^Transfer3:"}),
                    # "Syngo TaskflowIdCode": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//TaskflowIdCode",
                    #                                                                         "entry_node_xpath": ".//MlModeEntryType",
                    #                                                                         "entry_node_id_attrib": "@EntryNo",
                    #                                                                         "sub_node_xpath": "./MlModeReconType",
                    #                                                                         "sub_node_id_attrib": "@ReconJob"}),
                    # "Syngo TaskflowProcessingIdCode": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//TaskflowProcessingIdCode",
                    #                                                                                   "entry_node_xpath": ".//MlModeEntryType",
                    #                                                                                   "entry_node_id_attrib": "@EntryNo",
                    #                                                                                   "sub_node_xpath": "./MlModeReconType",
                    #                                                                                   "sub_node_id_attrib": "@ReconJob"}),
                    # "Syngo TaskflowProcessingIdMeaning": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//TaskflowProcessingIdMeaning",
                    #                                                                                      "entry_node_xpath": ".//MlModeEntryType",
                    #                                                                                      "entry_node_id_attrib": "@EntryNo",
                    #                                                                                      "sub_node_xpath": "./MlModeReconType",
                    #                                                                                      "sub_node_id_attrib": "@ReconJob"}),
                    # "Comment1": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//Comment1",
                    #                                                             "entry_node_xpath": ".//MlModeEntryType",
                    #                                                             "entry_node_id_attrib": "@EntryNo",
                    #                                                             "sub_node_xpath": "./MlModeReconType",
                    #                                                             "sub_node_id_attrib": "@ReconJob"}),
                    # "Comment2": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//Comment1",
                    #                                                             "entry_node_xpath": ".//MlModeEntryType",
                    #                                                             "entry_node_id_attrib": "@EntryNo",
                    #                                                             "sub_node_xpath": "./MlModeReconType",
                    #                                                             "sub_node_id_attrib": "@ReconJob"}),
                    }

# for pre-monitoring and monitoring scans
monitoring_scan_lookup_tbl = {"Range": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//RangeName",
                                                                                       "entry_node_xpath": ".//MlModeEntryType",
                                                                                       "entry_node_id_attrib": "@EntryNo",
                                                                                       "sub_node_xpath": "./MlModeScanType"}),
                              # "Scan Mode": ("calculate_scan_para_Siemens_Force", {}),
                              "Reference kVp": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//QualityReferenceVoltage",
                                                                                               "entry_node_xpath": ".//MlModeEntryType",
                                                                                               "entry_node_id_attrib": "@EntryNo",
                                                                                               "sub_node_xpath": "./MlModeScanType"}),
                              "kVp": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//Voltage",
                                                                                     "entry_node_xpath": ".//MlModeEntryType",
                                                                                     "entry_node_id_attrib": "@EntryNo",
                                                                                     "sub_node_xpath": "./MlModeScanType"}),
                              "Qref mAs": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//QualityReferencemAs",
                                                                                          "entry_node_xpath": ".//MlModeEntryType",
                                                                                          "entry_node_id_attrib": "@EntryNo",
                                                                                          "sub_node_xpath": "./MlModeScanType"}),
                              "mAs": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//CustomMAs",
                                                                                     "entry_node_xpath": ".//MlModeEntryType",
                                                                                     "entry_node_id_attrib": "@EntryNo",
                                                                                     "sub_node_xpath": "./MlModeScanType"}),
                              "Auto kV Mode": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//AutokVMode",
                                                                                              "entry_node_xpath": ".//MlModeEntryType",
                                                                                              "entry_node_id_attrib": "@EntryNo",
                                                                                              "sub_node_xpath": "./MlModeScanType"}),
                              # "Auto kV Tissue": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//AutokVOptiCriteria",
                              #                                                                   "entry_node_xpath": ".//MlModeEntryType",
                              #                                                                   "entry_node_id_attrib": "@EntryNo",
                              #                                                                   "sub_node_xpath": "./MlModeScanType"}),
                              # "Auto kV Min": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//AutokVVoltageMin",
                              #                                                                "entry_node_xpath": ".//MlModeEntryType",
                              #                                                                "entry_node_id_attrib": "@EntryNo",
                              #                                                                "sub_node_xpath": "./MlModeScanType"}),
                              # "Auto kV Max": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//AutokVVoltageMax",
                              #                                                                "entry_node_xpath": ".//MlModeEntryType",
                              #                                                                "entry_node_id_attrib": "@EntryNo",
                              #                                                                "sub_node_xpath": "./MlModeScanType"}),
                              "Dose Modulation On/Off": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//Care",
                                                                                                        "entry_node_xpath": ".//MlModeEntryType",
                                                                                                        "entry_node_id_attrib": "@EntryNo",
                                                                                                        "sub_node_xpath": "./MlModeScanType"}),
                              # "Dose Modulation": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//CareDoseType",
                              #                                                                    "entry_node_xpath": ".//MlModeEntryType",
                              #                                                                    "entry_node_id_attrib": "@EntryNo",
                              #                                                                    "sub_node_xpath": "./MlModeScanType"}),
                              "Rotation Time (s)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//ExposureTimePerRotation",
                                                                                                   "entry_node_xpath": ".//MlModeEntryType",
                                                                                                   "entry_node_id_attrib": "@EntryNo",
                                                                                                   "sub_node_xpath": "./MlModeScanType"}),
                              "Delay Time (s)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//StartDelay",
                                                                                                "entry_node_xpath": ".//MlModeEntryType",
                                                                                                "entry_node_id_attrib": "@EntryNo",
                                                                                                "sub_node_xpath": "./MlModeScanType"}),
                              "Pitch": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//PitchFactor",
                                                                                       "entry_node_xpath": ".//MlModeEntryType",
                                                                                       "entry_node_id_attrib": "@EntryNo",
                                                                                       "sub_node_xpath": "./MlModeScanType"}),
                              # "Slice No (Nominal)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//NoOfSlicesEffective",
                              #                                                                       "entry_node_xpath": ".//MlModeEntryType",
                              #                                                                       "entry_node_id_attrib": "@EntryNo",
                              #                                                                       "sub_node_xpath": "./MlModeScanType"}),
                              "Slice No (Actual)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//NoOfSlicesActual",
                                                                                                   "entry_node_xpath": ".//MlModeEntryType",
                                                                                                   "entry_node_id_attrib": "@EntryNo",
                                                                                                   "sub_node_xpath": "./MlModeScanType"}),
                              "Slice Width (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//SliceWidthCollimated",
                                                                                             "entry_node_xpath": ".//MlModeEntryType",
                                                                                             "entry_node_id_attrib": "@EntryNo",
                                                                                             "sub_node_xpath": "./MlModeScanType"}),
                              # "Table Feed/Rotation (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//SpiralFeedRot",
                              #                                                                             "entry_node_xpath": ".//MlModeEntryType",
                              #                                                                             "entry_node_id_attrib": "@EntryNo",
                              #                                                                             "sub_node_xpath": "./MlModeScanType"}),
                              "Scan FOV (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//FOVLimitForThreshold",
                                                                                               "entry_node_xpath": ".//MlModeEntryType",
                                                                                               "entry_node_id_attrib": "@EntryNo",
                                                                                               "sub_node_xpath": "./MlModeScanType"}),
                              "No of Scans": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//NoOfScans",
                                                                                             "entry_node_xpath": ".//MlModeEntryType",
                                                                                             "entry_node_id_attrib": "@EntryNo",
                                                                                             "sub_node_xpath": "./MlModeScanType"}),
                              }

de_scan_lookup_tbl = {"Range": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//RangeName",
                                                                               "entry_node_xpath": ".//MlModeEntryType",
                                                                               "entry_node_id_attrib": "@EntryNo",
                                                                               "sub_node_xpath": "./MlModeScanType"}),
                      # "Scan Mode": ("calculate_scan_para_Siemens_Force", {}),
                      "Reference kVp": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//QualityReferenceVoltage",
                                                                                       "entry_node_xpath": ".//MlModeEntryType",
                                                                                       "entry_node_id_attrib": "@EntryNo",
                                                                                       "sub_node_xpath": "./MlModeScanType"}),
                      "kVp": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//Voltage",
                                                                             "entry_node_xpath": ".//MlModeEntryType",
                                                                             "entry_node_id_attrib": "@EntryNo",
                                                                             "sub_node_xpath": "./MlModeScanType"}),
                      "Qref mAs": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//QualityReferencemAs",
                                                                                  "entry_node_xpath": ".//MlModeEntryType",
                                                                                  "entry_node_id_attrib": "@EntryNo",
                                                                                  "sub_node_xpath": "./MlModeScanType"}),
                      "Eff. mAs": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//EffectiveMAs",
                                                                                  "entry_node_xpath": ".//MlModeEntryType",
                                                                                  "entry_node_id_attrib": "@EntryNo",
                                                                                  "sub_node_xpath": "./MlModeScanType"}),
                      "Auto kV Mode": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//AutokVMode",
                                                                                      "entry_node_xpath": ".//MlModeEntryType",
                                                                                      "entry_node_id_attrib": "@EntryNo",
                                                                                      "sub_node_xpath": "./MlModeScanType"}),
                      "Auto kV Tissue": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//AutokVOptiCriteria",
                                                                                        "entry_node_xpath": ".//MlModeEntryType",
                                                                                        "entry_node_id_attrib": "@EntryNo",
                                                                                        "sub_node_xpath": "./MlModeScanType"}),
                      "Auto kV Min": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//AutokVVoltageMin",
                                                                                     "entry_node_xpath": ".//MlModeEntryType",
                                                                                     "entry_node_id_attrib": "@EntryNo",
                                                                                     "sub_node_xpath": "./MlModeScanType"}),
                      "Auto kV Max": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//AutokVVoltageMax",
                                                                                     "entry_node_xpath": ".//MlModeEntryType",
                                                                                     "entry_node_id_attrib": "@EntryNo",
                                                                                     "sub_node_xpath": "./MlModeScanType"}),
                      "Dose Modulation On/Off": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//Care",
                                                                                                "entry_node_xpath": ".//MlModeEntryType",
                                                                                                "entry_node_id_attrib": "@EntryNo",
                                                                                                "sub_node_xpath": "./MlModeScanType"}),
                      "Dose Modulation": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//CareDoseType",
                                                                                         "entry_node_xpath": ".//MlModeEntryType",
                                                                                         "entry_node_id_attrib": "@EntryNo",
                                                                                         "sub_node_xpath": "./MlModeScanType"}),
                      "Rotation Time (s)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//ExposureTimePerRotation",
                                                                                           "entry_node_xpath": ".//MlModeEntryType",
                                                                                           "entry_node_id_attrib": "@EntryNo",
                                                                                           "sub_node_xpath": "./MlModeScanType"}),
                      "Delay Time (s)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//StartDelay",
                                                                                        "entry_node_xpath": ".//MlModeEntryType",
                                                                                        "entry_node_id_attrib": "@EntryNo",
                                                                                        "sub_node_xpath": "./MlModeScanType"}),
                      "Pitch": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//PitchFactor",
                                                                               "entry_node_xpath": ".//MlModeEntryType",
                                                                               "entry_node_id_attrib": "@EntryNo",
                                                                               "sub_node_xpath": "./MlModeScanType"}),
                      "Slice No (Nominal)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//NoOfSlicesEffective",
                                                                                            "entry_node_xpath": ".//MlModeEntryType",
                                                                                            "entry_node_id_attrib": "@EntryNo",
                                                                                            "sub_node_xpath": "./MlModeScanType"}),
                      "Slice No (Actual)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//NoOfSlicesActual",
                                                                                           "entry_node_xpath": ".//MlModeEntryType",
                                                                                           "entry_node_id_attrib": "@EntryNo",
                                                                                           "sub_node_xpath": "./MlModeScanType"}),
                      "Slice Width (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//SliceWidthCollimated",
                                                                                          "entry_node_xpath": ".//MlModeEntryType",
                                                                                          "entry_node_id_attrib": "@EntryNo",
                                                                                          "sub_node_xpath": "./MlModeScanType"}),
                      "Table Feed/Rotation (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//SpiralFeedRot",
                                                                                                  "entry_node_xpath": ".//MlModeEntryType",
                                                                                                  "entry_node_id_attrib": "@EntryNo",
                                                                                                  "sub_node_xpath": "./MlModeScanType"}),
                      "Scan FOV (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//FOVLimitForThreshold",
                                                                                       "entry_node_xpath": ".//MlModeEntryType",
                                                                                       "entry_node_id_attrib": "@EntryNo",
                                                                                       "sub_node_xpath": "./MlModeScanType"}),
                      "Max recon FOV for TF (mm)": ("get_para_from_indiv_prot_xml_Siemens_Force", {"para_xpath": ".//FoVMaxFlashTotal",
                                                                                                   "entry_node_xpath": ".//MlModeEntryType",
                                                                                                   "entry_node_id_attrib": "@EntryNo",
                                                                                                   "sub_node_xpath": "./MlModeScanType"}),
                      }

# save lookup tables into json
# save lookup tables to json files
print("saved topo_lookup_tbl to ./para_lookup_tbl/topo_lookup_tbl_S.json")
with open('./para_lookup_tbl/topo_lookup_tbl_S.json', 'w') as fp:
    json.dump(topo_lookup_tbl, fp, indent=4)

print("saved scan_lookup_tbl to ./para_lookup_tbl/scan_lookup_tbl_S.json")
with open('./para_lookup_tbl/scan_lookup_tbl_S.json', 'w') as fp:
    json.dump(scan_lookup_tbl, fp, indent=4)

print("saved recon_lookup_tbl to ./para_lookup_tbl/recon_lookup_tbl_S.json")
with open('./para_lookup_tbl/recon_lookup_tbl_S.json', 'w') as fp:
    json.dump(recon_lookup_tbl, fp, indent=4)

print("saved monitoring_scan_lookup_tbl to ./para_lookup_tbl/monitoring_scan_lookup_tbl_S.json")
with open('./para_lookup_tbl/monitoring_scan_lookup_tbl_S.json', 'w') as fp:
    json.dump(monitoring_scan_lookup_tbl, fp, indent=4)
