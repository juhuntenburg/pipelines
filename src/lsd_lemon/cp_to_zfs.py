import os
import shutil
import sys
import pandas as pd


# copy also nifti files of those subjects which have not been (successfully) preprocessed
subjects = list(pd.read_csv('/home/raid3/huntenburg/workspace/lsd_data_paper/lsd_preproc.csv', dtype='str')['ID'])
subjects.sort()

afs_dir = '/afs/cbs.mpg.de/projects/mar004_lsd-lemon-preproc/probands/%s/'
fix_dir = '/nobackup/ilz2/fix_mni/%s/'
zfs_dir = '/data/pt_mar004/mri/%s/'#'/data/mar004_lsd-lemon-preproc/%s/'
freesurfer_dir = '/data/pt_mar004/mri/freesurfer/%s'

for sub in subjects:
    
    old_dir = afs_dir%sub
    new_dir = zfs_dir%sub
    
    # check if already copied
    if os.path.isdir(new_dir):
        print "subject %s exists"%sub
        
    else: 
        print "copying %s"%sub
        # make subject dir
        os.mkdir(new_dir)
        
        # make nifti dir and copy data
        print '...nifti'
        shutil.copytree(os.path.join(old_dir, 'nifti'), os.path.join(new_dir, 'nifti'))
        
        # make freesurfer dir and copy data
        print '...freesurfer'
        shutil.copytree(os.path.join(old_dir, 'freesurfer'), os.path.join(new_dir, 'freesurfer'))
        
        # create symlink in freesurfer dir
        os.symlink(os.path.join(new_dir, 'freesurfer'), freesurfer_dir%sub)
        
        # make preprocessed folder and copy
        os.mkdir(os.path.join(new_dir, 'preprocessed'))
        
        # anatomical files
        print '...anatomy'
        old_anat = os.path.join(old_dir, 'preprocessed', 'anat')
        new_anat = os.path.join(new_dir, 'preprocessed', 'anat')
        fix_anat = os.path.join(fix_dir%sub, 'preprocessed', 'anat')
        os.mkdir(new_anat)
        shutil.copyfile(os.path.join(old_anat, 'T1.nii.gz'), 
                        os.path.join(new_anat, 'T1.nii.gz'))
        shutil.copyfile(os.path.join(old_anat, 'T1_brain_wmedge.nii.gz'), 
                        os.path.join(new_anat, 'T1_brain_wmedge.nii.gz'))
        shutil.copyfile(os.path.join(old_anat, 'T1_brain_mask.nii.gz'), 
                        os.path.join(new_anat, 'func_mask.nii.gz'))
        
        # new MNI transformation files
        shutil.copyfile(os.path.join(fix_anat, 'T1_brain.nii.gz'), 
                        os.path.join(new_anat, 'T1_brain.nii.gz'))
        shutil.copyfile(os.path.join(fix_anat, 'T1_brain2mni.nii.gz'), 
                        os.path.join(new_anat, 'T1_brain2mni.nii.gz'))
        shutil.copytree(os.path.join(fix_anat, 'transforms2mni'), 
                        os.path.join(new_anat, 'transforms2mni'))
        
        # lsd resting files
        print '...lsd'
        old_lsd = os.path.join(old_dir, 'preprocessed', 'lsd_resting')
        new_lsd = os.path.join(new_dir, 'preprocessed', 'lsd_resting')
        fix_lsd = os.path.join(fix_dir%sub, 'preprocessed', 'lsd_resting')
        if os.path.isdir(old_lsd):
            os.mkdir(new_lsd)
        for sess in ['rest1a', 'rest1b', 'rest2a', 'rest2b']:
            if os.path.isdir(os.path.join(old_lsd, sess)):
                os.mkdir(os.path.join(new_lsd, sess))
                shutil.copyfile(os.path.join(old_lsd, sess, 'rest_preprocessed.nii.gz'), 
                                os.path.join(new_lsd, sess, 'rest_preprocessed.nii.gz'))
                shutil.copytree(os.path.join(old_lsd, sess, 'coregister'), 
                                os.path.join(new_lsd, sess, 'coregister'))
                shutil.copytree(os.path.join(old_lsd, sess, 'denoise'), 
                                os.path.join(new_lsd, sess, 'denoise'))
                shutil.copytree(os.path.join(old_lsd, sess, 'realign'), 
                                os.path.join(new_lsd, sess, 'realign'))
                
                # new MNI transformed files
                shutil.copyfile(os.path.join(fix_lsd, sess, 'rest_preprocessed2mni.nii.gz'), 
                                os.path.join(new_lsd, sess, 'rest_preprocessed2mni.nii.gz'))
        
                
        # lemon resting files
#         old_lsd = os.path.join(old_dir, 'preprocessed', 'lemon_resting')
#         new_lsd = os.path.join(new_dir, 'preprocessed', 'lemon_resting')
#         if os.path.isdir(old_lemon):
#             os.mkdir(new_lemon)
#             shutil.copyfile(os.path.join(old_lemon, 'rest_preprocessed.nii.gz'), 
#                             os.path.join(new_lemon, 'rest_preprocessed.nii.gz'))
#             shutil.copytree(os.path.join(old_lemon, 'coregister'), 
#                             os.path.join(new_lemon, 'coregister'))
#             shutil.copytree(os.path.join(old_lemon, 'denoise'), 
#                             os.path.join(new_lemon, 'denoise'))
#             shutil.copytree(os.path.join(old_lemon, 'realign'), 
#                             os.path.join(new_lemon, 'realign'))