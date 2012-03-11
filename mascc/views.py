'''
Created on Mar 6, 2012

@author: hoekstra
'''
from rdflib import ConjunctiveGraph, Namespace, RDF, RDFS, Literal, URIRef, XSD
from django.http import HttpResponse
from logging import getLogger, DEBUG, FileHandler, Formatter
from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint
import httplib, urllib, json
from util.util import not_turtle_response, multiple_patients_response, not_febrile_neutropenia_response


def parse(request, graph):
    
    
    l = getLogger('MASCC')
    fh = FileHandler('mascc.log')
    fh.setLevel(DEBUG)
    formatter = Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    l.addHandler(fh)
    l.info('Baaa')
    
    try :
        cg = ConjunctiveGraph().parse(data=graph, format='n3')
    except :   
        return not_turtle_response(graph)
    
    DRUG = Namespace('http://aers.data2semantics.org/resource/drug/')
    IND = Namespace('http://aers.data2semantics.org/resource/indication/')
    PO = Namespace('http://www.data2semantics.org/ontology/patient/')
    UMLS = Namespace('http://linkedlifedata.com/resource/umls/id/')
    
    
    cg.bind('drug',DRUG)
    cg.bind('po',PO)
    cg.bind('umls',UMLS)
    cg.bind('indication',IND)
    
    try :
        patient = cg.value(predicate=RDF.type, object=PO['Patient'], any=False)
    except:
        # More than one patient
        return multiple_patients_response(cg.serialize(format='turtle'))
    
    # If the patient does not have fever, nor neutropenia, return null
    if not (cg.value(predicate=PO['hasIndication'],object=UMLS['C0027947']) and cg.value(predicate=PO['hasMeasurement'],object=UMLS['C0015967'])) :
        return not_febrile_neutropenia_response(cg.serialize(format='turtle'))
    else :
        # We now know the patient has Febrile Neutropenia
        cg.add((patient,PO['hasIndication'],UMLS['C0746883']))
    
    # Initialise the score to zero
    score = 0
    
    if cg.value(predicate=PO['burdernOfIllness'],object=PO['MildSymptoms']) or cg.value(predicate=PO['burdernOfIllness'],object=PO['NoSymptoms']) :
        # Burden of illness: no or mild symptoms
        l.debug("No or mild symptoms\n")
        score += 5
    if not cg.value(predicate=PO['hasIndication'],object=UMLS['C0020649']) :
        # No hypotension
        l.debug("No hypotension\n")
        score += 5
    if not cg.value(predicate=PO['hasIndication'],object=UMLS['C0024117']) :
        # No COPD
        l.debug("No COPD\n")
        score += 4
    if cg.value(predicate=PO['hasIndication'],object=UMLS['C0280100']) or not cg.value(predicate=PO['hadPreviousIndication'],object=UMLS['C0026946']) :
        # Adult: C0280099
        # Child: C0279068
        # Solid tumor or no previous fungal infection (Mycoses)
        l.debug("Solid tumor or no previous fungal infection\n")
        score += 4
    if not cg.value(predicate=PO['hasIndication'],object=UMLS['C0011175']) :
        # No dehydration
        l.debug("No dehydration\n")
        score += 3
    if cg.value(predicate=PO['burdernOfIllness'],object=PO['ModerateSymptoms']) :
        # Burden of illness: no or mild symptoms
        l.debug("Moderate symptoms\n")
        score += 3
    if cg.value(predicate=PO['hasStatus'],object=PO['outpatient']) :
        # Burden of illness: no or mild symptoms
        l.debug("Outpatient\n")
        score += 3
        
    patient = cg.value(predicate=RDF.type, object=PO['Patient'])
    age = cg.value(subject=patient,predicate=PO['hasAge'])
    
    if age.toPython < 20 :
        # Age is under 20
        l.debug("Age is under 20\n")
        score += 2 

    l.debug("Age: {} \n".format(age))
        
    l.debug("Score: {}".format(score))
        
    if score > 21 :
        cg.add((patient, PO['complicationRisk'], PO['lowRisk']))
    else :
        cg.add((patient, PO['complicationRisk'], PO['highRisk']))
        
    cg.add((patient, PO['masccIndex'], Literal(score, datatype=XSD['int'])))
        
    response =  HttpResponse(cg.serialize(format='turtle'), content_type='text/turtle')
    response['Content-Disposition'] = 'attachment; filename=patient.ttl'
    
    return response

    