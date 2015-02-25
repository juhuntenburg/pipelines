from nipype.pipeline.engine import Node, Workflow
import nipype.interfaces.utility as util
from conversion.dcmconvert import create_dcmconvert_pipeline
import nipype.interfaces.io as nio

'''
Workflow to access dicom files from xnat and convert them to nifti.
'''

def create_conversion(name, subject, scans, working_dir, out_dir, folder, data_dir, experiment):

    convert = Workflow(name=name)
    convert.base_dir = working_dir
    convert.config['execution']['crashdump_dir'] = convert.base_dir + "/crash_files"
    
    
    scan_key=scans.keys()
    scan_val=[]
    for i in range(len(scans.values())):
        scan_val.append(str(int(scans.values()[i])))
 
    
    # infosource to iterate over scans
    scan_infosource = Node(util.IdentityInterface(fields=['scan_key', 'scan_val']), 
                      name='scan_infosource')
    scan_infosource.iterables=[('scan_key', scan_key), ('scan_val', scan_val)]
    scan_infosource.synchronize=True
    
    
    # select files
    templates={'dicom': '{subject}/{exp}/{scan}/DICOM/*'}
    selectfiles = Node(nio.SelectFiles(templates,
                                       base_directory=data_dir),
                       name="selectfiles")
    selectfiles.inputs.subject=subject
    selectfiles.inputs.exp=experiment
    convert.connect([(scan_infosource, selectfiles, [('scan_val', 'scan')])])
    
    
    # xnat source
#     xnatsource = Node(nio.XNATSource(infields=['project_id', 'subject_id', 
#                                            'exp_id', 'scan_id'],
#                                  outfields=['dicom'],
#                                  server=xnat_server,
#                                  user=xnat_user,
#                                  pwd=xnat_pass, 
#                                  cache_dir=working_dir),
#               name='xnatsource')
#     
#     xnatsource.inputs.query_template=('/projects/%s/subjects/%s/experiments/%s/scans/%d/resources/DICOM/files')#files')
#     xnatsource.inputs.query_template_args['dicom']=[['project_id', 'subject_id', 'exp_id', 'scan_id']]
#     xnatsource.inputs.project_id = project_id
#     xnatsource.inputs.subject_id = subject
#     xnatsource.inputs.exp_id = exp_id
#     convert.connect([(scan_infosource, xnatsource, [('scan_val', 'scan_id')])])
    
    
    # workflow to convert dicoms
    dcmconvert=create_dcmconvert_pipeline()
    convert.connect([(scan_infosource, dcmconvert, [('scan_key', 'inputnode.filename')]),
                     (selectfiles, dcmconvert, [('dicom', 'inputnode.dicoms')])])
    
    
    # xnat sink
    sink = Node(nio.DataSink(base_directory=out_dir,
                             parameterization=False),
                    name='sink')
    
    convert.connect([(dcmconvert, sink, [('outputnode.nifti', folder)])])
    
    #convert.run() 
    #convert.run(plugin='CondorDAGMan')
    convert.run(plugin='MultiProc')