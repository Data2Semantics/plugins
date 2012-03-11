from django.http import HttpResponse
from django.shortcuts import render_to_response
import httplib, urllib, json
from rdflib import ConjunctiveGraph
from glob import glob
import re

def home(request):
    return render_to_response('home.html')
    

def test(request, ttype, test):
    # Get the request_host (without the port)
    
    request_host = 'http://'+request.get_host()
    print request_host
    
    html_response = HttpResponse('')
    html_response.status_code = 303
    
    if ttype in ['publications', 'mascc'] :
        if test in [re.search(r'ttl/(.*)\.ttl',n).group(1) for n in glob('ttl/*.ttl')] :
            filename = "ttl/{}.ttl".format(test)
            cg = ConjunctiveGraph()
            cg.parse(filename, format='n3')
        
            print "Request received"
            
            if ttype == 'publications' :
                html_response['Location'] = request_host+'/publications/{}'.format(urllib.quote(cg.serialize(format='turtle'),safe=''))
            elif ttype == 'mascc' :
                html_response['Location'] = request_host+'/mascc/{}'.format(urllib.quote(cg.serialize(format='turtle'),safe=''))
    elif ttype == 'bad' :
        html_response['Location'] = request_host+'/mascc/bad_request'



    return html_response