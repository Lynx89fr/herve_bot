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
        await update.message.reply_video(video=open(fichier, "rb"))

async def envoyer_reponse(update):
    choix = random.choice(["texte", "audio"])
    if choix == "texte":
        await update.message.reply_text(choisir_replique())
    else:
        await envoyer_audio(update)

async def repond_hervé(update, context):
    message = update.message.text.lower()

    # ✅ Si le message contient "bouboulle" → toujours un audio/vidéo
    if "bouboulle" in message:
        await envoyer_audio(update)
        return

    # ✅ Si on répond à Hervé_Bot
    if update.message.reply_to_message and update.message.reply_to_message.from_user.is_bot:
        await envoyer_reponse(update)
        return

    # ✅ Si on écrit "Hervé" ou "RV"
    if re.search(r"\b(hervé|rv)\b", message, re.IGNORECASE):
        # Cas spécial "parle" → uniquement un audio/vidéo
        if "parle" in message:
            await envoyer_audio(update)
            return
        await envoyer_reponse(update)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repond_hervé))

print("🤖 Hervé_Bot peut maintenant envoyer des MP4 comme des audios 🎉")
app.run_polling()
