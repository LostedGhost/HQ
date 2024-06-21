from django.shortcuts import render
from app.models import *

# Create your views here.
def index(request):
    nb_membres = f"{User.objects.filter(profil_id=2).count()}".zfill(2)
    nb_publications = f"{Publication.objects.count()}".zfill(2)
    nb_couples = f"{Couple.objects.count()}".zfill(2)
    print("nb_membres: ", nb_membres)
    print("nb_publications: ", nb_publications)
    print("nb_couples: ", nb_couples)
    return render(request, 'presentation/index.html',{
        "nb_membres": nb_membres,
        "nb_publications": nb_publications,
        "nb_couples": nb_couples,
    })

def logout(request):
    return render(request, 'presentation/index.html')