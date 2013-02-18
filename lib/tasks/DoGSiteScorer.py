### Script to generate individual analyze_hyde_ppi.bat scripts



import sys
import os
from os import *
from subprocess import*
from math import *



def calculate_pockets_and_descriptors(pdb, timestamp):

  script = 'dogsitescorer_'+pdb+'_'+timestamp+'.bat'
  dogsite = './dogsite_server'
  i = Popen([dogsite, '-b', script])
  i.wait()


def generate_batch_script():
# args: pdb_id, chain1, pocLev, scoreType, gridSpacing, timestamp, chain_ID, lig_id 

  timestamp = sys.argv[6]
  pdb = sys.argv[1].upper()
  outfile = file("results/dogsitescorer_"+pdb+"_"+timestamp+".bat", 'w')

  mono= 0
  chain=0
  if(int(sys.argv[2])>0):
    mono=1
    chain=sys.argv[7]
  delta=sys.argv[5]  
  spoc_out=int(sys.argv[3])
  score_type=int(sys.argv[4])
  lig_id = int(sys.argv[8])

  # set parameters
  outfile.write("set COMPAS_DP_MAP_CUTOFF 3.0\n")
  outfile.write("set COMPAS_DP_NUM_FILTER 1.75\n")
  outfile.write("set COMPAS_IP_RANK 0\n")
  outfile.write("set COMPAS_IP_POC_ALG 3\n")
  outfile.write("set COMPAS_IP_NEIGHBORS 5\n")
  outfile.write("set COMPAS_IP_MONOMER "+str(mono)+"\n")
  outfile.write("set COMPAS_DP_GRID_DELTA "+str(delta)+"\n")
  outfile.write("set COMPAS_IP_SPOC_MERGE 1\n")
  outfile.write("set COMPAS_DP_CL_CUTOFF -0.01\n")
  outfile.write("set COMPAS_IP_SPOC_OUT "+str(spoc_out)+"\n")
  outfile.write("set COMPAS_DP_FIX_CL -0.165\n")

  outfile.write("SETVAR $(complex) \"tmp/cache/"+pdb+"_"+timestamp+".pdb\"\n")
  outfile.write("SETVAR $(result) \"descriptor_data_"+pdb+"_"+timestamp+".txt\"\n")
  outfile.write("SETVAR $(result_dir) \"results/\"\n")

  outfile.write("SET VERBOSITY 5\n")
  outfile.write(" REC\n")
  outfile.write("  read $(complex)\n")
  outfile.write(" COMPASITE\n")
  if(mono==1):
    outfile.write(" POCKET "+chain+"\n")
  else:
    outfile.write("POCKET\n")
  outfile.write("  SELOUTP $(result_dir)$(result) o %\n")
  if(lig_id>=0):
    outfile.write("  LIG_CHECK \"./downloads/"+pdb+"_LIG_"+timestamp+".mol2\"\n")
  outfile.write("  DESCRIPT\n")
  #if(spoc_out==0):
  #pocket based 
  outfile.write(" WRITE_DESC $(result_dir)PocXls_$(result) 0 1\n")
  if(spoc_out==1): #else:
    outfile.write(" WRITE_DESC $(result_dir)SpocXls_$(result) 1 1\n")
  #write pdb files
  #outfile.write("  WRITE_PDB $(result_dir)poc_"+pdb+"_"+timestamp+" 50 0 0\n")
  outfile.write("  WRITE_PDB $(result_dir)poc_reduced_"+pdb+"_"+timestamp+" 50 0 1\n")
  outfile.write("  WRITE_PDB $(result_dir)atms_"+pdb+"_"+timestamp+" 50 1\n")   
  #if drug chosen
  if(score_type==1):
    #pocket based
    #if(spoc_out==0):
    outfile.write("  WRITE_SVM 0 results/myLibsvmPoc_"+pdb+"_"+timestamp+".txt\n")
    #extern call off svm script
    outfile.write("  !./models/DoGSiteScorer.sh results/myLibsvmPoc_"+pdb+"_"+timestamp+" svmModelPoc ./models\n") 
    if(spoc_out==1): #else:
      #write svm file subpocket
       outfile.write("  WRITE_SVM 1 results/myLibsvmSpoc_"+pdb+"_"+timestamp+".txt\n")
      #extern call off svm script
       outfile.write("  !./models/DoGSiteScorer.sh results/myLibsvmSpoc_"+pdb+"_"+timestamp+" svmModelSPoc4 ./models \n")
  outfile.write(" MAIN\n")
  outfile.write("  DELALL\n")

  outfile.close()

  calculate_pockets_and_descriptors(pdb, timestamp)

generate_batch_script()
