#from structural_cbstools import create_structural
from structural import create_structural
import sys

'''
Meta script to run structural preprocessing
------------------------------------------
Can run in two modes:
python run_structural.py s {subject_id}
python run_structural.py f {text file containing list of subjects}
'''

mode=sys.argv[1]

if mode == 's':
    subjects=[sys.argv[2]]
elif mode == 'f':
    with open(sys.argv[2], 'r') as f:
        subjects = [line.strip() for line in f]

for subject in subjects:
    
    print 'Running subject '+subject
    
    working_dir = '/nobackup/ilz2/LEMON_LSD/rescue_julia/working_dir/' +subject+'/' 
    data_dir = '/nobackup/ilz2/LEMON_LSD/rescue_julia/'+subject+'/'
    out_dir = '/nobackup/ilz2/LEMON_LSD/rescue_julia/'+subject+'/'
    freesurfer_dir = '/nobackup/ilz2/LEMON_LSD/rescue_julia/freesurfer/' 
    standard_brain = '/usr/share/fsl/5.0/data/standard/MNI152_T1_1mm_brain.nii.gz'
    
    create_structural(subject=subject, working_dir=working_dir, data_dir=data_dir, 
                freesurfer_dir=freesurfer_dir, out_dir=out_dir,
                standard_brain=standard_brain)
    