from django.http import HttpResponse
import httplib, urllib, json
from rdflib import ConjunctiveGraph
from glob import glob
import re

def test(request, ttype, test):

    html_response = HttpResponse('')
    html_response.status_code = 303
    
    if ttype in ['publications', 'mascc'] :
        if test in [re.search(r'ttl/(.*)\.ttl',n).group(1) for n in glob('ttl/*.ttl')] :
            filename = "ttl/{}.ttl".format(test)
            cg = ConjunctiveGraph()
            cg.parse(filename, format='n3')
        
            print "Request received"
            
            if ttype == 'publications' :
                html_response['Location'] = 'http://localhost:2000/publications/{}'.format(urllib.quote(cg.serialize(format='turtle'),safe=''))
            elif ttype == 'mascc' :
                html_response['Location'] = 'http://localhost:2000/mascc/{}'.format(urllib.quote(cg.serialize(format='turtle'),safe=''))
    elif ttype == 'bad' :
        html_response['Location'] = 'http://localhost:2000/mascc/bad_request'



    return html_response