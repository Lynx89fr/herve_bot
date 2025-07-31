from telegram.ext import ApplicationBuilder, MessageHandler, filters
import random, re, os

TOKEN = os.getenv("TOKEN", "TON_TOKEN_ICI")

with open("repliques.txt", "r", encoding="utf-8") as f:
    repliques = [line.strip() for line in f if line.strip()]

mp4_files = [f"audios/{f}" for f in os.listdir("audios") if f.endswith(".mp4")]
videos = [f"videos/{f}" for f in os.listdir("videos") if f.endswith(".mp4")]

dernieres_repliques, derniers_mp4, dernieres_videos = [], [], []

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
def choisir_mp4(): return choisir_sans_repete(mp4_files, derniers_mp4, 3)
def choisir_video(): return choisir_sans_repete(videos, dernieres_videos, 3)

async def envoyer_mp4(update):
    fichier = choisir_mp4()
    await update.message.reply_video(video=open(fichier, "rb"))

async def repond_hervé(update, context):
    message = update.message.text.lower()

    # 🎥 Cas spécial "bouboule"
    if "bouboule" in message and videos:
        fichier = choisir_video()
        await update.message.reply_video(video=open(fichier, "rb"))
        return

    if re.search(r"\b(hervé|rv)\b", message, re.IGNORECASE):
        if "parle" in message and mp4_files:
            await envoyer_mp4(update)
        else:
            if random.choice([True, False]):
                await update.message.reply_text(choisir_replique())
            else:
                await envoyer_mp4(update)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repond_hervé))

print("🤖 Hervé_Bot : tous les MP4 envoyés comme VIDÉO 🎥")
app.run_polling()
