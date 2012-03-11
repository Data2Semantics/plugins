from django.http import HttpResponse
from django.shortcuts import render_to_response
from pygments.lexers import (get_lexer_by_name,get_lexer_for_filename)
from pygments import highlight
from pygments.formatters import HtmlFormatter


pygments_css = HtmlFormatter().get_style_defs('.highlight')
bad_request_pattern = '<html><head><style>{}</style></head><body><h1>Bad Request</h1><p>{}<p><p>This is what you sent me:</p>{}</body></html>'

def not_turtle_response(data):
    response = render_to_response('error.html', { 'pygcss' : pygments_css, 'message': 'Request is not valid: I expect turtle!', 'code': data})
    response.status_code = 400
    return response

def multiple_patients_response(data):
    response = render_to_response('error.html', { 'pygcss' : pygments_css, 'message': 'Request is not valid: you gave me multiple patients', 'code': format_code(data)})
    response.status_code = 500
    return response

def not_febrile_neutropenia_response(data):
    response = render_to_response('error.html', { 'pygcss' : pygments_css, 'message': 'Cannot calculate MASCC: your patient does not have Febrile Neutropenia', 'code': format_code(data)})
    response.status_code = 500
    return response

def format_code(turtle):
    turtle_lexer = get_lexer_by_name("turtle")
    return highlight(turtle, turtle_lexer, HtmlFormatter())