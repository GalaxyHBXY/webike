from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, template_name="main/index.html", context={'hide_hr': True})


def fail(request, context):
    return render(request, "main/fail.html", context=context)
