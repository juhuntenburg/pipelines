import os
import shutil
import pandas as pd
#sub-010233/func/sub-010233_ses-02_task-rest_acq-PA_run-02_MNI2mm.nii.gz

source_func = '/nobackup/ilz2/fix_mni/%s/preprocessed/lsd_resting/%s/'
#source_noise = '/afs/cbs.mpg.de/projects/mar004_lsd-lemon-preproc/probands/%s/preprocessed/lsd_resting/%s/denoise/regress/noise_regressor.txt'
source_anat = '/nobackup/ilz2/fix_mni/%s/preprocessed/anat/'
#source_qc = '/afs/cbs.mpg.de/projects/mar004_lsd-lemon-preproc/results/reports/lsd_new/%s_%s_report.pdf'
mp2rage_sess = '/nobackup/adenauer2/marcel/LSD/MPI_Leipzig_MindBodyBrain/sub-%s/ses-%s/anat/sub-%s_ses-%s_acq-mp2rage_defacemask.nii.gz'
dest = '/data/pt_gr_margulies-internal1/derivatives/sub-%s'

#rest_template = dest + "sub-%s/func/sub-%s_ses-02_task-rest_%s_native.nii.gz"
rest_mni_template = dest + "/func/sub-%s_ses-02_task-rest_%s_MNI2mm.nii.gz"
#noise_template = dest + "sub-%s/func/sub-%s_ses-02_task-rest_%s_confounds.txt"
#qc_template = dest + "sub-%s/func/sub-%s_ses-02_task-rest_%s_QC.pdf"
brain_template = dest + "/anat/sub-%s_ses-%s_acq-mp2rage_brain.nii.gz"

subjects_lsd = list(pd.read_csv('/home/raid3/huntenburg/workspace/lsd_data_paper/lsd_preproc.csv', dtype='str')['ID'])
subjects_lsd.sort()

lut = pd.read_csv('/home/raid3/huntenburg/workspace/lsd_data_paper/lookup_table.csv', dtype='str')

for sub_old in subjects_lsd: 
    
    # translate subject id
    sub_new = list(lut.loc[lut['ids_probanden_db']==sub_old]['ids_xnat_publicp'])[0]
    
    # check which session the mp2rage was taken from  (13753)
    if os.path.isfile(mp2rage_sess % (sub_new, '02', sub_new, '02')):
        sess = '02'
    elif os.path.isfile(mp2rage_sess % (sub_new, '01', sub_new, '01')):
        sess = '01'
    else:
        print '%s no brainmask on adenauer' % sub_new
    
    
    # translate scans
    scans_old = ['rest1a', 'rest1b', 'rest2a', 'rest2b']
    scans_new = ['acq-AP_run-01', 'acq-PA_run-01', 'acq-AP_run-02', 'acq-PA_run-02']
    
    # for some subjects exclude scans
    if sub_old == '24945':
        scans_old = ['rest1a']
        scans_new = ['acq-AP_run-01']
    if sub_old == '25188':
        scans_old = ['rest1a', 'rest1b']
        scans_new = ['acq-AP_run-01', 'acq-PA_run-01']
    if sub_old in ['26500', '25019', '23700']:
        scans_old = ['rest1a', 'rest1b', 'rest2a']
        scans_new = ['acq-AP_run-01', 'acq-PA_run-01', 'acq-AP_run-02']


    ## testing if all files are there
    if not os.path.isfile(source_anat %(sub_old) + 'T1_brain.nii.gz'):
        print "%s brain missing" % sub_old
    
    for scan in range(len(scans_old)):
        
        #if not os.path.isfile(source_func %(sub_old, scans_old[scan]) + 'rest_preprocessed.nii.gz'):
        #    print "%s %s rest native missing" % (sub_old, scans_old[scan])
        if not os.path.isfile(source_func %(sub_old, scans_old[scan]) + 'rest_preprocessed2mni.nii.gz'):
            print "%s %s rest mni missing" % (sub_old, scans_old[scan])
        #if not os.path.isfile(source_noise %(sub_old, scans_old[scan])):
        #    print "%s %s nuissance missing" % (sub_old, scans_old[scan])
            
            
    ### actual copying
    sub_folder = dest %(sub_new)
    func_folder = os.path.join(sub_folder, 'func')
    anat_folder = os.path.join(sub_folder, 'anat')
    if not os.path.isdir(sub_folder):
        os.mkdir(sub_folder)
    if not os.path.isdir(func_folder):
        os.mkdir(func_folder)
    if not os.path.isdir(anat_folder):
        os.mkdir(anat_folder)
      
    for scan in range(len(scans_old)):
          
        #if not os.path.isfile(rest_template % (sub_new, sub_new, scans_new[scan])): 
        #    print "copying rest %s %s to %s %s" % (sub_old, scans_old[scan], sub_new, scans_new[scan])
        #    shutil.copyfile(source_func %(sub_old, scans_old[scan]) + 'rest_preprocessed.nii.gz', rest_template % (sub_new, sub_new, scans_new[scan]))
        if not os.path.isfile(rest_mni_template % (sub_new, sub_new, scans_new[scan])): 
            print "copying rest mni %s %s to %s %s" % (sub_old, scans_old[scan], sub_new, scans_new[scan])
            shutil.copyfile(source_func %(sub_old, scans_old[scan]) + 'rest_preprocessed2mni.nii.gz', rest_mni_template % (sub_new, sub_new, scans_new[scan]))
        #if not os.path.isfile(noise_template % (sub_new, sub_new, scans_new[scan])):
        #    print "copying confounds %s %s to %s %s" % (sub_old, scans_old[scan], sub_new, scans_new[scan]) 
        #    shutil.copyfile(source_noise %(sub_old, scans_old[scan]), noise_template % (sub_new, sub_new, scans_new[scan]))
         
        #if not os.path.isfile(qc_template % (sub_new, sub_new, scans_new[scan])):
        #    print "copying QC %s %s to %s %s" % (sub_old, scans_old[scan], sub_new, scans_new[scan]) 
        #    shutil.copyfile(source_qc %(sub_old, scans_old[scan]), qc_template % (sub_new, sub_new, scans_new[scan]))
      
    if not os.path.isfile(brain_template % (sub_new, sub_new, sess)): 
        print "copying %s to %s brain, session is %s" % (sub_old, sub_new, sess)
        shutil.copyfile(source_anat %(sub_old) + 'T1_brain.nii.gz', brain_template % (sub_new, sub_new, sess))
     
            