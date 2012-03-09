from rdflib import ConjunctiveGraph, Namespace, RDF, RDFS, Literal, URIRef, XSD
from django.http import HttpResponse
from logging import getLogger, DEBUG, FileHandler, Formatter
from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint
import httplib, urllib, json
from util.util import not_turtle_response, multiple_patients_response
import itertools
from collections import Counter

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
        
    aers_sparql = SPARQLWrapper("http://eculture2.cs.vu.nl:5020/sparql/")
    aers_sparql.setReturnFormat(JSON)

    lld_sparql = SPARQLWrapper("http://linkedlifedata.com/sparql")
    lld_sparql.setReturnFormat(JSON)
    
    ranking = Counter()
    
    # Chain generators for all values for the attributes of the patient
    features = itertools.chain(cg.objects(subject=patient, predicate=PO['hasIndication']), \
        cg.objects(subject=patient, predicate=PO['hasMeasurement']), \
        cg.objects(subject=patient, predicate=PO['usesMedication']), \
        cg.objects(subject=patient, predicate=PO['hadPreviousIndication']), \
        cg.objects(subject=patient, predicate=PO['hadRecentTreatment']))
        
    exp_features = set()
    q_part = ""

    # First get all sameAs uris for the values
    for f in features :
        if str(f).startswith('http://linkedlifedata.com'): 
            exp_features.add(str(f))
        
        q_part += "{?altname owl:sameAs <"+f+"> .} UNION { <"+f+"> owl:sameAs ?altname .} UNION \n"

    q_part = q_part[:-8]
    
    q = """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX owl: <http://www.w3.org/2002/07/owl#>
        SELECT ?altname
        WHERE { """ + q_part + """ }
    """

    aers_sparql.setQuery(q)
    
    results = aers_sparql.query().convert()

    # Only query LLD for stuff that LLD knows about (saves quite some time)
    for result in results["results"]["bindings"]:
        if result["altname"]["value"].startswith('http://linkedlifedata.com') :
            exp_features.add(result["altname"]["value"])
        
    # Then lookup the publications that mention these, and add them to a tally (Counter)
    for ef in exp_features :
        q = """
            PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
            PREFIX lifeskim: <http://linkedlifedata.com/resource/lifeskim/>
            SELECT ?pubmed
            WHERE { ?pubmed lifeskim:mentions <"""+ef+"""> . }
            LIMIT 250
        """
        lld_sparql.setQuery(q)
        
        results = lld_sparql.query().convert()

        for result in results["results"]["bindings"]:
            ranking[result["pubmed"]["value"]] += 1
    
    # Return only the 20 most frequent publications
    ranking_json = json.dumps(ranking.most_common(50))
    # print ranking_json
    return HttpResponse(ranking_json, mimetype='application/json')