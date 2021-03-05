#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import ipywidgets as widgets
import xml.etree.ElementTree as ET
from IPython.display import clear_output

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

def getDisabilityAssociationList(m_disorder):
    dis_array = []
    
    dis_list = m_disorder.find("DisabilityDisorderAssociationList")
    for dis in dis_list.findall("DisabilityDisorderAssociation"):
        disObject = {}
        disObject["Disability"] = dis.find("Disability").find("Name").text
        
        if dis.find("FrequenceDisability").find("Name") is not None:
            disObject["FrequenceDisability"] = dis.find("FrequenceDisability").find("Name").text
            
        if dis.find("TemporalityDisability").find("Name") is not None:
            disObject["TemporalityDisability"] = dis.find("TemporalityDisability").find("Name").text
            
        if dis.find("SeverityDisability").find("Name") is not None:
            disObject["SeverityDisability"] = dis.find("SeverityDisability").find("Name").text
        
        disObject["LossOfAbility"] = dis.find("LossOfAbility").text
        disObject["Type"] = dis.find("Type").text
        disObject["Defined"] = dis.find("Defined").text
        
        dis_array.append(disObject)
    
    return dis_array

def getHPODisorderAssociationList(m_disorder):
    hpo_array = []
    
    hpo_list = m_disorder.find("HPODisorderAssociationList")
    for hpo in hpo_list.findall("HPODisorderAssociation"):
        hpoObject = {}
        hpoObject["HPOId"] = hpo.find("HPO").find("HPOId").text
        hpoObject["HPOTerm"] = hpo.find("HPO").find("HPOTerm").text
        hpoObject["HPOFrequency"] = hpo.find("HPOFrequency").find("Name").text
        
        hpo_array.append(hpoObject)
    
    return hpo_array

def getNumberOfHPO(m_disorder):
    hpo_list = m_disorder.find("HPODisorderAssociationList")
    return hpo_list.attrib['count']

def getId(node, find_str):
    node_id = node.find(find_str).attrib
    node_id = node_id['id']
    return node_id

def maxOfGenes():
    all_diff_genes = []
    genes = []
    
    for disorder in root.findall("Disorder"):
        a = disorder.find("DisorderGeneAssociationList")
        a = a.findall("DisorderGeneAssociation")
        for b in a:
            genes.append(b.find("Gene"))
        
    for gene in genes:
        if gene.attrib['id'] not in all_diff_genes:
            all_diff_genes.append(gene.attrib['id'])
    
    print(len(genes))
    return all_diff_genes

def getGeneArray(m_disorder):  
    genes = []
    
    d_list = m_disorder.find("DisorderGeneAssociationList")
    d_list = d_list.findall("DisorderGeneAssociation")
    for g in d_list:
        g = g.find("Gene")
        geneObject = {}
        geneObject["id"] = g.attrib["id"]
        geneObject["name"] = g.find("Name").text
        geneObject["symbol"] = g.find("Symbol").text
        geneObject["type"] = g.find("GeneType").find("Name").text
        
        
        geneObject["synonyms"] = []
        synonyms = g.find("SynonymList").findall("Synonym")
        for s in synonyms:
            geneObject["synonyms"].append(s.text)
        
        geneObject["ExternalReferences"] = []
        ex = g.find("ExternalReferenceList").findall("ExternalReference")
        for e in ex:
            exObject = {}
            exObject["Source"] = e.find("Source").text
            exObject["Reference"] = e.find("Reference").text
            geneObject["ExternalReferences"].append(exObject)
        
        genes.append(geneObject)
            
    return genes


def get_disease_with_phenotypes_df():
    tree = ET.parse('DataXML/phenotype-data.xml')
    root = tree.getroot()

    df_cols = ['OrphaCode', 
               'Expert Link', 
               'Name', 
               'DisorderType', 
               'DisorderGroup', 
               'Number of HPO Disorder Association',
               'HPODisorderAssociationList',
              ]
    rows = []

    root = root.find('HPODisorderSetStatusList')
    
    for hpo_disorder_set in root.findall("HPODisorderSetStatus"):
        disorder = hpo_disorder_set.find("Disorder")
        orphacode = disorder.find("OrphaCode").text
        expertlink = disorder.find("ExpertLink").text
        name = disorder.find("Name").text
        disordertype = disorder.find('DisorderType').find('Name').text 
        disordergroup = disorder.find('DisorderGroup').find('Name').text
        hpo_list = getHPODisorderAssociationList(disorder)
        number_hpo = getNumberOfHPO(disorder)

        rows.append({"OrphaCode": orphacode, 
                     "Expert Link": expertlink, 
                     "Name": name, 
                     "DisorderType": disordertype, 
                     "DisorderGroup": disordergroup,
                     'Number of HPO Disorder Association': number_hpo,
                     "HPODisorderAssociationList": hpo_list,
                    })

    df = pd.DataFrame(rows, columns=df_cols)
    return df

