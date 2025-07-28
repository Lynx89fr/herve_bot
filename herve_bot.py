from telegram.ext import ApplicationBuilder, MessageHandler, filters
import random, re, os

TOKEN = os.getenv("TOKEN", "8322144216:AAGl57jkOVHJzHJPuy_F9eIJ1gDKyNAKNtk")

# ✅ Charger les répliques depuis repliques.txt
with open("repliques.txt", "r", encoding="utf-8") as f:
    repliques = [line.strip() for line in f if line.strip()]

# ✅ Charger automatiquement les audios (pas de vidéos)
audios = [f"audios/{f}" for f in os.listdir("audios") if f.endswith(".ogg")]

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
def choisir_audio(): return choisir_sans_repete(audios, derniers_audios, 2)

async def envoyer_reponse(update):
    choix = random.choice(["texte", "audio"])  # Plus de "video"
    if choix == "texte":
        await update.message.reply_text(choisir_replique())
    elif choix == "audio" and audios:
        fichier = choisir_audio()
        await update.message.reply_voice(voice=open(fichier, "rb"))

async def repond_hervé(update, context):
    message = update.message.text.lower()

    # ✅ Si on répond à Hervé_Bot
    if update.message.reply_to_message and update.message.reply_to_message.from_user.is_bot:
        await envoyer_reponse(update)
        return

    # ✅ Si on écrit "Hervé" ou "RV"
    if re.search(r"\b(hervé|rv)\b", message, re.IGNORECASE):

        # Cas spécial "parle" → audio uniquement
        if "parle" in message and audios:
            fichier = choisir_audio()
            await update.message.reply_voice(voice=open(fichier, "rb"))
            return

        # Sinon réponse normale
        await envoyer_reponse(update)

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repond_hervé))

print("🤖 Hervé_Bot est en ligne !")
app.run_polling()
