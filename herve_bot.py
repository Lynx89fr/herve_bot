from telegram.ext import ApplicationBuilder, MessageHandler, filters
import random, re, os

TOKEN = os.getenv("TOKEN", "TON_TOKEN_ICI")

# Charger les répliques
with open("repliques.txt", "r", encoding="utf-8") as f:
    repliques = [line.strip() for line in f if line.strip()]

# Charger les fichiers audio (ogg et mp4)
audios = [f"audios/{f}" for f in os.listdir("audios") if f.endswith(".ogg") or f.endswith(".mp4")]

# Charger les vraies vidéos
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

async def envoyer_audio(update):
    fichier = choisir_audio()
    if fichier.endswith(".ogg"):
        await update.message.reply_voice(voice=open(fichier, "rb"))
    else:  # Si c'est un .mp4 dans audios/
        await update.message.reply_video(video=open(fichier, "rb"))

async def repond_hervé(update, context):
    message = update.message.text.lower()

    # ✅ Cas spécial bouboule → envoyer uniquement une vraie vidéo
    if "bouboule" in message and videos:
        fichier = choisir_video()
        await update.message.reply_video(video=open(fichier, "rb"))
        return

    # ✅ Cas normal (Hervé ou RV)
    if re.search(r"\b(hervé|rv)\b", message, re.IGNORECASE):
        if "parle" in message:
            await envoyer_audio(update)
        else:
            if random.choice([True, False]):
                await update.message.reply_text(choisir_replique())
            else:
                await envoyer_audio(update)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repond_hervé))

print("🤖 Hervé_Bot : Bouboule = vraie vidéo 🎥")
app.run_polling()
