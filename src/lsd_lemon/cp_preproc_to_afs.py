import os
import shutil
import sys

with open('/nobackup/ilz2/LEMON_LSD/rescue_julia/subjects.txt', 'r') as f:
    subjects = [line.strip() for line in f]
subjects.sort()

subjects.remove('24051')
afs_dir = '/afs/cbs.mpg.de/projects/mar004_lsd-lemon-preproc/probands/%s/preprocessed/lsd_resting/'
data_dir = '/nobackup/ilz2/LEMON_LSD/rescue_julia/%s/preprocessed/lsd_resting/'

for sub in subjects:
    print sub
    if os.path.isdir(afs_dir % sub):
        shutil.rmtree(afs_dir % sub)
    #os.mkdir(afs_dir % sub)
    shutil.copytree(data_dir % sub, afs_dir % sub)