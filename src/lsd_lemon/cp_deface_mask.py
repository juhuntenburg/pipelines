import os
import shutil


path_template = '/nobackup/adenauer2/marcel/LSD/LEMON_LSD/%s/ses-%s/anat/'
#all_imgs = os.listdir('/nobackup/ilz2/defacing/collect_output/')
all_imgs = ['/nobackup/ilz2/defacing/collect_output/sub-25004_ses-02_acq-mp2rage_defacemask.nii.gz']

#os.chdir('/nobackup/ilz2/defacing/collect_output/sub-25004_ses-02_acq-mp2rage_defacemask.nii.gz')
#if len(all_imgs) != 317:
#    print 'wrong length'
#else:
#    print 'correct length'
     
for img in all_imgs: 
    sub = img.split('-')[1].split('_')[0]
    sess = img.split('-')[2].split('_')[0]
    new_path = path_template % (sub, sess)
    print img
    print new_path
    shutil.copy2(img, new_path)