from telegram.ext import ApplicationBuilder, MessageHandler, filters
import random, re, os

TOKEN = os.getenv("TOKEN", "TON_TOKEN_ICI")

# ✅ Charger les répliques
with open("repliques.txt", "r", encoding="utf-8") as f:
    repliques = [line.strip() for line in f if line.strip()]

# ✅ Charger les fichiers audio (ogg et mp4)
audios = [f"audios/{f}" for f in os.listdir("audios") if f.endswith(".ogg") or f.endswith(".mp4")]

dernieres_repliques, derniers_audios = [], []

def choisir_sans_repete(liste, memoire, max_memoire):
    dispo = [x for x in liste if x not in memoire]
    if not dispo:
        memoire.clear()
        dispo = liste.copy()
    choix = random.choice(dispo)
    memoire.append(choix)
    if len(memoire) > max_memoire:
        memoire.pop(0)
    return choix

def choisir_replique(): return choisir_sans_repete(repliques, dernieres_repliques, 5)
def choisir_audio(): return choisir_sans_repete(audios, derniers_audios, 3)

async def envoyer_audio(update):
    fichier = choisir_audio()
    if fichier.endswith(".ogg"):
        await update.message.reply_voice(voice=open(fichier, "rb"))
    else:  # Si c'est un .mp4, on l'envoie comme vidéo
        a
