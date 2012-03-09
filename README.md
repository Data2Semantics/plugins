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

## Requirements

* Python 2.7
* [Pygments](http://pygments.org) for syntax highlighting
* [N3Pygments](https://github.com/gniezen/n3pygments) lexer for Pygments
* [RDFLib](http://rdflib.net) library for parsing RDF
* [SPARQLWrapper](http://sparql-wrapper.sourceforge.net/) library for querying SPARQL endpoints

The plugins make a number of (rather silly) assumptions:

1. The AERS-LD dataset is hosted behind a SPARQL endpoint at <http://eculture2.cs.vu.nl/sparql/>

