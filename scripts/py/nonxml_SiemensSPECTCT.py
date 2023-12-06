# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 12:23:18 2023

@author: CH226683
"""

import re
import pandas as pd

target_file = 'G:\\My Drive\\BCH\\Rotations\\Informatics\\CT wiki\\SPECT-CT_UserProtocols\\Import\MlAbdomen\ABDOMEN_OVER_55KG_CLASS_1_R.MlAdult'

with open(target_file) as f:
    lines = f.readlines()
    
res = [lines.index(i) for i in lines if 'PROTOCOL_ENTRY_NO' in i]

sub_protocol = []
prot_se_list=[]
prot_dict_list=[]

for i in range(0,len(res)):
    if i == len(res)-1:
        sub_protocol.append(lines[res[i]:])
    else:
        sub_protocol.append(lines[res[i]:res[i+1]])
    
    if any('MlTopo' in sub for sub in sub_protocol[i]) == True:              
        range_name = list(filter(lambda x: 'RangeName[' in x, sub_protocol[i]))[0]
        rn = range_name.split(":",1)[1].strip()
        
        angle_type = list(filter(lambda x: 'AngleType' in x, sub_protocol[i]))[0]
        at = angle_type.split(":",1)[1].strip()
        
       # kvp ma kernel series description
        kvp = list(filter(lambda x: re.match('^Voltage:',x), sub_protocol[i]))[0]
        kv = kvp.split(":",1)[1].strip()
        
        current = list(filter(lambda x: re.match('^Current:',x), sub_protocol[i]))[0]
        ma = current.split(":",1)[1].strip()
        
        kernel = list(filter(lambda x: 'Kernel' in x, sub_protocol[i]))[0]
        kl = kernel.split(":",1)[1].strip()
        
        series_desc = list(filter(lambda x: 'SeriesDescription' in x, sub_protocol[i]))[0]
        sd = series_desc.split(":",1)[1].strip()
        
        dict1 = {'Range': rn, 'Tube Position': at, 'kVp': kv, 'mA': ma,
                 'Kernel': kl, 'Series Description': sd}
        
        scan_se = pd.Series(dict1)
        prot_se_list.append(scan_se)
        prot_dict_list.append(dict1)
        
    else:
        range_name = list(filter(lambda x: 'RangeName[' in x, sub_protocol[i]))[0]
        rn = range_name.split(":",1)[1].strip()
        
        ref_kvp = list(filter(lambda x: 'AutokVVoltage:' in x, sub_protocol[i]))[0]
        rkv = ref_kvp.split(":",1)[1].strip()
        
       # kvp ma kernel series description
        kvp = list(filter(lambda x: re.match('^Voltage:',x), sub_protocol[i]))[0]
        kv = kvp.split(":",1)[1].strip()
        
        q_r_mas = list(filter(lambda x: re.match('^AECReferenceMAs:',x), sub_protocol[i]))[0]
        qrmas = q_r_mas.split(":",1)[1].strip()
        
        eff_mas = list(filter(lambda x: re.match('^EffectiveMAs:',x), sub_protocol[i]))[0]
        emas = eff_mas.split(":",1)[1].strip()
        
        akv_mode = list(filter(lambda x: re.match('^AutokV:',x), sub_protocol[i]))[0]
        akm = akv_mode.split(":",1)[1].strip()
        
        dose_mod_onoff = list(filter(lambda x: re.match('^DoseModulationType:',x), sub_protocol[i]))[0]
        dmoo = dose_mod_onoff.split(":",1)[1].strip()
        
        dose_mod = list(filter(lambda x: re.match('^AECDoseModulationType:',x), sub_protocol[i]))[0]
        dm = dose_mod.split(":",1)[1].strip()
        
        rot_time = list(filter(lambda x: re.match('^RotTime:',x), sub_protocol[i]))[0]
        rt = rot_time.split(":",1)[1].strip()
        
        delay_time = list(filter(lambda x: re.match('^StartDelay:',x), sub_protocol[i]))[0]
        dt = delay_time.split(":",1)[1].strip()
        
        pitch_factor = list(filter(lambda x: re.match('^PitchFactor:',x), sub_protocol[i]))[0]
        pf = pitch_factor.split(":",1)[1].strip()
        
        slice_nom = list(filter(lambda x: re.match('^SlicesPerScan:',x), sub_protocol[i]))[0]
        sn = slice_nom.split(":",1)[1].strip()
         
        slice_act = list(filter(lambda x: re.match('^NoOfSlicesAfterFusing:',x), sub_protocol[i]))[0]
        sa = slice_act.split(":",1)[1].strip()
        
        slice_width = list(filter(lambda x: re.match('^SliceDetector:',x), sub_protocol[i]))[0]
        sw = slice_width.split(":",1)[1].strip()
        
        feed_rot = list(filter(lambda x: re.match('^SpiralFeedRot:',x), sub_protocol[i]))[0]
        fr = feed_rot.split(":",1)[1].strip()
        
        scan_fov = list(filter(lambda x: re.match('^FOV:',x), sub_protocol[i]))[0]
        sf = scan_fov.split(":",1)[1].strip()
        
        #Auto kV Tissue, Auto kV Min, Auto kV Max, Max recon FOV for TF (mm)
        
        dict1 = {'Range': rn, 'Reference kVp': rkv, 'kVp': kv, 'Qref mAs': qrmas,
                 'Eff mAs': emas, 'Auto kV Mode': akm, 'Dose Modulation On/Off':dmoo,
                 'Dose Modulation': dm, 'Rotation Time (s)': rt, 'Delay Time (s)': dt,
                 'Pitch': pf, 'Slice No (Nominal)': sn, 'Slice No (Actual)': sa,
                 'Slice Width (mm)': sw, 'Table Feed/Rotation (mm)': fr,
                 'Scan FOV (mm)': sf}
        
        scan_se = pd.Series(dict1)
        prot_se_list.append(scan_se)
        prot_dict_list.append(dict1)
        ############################################################
        recon_inds = [j for j, s in enumerate(sub_protocol[i]) if 'MlModeRecon_Begin' in s]
        sub_recon = []
        
        for k in range(0,len(recon_inds)):
            if k == len(recon_inds)-1 or len(recon_inds) == 1:
                sub_recon.append(sub_protocol[i][recon_inds[k]:])
            else:
                sub_recon.append(sub_protocol[i][recon_inds[k]:recon_inds[k+1]])
            
            series_desc = list(filter(lambda x: 'SeriesDescription' in x, sub_recon[k]))[0]
            sd = series_desc.split(":",1)[1].strip()
            
            slice_thickness = list(filter(lambda x: re.match('^SliceEffective:',x), sub_recon[k]))[0]
            st = slice_thickness.split(":",1)[1].strip()
            
            slice_increment = list(filter(lambda x: re.match('^SliceEffectiveTiltCorrected:',x), sub_recon[k]))[0]
            si = slice_increment.split(":",1)[1].strip()
            
            kernel = list(filter(lambda x: 'Kernel' in x, sub_recon[k]))[0]
            kl = kernel.split(":",1)[1].strip()
            
            window_name = list(filter(lambda x: 'Window[' in x, sub_recon[k]))[0]
            wn = window_name.split(":",1)[1].strip()
            
            iter_rec_typ = list(filter(lambda x: re.match('^ReconMode',x), sub_recon[k]))[0]
            irt = iter_rec_typ.split(":",1)[1].strip()
            
            iter_rec_str = list(filter(lambda x: re.match('^ImageReconType:',x), sub_recon[k]))[0]
            irs = iter_rec_str.split(":",1)[1].strip()
            
            fov_hl = list(filter(lambda x: re.match('^FoVHorLength:',x), sub_recon[k]))[0]
            fhl = fov_hl.split(":",1)[1].strip()
            
            fov_vl = list(filter(lambda x: re.match('^FoVVertLength:',x), sub_recon[k]))[0]
            fvl = fov_vl.split(":",1)[1].strip()
            
            tr1 = list(filter(lambda x: re.match('^Transfer1:',x), sub_recon[k]))[0]
            t1 = tr1.split(":",1)[1].strip()
            
            tr2 = list(filter(lambda x: re.match('^Transfer2:',x), sub_recon[k]))[0]
            t2 = tr2.split(":",1)[1].strip()
            
            tr3 = list(filter(lambda x: re.match('^Transfer2:',x), sub_recon[k]))[0]
            t3 = tr3.split(":",1)[1].strip()
            
            dict2 = {'Series Description': sd, 'Slice Thickness': st, 'Slice Increment': si,
                     'Kernel': kl, 'Window Name': wn, 'Iter. Recon Type': irt, 'Iter. Recon Strength': irs,
                     'Hor FOV for Recon (mm)': fhl,'Vert FOV for Recon (mm)': fvl,
                     'Transfer1': t1,'Transfer2': t2,'Transfer3': t3}
            
            recon_se = pd.Series(dict1)
            prot_se_list.append(recon_se)
            prot_dict_list.append(dict2)