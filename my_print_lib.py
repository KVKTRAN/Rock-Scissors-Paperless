#!/usr/bin/env python
# coding: utf-8

# In[2]:


def print_disability(disease):
    count = 0
    
    print(" | Disabilities:")
    for dis in disease["DisabilityDisorderAssociationList"]:
        for d in dis:
            if count == 10:
                break
            print(" | ----------------------------------------------------")
            print(" | Disability : " + d["Disability"])
            print(" | FrequenceDisability : " + d["FrequenceDisability"])
            print(" | TemporalityDisability : " + d["TemporalityDisability"])
            print(" | SeverityDisability : " + d["SeverityDisability"])
            print(" | LossOfAbility : " + d["LossOfAbility"])
            print(" | Type : " + d["Type"])
            print(" | Defined : " + d["Defined"])
            count = count + 1

def print_phenotypes(disease):
    count = 0
    
    if disease["Number of HPO Disorder Association"] is not None:
        print(" | Phenotypes: there are " + disease["Number of HPO Disorder Association"].values[0] + " phenotypes.")
    else:
        print(" | Phenotypes:")
    for phe in disease["HPODisorderAssociationList"]:
        for p in phe:
            if count == 10:
                break
            print(" | ----------------------------------------------------")
            print(" | HPO Id: " + p["HPOId"])
            print(" | HPO Term: " + p["HPOTerm"])
            print(" | HPO Frequency: " + p["HPOFrequency"])
            
def print_prevalances(disease):
    print(" | Prevalences:")
    for pre in disease["PrevelanceList"]:
        for p in pre:
            print(" | ----------------------------------------------------")
            print(" | id: " + p["id"])
            print(" | Source: " + p["Source"])
            print(" | Prevalence Type: " + p["PrevalenceType"])
            print(" | Prevalence Qualication: " + p["PrevalenceQualification"])
            print(" | Prevalence Class: " + p["PrevalenceClass"])
            if p["Valmoy"] is not None:
                print(" | Valmoy: " + p["Valmoy"])
            else:
                print(" | Valmot: None")
            print(" | Prevalence Geographic: " + p["PrevalenceGeographic"])
            print(" | Prevalence Validation Status: " + p["PrevalenceValidationStatus"])

def print_genes(disease):
    print("Gene Associations:")
    for gene in disease.Genes:
        for ge in gene:
            print("----------------------------------------------------")
            print("ID: " + ge["id"])
            print("Name: " + ge["name"])
            print("Symbol: " + ge["symbol"])
            print("Type: " + ge["type"])
            print("Synonyms: ")
            for sy in ge["synonyms"]:
                print("     - " + sy)
            print("References List: ")
            for re in ge["ExternalReferences"]:
                print("     - Source: " + re["Source"] + " | Reference: " + re["Reference"])
       
def print_disease(disease):
    print("----------------------------------------------------")
    print("Orpha Code: " + str(disease.OrphaCode.values[0]))
    print("Expert Link: " + disease["Expert Link"].values[0])
    print("Name: " + disease.Name.values[0])
    print("Disorder Type: " + disease.DisorderType.values[0])
    print("Disorder Group: " + disease.DisorderGroup.values[0])
    print("----------------------------------------------------")
    # print_genes(disease)

def print_disease2(disease):
    print("----------------------------------------------------")
    print("Orpha Code: " + str(disease.OrphaCode.values[0]))
    print("Expert Link: " + disease["Expert Link"].values[0])
    print("Name: " + disease.Name.values[0])
    print("Disorder Type: " + disease.DisorderType.values[0])
    print("Disorder Group: " + disease.DisorderGroup.values[0])
    print("----------------------------------------------------")
# In[ ]:




