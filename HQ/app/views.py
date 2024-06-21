from django.shortcuts import render, redirect
from app.models import *
from app.utils import *

# Create your views here.
def index(request):
    error = request.session.pop('error',None)
    success = request.session.pop('success',None)
    user_id = request.session.get('user_id',None)
    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect("/app/login")
    
    return render(request, 'app/index.html', {
        "error": error,
        "success": success,
        "user": user,
    })

def signup(request):
    error = request.session.pop('error',None)
    success = request.session.pop('success',None)
    if request.POST:
        nom = request.POST.get('nom', None)
        prenom = request.POST.get('prenom', None)
        sexe = bool(int(request.POST.get('sexe')))
        dateNaissance = request.POST.get('dateNaissance', None)
        lieuNaissance = request.POST.get('lieuNaissance', None)
        bio = request.POST.get('bio', None)
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        
        membre = User(nom=nom, prenom=prenom, sexe=sexe, date_naissance=dateNaissance,lieu_naissance=lieuNaissance, bio=bio, email=email, password=chiffrement(password), profil_id=2)
        membre.save()
        
        photo = PhotoUtilisateur(user=membre, photo=request.FILES["photo"])
        photo.save()
        
        return redirect("/app/login")
    return render(request, 'app/signup.html',{
        "error":error,
        "success":success,
    })

def login(request):
    error = request.session.pop('error',None)
    success = request.session.pop('success',None)
    user_id = request.session.get('user_id',None)
    try:
        user = User.objects.get(id=user_id)
        return redirect("/app/")
    except:
        pass
    if request.POST:
        email = request.POST.get('email', None)
        password = request.POST.get('password', None)
        u = User.objects.filter(email=email, password=chiffrement(password))
        if u.exists():
            user = u.first()
            request.session["user_id"] = user.id
            return redirect("/app/")
        else:
            request.session["error"] = "Identifiants incorrects !!!"
            return redirect("/app/login")
    return render(request, 'app/login.html',{
        "error":error,
        "success":success,
    })

def logout(request):
    del request.session["user_id"]
    return redirect("/app/login")

def profil(request):
    error = request.session.pop('error',None)
    success = request.session.pop('success',None)
    user_id = request.session.get('user_id',None)
    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect("/app/login")
    if request.POST:
        if request.POST.get('password', None) == request.POST.get('repassword', None):
            nom = request.POST.get('nom', None)
            prenom = request.POST.get('prenom', None)
            date_naissance = request.POST.get('date_naissance', None)
            lieu_naissance = request.POST.get('lieu_naissance', None)
            bio = request.POST.get('bio', None)
            photo = request.FILES.get("photo", None)
            try:
                user.nom = nom
                user.prenom = prenom
                user.date_naissance = date_naissance
                user.lieu_naissance = lieu_naissance
                user.bio = bio
                user.password = chiffrement(request.POST.get('password', None))
                user.save()
                if photo:
                    photo = PhotoUtilisateur(user=user, photo=photo)
                    photo.save()
                request.session["success"] = "Profil mis à jour avec succès"
            except:
                request.session["error"] = "Erreur lors de la mise à jour du profil"
            return redirect("/app/profil")
        else:
            request.session["error"] = "Les deux mots de passe ne sont pas identiques"
            return redirect("/app/profil")
    return render(request, 'app/profil.html', {
        "error": error,
        "success": success,
        "user": user
    })

def liste_utilisateurs(request):
    error = request.session.pop('error',None)
    success = request.session.pop('success',None)
    user_id = request.session.get('user_id',None)
    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect("/app/login")
    members = User.objects.filter(profil_id=2)
    return render(request, "app/membres/list.html",{
        "error": error,
        "success": success,
        "user": user,
        "members": members
    })

def ajout_utilisateur(request):
    error = request.session.pop('error',None)
    success = request.session.pop('success',None)
    user_id = request.session.get('user_id',None)
    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect("/app/login")
    if request.POST:
        nom = request.POST.get('nom', None)
        prenom = request.POST.get('prenom', None)
        sexe = bool(int(request.POST.get('sexe')))
        dateNaissance = request.POST.get('dateNaissance', None)
        lieuNaissance = request.POST.get('lieuNaissance', None)
        bio = request.POST.get('bio', None)
        email = request.POST.get('email', None)
        password = generate_strong_password()
        
        try:
            membre = User(nom=nom, prenom=prenom, sexe=sexe, date_naissance=dateNaissance,lieu_naissance=lieuNaissance, bio=bio, email=email, password=chiffrement(password), profil_id=2)
            membre.save()
            photo = PhotoUtilisateur(user=membre, photo=request.FILES["photo"])
            photo.save()
            request.session["success"] = "Membre ajouté avec succès !!!"
        except:
            request.session["error"] = "Erreur lors de l'enregistrement !!!"
            return redirect("/app/membres/ajout")
        
        return redirect("/app/membres/list")
    return render(request, 'app/membres/add.html',{
        "error":error,
        "success":success,
        "user": user
    })

