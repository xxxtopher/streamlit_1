# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 11:14:43 2020

@author: Bogdan Tudose
"""


#%%Import Packages
import streamlit as st
import pandas as pd

import spacy
from spacy import displacy
from collections import Counter
import en_core_web_sm
#%%
#Headings for Web Application
st.title("Natural Language Processing Web Application Example")
nlp = en_core_web_sm.load()
#Textbox for text user is entering
st.subheader("Enter the text you'd like to analyze.")
text = st.text_area('Enter text') #text is stored in this variable

text2 = """In February 2012, Equedia was paid $35,000 by MAG Silver Corp. (“MAG Silver”)
 for six months of media coverage, which includes related marketing expenses.
  In July 2012, Equedia was paid an additional $40,000 for an additional 
  six months of media coverage on MAG Silver, plus an expenses advance 
  of $150,000 for advertisements made on third party sites or other third party 
  coverage that we arranged for MAG Silver."""
st.write("or copy the text below")
st.text(text2)

#Display results of the NLP task
st.header("Results")

st.subheader("Named Entities")
#Function to take in dictionary of entities, type of entity, and returns specific entities of specific type
def entRecognizer(entDict, typeEnt):
    entList = [ent for ent in entDict if entDict[ent] == typeEnt]
    return entList

#Getting Entity and type of Entity
entities = []
entityLabels = []
doc = nlp(text)
for ent in doc.ents:
    entities.append(ent.text)
    entityLabels.append(ent.label_)
entDict = dict(zip(entities, entityLabels)) #Creating dictionary with entity and entity types

#Using function to create lists of entities of each type
entOrg = entRecognizer(entDict, "ORG")
entCardinal = entRecognizer(entDict, "CARDINAL")
entPerson = entRecognizer(entDict, "PERSON")
entDate = entRecognizer(entDict, "DATE")
entGPE = entRecognizer(entDict, "GPE")
entMoney = entRecognizer(entDict, "MONEY")

#Displaying entities of each type
st.write("Organization Entities: " + str(entOrg))
st.write("Monetary Entities: " + str(entMoney))
st.write("Cardinal Entities: " + str(entCardinal))
st.write("Personal Entities: " + str(entPerson))
st.write("Date Entities: " + str(entDate))
st.write("GPE Entities: " + str(entGPE))

#Visualize with Displacy
st.subheader("Named Entities with Displacy")
html = displacy.render(doc,style="ent")
st.write(html,unsafe_allow_html=True)

# HTML_WRAPPER = """<div style="overflow-x: auto; border: 1px solid #e6e9ef; border-radius: 0.25rem; padding: 1rem">{}</div>"""
# html = html.replace("\n\n","\n")
# st.write(HTML_WRAPPER.format(html),unsafe_allow_html=True)

