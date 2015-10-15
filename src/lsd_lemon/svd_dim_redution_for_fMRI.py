'''
Created on 25.09.2015

@author: sven
'''

import os
import numpy as np
import nibabel as nib
import h5py


if __name__ == '__main__':
    
    min_var_expl = 0.999 # the minimum variance that should still be explained by the retained SVD components
    
    data_folder = '/scr/ilz2/LEMON_LSD/data4sven/mni3mm/'
    subject_list= '/scr/ilz2/LEMON_LSD/data4sven/subjects4sven.txt'

    with open(subject_list, 'r') as f:
        subject_idx_list = [line.strip() for line in f]
    
    # create the mask from the T1 image
    T1_image_file = os.path.join(data_folder,'MNI152_T1_3mm_brain.nii.gz')
    T1_img = nib.load(T1_image_file).get_data()
    mask = T1_img > 0.0
    mask_rs = mask.flatten('F')
    
    #subject_idx_list = [
                    #'23302',
                    #'23574',
                    #'23651',
                    #'23700',
                    #'23708',
                    #'23965',
                    #'24720',
                    #'24844',
                    #'24877',
                    #'26526',
                    #'26803',
                    #'26843',
                    #]
    
    for sbj_idx in subject_idx_list:
        
        print 'processing sbj '+sbj_idx
        
        # construct the file name
        file_name = os.path.join(data_folder, sbj_idx+'_rest_preprocessed2mni.nii.gz')
        
        # load the image data
        print ' --> loading the fMRI data'
        img = nib.load(file_name)
        X = img.get_data()
         
        # reshape image and apply the mask
        new_shape = (np.prod(X.shape[0:3]), X.shape[3])
        X = X.reshape(new_shape, order='F')
        X = X[mask_rs, :].squeeze()
         
        # normalize the time-courses, i.e. z-score the data
        print ' --> z-scoring'
        stds = X.std(axis=1, keepdims=True)
        X = (X - X.mean(axis=1, keepdims=True)) / stds    
        
        # apply the singular value decomposition
        print ' --> computing SVD'
        V, s, U = np.linalg.svd(X, full_matrices=False)
        
        # determine the number of SVD components to keep
        eigenvals = s**2
        n_components = np.where(np.cumsum(eigenvals) / np.sum(eigenvals) >= min_var_expl)[0][0]
        print ' --> keeping n = %d SVD components' % n_components
        
        # reduce the SVD results
        V = V[:,0:n_components]
        U = U[0:n_components,:]
        s = s[0:n_components]
        
        print ' --> saving the results'
        # save as hdf5
        file_name = os.path.join(data_folder, sbj_idx+'_rest_preprocessed2mni_masked_zscored_SVD.hdf5')
        with h5py.File(file_name, 'w') as f:
            g = f.create_group("svd_results")
            g.create_dataset('V', data=V)
            g.create_dataset('U', data=U)
            g.create_dataset('s', data=s)
            g.create_dataset('eigenvalues', data=eigenvals)
            f.create_dataset('voxelwise_standard_deviation', data=stds)
            
    
        
    print 'done'    
        
        



# ---- old code ----

#         # save the SVD results as csv files
#         file_name = os.path.join(data_folder, sbj_idx+'_rest_preprocessed2mni_SVD_U.csv')
#         np.savetxt(file_name, U, delimiter=",")
#         file_name = os.path.join(data_folder, sbj_idx+'_rest_preprocessed2mni_SVD_V.csv')
#         np.savetxt(file_name, V, delimiter=",")
#         file_name = os.path.join(data_folder, sbj_idx+'_rest_preprocessed2mni_SVD_s.csv')
#         np.savetxt(file_name, s, delimiter=",")
#         # save the SVD results as numpy arrays
#         file_name = os.path.join(data_folder, sbj_idx+'_rest_preprocessed2mni_SVD_U')
#         np.save(file_name, U)
#         file_name = os.path.join(data_folder, sbj_idx+'_rest_preprocessed2mni_SVD_V')
#         np.save(file_name, V)
#         file_name = os.path.join(data_folder, sbj_idx+'_rest_preprocessed2mni_SVD_s')
#         np.save(file_name, s)
        