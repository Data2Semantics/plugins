'''
Created on Mar 6, 2012

@author: hoekstra
'''
import urllib
import httplib


patient1 = """@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix : <http://www.data2semantics.org/patient-example.owl#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://www.data2semantics.org/patient-example.owl> .

<http://www.data2semantics.org/patient-example.owl/john_doe> rdf:type <http://www.data2semantics.org/ontology/patient/Patient> ,
                                                                      owl:NamedIndividual ;
                                                             
                                                             rdfs:label "john_doe"@en ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasAge> 67 ;
                                                             
                                                             rdfs:comment "over 60, matches all other criteria" ;
                                                             <http://www.data2semantics.org/ontology/patient/burdenOfIllness> <http://www.data2semantics.org/ontology/patient/Severe> ;
                                                             <http://www.data2semantics.org/ontology/patient/usesMedication> <http://aers.data2semantics.org/resource/drug/AMBISOME> ,
                                                                                                                             <http://aers.data2semantics.org/resource/drug/CEFPROZIL> ,
                                                                                                                             <http://aers.data2semantics.org/resource/drug/CETIRIZINE_HYDROCHLORIDE> ,
                                                                                                                             <http://aers.data2semantics.org/resource/drug/FORADIL> ,
                                                                                                                             <http://aers.data2semantics.org/resource/drug/MERCAPTOPURINE> ,
                                                                                                                             <http://aers.data2semantics.org/resource/indication/CLOSTRIDIUM_COLITIS> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://aers.data2semantics.org/resource/indication/DIARRHOEA> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/usesMedication> <http://aers.data2semantics.org/resource/indication/LEUKAEMIA_RECURRENT> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://aers.data2semantics.org/resource/indication/VOMITING> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hadRecentTreatment> <http://linkedlifedata.com/resource/id/umls/C0559692> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasMeasurement> <http://linkedlifedata.com/resource/umls/id/C0015967> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://linkedlifedata.com/resource/umls/id/C0024117> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hadPreviousIndication> <http://linkedlifedata.com/resource/umls/id/C0026946> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://linkedlifedata.com/resource/umls/id/C0027947> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasMeasurement> <http://linkedlifedata.com/resource/umls/id/C0277884> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://linkedlifedata.com/resource/umls/id/C0280100> ,
                                                                                                                            <http://linkedlifedata.com/resource/umls/id/C0376545> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasStatus> <http://www.data2semantics.org/ontology/patient/outpatient> ."""
                                            
two_patients = """@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix : <http://www.data2semantics.org/patient-example.owl#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://www.data2semantics.org/patient-example.owl> .

<http://www.data2semantics.org/patient-example.owl/dummy> rdf:type <http://www.data2semantics.org/ontology/patient/Patient> .

<http://www.data2semantics.org/patient-example.owl/john_doe> rdf:type <http://www.data2semantics.org/ontology/patient/Patient> ,
                                                                      owl:NamedIndividual ;
                                                             
                                                             rdfs:label "john_doe"@en ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasAge> 67 ;
                                                             
                                                             rdfs:comment "over 60, matches all other criteria" ;
                                                             <http://www.data2semantics.org/ontology/patient/burdenOfIllness> <http://www.data2semantics.org/ontology/patient/Severe> ;
                                                             <http://www.data2semantics.org/ontology/patient/usesMedication> <http://aers.data2semantics.org/resource/drug/AMBISOME> ,
                                                                                                                             <http://aers.data2semantics.org/resource/drug/CEFPROZIL> ,
                                                                                                                             <http://aers.data2semantics.org/resource/drug/CETIRIZINE_HYDROCHLORIDE> ,
                                                                                                                             <http://aers.data2semantics.org/resource/drug/FORADIL> ,
                                                                                                                             <http://aers.data2semantics.org/resource/drug/MERCAPTOPURINE> ,
                                                                                                                             <http://aers.data2semantics.org/resource/indication/CLOSTRIDIUM_COLITIS> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://aers.data2semantics.org/resource/indication/DIARRHOEA> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/usesMedication> <http://aers.data2semantics.org/resource/indication/LEUKAEMIA_RECURRENT> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://aers.data2semantics.org/resource/indication/VOMITING> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hadRecentTreatment> <http://linkedlifedata.com/resource/id/umls/C0559692> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasMeasurement> <http://linkedlifedata.com/resource/umls/id/C0015967> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://linkedlifedata.com/resource/umls/id/C0024117> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hadPreviousIndication> <http://linkedlifedata.com/resource/umls/id/C0026946> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://linkedlifedata.com/resource/umls/id/C0027947> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasMeasurement> <http://linkedlifedata.com/resource/umls/id/C0277884> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://linkedlifedata.com/resource/umls/id/C0280100> ,
                                                                                                                            <http://linkedlifedata.com/resource/umls/id/C0376545> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasStatus> <http://www.data2semantics.org/ontology/patient/outpatient> ."""

