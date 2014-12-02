import cStringIO as StringIO
import ho.pisa as pisa
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse
from cgi import escape
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User

def render_to_pdf(template_src, context_dict):
    template = get_template(template_src)
    context = Context(context_dict)
    html  = template.render(context)
    result = StringIO.StringIO()

    pdf = pisa.pisaDocument(StringIO.StringIO(html.encode("ISO-8859-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), mimetype='application/pdf')
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))

def myview(request,username=None):
    try:
        usr =  User.objects.get(username=username)
        return render_to_pdf(
            'pdf/template.html',
            {
                'pagesize':'A4',
                'usr':usr,

            }
        )
    except Exception, e:
        return render(request,'404.html')
    