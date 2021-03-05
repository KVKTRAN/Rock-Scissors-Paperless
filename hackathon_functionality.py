#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import ipywidgets as widgets
import xml.etree.ElementTree as ET
from IPython.display import clear_output
import hackathon_lib

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

df_genes = hackathon_lib.get_disease_with_genes_df()
df_hpo = hackathon_lib.get_disease_with_phenotypes_df()

def new_gene():
    newGene = []

    for genes in df.Genes:
        # print(genes)
        arr = []
        for g in genes:
            arr.append(int(g['id']))
        # print(arr)
        newGene.append(arr)
        
    return newGene

def get_single_gene_data():
    df_cols = ['OrphaCode', 
           'Expert Link', 
           'Name', 
           'DisorderType', 
           'DisorderGroup', 
           'GeneID',
           'GeneName',
           'GeneSymbol',
           'GeneType',
          ]
    
    rows = []
    
    for i in range(len(df_genes)):
        genes = df_genes.loc[i].Genes
        for gene in genes:
            rows.append({"OrphaCode": df_genes.loc[i].OrphaCode, 
                     "Expert Link": df_genes.loc[i]["Expert Link"], 
                     "Name": df_genes.loc[i].Name, 
                     "DisorderType": df_genes.loc[i].DisorderType, 
                     "DisorderGroup": df_genes.loc[i].DisorderGroup,
                     "GeneID": gene["id"],
                     "GeneName": gene["name"],
                     "GeneType": gene["type"],
                     "GeneSymbol": gene["symbol"],
                })
    df1 = pd.DataFrame(rows, columns=df_cols)
    return df1

def get_single_HPO_data():
    df_cols = ['OrphaCode', 
           'Expert Link', 
           'Name', 
           'DisorderType', 
           'DisorderGroup', 
           'HPOID',
           'HPOTerm',
           'HPOFrequency',
          ]
    
    rows = []
    
    for i in range(len(df_hpo)):
        hpos = df_hpo.loc[i].HPODisorderAssociationList
        for hpo in hpos:
            rows.append({"OrphaCode": df_hpo.loc[i].OrphaCode, 
                     "Expert Link": df_hpo.loc[i]["Expert Link"], 
                     "Name": df_hpo.loc[i].Name, 
                     "DisorderType": df_hpo.loc[i].DisorderType, 
                     "DisorderGroup": df_hpo.loc[i].DisorderGroup,
                     "HPOID": hpo["HPOId"],
                     "HPOTerm": hpo["HPOTerm"],
                     "HPOFrequency": hpo["HPOFrequency"],
                })
    df1 = pd.DataFrame(rows, columns=df_cols)
    return df1

def get_disease_from_gene(symbol):
    df = get_single_gene_data()
    a = df.loc[df["GeneSymbol"] == symbol]
    return a

def get_disease_from_hpo_by_id(hpo):
    df = get_single_HPO_data()
    a = df.loc[df["HPOID"] == hpo]
    return a

