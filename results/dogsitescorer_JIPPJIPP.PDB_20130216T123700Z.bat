set COMPAS_DP_MAP_CUTOFF 3.0
set COMPAS_DP_NUM_FILTER 1.75
set COMPAS_IP_RANK 0
set COMPAS_IP_POC_ALG 3
set COMPAS_IP_NEIGHBORS 5
set COMPAS_IP_MONOMER 1
set COMPAS_DP_GRID_DELTA 0.6
set COMPAS_IP_SPOC_MERGE 1
set COMPAS_DP_CL_CUTOFF -0.01
set COMPAS_IP_SPOC_OUT 1
set COMPAS_DP_FIX_CL -0.165
SETVAR $(complex) "tmp/cache/JIPPJIPP.PDB_20130216T123700Z.pdb"
SETVAR $(result) "descriptor_data_JIPPJIPP.PDB_20130216T123700Z.txt"
SETVAR $(result_dir) "results/"
SET VERBOSITY 5
 REC
  read $(complex)
 COMPASITE
 POCKET 0
  SELOUTP $(result_dir)$(result) o %
  DESCRIPT
 WRITE_DESC $(result_dir)PocXls_$(result) 0 1
 WRITE_DESC $(result_dir)SpocXls_$(result) 1 1
  WRITE_PDB $(result_dir)poc_reduced_JIPPJIPP.PDB_20130216T123700Z 50 0 1
  WRITE_PDB $(result_dir)atms_JIPPJIPP.PDB_20130216T123700Z 50 1
 MAIN
  DELALL
