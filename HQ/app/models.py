from django.db import models
from app.utils import *

# Create your models here.
class Profil(models.Model):
    libelle = models.CharField(max_length = 200)

class User(models.Model):
    nom = models.CharField(max_length = 200)
    prenom = models.CharField(max_length = 200)
    sexe = models.BooleanField(default=True) # True pour les garçons, False pour les filles
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length = 200)
    bio = models.TextField(default="Biographie")
    email = models.EmailField()
    password = models.CharField(max_length = 200)
    profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
    date_enregistrement = models.DateTimeField(auto_now_add=True)
    slug = models.CharField(max_length=20, default=None, null=True, unique=True)
    
    def save(self, *args, **kwargs):
        if not self.slug:
            g = generate_string()
            slug_list = [s.slug for s in User.objects.all()]
            while g in slug_list:
                g = generate_string()
            self.slug = g
        super().save(*args, **kwargs)
    
    def prenom_nom_rep(self):
        return truncatechars(self.prenom_nom(), 13)
    
    def bio_rep(self):
        return truncatechars(self.bio, 20)
    
    def date_enregistrement_rep(self):
        return temps_ecoule(self.date_enregistrement)
    
    def total_membre(self):
        return f"{User.objects.filter(profil_id=2).count()}".zfill(2)
    
    def nb_couples(self):
        return f"{Couple.objects.filter(user1=self).union(Couple.objects.filter(user2=self)).count()}".zfill(2)
    
    def total_conversation(self):
        return f"{Conversation.objects.all().count()}".zfill(2)
    
    def total_publication(self):
        return f"{Publication.objects.all().count()}".zfill(2)
    
    def total_message(self):
        return f"{Message.objects.all().count()}".zfill(2)
    
    def prenom_nom(self):
        return f"{self.prenom} {self.nom}"
    
    def nom_prenom(self):
        return f"{self.nom} {self.prenom}"
    
    def actual_photo(self):
        return PhotoUtilisateur.objects.filter(user=self).last()
    
    def all_photos(self):
        return PhotoUtilisateur.objects.filter(user=self).all()
    
    def statut(self):
        couples = Couple.objects.filter(user1=self).union(Couple.objects.filter(user2=self))
        if couples.count() == 1:
            return "En couple"
        elif couples.count() == 0:
            return "Célibataire"
        else:
            return "En concubinage"
    
    def age(self):
        return calculer_age(self.date_naissance)
    
    def date_naissance_rep(self):
        return date_to_text(self.date_naissance)
    
    def true_pass(self):
        return dechiffrement(self.password)
    
    def my_publications(self):
        return Publication.objects.filter(user=self).order_by("-date_ajout")
    
    def typePublications(self):
        return TypePublication.objects.all()
    
    def centreInterets(self):
        return CentreInteret.objects.all()
    
    def centreInteretUtilisateur(self):
        return CentreInteretUtilisateur.objects.filter(user=self).order_by("-id")
    
    def conversations(self):
        return Conversation.objects.filter(user1=self).union(Conversation.objects.filter(user2=self))
    
    def nb_conversation_unread(self):
        conversations = Conversation.objects.filter(user1=self).union(Conversation.objects.filter(user2=self))
        nb = 0
        for conv in conversations:
            if conv.is_read_by_other(self):
                nb += 1
        return nb
    
    def suggestions(self):
        return User.objects.filter(sexe=not self.sexe, profil_id=2).order_by("-date_naissance")

class PhotoUtilisateur(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to='images/Utilisateur/')
    date_ajout = models.DateTimeField(auto_now_add=True)

