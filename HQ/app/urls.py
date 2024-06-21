from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='index'),
    path('signup', signup, name='signup'),
    path('login', login, name='login'),
    path('logout', logout, name='logout'),
    path('profil', profil, name='profil'),
    path('membres/list', liste_utilisateurs, name='liste_utilisateurs'),
    path('membres/add', ajout_utilisateur, name='ajout_utilisateur'),
    path('membres/delete/<str:slug>', suppression_utilisateur, name='suppression_utilisateur'),
    path('my_publications/list', vue_globale_publications, name='vue_globale_publications'),
    path('my_publications/add', creation_publication, name='creation_publication'),
    path('my_publications/add/type=<int:type>', publication_add, name='publication_add'),
    path('my_publications/delete/<int:id>', delete_publication, name='delete_publication'),
    path('centre_interets', centre_interets, name='centre_interets'),
    path('conversations/all', conversations, name='conversations'),
    path('conversations/membre/<str:membre_slug>', conversation_membre, name='conversation_membre'),
    path('message/delete/<int:message_id>', supprimer_message, name='supprimer_message'),
    
]
    