from django.shortcuts import render # type: ignore

def asct_home(request):
    return render(request, 'asct/asct-home.html')



def index(request):
    return render(request, 'index.html')