# Plugins for Hubble

This repository contains the code for several plugins for Hubble. These plugins are based on the Python [Django](http://django.org) framework.

## Plugins

### MASCC Index plugin

This plugin takes a Turtle representation of a patient (expressed using the [Patient Ontology](https://github.com/Data2Semantics/raw2ld/blob/master/vocab/patient_vocab.owl)), and interprets the values for the `po:hasIndication`, `po:hadPreviousIndication`, `po:burdenOfIllness` and `po:patientStatus` properties to determine the **MASCC** index for that patient. 

The **MASCC** index gives an estimation whether the patient is a `po:highRisk` patient or not, in the case of [Febrile Neutropenia](http://aers.data2semantics.org/resource/indication/FEBRILE_NEUTROPENIA). We take the MASCC score as defined in "[Management of febrile neutropenia: ESMO Clinical Recommendations](http://dx.doi.org/doi:10.1093/annonc/mdp163)".

The plugin outputs an "enriched" version of the patient record, including the MASCC score, the inference that the patient has Febrile Neutropenia, and a conclusion as to whether the patient is `po:highRisk` or not. 

* Only works for Turtle serializations containing a *single* patient
* Only works for patients that are both Febrile and have Neutropenia
* Only works if these diagnoses are expressed using UMLS codes from the [Linked Life Data](http://linkedlifedata.com) repository.

**NB:** This is all still **very hacky**!!


#### Usage

* Create a patient record according to the [Patient Ontology](https://github.com/Data2Semantics/raw2ld/blob/master/vocab/patient_vocab.owl) vocabulary, using the UMLS identifiers specified by [Linked Life Data](http://linkedlifedata.com). A couple of tips:
	* Make sure there is only one instance of `po:Patient` in the turtle serialization
	* Make sure the patient has at least the value `umls:C0027947` (Neutropenia) for a `po:hasIndication` property.  
	* Make sure the patient has at least the value `umls:C0015967` (Fever) for a `po:hasMeasurement` property. 
* Append a URL encoded Turtle serialisation of your patient record to the <http://YOURHOSTHERE/mascc/> URL.
* Perform an HTTP GET to that URL (i.e. copy paste it to your browser's address bar)
* The service will return an enriched version of the patient record

#### Example

This is a patient called "John Doe". The patient has a number of "indications" (diagnoses), most notably `umls:C0027947` (Neutropenia), and a measurement `umls:C0015967` (Fever):

	@prefix drug: <http://aers.data2semantics.org/resource/drug/> .
	@prefix indication: <http://aers.data2semantics.org/resource/indication/> .
	@prefix owl: <http://www.w3.org/2002/07/owl#> .
	@prefix po: <http://www.data2semantics.org/ontology/patient/> .
	@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
	@prefix umls: <http://linkedlifedata.com/resource/umls/id/> .
	@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
	
	<http://www.data2semantics.org/patient-example.owl/john_doe> a po:Patient,
	        owl:NamedIndividual;
	    rdfs:label "john_doe"@en;
	    po:burdenOfIllness po:Severe;
	    po:complicationRisk po:highRisk;
	    po:hadPreviousIndication umls:C0026946;
	    po:hadRecentTreatment umls:C0559692;
	    po:hasAge 67;
	    po:hasIndication indication:DIARRHOEA,
	        indication:VOMITING,
	        umls:C0024117,
	        umls:C0027947,
	        umls:C0280100,
	        umls:C0376545,
	        umls:C0746883,
	        indication:CLOSTRIDIUM_COLITIS,
	        indication:LEUKAEMIA_RECURRENT;
	    po:hasMeasurement umls:C0015967,
	        umls:C0277884;
	    po:hasStatus po:outpatient;
	    po:masccIndex "15"^^xsd:int;
	    po:usesMedication drug:AMBISOME,
	        drug:CEFPROZIL,
	        drug:CETIRIZINE_HYDROCHLORIDE,
	        drug:FORADIL,
	        drug:MERCAPTOPURINE;
	    rdfs:comment "over 60, matches all other criteria" .
    
Using the demo MASCC service at <http://semweb.cs.vu.nl/plugins/mascc>, we can now compute the MASCC score for John Doe, by following [this link](http://semweb.cs.vu.nl/plugins/mascc/%40prefix%20ns1%3A%20%3Chttp%3A%2F%2Fwww.data2semantics.org%2Fontology%2Fpatient%2F%3E%20.%0A%40prefix%20owl%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2002%2F07%2Fowl%23%3E%20.%0A%40prefix%20rdfs%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2000%2F01%2Frdf-schema%23%3E%20.%0A%40prefix%20xsd%3A%20%3Chttp%3A%2F%2Fwww.w3.org%2F2001%2FXMLSchema%23%3E%20.%0A%0A%3Chttp%3A%2F%2Fwww.data2semantics.org%2Fpatient-example.owl%2Fjohn_doe%3E%20a%20ns1%3APatient%2C%0A%20%20%20%20%20%20%20%20owl%3ANamedIndividual%3B%0A%20%20%20%20rdfs%3Alabel%20%22john_doe%22%40en%3B%0A%20%20%20%20ns1%3AburdenOfIllness%20ns1%3ASevere%3B%0A%20%20%20%20ns1%3AhadPreviousIndication%20%3Chttp%3A%2F%2Flinkedlifedata.com%2Fresource%2Fumls%2Fid%2FC0026946%3E%3B%0A%20%20%20%20ns1%3AhadRecentTreatment%20%3Chttp%3A%2F%2Flinkedlifedata.com%2Fresource%2Fid%2Fumls%2FC0559692%3E%3B%0A%20%20%20%20ns1%3AhasAge%2067%3B%0A%20%20%20%20ns1%3AhasIndication%20%3Chttp%3A%2F%2Faers.data2semantics.org%2Fresource%2Findication%2FDIARRHOEA%3E%2C%0A%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Faers.data2semantics.org%2Fresource%2Findication%2FVOMITING%3E%2C%0A%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Flinkedlifedata.com%2Fresource%2Fumls%2Fid%2FC0024117%3E%2C%0A%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Flinkedlifedata.com%2Fresource%2Fumls%2Fid%2FC0027947%3E%2C%0A%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Flinkedlifedata.com%2Fresource%2Fumls%2Fid%2FC0280100%3E%2C%0A%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Flinkedlifedata.com%2Fresource%2Fumls%2Fid%2FC0376545%3E%3B%0A%20%20%20%20ns1%3AhasMeasurement%20%3Chttp%3A%2F%2Flinkedlifedata.com%2Fresource%2Fumls%2Fid%2FC0015967%3E%2C%0A%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Flinkedlifedata.com%2Fresource%2Fumls%2Fid%2FC0277884%3E%3B%0A%20%20%20%20ns1%3AhasStatus%20ns1%3Aoutpatient%3B%0A%20%20%20%20ns1%3AusesMedication%20%3Chttp%3A%2F%2Faers.data2semantics.org%2Fresource%2Fdrug%2FAMBISOME%3E%2C%0A%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Faers.data2semantics.org%2Fresource%2Fdrug%2FCEFPROZIL%3E%2C%0A%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Faers.data2semantics.org%2Fresource%2Fdrug%2FCETIRIZINE_HYDROCHLORIDE%3E%2C%0A%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Faers.data2semantics.org%2Fresource%2Fdrug%2FFORADIL%3E%2C%0A%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Faers.data2semantics.org%2Fresource%2Fdrug%2FMERCAPTOPURINE%3E%2C%0A%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Faers.data2semantics.org%2Fresource%2Findication%2FCLOSTRIDIUM_COLITIS%3E%2C%0A%20%20%20%20%20%20%20%20%3Chttp%3A%2F%2Faers.data2semantics.org%2Fresource%2Findication%2FLEUKAEMIA_RECURRENT%3E%3B%0A%20%20%20%20rdfs%3Acomment%20%22over%2060%2C%20matches%20all%20other%20criteria%22%20.%0A%0A) (view the source of this page to see the actual URL… it's ugly!)

The service will respond with:

	@prefix drug: <http://aers.data2semantics.org/resource/drug/> .
	@prefix indication: <http://aers.data2semantics.org/resource/indication/> .
	@prefix owl: <http://www.w3.org/2002/07/owl#> .
	@prefix po: <http://www.data2semantics.org/ontology/patient/> .
	@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
	@prefix umls: <http://linkedlifedata.com/resource/umls/id/> .
	@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
	
	<http://www.data2semantics.org/patient-example.owl/john_doe> a po:Patient,
	        owl:NamedIndividual;
	    rdfs:label "john_doe"@en;
	    po:burdenOfIllness po:Severe;
	    po:complicationRisk po:highRisk;
	    po:hadPreviousIndication umls:C0026946;
	    po:hadRecentTreatment <http://linkedlifedata.com/resource/id/umls/C0559692>;
	    po:hasAge 67;
	    po:hasIndication indication:DIARRHOEA,
	        indication:VOMITING,
	        umls:C0024117,
	        umls:C0027947,
	        umls:C0280100,
	        umls:C0376545,
	        umls:C0746883;
	    po:hasMeasurement umls:C0015967,
	        umls:C0277884;
	    po:hasStatus po:outpatient;
	    po:masccIndex "15"^^xsd:int;
	    po:usesMedication drug:AMBISOME,
	        drug:CEFPROZIL,
	        drug:CETIRIZINE_HYDROCHLORIDE,
	        drug:FORADIL,
	        drug:MERCAPTOPURINE,
	        indication:CLOSTRIDIUM_COLITIS,
	        indication:LEUKAEMIA_RECURRENT;
	    rdfs:comment """No hypotension
	Solid tumor or no previous fungal infection
	No dehydration
	Outpatient
	Age: 67 
	Score: 15"""^^xsd:string,
	        "over 60, matches all other criteria" .

What has changed? 

* John Doe now has an additional `po:hasIndication` for `umls:C0746883` (Febrile Neutropenia)	
* His MASCC index (`po:masccIndex`) is *"15"*
* As a consequence of which, his `po:complicationRisk` is `po:highRisk`
* There's also a `rdfs:comment` explaining what contributed to the score.


#### Testing

You can test whether the plugin works at these test URLs:

* <http://YOURHOSTHERE/test/mascc/john_doe>  
	computes the score for John Doe
* <http://YOURHOSTHERE/test/mascc/two_patients>  
	**ERROR**: expects only a single patient
* <http://YOURHOSTHERE/test/mascc/no_neutropenia>  
	**ERROR**: the patient does not have Febrile Neutropenia


### Publications plugin

This plugin takes a Turtle representation of a patient (expressed using the [Patient Ontology](https://github.com/Data2Semantics/raw2ld/blob/master/vocab/patient_vocab.owl)) and uses the values for the `po:hasIndication`, `po:hasMeasurement`, `po:usesMedication`, `po:hadPreviousIndication` and `po:hadRecentTreatment` properties to find related publications as listed in the [Linked Life Data](http://linkedlifedata.com) (LLD) repository.

The plugin first calls the AERS-LD dataset to find the equivalent identifiers for these resources that LLD uses to connect to publications ([PubMed](http://www.ncbi.nlm.nih.gov/pubmed/) identifiers). 

The plugin orders the results by frequency, and returns a JSON representation of pairs of PubMed identifiers (in LLD) and frequency.

* Only works for Turtle serializations containing a *single* patient

#### Testing

You can test whether the plugin works at these test URLs:

* <http://YOURHOSTHERE/test/publications/john_doe>  
	Returns the top 50 relevant publications related to John Doe
* <http://YOURHOSTHERE/test/publications/two_patients>  
	**ERROR**: expects only a single patient
* <http://YOURHOSTHERE/test/publications/no_neutropenia>  
	Returns the top 50 relevant publications related to John Doe (without FN)

#### Usage

* Create a patient record according to the [Patient Ontology](https://github.com/Data2Semantics/raw2ld/blob/master/vocab/patient_vocab.owl) vocabulary, using the UMLS identifiers specified by [Linked Life Data](http://linkedlifedata.com).
* Append a URL encoded Turtle serialisation of your patient record to the <http://YOURHOSTHERE/publications/> URL.
* Perform an HTTP GET to that URL (i.e. copy paste it to your browser's address bar)
* The service will return a list of publications related to the patient

## Requirements

* Python 2.7
* [Pygments](http://pygments.org) for syntax highlighting
* [N3Pygments](https://github.com/gniezen/n3pygments) lexer for Pygments
* [RDFLib](http://rdflib.net) library for parsing RDF
* [SPARQLWrapper](http://sparql-wrapper.sourceforge.net/) library for querying SPARQL endpoints

The plugins make a number of (rather silly) assumptions:

1. The AERS-LD dataset is hosted behind a SPARQL endpoint at <http://eculture2.cs.vu.nl/sparql/>

