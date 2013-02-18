# -*- coding: utf-8 -*-
### input:  PDB-ID  Chain1  Chain2
###     1) download_pdbfile.py
###     2) give_numbers_to_chains.py
###   Process 1 and 2: chechpdb.py
###     3) analyze_hyde_ppi.bat
###     4) table_twostage_testdatei.py
###     5) classify_testdatei.py
###     6) alignment.py
### output: classification probabilities for stage 1 and 2 and the alignment results for the whole chains and the interface


import sys

import glob
import os
from os import*
from math import *
from subprocess import *
from os.path import *
from string import *

def make_druggability_prediction(pdb_id, timestamp, pocLev):
    
    if(int(pocLev)==0):
      stage2 = file("results/myLibsvmPoc_"+pdb_id+"_"+timestamp+".txt.predict", 'r')
    else:
      stage2 = file("results/myLibsvmSpoc_"+pdb_id+"_"+timestamp+".txt.predict", 'r')
    lines2 = stage2.readlines()
    counter=0
    drug_scores=[]
    for l2 in lines2:
      if(counter==0):
  counter+=1
      else:
  cur_line=l2.split(' ')
  drug_score = '%4.2f' %(float(cur_line[1]))
  drug_scores.append(drug_score)
  counter+=1
    stage2.close()
    return drug_scores

def fill_line(entry, pos):
    descr_arr=['Name', 'volume [&Aring;&sup3;]', 'surface [&Aring;&sup2;]', 'lipophilic surface [&Aring;&sup2;]','depth [&Aring;]', 'SimpleScore', 'Ligand coverage', 'Pocket coverage', '# pocket atoms', 'ellipsoid main axis ratio c/a',  'ellipsoid main axis ratio b/a', 'enclosure', '# carbons (C)', '# nitrogens (N)', '# oxygens', '# sulfors (S)', '# other elements', '# special amino acids', '# ALA', '# ARG', '# ASN', '# ASP', '# CYS', '# GLN', '# GLU', '# GLY', '# HIS', '# ILE', '# LEU', '# LYS', '# MET', '# PHE', '# PRO', '# SER', '# THR', '# TRP', '# TYR', '# VAL', '# hydrogen bond donors', '# hydrogen bond acceptors', '# metals', '# hydrophobic interactions', 'hydrophobicity ratio', 'apolar amino acid ratio','polar amino acid ratio', 'positive amino acid ratio', 'negative amino acid ratio','non']
    out=''
    out += '<tr> \n'
    out += '<td> ' + descr_arr[pos] + '</td>\n' 
    out += '<td> ' +  entry[pos]+ ' </td>\n' 
    out += '</tr> \n'  
    return out
    
def write_poc_results(pdb_id, timestamp, name, entries):
    #descr_arr=['Name', 'Volume [A3]', 'Surface [A2;]', 'Lipophilic surface [A2]','Depth [A]', 'SimpleScore', 'Ligand coverage', 'Pocket coverage', '# pocket atoms', 'ellipsoid main axis ration c/a',  'ellipsoid main axis ration b/a', 'surface to hull ratio', '# carbons (C)', '# nitrogens (N)', '# oxygens', '# sulfors (S)', '# other elements', '# special amino acids', '# ALA', '# ARG', '# ASN', '# ASP', '# CYS', '# GLN', '# GLU', '# GLY', '# HIS', '# ILE', '# LEU', '# LYS', '# MET', '# PHE', '# PRO', '# SER', '# THR', '# TRP', '# TYR', '# VAL', '# hydrogen bond donors', '# hydrogen bond acceptors', '# metals', '# hydrophobic interactions', 'hydrophobicity ratio', 'apolar amino acid ratio','polar amino acid ratio', 'positive amino acid ratio', 'negative amino acid ratio','non']
    
    poc_results = file('/home/other/dogsite/public_html/DoGSiteServer/results/results_'+pdb_id+'_'+timestamp+'_'+name[2]+'.html','w')  # writes the result html 
    poc_results.write('<?xml version="1.0" encoding="utf-8"?>\n')
    poc_results.write('<!DOCTYPE html\n')
    poc_results.write('    PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n')
    poc_results.write('    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n')
    poc_results.write(' <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">\n')
    poc_results.write('<head>\n')
    poc_results.write('<title>Descriptor results for '+name[2]+'</title><link rel="stylesheet" type="text/css" href="http://www.zbh.uni-hamburg.de/uploads/tf/zbh.css" />\n')
    poc_results.write(' </head>\n')
    poc_results.write(' <body>\n')
    poc_results.write("<br><font size=\"3\">Descriptor information for pocket %s of target %s<br>\n" %(name[2],pdb_id)) 
    if(float(entries[6])>0.):
      poc_results.write("<br><font size=\"3\">Ligand coverage %s percent and pocket coverage %s percent.<br>\n" %(entries[6],entries[7])) 
    #result table
    poc_results.write("<br><br>\n<table>\n")
    #poc_results.write('<td> Descriptor </td> <td> Value </td> \n')
    
    #make result table
    #first row
    poc_results.write('<tr> \n')
    # 1. row 1. column
    poc_results.write('<td align="center" valign="top"> \n')
    
    poc_results.write('Size and shape descriptors \n')
    #make result table
    poc_results.write("<br><br>\n<table border='3' frame='void'>\n")
    poc_results.write('<tr> \n')
    poc_results.write('<td> Descriptor </td> <td> Value </td> \n')
    poc_results.write('</tr> \n')
    for i in range(1,5):
      #vol, surf, lipo surf, depth
      poc_results.write(fill_line(entries, i))
    for i in range(9,12):
      #vell, surf gps
      poc_results.write(fill_line(entries, i))   
    poc_results.write('</table> \n')
    
    poc_results.write('<br><br>Functional group descriptors \n')
    #make result table
    poc_results.write("<br><br>\n<table border='3' frame='void'>\n")
    poc_results.write('<tr> \n')
    poc_results.write('<td> Descriptor </td> <td> Value </td> \n')
    poc_results.write('</tr> \n')
    for i in range(38,43):
      #donor, acc, ratios
      poc_results.write(fill_line(entries, i))  
    poc_results.write('</table> \n')
    
    poc_results.write('</td> \n')
    #poc_results.write('</tr> \n')
    
    # 1. row 2. column
    poc_results.write('<td  align="center"  valign="top"> \n')
    poc_results.write('Element descriptors \n')
    #make result table
    poc_results.write("<br><br>\n<table border='3' frame='void'>\n")
    poc_results.write('<tr> \n')
    poc_results.write('<td> Descriptor </td> <td> Value </td> \n')
    poc_results.write('</tr> \n')
    #nof atoms
    poc_results.write(fill_line(entries, 8))
    for i in range(12,17):
      # elements
      poc_results.write(fill_line(entries, i))
    poc_results.write('</table> \n')
    
    poc_results.write('<br><br><br>Amino acid composition \n')
    #make result table
    poc_results.write("<br><br>\n<table border='3' frame='void'>\n")
    poc_results.write('<tr> \n')
    poc_results.write('<td> Descriptor </td> <td> Value </td> \n')
    poc_results.write('</tr> \n')
    for i in range(43,47):
      #donor, acc, ratios
      poc_results.write(fill_line(entries, i))
    poc_results.write('</table> \n')
    
    poc_results.write('</td> \n')
    #poc_results.write('</tr> \n')
    
    # 1. row 3. column
    poc_results.write('<td align="center" valign="top"> \n')
    poc_results.write('Amino acid descriptors \n')
    #make result table
    poc_results.write("<br><br>\n<table border='3' frame='void'>\n")
    poc_results.write('<tr> \n')
    poc_results.write('<td> Descriptor </td> <td> Value </td> \n')
    poc_results.write('</tr> \n')
    #amino acids
    for i in range(18,38):
      # amino acids
      poc_results.write(fill_line(entries, i))
    poc_results.write(fill_line(entries, 17)) 
    
    poc_results.write('</table> \n')
    poc_results.write('</td> \n')
    
    poc_results.write('</tr> \n')
    
    poc_results.write('</table>\n')
    poc_results.write('</body>\n')
    poc_results.write('</html>\n')  


