from telegram.ext import ApplicationBuilder, MessageHandler, filters
import random, re, os

TOKEN = os.getenv("TOKEN", "TON_TOKEN_ICI")

# Charger les répliques
with open("repliques.txt", "r", encoding="utf-8") as f:
    repliques = [line.strip() for line in f if line.strip()]

# Charger automatiquement les fichiers
audios = [f"audios/{f}" for f in os.listdir("audios") if f.endswith(".ogg")]
videos = [f"videos/{f}" for f in os.listdir("videos") if f.endswith(".mp4")]

dernieres_repliques, derniers_audios, dernieres_videos = [], [], []

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
def choisir_video(): return choisir_sans_repete(videos, dernieres_videos, 3)

async def envoyer_reponse(update):
    choix = random.choice(["texte", "audio", "video"])
    if choix == "texte":
        await update.message.reply_text(choisir_replique())
    elif choix == "audio" and audios:
        fichier = choisir_audio()
        await update.message.reply_voice(voice=open(fichier, "rb"))
    elif choix == "video" and videos:
        fichier = choisir_video()
        await update.message.reply_video(video=open(fichier, "rb"))

async def repond_hervé(update, context):
    message = update.message.text.lower()

    # ✅ Cas spécial "bouboulle" → toujours une vidéo
    if "bouboulle" in message and videos:
        fichier = choisir_video()
        await update.message.reply_video(video=open(fichier, "rb"))
        return

    # ✅ Si on répond à Hervé_Bot
    if update.message.reply_to_message and update.message.reply_to_message.from_user.is_bot:
        await envoyer_reponse(update)
        return

    # ✅ Si on écrit "Hervé" ou "RV"
    if re.search(r"\b(hervé|rv)\b", message, re.IGNORECASE):

        # Cas spécial "parle" → uniquement un audio
        if "parle" in message and audios:
            fichier = choisir_audio()
            await update.message.reply_voice(voice=open(fichier, "rb"))
            return

        # Réponse normale aléatoire
        await envoyer_reponse(update)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repond_hervé))

print("🤖 Hervé_Bot avec vidéos et mot-clé bouboulle est en ligne !")
app.run_polling()
