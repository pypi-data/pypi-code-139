import os
import shutil
import sys
from phybers.clustering.hclust import mainHClust
from phybers.clustering.ffclust import mainFFClust

pathname = os.path.dirname(__file__)
sys.path.insert(0,os.path.join(pathname,'hclust'))

def hclust(fiber_input,work_dir,MaxDistance_Threshold,var,PartDistance_Threshold):
    
    if os.path.exists(work_dir):   
      shutil.rmtree(work_dir)
    
    os.makedirs(work_dir)
    
    #final_bundles_dir = work_dir + '/FinalBundles'
    final_bundles_dir = os.path.join(work_dir, 'FinalBundles')

    os.makedirs(final_bundles_dir, exist_ok=True)

    #final_bundles21p_dir = work_dir + '/FinalBundles21p'
    final_bundles21p_dir = os.path.join(work_dir, 'FinalBundles21p')    
    os.makedirs(final_bundles21p_dir, exist_ok=True)
    
    #final_centroids_dir = work_dir + '/FinalCentroids'    
    final_centroids_dir = os.path.join(work_dir, 'FinalCentroids') 
    os.makedirs(final_centroids_dir, exist_ok=True)
    
    #outfile_dir= work_dir + '/outfile'
    outfile_dir= os.path.join(work_dir, 'outfile')
    os.makedirs(outfile_dir, exist_ok=True)
    
    
    mainHClust.hierarchical(fiber_input,outfile_dir,str(MaxDistance_Threshold))
    mainHClust.particional_hierarchical(fiber_input,outfile_dir, PartDistance_Threshold,var,final_bundles_dir)
    
def ffclust(infile, output_directory, thr_assign=6, thr_join=6):
    mainFFClust.fastfiber(infile, output_directory, thr_assign, thr_join)