no_neutropenia = """@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix : <http://www.data2semantics.org/patient-example.owl#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@base <http://www.data2semantics.org/patient-example.owl> .

<http://www.data2semantics.org/patient-example.owl/john_doe> rdf:type <http://www.data2semantics.org/ontology/patient/Patient> ,
                                                                      owl:NamedIndividual ;
                                                             
                                                             rdfs:label "john_doe"@en ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasAge> 67 ;
                                                             
                                                             rdfs:comment "over 60, matches all other criteria" ;
                                                             <http://www.data2semantics.org/ontology/patient/burdenOfIllness> <http://www.data2semantics.org/ontology/patient/Severe> ;
                                                             <http://www.data2semantics.org/ontology/patient/usesMedication> <http://aers.data2semantics.org/resource/drug/AMBISOME> ,
                                                                                                                             <http://aers.data2semantics.org/resource/drug/CEFPROZIL> ,
                                                                                                                             <http://aers.data2semantics.org/resource/drug/CETIRIZINE_HYDROCHLORIDE> ,
                                                                                                                             <http://aers.data2semantics.org/resource/drug/FORADIL> ,
                                                                                                                             <http://aers.data2semantics.org/resource/drug/MERCAPTOPURINE> ,
                                                                                                                             <http://aers.data2semantics.org/resource/indication/CLOSTRIDIUM_COLITIS> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://aers.data2semantics.org/resource/indication/DIARRHOEA> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/usesMedication> <http://aers.data2semantics.org/resource/indication/LEUKAEMIA_RECURRENT> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://aers.data2semantics.org/resource/indication/VOMITING> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hadRecentTreatment> <http://linkedlifedata.com/resource/id/umls/C0559692> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasMeasurement> <http://linkedlifedata.com/resource/umls/id/C0015967> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://linkedlifedata.com/resource/umls/id/C0024117> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hadPreviousIndication> <http://linkedlifedata.com/resource/umls/id/C0026946> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasMeasurement> <http://linkedlifedata.com/resource/umls/id/C0277884> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasIndication> <http://linkedlifedata.com/resource/umls/id/C0280100> ,
                                                                                                                            <http://linkedlifedata.com/resource/umls/id/C0376545> ;
                                                             
                                                             <http://www.data2semantics.org/ontology/patient/hasStatus> <http://www.data2semantics.org/ontology/patient/outpatient> ."""


conn = httplib.HTTPConnection("localhost:8000")
conn.request("GET", "/mascc/"+urllib.quote(patient1,safe=''))
r1 = conn.getresponse()

data = r1.read()
conn.close()

#print "Patient 1"
#print "URL: {}".format('http://mac311.few.vu.nl:8000/mascc/'+urllib.quote(patient1,safe=''))
print data

#print "Patient 2"
#print "URL: {}".format('http://mac311.few.vu.nl:8000/mascc/'+urllib.quote(patient2,safe=''))
#conn = httplib.HTTPConnection("localhost:8000")
#conn.request("GET", "/mascc/"+urllib.quote(patient2,safe=''))
#r1 = conn.getresponse()
#
#data = r1.read()
#conn.close()
#
#print data
            