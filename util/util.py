from django.http import HttpResponse
from pygments.lexers import (get_lexer_by_name,get_lexer_for_filename)
from pygments import highlight
from pygments.formatters import HtmlFormatter


pygments_css = HtmlFormatter().get_style_defs('.highlight')
bad_request_pattern = '<html><head><style>{}</style></head><body><h1>Bad Request</h1><p>{}<p><p>This is what you sent me:</p>{}</body></html>'

def not_turtle_response(data):
    bad_request = HttpResponse(bad_request_pattern.format(pygments_css, 'Request is not valid: I expect turtle!',data))
    bad_request.status_code = 400
    return bad_request

def multiple_patients_response(data):
    bad_request = HttpResponse(bad_request_pattern.format(pygments_css, 'Request is not valid: you gave me multiple patients',format_code(data)))
    bad_request.status_code = 500
    return bad_request


def format_code(turtle):
    turtle_lexer = get_lexer_by_name("turtle")
    return highlight(turtle, turtle_lexer, HtmlFormatter())