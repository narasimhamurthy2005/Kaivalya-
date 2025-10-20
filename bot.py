import os
import tempfile
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
    ContextTypes
)
from rag_local import rag_query  

BOT_TOKEN = "telegram token " 
HOSPITALS = [
    {
        "name": "Archana Hospital (A Block) - Best Multispeciality Hospital in Madinaguda",
        "address": "1-56/AH, NH 65, beside Reliance Digital, Madinaguda, Durga Estates, Miyapur, Hyderabad, Telangana 500049",
        "maps_link": "https://share.google/2xmZ1UYZ7nDz3bfOs"
    },
    {
        "name": "Sunrise Hospital",
        "address": "Plot no, 16 & 17, beside New Collectorate, HMT Swarnapuri Colony, Sai, Krushi Nagar, Sangareddy, Hyderabad, Telangana 502001",
        "maps_link": "https://share.google/JNhL7mZD1mya8S5cC"
    },
    {
        "name": "SLG Hospitals",
        "address": "SLG Circle, Krishnaja Hills, Nizampet, Hyderabad, Telangana 500118",
        "maps_link": "https://share.google/AVfA5qL29nL6DQkhY"
    }
]
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Symptoms → Advice", callback_data='symptoms_advice')],
        [InlineKeyboardButton("🏥 Nearby Hospitals", callback_data='nearby_hospitals')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "🤖 Welcome to the Health RAG Bot!\n"
        "Choose an option below:",
        reply_markup=reply_markup
    )

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == 'symptoms_advice':
        keyboard = [
            [InlineKeyboardButton("1️⃣ Text", callback_data='option_text')],
            [InlineKeyboardButton("2️⃣ Audio", callback_data='option_audio')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="Choose how you want to provide your symptoms:",
            reply_markup=reply_markup
        )

    elif data == 'option_text':
        context.user_data['mode'] = 'text'
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="💬 Please type your symptoms. You can add language at the end:\n"
                 "'in English', 'in Hindi', or 'in Telugu' (defaults to English)."
        )

    elif data == 'option_audio':
        context.user_data['mode'] = 'audio'
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="🎤 Please send your symptoms as a voice message (MP3/OGG)."
        )

    elif data == 'nearby_hospitals':
        context.user_data['mode'] = 'location'
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text="📍 Please share your location so I can suggest nearby hospitals."
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get('mode')
    user_input = update.message.text

    if mode is None or mode == 'text':
        msg = await update.message.reply_text("⏳ Processing your request, please wait...")
        answer = rag_query(user_input)
        await msg.edit_text(answer)
    else:
        await update.message.reply_text(
            "⚠️ You are in Audio or Location mode. Please send the correct input or press /start to reset."
        )

async def handle_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mode = context.user_data.get('mode', None)
    if mode != 'audio':
        await update.message.reply_text("⚠️ Please press 'Symptoms → Advice' → 'Audio' first.")
        return

    voice = update.message.voice or update.message.audio
    if not voice:
        await update.message.reply_text("⚠️ Please send a valid audio file.")
        return

    file = await voice.get_file()
    processing_msg = await update.message.reply_text("⏳ Processing your audio, please wait...")
    tmp_mp3 = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tmp_mp3_path = tmp_mp3.name
    tmp_mp3.close()
    await file.download_to_drive(tmp_mp3_path)
    wav_path = tmp_mp3_path.replace(".mp3", ".wav")
    try:
        audio_segment = AudioSegment.from_file(tmp_mp3_path)
        audio_segment.export(wav_path, format="wav")
    except Exception as e:
        await processing_msg.edit_text(f"⚠️ Audio conversion failed: {e}")
        os.remove(tmp_mp3_path)
        return

    recognizer = sr.Recognizer()
    try:
        with sr.AudioFile(wav_path) as source:
            audio_data = recognizer.record(source)
            text = recognizer.recognize_google(audio_data, language="en-US")
    except sr.UnknownValueError:
        await processing_msg.edit_text("🤖 Sorry, I could not understand the audio.")
        os.remove(tmp_mp3_path)
        os.remove(wav_path)
        return
    except sr.RequestError:
        await processing_msg.edit_text("🤖 Speech recognition service error.")
        os.remove(tmp_mp3_path)
        os.remove(wav_path)
        return

    answer_text = rag_query(text + " in english")
    await processing_msg.edit_text("✅ Processing done! Sending audio reply...")
    tts = gTTS(text=answer_text, lang='en')
    output_mp3 = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
    tts.save(output_mp3.name)
    output_mp3_path = output_mp3.name
    output_mp3.close()

    with open(output_mp3_path, 'rb') as f:
        await update.message.reply_voice(f)

    os.remove(tmp_mp3_path)
    os.remove(wav_path)
    os.remove(output_mp3_path)

async def handle_location(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('mode') != 'location':
        return
    reply_text = "Here are some hospitals near you:\n\n"
    for hospital in HOSPITALS:
        reply_text += f"🏥 *{hospital['name']}*\n📍 {hospital['address']}\n🔗 [Google Maps Link]({hospital['maps_link']})\n\n"

    await update.message.reply_text(reply_text, parse_mode="Markdown")

    # Reset mode
    context.user_data['mode'] = None

# -------------------- MAIN --------------------
if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE | filters.AUDIO, handle_audio))
    app.add_handler(MessageHandler(filters.LOCATION, handle_location))

    print("🤖 Telegram RAG Bot with text/audio + hospital finder is running...")
    app.run_polling()
