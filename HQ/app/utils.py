from app.config import KEY
from datetime import datetime, timedelta
import random
import string
import pytz
from django.utils import timezone

def generate_string(length=12):
    """Generate a strong password."""
    # Define character sets
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation

    # Combine character sets
    all_characters = lowercase_letters + uppercase_letters + digits + special_characters

    # Ensure at least one character from each set
    password = random.choice(lowercase_letters)
    password += random.choice(uppercase_letters)
    password += random.choice(digits)
    password += random.choice(special_characters)

    # Fill remaining length with random characters
    for _ in range(length - 4):
        password += random.choice(all_characters)

    # Shuffle the password to make it more random
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password


def format_datetime(dt):
    # Obtenir l'heure actuelle en utilisant le fuseau horaire de l'utilisateur
    now = timezone.now()
    
    # Convertir dt au fuseau horaire actuel
    dt = dt.astimezone(now.tzinfo)
    
    if dt.date() == now.date():
        # Si le jour n'a pas changé, renvoyer l'heure au format HH:MM
        return dt.strftime('%H:%M')
    elif dt.date() == (now.date() - timedelta(days=1)):
        # Si le jour est le lendemain du jour du DateTimeField, renvoyer "Hier à HH:MM"
        return f'Hier à {dt.strftime("%H:%M")}'
    else:
        # Dans tous les autres cas, renvoyer JJ/MM/AAAA à HH:MM
        return dt.strftime('%d/%m/%Y à %H:%M')

def temps_ecoule(date_str):
    # Convertir la date de naissance en un objet datetime
    # Assume the input date_str format is 'YYYY-MM-DD HH:MM:SS'
    if isinstance(date_str, str):
        date_naissance = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
    else:
        date_naissance = date_str
    
    # Obtenir la date actuelle avec le même fuseau horaire
    maintenant = datetime.now(pytz.utc)
    if date_naissance.tzinfo is None:
        date_naissance = date_naissance.replace(tzinfo=pytz.utc)
    
    # Calculer la différence
    delta = maintenant - date_naissance
    
    # Convertir la différence en secondes
    secondes = delta.total_seconds()
    
    if secondes < 60:
        return "A l'instant"
    elif secondes < 3600:
        minutes = int(secondes // 60)
        return f"{str(minutes).zfill(2)} minute(s)"
    elif secondes < 86400:
        heures = int(secondes // 3600)
        return f"{str(heures).zfill(2)} heure(s)"
    elif secondes < 2592000:
        jours = int(secondes // 86400)
        return f"{str(jours).zfill(2)} jour(s)"
    elif secondes < 31536000:
        mois = int(secondes // 2592000)
        return f"{str(mois).zfill(2)} mois"
    else:
        annees = int(secondes // 31536000)
        return f"{str(annees).zfill(2)} année(s)"

def calculer_age(date_naissance):
    # Convertir la date de naissance en un objet datetime
    if isinstance(date_naissance, str):
        date_naissance = datetime.strptime(date_naissance, '%Y-%m-%d')
    
    # Obtenir la date actuelle
    today = datetime.today()
    
    # Calculer l'âge en années
    age = today.year - date_naissance.year
    
    # Ajuster l'âge si l'anniversaire de cette année n'est pas encore passé
    if today.month < date_naissance.month or (today.month == date_naissance.month and today.day < date_naissance.day):
        age -= 1
    
    return age

def generate_strong_password(length=12):
    """Generate a strong password."""
    # Define character sets
    lowercase_letters = string.ascii_lowercase
    uppercase_letters = string.ascii_uppercase
    digits = string.digits
    special_characters = string.punctuation

    # Combine character sets
    all_characters = lowercase_letters + uppercase_letters + digits + special_characters

    # Ensure at least one character from each set
    password = random.choice(lowercase_letters)
    password += random.choice(uppercase_letters)
    password += random.choice(digits)
    password += random.choice(special_characters)

    # Fill remaining length with random characters
    for _ in range(length - 4):
        password += random.choice(all_characters)

    # Shuffle the password to make it more random
    password_list = list(password)
    random.shuffle(password_list)
    password = ''.join(password_list)

    return password


def truncatechars(string, max_length):
        if len(string) <= max_length:
            return string
        else:
            return string[:max_length] + "..."

def nombre_de_jours(j1, j2):
    # Convertir les dates en objets datetime si elles ne le sont pas déjà
    if not isinstance(j1, datetime):
        j1 = datetime.strptime(j1, '%Y-%m-%d')
    if not isinstance(j2, datetime):
        j2 = datetime.strptime(j2, '%Y-%m-%d')

    # Calculer la différence entre les deux dates
    difference = j2 - j1

    # Retourner le nombre de jours en valeur absolue
    return difference.days

def date_to_text(date):
    return date.strftime('%Y-%m-%d')

def text_to_date(text):
    return datetime.strptime(text, '%Y-%m-%d')

def chiffrement(message) -> str:
    decalage = KEY
    message_chiffre = ""
    for caractere in message:
        # Vérifier si le caractère est une lettre majuscule
        if caractere.isupper():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('A') + decalage) % 26 + ord('A')
            message_chiffre += chr(nouveau_code)
        # Vérifier si le caractère est une lettre minuscule
        elif caractere.islower():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('a') + decalage) % 26 + ord('a')
            message_chiffre += chr(nouveau_code)
        # Vérifier si le caractère est un chiffre
        elif caractere.isdigit():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('0') + decalage) % 10 + ord('0')
            message_chiffre += chr(nouveau_code)
        # Si le caractère est un caractère spécial, le laisser inchangé
        else:
            message_chiffre += caractere
    return message_chiffre

def dechiffrement(message) -> str:
    decalage = -KEY
    message_chiffre = ""
    for caractere in message:
        # Vérifier si le caractère est une lettre majuscule
        if caractere.isupper():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('A') + decalage) % 26 + ord('A')
            message_chiffre += chr(nouveau_code)
        # Vérifier si le caractère est une lettre minuscule
        elif caractere.islower():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('a') + decalage) % 26 + ord('a')
            message_chiffre += chr(nouveau_code)
        # Vérifier si le caractère est un chiffre
        elif caractere.isdigit():
            ascii_code = ord(caractere)
            nouveau_code = (ascii_code - ord('0') + decalage) % 10 + ord('0')
            message_chiffre += chr(nouveau_code)
        # Si le caractère est un caractère spécial, le laisser inchangé
        else:
            message_chiffre += caractere
    return message_chiffre