def calc_Pockets():

    pwd = 'bin' 
    pdb_id = sys.argv[1].upper() 
    chain1 = sys.argv[2] 
    pocLev = sys.argv[3]
    scoreType = sys.argv[4] 
    gridSpacing = sys.argv[5]
    timestamp = sys.argv[6]
    chain1_ID = sys.argv[7] 
    email = sys.argv[8]
    lig_id = sys.argv[9]
    
### calculate pockets and descriptors, generate dogsitescorer_script 
    program = '/usr/bin/python'
    script = '/DoGSiteScorer.py'
    arg1 = pdb_id
    arg2 = chain1
    arg3 = pocLev
    arg4 = scoreType
    arg5 = gridSpacing    
    arg6 = timestamp
    arg7 = chain1_ID
    arg8 = lig_id
    analyze_pocket = Popen([program, script, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8])
    analyze_pocket.wait()

    if not exists("results/descriptor_data_"+pdb_id+"_"+timestamp+".txt"):
      remove("downloads/"+pdb_id+"_"+timestamp+".pdb")
      remove("results/dogsitescorer_"+pdb_id+"_"+timestamp+".bat")
      return "No pockets could be calculated for selection! Please change your input."
######

    title = str(arg1)
      
#### write a pdb-file if single chain was chosen
    if(int(chain1)!=0):
      pdb_file = file("downloads/"+pdb_id+"_"+timestamp+".pdb", 'r')
      pdb_lines = pdb_file.readlines()
      outfile = file("results/"+pdb_id+"_chain_"+timestamp+".pdb", 'w')
      for pdb in pdb_lines:
  if pdb.startswith('TITLE'):
    title = title + ' ' + lower(pdb.strip('TITLE').strip().lstrip('2').lstrip('3'))
  if pdb.startswith('ATOM'):
    if pdb[21] == chain1_ID:
      outfile.write(pdb)
      outfile.close()
      pdb_file.close()

#######

    #remove("downloads/"+pdb_id+"_"+timestamp+".pdb")
    
    return ("OK", title)

        
def main():

  pdb_id = sys.argv[1].upper() 
  chain1 = sys.argv[2] 
  pocLev = sys.argv[3]
  scoreType = sys.argv[4] 
  gridSpacing = sys.argv[5]
  timestamp = sys.argv[6]
  chain1_ID = sys.argv[7] 
  email = sys.argv[8]
  lig_id = sys.argv[9]
  
  t = calc_Pockets()

  #results = file('results/results_'+sys.argv[6]+'.html','w')  # writes the result html 
  results = file('/home/other/dogsite/public_html/DoGSiteServer/results/results_'+sys.argv[6]+'.html','w')  # writes the result html  
  results.write('<?xml version="1.0" encoding="utf-8"?>\n')
  results.write('<!DOCTYPE html\n')
  results.write('    PUBLIC "-//W3C//DTD XHTML 1.1//EN"\n')
  results.write('    "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">\n')
  results.write(' <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">\n')
  results.write('<head>\n')
  results.write(' <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n')
  results.write(' <!-- \n')
  results.write(' ZBH Zentrum fuer Bioinformatik Hamburg\n')
  results.write('This website is powered by TYPO3 - inspiring people to share!\n')
  results.write('TYPO3 is a free open source Content Management Framework initially created by Kasper Skaarhoj and licensed under GNU/GPL.\n')
  results.write(' TYPO3 is copyright 1998-2010 of Kasper Skaarhoj. Extensions are copyright of their respective owners.\n')
  results.write(' Information and contribution at http://typo3.com/ and http://typo3.org/\n')
  results.write(' -->\n')
  results.write(' <meta name="generator" content="TYPO3 4.4 CMS" />\n')
  results.write('<title>DoGSiteScorer: Active Site Prediction and Analysis Server</title><link rel="stylesheet" type="text/css" href="http://www.zbh.uni-hamburg.de/uploads/tf/zbh.css" />\n')