def getPrevelanceArray(m_disorder):
    prevalence_array = []
    
    p_list = m_disorder.find("PrevalenceList")
    # p_list = p_list.findall("Prevalence")
    for p in p_list.findall("Prevalence"):
        pObject = {}
        pObject["id"] = p.attrib["id"]
        pObject["Source"] = p.find("Source").text
        pObject["PrevalenceType"] = p.find("PrevalenceType").find("Name").text
        pObject["PrevalenceQualification"] = p.find("PrevalenceQualification").find("Name").text
        
        if p.find("PrevalenceClass").find("Name") is not None:
            pObject["PrevalenceClass"] = p.find("PrevalenceClass").find("Name").text
        
        pObject["Valmoy"] = p.find("Valmoy").text if p.find("Valmoy") is not None else None
        pObject["PrevalenceGeographic"] = p.find("PrevalenceGeographic").find("Name").text
        pObject["PrevalenceValidationStatus"] = p.find("PrevalenceValidationStatus").find("Name").text
        
        prevalence_array.append(pObject)
        
    return prevalence_array


def get_disease_with_epidemiology_df():
    tree = ET.parse('DataXML/epidemiology.xml')
    root = tree.getroot()

    df_cols = ['OrphaCode', 
               'Expert Link', 
               'Name', 
               'DisorderType', 
               'DisorderGroup', 
               'PrevelanceList',
              ]
    rows = []

    root = root.find('DisorderList')
    # print(root)
    
    for disorder in root.findall("Disorder"):
        orphacode = disorder.find("OrphaCode").text
        expertlink = disorder.find("ExpertLink").text
        name = disorder.find("Name").text
        disordertype = disorder.find('DisorderType').find('Name').text 
        disordergroup = disorder.find('DisorderGroup').find('Name').text
        prevalence_list = getPrevelanceArray(disorder)

        rows.append({"OrphaCode": orphacode, 
                     "Expert Link": expertlink, 
                     "Name": name, 
                     "DisorderType": disordertype, 
                     "DisorderGroup": disordergroup,
                     "PrevelanceList": prevalence_list
                    })

    df = pd.DataFrame(rows, columns=df_cols)
    return df

def get_disease_with_func_consequences_df():
    tree = ET.parse('DataXML/funct_consequences.xml')
    root = tree.getroot()

    df_cols = ['OrphaCode', 
               'Expert Link', 
               'Name', 
               'DisorderType', 
               'DisorderGroup', 
               'DisabilityDisorderAssociationList',
              ]
    rows = []

    root = root.find('DisorderDisabilityRelevanceList')
    
    for hpo_disorder_set in root.findall("DisorderDisabilityRelevance"):
        disorder = hpo_disorder_set.find("Disorder")
        orphacode = disorder.find("OrphaCode").text
        expertlink = disorder.find("ExpertLink").text
        name = disorder.find("Name").text
        disordertype = disorder.find('DisorderType').find('Name').text 
        disordergroup = disorder.find('DisorderGroup').find('Name').text

        disability_list = getDisabilityAssociationList(disorder)

        rows.append({"OrphaCode": orphacode, 
                     "Expert Link": expertlink, 
                     "Name": name, 
                     "DisorderType": disordertype, 
                     "DisorderGroup": disordergroup,
                     "DisabilityDisorderAssociationList": disability_list,
                    })

    df = pd.DataFrame(rows, columns=df_cols)
    return df


def get_disease_with_genes_df():
    tree = ET.parse('DataXML/geneotype-data.xml')
    root = tree.getroot()

    df_cols = ['OrphaCode', 
               'Expert Link', 
               'Name', 
               'DisorderType', 
               'DisorderGroup', 
               'Genes',
              ]
    rows = []

    root = root.find('DisorderList')
    
    for disorder in root.findall("Disorder"):
        orphacode = disorder.find("OrphaCode").text
        expertlink = disorder.find("ExpertLink").text
        name = disorder.find("Name").text
        disordertype = disorder.find('DisorderType').find('Name').text 
        disordergroup = disorder.find('DisorderGroup').find('Name').text
        genes = []
    
        d_list = disorder.find("DisorderGeneAssociationList")
        d_list = d_list.findall("DisorderGeneAssociation")
        for g in d_list:
            g = g.find("Gene")
            geneObject = {}
            geneObject["id"] = g.attrib["id"]
            geneObject["name"] = g.find("Name").text
            geneObject["symbol"] = g.find("Symbol").text
            geneObject["type"] = g.find("GeneType").find("Name").text

            geneObject["synonyms"] = []
            synonyms = g.find("SynonymList").findall("Synonym")
            for s in synonyms:
                geneObject["synonyms"].append(s.text)

            geneObject["ExternalReferences"] = []
            ex = g.find("ExternalReferenceList").findall("ExternalReference")
            for e in ex:
                exObject = {}
                exObject["Source"] = e.find("Source").text
                exObject["Reference"] = e.find("Reference").text
                geneObject["ExternalReferences"].append(exObject)

            genes.append(geneObject)

        rows.append({"OrphaCode": orphacode, 
                     "Expert Link": expertlink, 
                     "Name": name, 
                     "DisorderType": disordertype, 
                     "DisorderGroup": disordergroup,
                     "Genes": genes
                })

    df = pd.DataFrame(rows, columns=df_cols)
    
    return df

