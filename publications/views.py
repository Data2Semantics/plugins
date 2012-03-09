from rdflib import ConjunctiveGraph, Namespace, RDF, RDFS, Literal, URIRef, XSD
from django.http import HttpResponse
from logging import getLogger, DEBUG, FileHandler, Formatter
from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint
import httplib, urllib, json
from util.util import not_turtle_response, multiple_patients_response
import itertools

def retrieve(request, graph):
    
    try :
        cg = ConjunctiveGraph().parse(data=graph, format='n3')
    except :   
        return not_turtle_response(graph)

    
    DRUG = Namespace('http://aers.data2semantics.org/resource/drug/')
    PO = Namespace('http://www.data2semantics.org/ontology/patient/')
    UMLS = Namespace('http://linkedlifedata.com/resource/umls/id/')
    LS = Namespace('http://linkedlifedata.com/resource/lifeskim/')
    
    cg.bind('drug',DRUG)
    cg.bind('po',PO)
    cg.bind('umls',UMLS)
    cg.bind('lifeskim',LS)
    
    try :
        patient = cg.value(predicate=RDF.type, object=PO['Patient'], any=False)
    except:
        # More than one patient
        return multiple_patients_response(cg.serialize(format='turtle'))
        
    if (cg.value(predicate=PO['hasIndication'],object=UMLS['C0027947']) and cg.value(predicate=PO['hasMeasurement'],object=UMLS['C0015967'])) :
        # We now know the patient has Febrile Neutropenia
        cg.add((patient,PO['hasIndication'],UMLS['C0746883']))
        
    sparql = SPARQLWrapper("http://linkedlifedata.com/sparql")
    sparql.setReturnFormat(JSON)
    
    ranking = {}
    
    # Chain generators for all values for the attributes of the patient
    features = itertools.chain(cg.objects(subject=patient, predicate=PO['hasIndication']), cg.objects(subject=patient, predicate=PO['hasMeasurement']), cg.objects(subject=patient, predicate=PO['usesMedication']))
    
    for f in features :
        q = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX lifeskim: <http://linkedlifedata.com/resource/lifeskim/>
            SELECT ?pubmed
            WHERE { ?pubmed lifeskim:mentions <"""+f+"""> . }
            LIMIT 100
        """
        sparql.setQuery(q)
        
        results = sparql.query().convert()

        for result in results["results"]["bindings"]:
            ranking.setdefault(result["pubmed"]["value"],0)
            ranking[result["pubmed"]["value"]] += 1
    
        
    ranking_json = json.dumps(ranking)
    # print ranking_json
    return HttpResponse(ranking_json, mimetype='application/json')