### jmol ###
  results.write('<script src="../jmol/jmol-12.0.49/Jmol.js"></script>\n')
 #jquery 
  results.write(' <script type="text/javascript" src="../jquery/jquery-1.7.2.min.js"></script>\n') 
  results.write(' <script type="text/javascript" src="../jquery/jquery.tablesorter.js"></script>\n') 
  results.write('  <script type = "text/javascript">\n')
  results.write('  $(document).ready(function() \n')
  results.write('   { \n')
  results.write('       $("#pocTable").tablesorter(); \n')
  results.write('       $("#spocTable").tablesorter(); \n')
  results.write('   } \n')
  results.write(' ); </script>\n')
  results.write('<link rel="stylesheet" type="text/css" href="../jquery/sortTable.css" />\n')
###
  results.write(' </head>\n')
  results.write(' <body>\n')
  results.write('<div id="header">\n')
  results.write('  <a href="http://www.zbh.uni-hamburg.de/en/home.html" ><img src="http://www.zbh.uni-hamburg.de/uploads/tf/zbh_logo_en.png" width="282" height="72" id="zbh_logo" alt="" title="" /></a><a href="http://www.uni-hamburg.de"><img src="http://www.zbh.uni-hamburg.de/uploads/tf/uhh_2010.png" width="300" height="120" id="uhh_logo" alt="" title="" /></a>\n')
  results.write(' </div>\n')
  results.write('<div id="navigation">\n')
  results.write('  <span class="navigation">      <a href="http://www.uni-hamburg.de">UHH</a>\n')
  results.write('     <strong>&gt;</strong>&nbsp;<a href="http://www.zbh.uni-hamburg.de">Center for Bioinformatics</a>\n')
  results.write('     <strong>&gt;</strong>&nbsp;Servers\n')
  results.write('     <strong>&gt;</strong>&nbsp;DoGSiteScorer: Active Site Prediction and Analysis Server</span>\n')
  results.write('</div>\n')
  results.write('<table id="content-container">\n')
  results.write('<tr>\n')
  results.write('\t<td id="menu">\n')
  results.write('\t<!--###MENU###--><div class="menu-no"><a href="http://www.zbh.uni-hamburg.de/en/home.html" onfocus="blurLink(this);"  >Home</a>\n')
  results.write('\t</div><div class="menu-no"><a href="http://www.zbh.uni-hamburg.de/en/staff.html" onfocus="blurLink(this);"  >Staff</a>\n')
  results.write('\t</div><div class="menu-no"><a href="http://www.zbh.uni-hamburg.de/en/research.html" onfocus="blurLink(this);"  >Research</a>\n')
  results.write('\t</div><div class="menu-no"><a href="http://www.zbh.uni-hamburg.de/en/publications.html" onfocus="blurLink(this);"  >Publications</a>\n')
  results.write('\t</div><div class="menu-spc"></div><div class="menu-no"><a href="http://www.zbh.uni-hamburg.de/en/scientific-talks.html" onfocus="blurLink(this);"  >Scientific Talks</a>\n')
  results.write('\t</div><div class="menu-no"><a href="http://www.zbh.uni-hamburg.de/en/servers.html" onfocus="blurLink(this);"  >Servers</a>\n')
  results.write('\t</div><div class="menu-spc"></div><div class="menu-no"><a href="http://www.zbh.uni-hamburg.de/en/studying.html" onfocus="blurLink(this);"  >Studying</a>\n')
  results.write('\t</div><div class="menu-no"><a href="http://www.zbh.uni-hamburg.de/en/information-for-prospective-students.html" onfocus="blurLink(this);"  >Information for prospective students</a>\n')
  results.write('\t</div><div class="menu-spc"></div><div class="menu-no"><a href="http://www.zbh.uni-hamburg.de/en/jobs.html" onfocus="blurLink(this);"  >Jobs</a>\n')
  results.write('\t</div><div class="menu-no"><a href="http://www.zbh.uni-hamburg.de/en/documents.html" onfocus="blurLink(this);"  >Documents</a>\n')
  results.write('\t</div><div class="menu-no"><a href="http://www.zbh.uni-hamburg.de/en/alumni/home.html" onfocus="blurLink(this);"  >Alumni</a>\n')
  results.write('\t</div><!--###MENU###-->\n')
  results.write('\t</td>\n')
  #spalte inhalt
  results.write('\t<td id="content">\n')


  if(t[0] == 'OK'):
    results.write("\t\t<table width=\"100%\" border='3' frame='void'>\n")
    results.write("\t\t<h2>DoGSiteScorer: Active Site Prediction and Analysis Server</h2>\n")
    #erste Zeile
    results.write("\t\t<tr>\n")
    #erste Spalte
    results.write("\t\t<td align=\"center\">\n")
    
    results.write("\t\t\t<font size=\"4\"><br>Pockets and descriptors have been calculated for "+pdb_id+":<br>\n")
    if(int(pocLev)==1):
      results.write("\t<br><font size=\"3\">Pocket descriptor table<br>\n")
  
    #xls output
    stage2 = file("/home/other/dogsite/public_html/DoGSiteServer/results/PocXls_descriptor_data_"+pdb_id+"_"+timestamp+".txt", 'r')
    #skip header
    header= stage2.readline()
    header_arr=header.split('\t')
    #result table
    results.write("<br><br>\n<table border='3' frame='void' id='pocTable' class='tablesorter'>\n")
    #header
    results.write("<thead>\n")
    results.write("<tr>\n")
    results.write("<th align=\"center\">  \t\t\t<font size=\"3\" title=\" P=Pocket, SP=subpocket, P[0-99]SP[0-99] \">Name </th>\n")
    results.write("<th align=\"center\"> \t\t\t<font size=\"3\">Volume [&Aring;&sup3]</th>\n")
    results.write("<th align=\"center\"> \t\t\t<font size=\"3\">Surface [&Aring;&sup2]</th>\n")
    results.write("<th align=\"center\"> \t\t\t<font size=\"3\">Lipo surface [&Aring;&sup2] </th>\n")
    results.write("<th align=\"center\"> \t\t\t<font size=\"3\">Depth [&Aring;] </th>\n")
    if(int(scoreType)==1):
      results.write("<th align=\"center\"> \t\t\t<font size=\"3\" title=\"Druggability scores are predicted based on an SVM model. The model was trained on pockets of a non-redundant version of the druggability data set of Schmidtke et al. The higher the score the more druggable the pocket is estimated to be. \">Drug Score </th>\n")
    else:  
      results.write("<th align=\"center\"> \t\t\t<font size=\"3\">Simple Score </th>\n") 
    results.write("</tr>\n")
    results.write("</thead>\n")
    lines2= stage2.readlines()
    poc_names=[]
    poc_colors=['lightskyblue', 'indianred', 'lightgreen', 'orange', 'gold', 'violet','rosybrown', 'mediumslateblue','silver', 'aquamarine', 'coral', 'lightblue','yellowgreen','salmon', 'lightsteelblue', 'lightpink', 'moccasin', 'mediumorchid', 'lightseagreen', 'royalblue', 'olive']
    #scale colors: traffic light colors
    scale_colors=['red','orangered', 'orange','gold','yellowgreen', 'mediumseagreen']
   
    descr_arr=['Name', 'volume [&Aring;&sup3]', 'surface [&Aring;&sup2]', 'lipophilic surface [&Aring;&sup2]','depth [&Aring;]', 'SimpleScore', 'Ligand coverage', 'Pocket coverage', '# pocket atoms', 'ellipsoid main axis ration c/a',  'ellipsoid main axis ration b/a', 'enclosure', '# carbons (C)', '# nitrogens (N)', '# oxygens', '# sulfors (S)', '# other elements', '# special amino acids', '# ALA', '# ARG', '# ASN', '# ASP', '# CYS', '# GLN', '# GLU', '# GLY', '# HIS', '# ILE', '# LEU', '# LYS', '# MET', '# PHE', '# PRO', '# SER', '# THR', '# TRP', '# TYR', '# VAL', '# hydrogen bond donors', '# hydrogen bond acceptors', '# metals', '# hydrophobic interactions', 'hydrophobicity ratio', 'apolar amino acid ratio','polar amino acid ratio', 'positive amino acid ratio', 'negative amino acid ratio','non']
    l2_counter=0
    if(int(scoreType)==1):
      drug_scores=make_druggability_prediction(pdb_id, timestamp, 0)
    for l2 in lines2:
      results.write("<tr>\n")
      entries=l2.split('\t')
      #if (pocLev==0 or (pocLev==1 and ('SP' in tmp_name[2]))):
      pos=0
      scale=0
      for entry in entries:
  if(pos<6):
    #score annotation
    if(pos==5):
      #druggability calculation
      if(int(scoreType)==1):
        #results.write("<td align=\"center\"> \t\t\t<font size=\"3\"> %4.2f</td>\n" %drug_scores[l2_counter])
        drug_score=float(drug_scores[l2_counter])
        if(drug_score < 0.166):
    scale=0
        elif(drug_score < 0.332):
    scale=1
        elif(drug_score < 0.499):
    scale=2
        elif(drug_score < 0.666):
    scale=3
        elif(drug_score < 0.832):
    scale=4
        elif(drug_score <= 1.):
    scale=5  
        results.write("<td align=\"center\" bgcolor=\""+scale_colors[scale]+"\"> \t\t\t<font size=\"3\"> %s</td>\n" %drug_scores[l2_counter])
        
      else:  
        score=float(entry)
        if(score<0):
    score=0
        elif(score>1.):
    score=1
        results.write("<td align=\"center\"> \t\t\t<font size=\"3\"> %4.2f</td>\n" %score)  
    elif(pos>0):
      results.write("<td align=\"center\"> \t\t\t<font size=\"3\"> %4.2f</td>\n" %float(entry))
    else:
      name=entry.split('_')
      
      results.write("<td align=\"center\" bgcolor=\""+poc_colors[l2_counter%len(poc_colors)]+"\"> \t\t\t<font size=\"3\"><a href=\"javascript: void(0)\" onclick=\"window.open('results_"+pdb_id+"_"+timestamp+"_%s.html', '%s', 'width=600, height=600, left=200, top=200, scrollbars=yes, resizable=yes'); return false;\">%s</a></td>\n" %(name[2],name[2],name[2]))
      poc_names.append(name[2])
  pos+=1
      write_poc_results(pdb_id, timestamp, name, entries)
      l2_counter+=1
      results.write("</tr>\n")
    results.write("</table>\n")
    results.write("<font size=\"1\"> Clicking on the name of a single pocket opens a separate window <br> containing further calculated pocket properties.<br>\n")
    stage2.close()
    
    #add row ad column with sub pocket information if selected    
    if(int(pocLev)==1):
  #results.write('\t<tr>\n')
  results.write("\t<br><font size=\"3\">Subpocket descriptor table<br>\n")
  #fix output
  stage2 = file("/home/other/dogsite/public_html/DoGSiteServer/results/SpocXls_descriptor_data_"+pdb_id+"_"+timestamp+".txt", 'r')
  #skip header
  header= stage2.readline()
  header_arr=header.split('\t')
  #result table
  results.write("<br><br>\n<table border='3' frame='void' id='spocTable' class='tablesorter'>\n")
  #header
  results.write("<thead>\n")
  results.write("<tr>\n")
  results.write("<th align=\"center\">  \t\t\t<font size=\"3\" title=\" P=Pocket, SP=subpocket, P[0-99]SP[0-99] \">Name </th>\n")
  results.write("<th align=\"center\"> \t\t\t<font size=\"3\">Volume [&Aring;&sup3]</th>\n")
  results.write("<th align=\"center\"> \t\t\t<font size=\"3\">Surface [&Aring;&sup2]</th>\n")
  results.write("<th align=\"center\"> \t\t\t<font size=\"3\">Lipo surface [&Aring;&sup2] </th>\n")
  results.write("<th align=\"center\"> \t\t\t<font size=\"3\">Depth [&Aring;]</th>\n")
  if(int(scoreType)==1):
    results.write("<th align=\"center\"> \t\t\t<font size=\"3\" title=\"Druggability scores are predicted based on an SVM model. Note that subpockets scores do not add up to the respective pocket score. Both - pocket and subpocket - scores are calculated based on individual druggability models, trained on pockets and subpockets, respectively. \">Drug Score </th>\n")
  else:  
    results.write("<th align=\"center\"> \t\t\t<font size=\"3\">Simple Score </th>\n") 
  results.write("</tr>\n")
  results.write("</thead>\n")
  lines2= stage2.readlines()
  poc_names=[]
  poc_colors=['lightskyblue', 'indianred', 'lightgreen', 'orange', 'gold', 'violet','rosybrown', 'mediumslateblue','silver', 'aquamarine', 'coral', 'lightblue','yellowgreen','salmon', 'lightsteelblue', 'lightpink', 'moccasin', 'mediumorchid', 'lightseagreen', 'royalblue', 'olive']
  #chaged to traffic light colors
  scale_colors=['red','orangered', 'orange','gold','yellowgreen', 'green']
      
  descr_arr=['Name', 'volume [&Aring;&sup3]', 'surface [&Aring;&sup2]', 'lipophilic surface [&Aring;&sup2]','depth [&Aring;]', 'SimpleScore', 'Ligand coverage', 'Pocket coverage', '# pocket atoms', 'ellipsoid main axis ration c/a',  'ellipsoid main axis ration b/a', 'enclosure', '# carbons (C)', '# nitrogens (N)', '# oxygens', '# sulfors (S)', '# other elements', '# special amino acids', '# ALA', '# ARG', '# ASN', '# ASP', '# CYS', '# GLN', '# GLU', '# GLY', '# HIS', '# ILE', '# LEU', '# LYS', '# MET', '# PHE', '# PRO', '# SER', '# THR', '# TRP', '# TYR', '# VAL', '# hydrogen bond donors', '# hydrogen bond acceptors', '# metals', '# hydrophobic interactions', 'hydrophobicity ratio', 'apolar amino acid ratio','polar amino acid ratio', 'positive amino acid ratio', 'negative amino acid ratio','non']
  l2_counter=0
  if(int(scoreType)==1):
    drug_scores=make_druggability_prediction(pdb_id, timestamp, pocLev)
  for l2 in lines2:
    results.write("<tr>\n")
    entries=l2.split('\t')
    #if (pocLev==0 or (pocLev==1 and ('SP' in tmp_name[2]))):
    pos=0
    scale=0
    for entry in entries:
      if(pos<6):
        #score annotation
        if(pos==5):
    #druggability calculation
    if(int(scoreType)==1):
      drug_score=float(drug_scores[l2_counter])
      if(drug_score < 0.166):
        scale=0
      elif(drug_score < 0.332):
        scale=1
      elif(drug_score < 0.499):
        scale=2
      elif(drug_score < 0.666):
        scale=3
      elif(drug_score < 0.832):
        scale=4
      elif(drug_score <= 1.):
        scale=5  
      results.write("<td align=\"center\" bgcolor=\""+scale_colors[scale]+"\"> \t\t\t<font size=\"3\"> %s</td>\n" %drug_scores[l2_counter])
      
    else:  
      score=float(entry)
      if(score<0):
        score=0
      elif(score>1.):
        score=1
      results.write("<td align=\"center\"> \t\t\t<font size=\"3\"> %4.2f</td>\n" %score)  
        elif(pos>0):
    results.write("<td align=\"center\"> \t\t\t<font size=\"3\"> %4.2f</td>\n" %float(entry))
        else:
    name=entry.split('_')
    results.write("<td align=\"center\" bgcolor=\""+poc_colors[l2_counter%len(poc_colors)]+"\"> \t\t\t<font size=\"3\"><a href=\"javascript: void(0)\" onclick=\"window.open('results_"+pdb_id+"_"+timestamp+"_%s.html', '%s', 'width=600, height=600, left=200, top=200, scrollbars=yes, resizable=yes'); return false;\">%s</a></td>\n" %(name[2],name[2],name[2]))
    poc_names.append(name[2])
      pos+=1
    write_poc_results(pdb_id, timestamp, name, entries)
    l2_counter+=1
    results.write("</tr>\n")
  results.write("</table>\n")
  results.write("<font size=\"1\"> Clicking on the name of a single subpocket opens a separate window <br> containing further calculated subpocket properties.<br>\n")
  results.write("<font size=\"1\"> Note: If a pocket contains no subpockets, it is not listed here.<br>\n")
  stage2.close()
    if(int(scoreType)==1):
      #print druggability legend
      results.write("<br> legend: undruggable => druggable <br>\n")
      results.write("<table align=\"center\"> <tr>\n")
      results.write(" <td align=\"center\" width=\"25\" bgcolor=\""+scale_colors[0]+"\"> 0 </td>\n")
      for i in range(1,5):
  results.write(" <td width=\"25\" bgcolor=\""+scale_colors[i]+"\"> </td>\n")
      results.write(" <td align=\"center\" width=\"25\" bgcolor=\""+scale_colors[5]+"\"> 1 </td>\n")
      results.write("</tr></table>\n")
    #ende erste Spalte
    results.write("\t\t</td>\n")
    
    #zweite Spalte Jmol
    results.write('\t\t<td>\n')
    results.write("\t\t\t<p align=\"center\"><br><br><br>\n")
    ### jmol ###
    results.write('\t\t\t<script>\n')
    results.write('\t\t\tjmolInitialize("../jmol/jmol-12.0.49/");\n')
    results.write('\t\t\tjmolSetAppletColor("mintcream");\n')
    #collect all pocket files
    jmol_string=''
    #collect pocket files
    poc_files=glob.glob("results/poc_reduced_"+pdb_id+"_"+timestamp+"_P[0-9].pdb")
    poc_files+=glob.glob("results/poc_reduced_"+pdb_id+"_"+timestamp+"_P[0-9][0-9].pdb")
    if(int(pocLev)==1):
      spoc_files=glob.glob("results/poc_reduced_"+pdb_id+"_"+timestamp+"_P*SP*.pdb")
    d={}
    poc_mols=0
    spoc_mols=0
    # count pockets and subpockets
    for i in poc_files:
      poc_mols+=1
    if(int(pocLev)==1):
      for i in spoc_files:
  spoc_mols+=1
  non, tmp =  str(i).split('_P')
  tmp2, non = tmp.split('.pdb')
  c_poc, c_spoc = tmp2.split('SP')
  #c_poc=int(c_poc)
  #c_spoc=int(c_spoc)
  if not d.has_key(c_poc):
    d[c_poc] = []
  if c_spoc not in d[c_poc]:
    d[c_poc].append(c_spoc)
    c=0
    #add file to jmol string
    while(c<poc_mols):
      jmol_string+="\"../results/poc_reduced_"+pdb_id+"_"+timestamp+"_P"+str(c)+".pdb \""
      c+=1
    if(int(pocLev)==1):
      int_key_list = d.keys()
      int_key_list.sort(key=int)
      for k in int_key_list: #sorted(d.keys()):
  for s in sorted(d[k]):
    jmol_string+="\"../results/poc_reduced_"+pdb_id+"_"+timestamp+"_P"+str(k)+"SP"+str(s)+".pdb \""
          
    #add ligand file
    jmol_lig_string=' '
    lig_select_string_on=' '
    lig_select_string_off=' '
    
    if(int(lig_id)>=0):
      lig_start = spoc_mols+c+2
      nof_lig=0
      lig_files=glob.glob("downloads/"+pdb_id+"_LIG_"+timestamp+"_*.mol2")
      for i in lig_files:
  if(nof_lig!=0):
    if(nof_lig<10):
      jmol_lig_string+="\"../downloads/"+pdb_id+"_LIG_"+timestamp+"_0"+str(nof_lig)+".mol2 \""
    else:
      jmol_lig_string+="\"../downloads/"+pdb_id+"_LIG_"+timestamp+"_"+str(nof_lig)+".mol2 \""
    lig_select_string_on+='select '+str(lig_start+nof_lig-1)+'.1; spacefill 20%; wireframe on;'
    lig_select_string_off+='select '+str(lig_start+nof_lig-1)+'.1; spacefill off; wireframe off;'
  nof_lig+=1
      
      
    c=0
    #set density
    if(float(gridSpacing) <=0.6):
      density = 6
    elif(float(gridSpacing) <=0.8):
      density= 5
    else:
      density=6
      
    select_string='select 1.1; ribbons; color chain;'
    #poc_colors=['red', 'blue', 'green', 'orange', 'yellow', 'violet','brown', 'grey', 'cyan', 'white']
     
    while (c<poc_mols):
      select_string+=' select '+str(c+2)+'.1; dots on; set dotDensity '+str(density)+'; color atoms '+poc_colors[c%len(poc_colors)]+';'
      c+=1
    if(int(pocLev)==1):
      c=0
      while (c<spoc_mols):
  select_string+=' select '+str(poc_mols+c+2)+'.1; dots off; set dotDensity '+str(density)+'; color atoms '+poc_colors[c%len(poc_colors)]+';'
  c+=1
    
    if(int(chain1)==0):
      results.write('\t\t\tjmolApplet([400,500], \'load files \"../downloads/'+pdb_id+'_'+timestamp+'.pdb\" '+jmol_string + jmol_lig_string +'; frame *; cpk off; wireframe off;'+select_string+'\') \n')
    else:
      results.write('\t\t\tjmolApplet([400,500], \'load files \"../results/'+pdb_id+'_chain_'+timestamp+'.pdb\" '+jmol_string + jmol_lig_string +'; frame *; cpk off; wireframe off; '+select_string+'\') \n')
    #selection
    c=0
    spoc_c=0
    radio_string='["frame *; cpk off; wireframe off;'+select_string +'", "all pockets", "checked"]'
    # poc level
    while (c<poc_mols):
      radio_string+=',["frame *; cpk off; wireframe off; select *; dots off; select '+ str(c+2)+'.1; dots on; set dotDensity '+str(density)+'; color atoms '+poc_colors[c%len(poc_colors)]+'", "pocket P'+ str(c)+' "]'
      if(int(pocLev)==1):
  #for k in sorted(d.keys()):
  tmp_string=''
  if d.has_key(str(c)):
    for s in sorted(d[str(c)]):
      tmp_string += '; select '+ str(poc_mols+spoc_c+2)+'.1; dots on; set dotDensity '+str(density)+'; color atoms '+poc_colors[spoc_c%len(poc_colors)]
      #radio_string+=',["frame *; cpk off; wireframe off; select *; dots off; select '+ str(c+2)+'.1; dots on; set dotDensity '+str(density)+'; color atoms '+poc_colors[c%len(poc_colors)]+'", "subpocket P'+ str(k)+'_SP'+str(s)+' "]'
      spoc_c+=1
    radio_string+=',["frame *; cpk off; wireframe off; select *; dots off'+tmp_string+'", "subpockets of P'+ str(c)+' "]'
      c+=1
      
    # test jmol radio group:
    results.write('\t\t\tjmolBr();\n')
    results.write('\t\t\tjmolHtml("Select pocket object to be drawn ");\n')
    
    results.write('\t\t\tjmolMenu(['+radio_string+']);\n')
    results.write('\t\t\tjmolBr();\n')
    # a button:
    results.write('\t\t\tjmolButton("reset", "Reset to original orientation");\n')
    results.write('\t\t\tjmolBr();\n')
    
      
    # test jmol ligand group:
    if(int(lig_id)>=0):
      results.write('\t\t\tjmolHtml("Draw ligand(s): ");\n')
      results.write('\t\t\tjmolRadioGroup([[\"'+lig_select_string_on+'\", "on"], [\"'+lig_select_string_off+'\", "off", "checked"]]);\n')
      results.write('\t\t\tjmolBr();\n')
    
    results.write('\t\t\t</script>\n')
    results.write('\t\t\t</p>\n')
    results.write('<tr><td colspan=\"2\" align=\"center\" ><font size=\"2\"> PDB files, containing the respective pocket atoms, and descriptor information can be send to you via email. <br> For this purpose, please resubmit your query and enter your email address on the previous page.</td></tr>\n ')
    # 2. Spalte Ende
    results.write('\t\t</td>\n')
    # 1. Reihe Ende
    results.write("\t\t</tr>\n")
   
    #letzte Zeile
    results.write('\t<tr>\n')
    results.write('\t<td colspan=\"2\">\n')
    results.write("\t\t<input type=\"button\" value=\"Start another calculation\" onclick=\"window.location.href='../index.html'\">\n")
    results.write('\t</td>\n')
    results.write('\t</tr>\n')
  
    #table ende
    results.write("\t</table>\n")
    
    if email == 'noemail':
      #descriptor file
      remove("results/descriptor_data_"+pdb_id+"_"+timestamp+".txt")
    
    #flex script
    remove("results/dogsitescorer_"+pdb_id+"_"+timestamp+".bat")
    
    #libsvm files
    if(int(scoreType)==1):
      files= glob.glob("results/myLibsvmPoc_"+pdb_id+"_"+timestamp+".txt.*")
      remove("results/myLibsvmPoc_"+pdb_id+"_"+timestamp+".txt")
      if(int(pocLev)==0):
  files= glob.glob("results/myLibsvmSpoc_"+pdb_id+"_"+timestamp+".txt.*")
  remove("results/myLibsvmSpoc_"+pdb_id+"_"+timestamp+".txt")
      for i in files:
  remove(i)
    #delete Poc and Spoc files
    #poc_files=glob.glob("results/poc_"+pdb_id+"_"+timestamp+"_P*S*.pdb")
    #for i in poc_files:
      #remove(i)
    #delete Poc and Spoc atms files
    #poc_files=glob.glob("results/atms_"+pdb_id+"_"+timestamp+"*.pdb")
    #for i in poc_files:
    #  remove(i)
     
  else:
  
    results.write("<h2>Prediction or classification not possible:</h2><br>\n")
    results.write("<p><b>"+t+"</b></p>\n")
    results.write("<p><br></p>\n")
    results.write("<p style=\"color:red\">Please <b><a style=\"color:red\" href=\"../index.html\">go back to the form</a></b> and correct your input</p>\n")
    
  #spalte Inhalt ende
  results.write('\t</td>\n')
  results.write('\t</tr>\n')
  results.write('</table>\n')

  
  results.write('</td>\n')
  results.write('</tr>\n')
  results.write('</table>\n')
  
      
  results.write('<div id="footer">\n')
  results.write(' <p id="lastchange">DoGSiteScorer: Active Site Prediction and Analysis Server</p><p id="impressum"><a href="http://www.zbh.uni-hamburg.de/en/imprint.html" >Imprint</a></p>\n')
  results.write('</div>\n')
  results.write('</body>\n')
  results.write('</html>\n')


  if email != 'noemail':
    import smtplib
    import zipfile
    import tempfile
    from email import encoders
    from email.message import Message
    from email.mime.base import MIMEBase
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    

    email_result = file('results/results_'+sys.argv[1]+'.txt','w')  # writes the result

    emailadd = "dogsite@zbh.uni-hamburg.de"
    subject = "Protein assesment results of "+pdb_id+""
    send_msg = MIMEMultipart()
    
    email_result.write("Thank you very much for using DoGSiteScorer Server.\n")
    email_result.write("\nPockets and descriptors have been calculated for "+sys.argv[1]+":\n")
    p_counter=0
    sp_counter=0
    #email_result.write("With the following arguments: pdb_id: "+pdb_id+", chain_nr: "+chain1+", pocLev: "+pocLev+", scoreType: "+scoreType+", gridSpacing: "+gridSpacing+", chain_ID: "+chain1_ID+"\n\n")
    stage = file("/home/other/dogsite/public_html/DoGSiteServer/results/PocXls_descriptor_data_"+pdb_id+"_"+timestamp+".txt", 'r')
    lines1 = stage.readlines()
    for l1 in lines1:
      p_counter+=1
      #email_result.write("%s" %l1)
    stage.close()
    
    if(int(pocLev)==1):
      stage = file("/home/other/dogsite/public_html/DoGSiteServer/results/SpocXls_descriptor_data_"+pdb_id+"_"+timestamp+".txt", 'r')
      lines1 = stage.readlines()
      for l1 in lines1:
  sp_counter+=1
  #email_result.write("%s" %l1)
      stage.close()
      
    if(int(pocLev)==0):
      email_result.write(str(p_counter-1)+" pockets have been detected.\n")
    else:
      email_result.write(str(p_counter-1)+" pockets with a total of "+str(sp_counter-1)+" subpockets have been detected.\n")

    email_result.write("\nDescriptor information and pocket lining atom files can be found in the attachment.\n")
    #email_result.write("If you would like to visualize the pockets, please use the DoGSiteScorer Server.\n\n")
    #email_result.write("Please do not reply to this email.")
    
    email_result.write("\n\n\n\n---- Short descriptor explanation -----------\n\n")
    email_result.write("lig_cov: percentage of ligand covered by the predicted pocket; \n")
    email_result.write("poc_cov: percentage of the pocket covered by the co-crystallized ligand; \n")
    
    email_result.write("\nSize and shape descriptors:\n")
    email_result.write("volume: pocket volume in A^3 calculated via grid points; \n")
    email_result.write("surface: pocket surface in A^2 calculated via grid points; \n")
    email_result.write("lipo_surf: solvent accessible lipophilic surface; \n")
    email_result.write("depth:  depth of the pocket in A; \n")
    email_result.write("ellips c/a or b/a: ellipsoid main axes ratios, with a > b > c;\n")
    email_result.write("enclosure: ratio of number of surface to hull grid points; \n")
        
    email_result.write("\nFunctional group descriptors:\n")
    email_result.write("H-don: number of hydrogen bond donors; \n")
    email_result.write("H-acc: number of hydrogen bond acceptors; \n")
    email_result.write("Met: number of metals; \n")
    email_result.write("Hphob: number of hydrophobic contacts; \n")
    email_result.write("siac ratio: relative number of hydrophobic SIACs; \n")
    
    email_result.write("\nElement descriptors:\n")
    email_result.write("nof_dif_atms:  number of surface atoms lining the pocket; \n")
    email_result.write("elem_x: number of elements of specific type in active site; types: C, N, O, S or other (X); \n")
    
    email_result.write("\nAmino acid composition:\n")
    email_result.write("aa_apol, aa_pol, aa_pos, aa_neg: relative number of amino acids apolar, polar, positive, and negative);\n")
    
    email_result.write("\nAmino acid descriptors:\n")
    email_result.write("ALA, ARG,...: number of amino acids in pocket, 3-letter code of 20 amino acid types; \n")
    
    email_result.close()
    
    fp = file('results/results_'+sys.argv[1]+'.txt','rb')
    msg = MIMEText(fp.read())
    fp.close()
    msg.add_header('Content-Disposition', 'attachment', filename='PocXlsDescriptors_'+pdb_id+'.txt')

    send_msg.attach(msg)
    
    
    #zip file
    the_file='results/poc_'+pdb_id+'_'+timestamp+'_P0.pdb'
    zf = tempfile.TemporaryFile(prefix='mail', suffix='.zip')
    my_zip = zipfile.ZipFile(zf, 'w')
    
    #add pocket files
    tmp_poc_files=glob.glob("results/atms_"+pdb_id+"_"+timestamp+"_P[0-9].pdb")
    tmp_poc_files+=glob.glob("results/atms_"+pdb_id+"_"+timestamp+"_P[0-9][0-9].pdb")
    #ADD DESCRIPTOR FILES
    tmp_poc_files+=glob.glob("results/PocXls_descriptor_data_"+pdb_id+"_"+timestamp+".txt")
    #add subpocket files
    if(int(pocLev)==1):
      tmp_poc_files+=glob.glob("results/atms_"+pdb_id+"_"+timestamp+"_P*S*.pdb")
      #ADD DESCRIPTOR FILES
      tmp_poc_files+=glob.glob("results/SpocXls_descriptor_data_"+pdb_id+"_"+timestamp+".txt")
    for my_file in tmp_poc_files:
      if  os.path.isfile(my_file):
  my_zip.write(my_file)
    #zip.write(the_file)
    my_zip.close()
    zf.seek(0)

    send_msg['Subject'] = subject
    send_msg['From'] = emailadd
    send_msg['To'] = email

    my_attachment = MIMEBase('application', 'zip')
    my_attachment.set_payload(zf.read() )
    encoders.encode_base64(my_attachment)
    my_attachment.add_header('Content-Disposition', 'attachment', filename=pdb_id+'_'+timestamp+'.zip')
    
    send_msg.attach(my_attachment)

      
    s = smtplib.SMTP('wendelstein.zbh.uni-hamburg.de')   ###HOST
    s.sendmail(emailadd, email, send_msg.as_string())

    #descriptor file
    remove("results/PocXls_descriptor_data_"+pdb_id+"_"+timestamp+".txt")
    if(int(pocLev==1)):
      remove("results/SpocXls_descriptor_data_"+pdb_id+"_"+timestamp+".txt")
    for i in tmp_poc_files:
      remove(i) 
main()