class Couple(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="couples1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="couples2")
    date_debut = models.DateTimeField(auto_now_add=True)
    date_fin = models.DateTimeField(null=True)

class CentreInteret(models.Model):
    libelle = models.CharField(max_length = 200)
    
    def nombre_membre(self):
        return f"{User.objects.filter(centreinteretutilisateur__centre_interet=self).count()}".zfill(2)
    
    def nombre_membre_same_sexe(self):
        return f"{User.objects.filter(centreinteretutilisateur__centre_interet=self, sexe=self.user.sexe).count()}".zfill(2)

class CentreInteretUtilisateur(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    centre_interet = models.ForeignKey(CentreInteret, on_delete=models.CASCADE)
    
    def nombre_membre(self):
        return f"{User.objects.filter(centreinteretutilisateur__centre_interet=self.centre_interet).count()-1}".zfill(2)
    
    def nombre_membre_same_sexe(self):
        return f"{User.objects.filter(centreinteretutilisateur__centre_interet=self.centre_interet, sexe=self.user.sexe).count()-1}".zfill(2)
    
    def nombre_membre_other_sexe(self):
        return f"{User.objects.filter(centreinteretutilisateur__centre_interet=self.centre_interet, sexe=not self.user.sexe).count()}".zfill(2)

class Conversation(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user1")
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user2")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_dernier_message = models.DateTimeField(null=True)
    
    def date_creation_rep(self):
        return format_datetime(self.date_creation)
    
    def last_date(self):
        now = timezone.now()
        dernier_message_date = self.last_message().date_envoi
        self.date_dernier_message = dernier_message_date.astimezone(now.tzinfo)
        self.save()
        return format_datetime(self.date_dernier_message)
    
    def last_message_other(self, user):
        if user.id == self.user1.id:
            u = self.user2
        else:
            u = self.user1
        m = Message.objects.filter(user=u).last()
        return m
    
    def last_message(self):
        return Message.objects.filter(conversation =self).last()
    
    def is_read_by_other(self, user):
        return self.last_message_other(user).date_lecture is None
    
    def messages(self):
        return Message.objects.filter(conversation=self).order_by('date_envoi')
            

class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
    texte = models.TextField(null=True)
    image = models.ImageField(upload_to='images/Messages/', null=True)
    video = models.FileField(upload_to='videos/Messages/', null=True)
    document = models.FileField(upload_to='documents/Messages/',null=True)
    audio = models.FileField(upload_to='audios/Messages/', null=True)
    date_envoi = models.DateTimeField(auto_now_add=True)
    date_lecture = models.DateTimeField(null=True)
    
    def non_lu(self):
        if not self.date_lecture:
            answer = True
            now = datetime.now()
            self.date_lecture = now
            self.save()
        else:
            answer = False
        return answer
    
    def is_last(self):
        return self.conversation.messages().last().id == self.id
    
    def texte_rep(self):
        return self.texte.replace("\n", "°")
    
    def date_envoi_rep(self):
        return format_datetime(self.date_envoi)
    
    def image_name(self):
        name = self.image.name.split("/")[-1]
        return name
    
    def video_name(self):
        name = self.video.name.split("/")[-1]
        return name
    
    def audio_name(self):
        name = self.audio.name.split("/")[-1]
        return name
    
    def document_name(self):
        name = self.document.name.split("/")[-1]
        return name
    
    def texte_truncate(self):
        return truncatechars(self.texte, 37).replace("\n", "°")
    
    def image_truncate(self):
        return truncatechars(self.image_name(), 37)
    
    def audio_truncate(self):
        return truncatechars(self.audio_name(), 37)
    
    def video_truncate(self):
        return truncatechars(self.video_name(), 37)
    
    def document_truncate(self):
        return truncatechars(self.document_name(), 37)
    
    def truncate_me(self):
        if self.texte:
            return self.texte_truncate()
        elif self.image:
            return self.image_truncate()
        elif self.audio:
            return self.audio_truncate()
        elif self.video:
            return self.video_truncate()
        elif self.document:
            return self.document_truncate()
    
    def temps_ecoule(self):
        return temps_ecoule(self.date_envoi)
        
    

class TypePublication(models.Model):
    libelle = models.CharField(max_length = 200)

class Publication(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    texte = models.TextField(null=True)
    image = models.ImageField(upload_to='images/Publications/', null=True)
    video = models.FileField(upload_to='videos/Publications/', null=True)
    type = models.ForeignKey(TypePublication, on_delete=models.CASCADE, default=None)
    date_ajout = models.DateTimeField(auto_now_add=True)
    
    def temps_ecoule(self):
        return temps_ecoule(self.date_ajout)
    
    def image_name(self):
        name = self.image.name.split("/")[-1]
        return name
    
    def video_name(self):
        name = self.video.name.split("/")[-1]
        return name