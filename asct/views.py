from django.shortcuts import render # type: ignore

def pcra_home(request):
    return render(request, 'pcra/pcra-home.html')
