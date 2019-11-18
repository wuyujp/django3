# from django.shortcuts import render
# from django.http import HttpResponse
# from django.template import Context, loader
from myhp.src import JudgeLanguage_Wiki

# def index(request):
#     template = loader.get_template('index.html')
#     context[pythonReturn] = HelloWorld.printHelloWorld("wuyu")
#     return HttpResponse(template.render(context, request))
#     #return HttpResponse(HelloWorld.printHelloWorld("wuyu"))

# # Create your views here.

from django.views.generic import TemplateView

class SampleTemplateView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        your_name = self.request.GET.get('your_name')
        context["Language"], context["Score"] = JudgeLanguage_Wiki.predictLanguage(your_name)
        return context

