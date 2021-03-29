from django.shortcuts import render

# Create your views here.
def index(request):
    context = {
        'turn_on_block': True,
    }
    return render(request, 'index.html', context=context)