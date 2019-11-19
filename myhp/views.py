# from django.shortcuts import render
# from django.http import HttpResponse
# from django.template import Context, loader
from myhp.src import JudgeLanguage_Wiki
import datetime

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
        if your_name :
        	your_name = your_name.upper()
        dt1 = datetime.date(2019,8,12)
        dt2 = datetime.date.today()
        dt = dt2-dt1
        year = dt2.year - dt1.year
        month = year * 12 + dt2.month - dt1.month
        days = dt.days
        context["version"] = "Version: " + ".".join([str(year), str(month), str(days)])



        if your_name in ["WUYU", "WU YU", "YU WU"] : 
        	context["Language"] = "老婆我爱你！"
        	return context
        if your_name in ["ZHOUWENJI", "ZHOU WEN JI", "ZHOU WENJI", "WENJI ZHOU", "WEN JI ZHOU"] : 
        	context["Language"] = "99天纪念日快乐！"
        	return context
        if your_name :
            context["Language"], context["Score"] = JudgeLanguage_Wiki.predictLanguage(your_name)
        return context

