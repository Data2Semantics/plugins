from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponseBadRequest
from django.shortcuts import render_to_response
import httplib, urllib, json
from rdflib import ConjunctiveGraph
from glob import glob
import re

def home(request):
    return render_to_response('home.html')
    

def test(request, ttype, test):
    # Get the request_host (without the port)
    
    request_path = request.path
    request_host = 'http://'+request.get_host()+request_path.replace(request.path_info,'')
    # print request_host
    
    if ttype in ['publications', 'mascc'] :
        if test in [re.search(r'ttl/(.*)\.ttl',n).group(1) for n in glob('/var/www/semweb.cs.vu.nl/plugins/ttl/*.ttl')] :
            filename = "/var/www/semweb.cs.vu.nl/plugins/ttl/{}.ttl".format(test)
            cg = ConjunctiveGraph()
            cg.parse(filename, format='n3')
        
            # print "Request received"
            
            if ttype == 'publications' :
                response = HttpResponseRedirect(request_host+'/publications/{}'.format(urllib.quote(cg.serialize(format='turtle'),safe='')))
            elif ttype == 'mascc' :
                response = HttpResponseRedirect(request_host+'/mascc/{}'.format(urllib.quote(cg.serialize(format='turtle'),safe='')))
            else :
                response = HttpResponseBadRequest()
        else :
            response = HttpResponseNotFound()
    elif ttype == 'bad' :
        response = HttpResponseRedirect(request_host+'/mascc/bad_request')
    else :
        response = HttpResponseNotFound()
                    
    return response