def suppression_utilisateur(request, slug):
    try:
        membre = User.objects.get(slug=slug)
        membre.delete()
        request.session["success"] = "Membre supprimé avec succès !!!"
    except:
        request.session["error"] = "Erreur lors de la suppression !!!"
    return redirect("/app/membres/list")

def vue_globale_publications(request):
    error = request.session.pop('error',None)
    success = request.session.pop('success',None)
    user_id = request.session.get('user_id',None)
    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect("/app/login")
    return render(request, "app/my_publications/list.html",{
        "error": error,
        "success": success,
        "user": user,
    })

def creation_publication(request):
    error = request.session.pop('error',None)
    success = request.session.pop('success',None)
    user_id = request.session.get('user_id',None)
    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect("/app/login")
    return render(request, "app/my_publications/add.html",{
        "error": error,
        "success": success,
        "user": user,
    })

def publication_add(request, type):
    error = request.session.pop('error',None)
    success = request.session.pop('success',None)
    user_id = request.session.get('user_id',None)
    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect("/app/login")
    if request.POST:
        try:
            texte = request.POST.get('texte', None)
            p = Publication(user=user, texte=texte, type_id=type)
            p.save()
            if type in [3, 4]:
                image = request.FILES.get('image', None)
                p.image = image
                p.save()
            if type in [5, 6]:
                video = request.FILES.get('video', None)
                p.video = video
                p.save()
            request.session["success"] = "Publication ajouté avec succès !!!"
        except:
            request.session["error"] = "Erreur lors de l'enregistrement !!!"
        return redirect("/app/my_publications/list")
    return render(request, "app/my_publications/add_for_type.html",{
        "error": error,
        "success": success,
        "user": user,
        "type": int(type),
    })

def delete_publication(request, id):
    p = Publication.objects.get(id=id)
    p.delete()
    request.session["success"] = "Publication supprimé avec succès !!!"
    return redirect("/app/my_publications/list")

def centre_interets(request):
    error = request.session.pop('error',None)
    success = request.session.pop('success',None)
    user_id = request.session.get('user_id',None)
    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect("/app/login")
    if request.POST:
        try:
            centres = request.POST.getlist('ctr_int', None)
            centres = [int(i) for i in centres]
            for ctr in user.centreInteretUtilisateur().all():
                if ctr.id not in centres:
                    ctr.delete()
            for centres_id in centres:
                ctr = CentreInteret.objects.get(id=centres_id)
                ctrUser = CentreInteretUtilisateur(centre_interet=ctr, user=user)
                ctrUser.save()
            request.session["success"] = "Centres d'intérêt ajoutés avec succès !!!"
        except:
            request.session["error"] = "Erreur lors de l'enregistrement !!!"
        return redirect("/app/centre_interets")
    return render(request,"app/centre_interets.html",{
        "error": error,
        "success": success,
        "user": user,
    })

def conversations(request):
    error = request.session.pop('error',None)
    success = request.session.pop('success',None)
    user_id = request.session.get('user_id',None)
    try:
        user = User.objects.get(id=user_id)
        conversations = Conversation.objects.filter(user1=user).union(Conversation.objects.filter(user2=user))
    except:
        return redirect("/app/login")
    return render(request,"app/conversation/all.html",{
        "error": error,
        "success": success,
        "user": user,
        "conversations": conversations,
    })

def conversation_membre(request, membre_slug):
    error = request.session.pop('error', None)
    success = request.session.pop('success', None)
    user_id = request.session.get('user_id', None)
    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect("/app/login")
    member = User.objects.get(slug=membre_slug)
    conversation_membre = Conversation.objects.filter(user1=user, user2=member).union(Conversation.objects.filter(user1=member, user2 = user))
    conversation = [c for c in conversation_membre]
    if len(conversation) > 0:
        conversation = conversation[0]
    else:
        conversation = None
    if request.POST:
        texte = request.POST.get('texte', None)
        if not conversation:
            conversation = Conversation(user1=user, user2=member)
            conversation.save()
        message = Message(texte=texte, conversation = conversation, user=user)
        if request.FILES:
            image = request.FILES.get('image', None)
            video = request.FILES.get('video', None)
            document = request.FILES.get('document',None)
            audio = request.FILES.get('audio', None)
            message.image = image
            message.video = video
            message.audio = audio
            message.document = document
        message.save()
        return redirect(f"/app/conversations/membre/{member.slug}")
        
    return render(request, 'app/conversation/membre.html',{
        "error":error,
        "success":success,
        "user":user,
        "conversation":conversation,
        "member":member
    })

def supprimer_message(request, message_id):
    user_id = request.session.get('user_id', None)
    try:
        user = User.objects.get(id=user_id)
    except:
        return redirect("/app/login")
    message = Message.objects.get(id=message_id)
    conversation = message.conversation
    if conversation.user1 == user:
        slug = conversation.user2.slug
    else:
        slug = conversation.user1.slug
    message.delete()
    request.session["success"] = "Message supprimé avec succès !!!"
    return redirect(f"/app/conversations/membre/{slug}")