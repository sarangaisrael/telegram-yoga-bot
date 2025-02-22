
import openai
import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# 🛠 הכנס את ה-API Key שלך של OpenAI
OPENAI_API_KEY = "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"
openai.api_key = OPENAI_API_KEY

# 🛠 שלבי השיחה של הבוט
WAITING_FOR_CONFIRMATION = 1
WAITING_FOR_LOCATION = 2
WAITING_FOR_DURATION = 3

# 🛠 קישור ישיר לסרטון (Dropbox או שרת חיצוני עם לינק ישיר)
VIDEO_URL = "https://drive.google.com/uc?export=download&id=1LcU48lhJxIzvln2WkrY7Ci0VQDirgbgT"

# 🔹 פונקציה שמטפלת בהודעת הפתיחה
async def start(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "היי, טוב שבאת! אני Omly ואלווה אותך כדי להשיג את השקט והרוגע שבסוף כולנו צריכים. כרגע אני מציע תרגולי מדיטציה קצרים, ובהמשך יהיו גם תרגולי יוגה! 🧘🥰",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("אישור")]], resize_keyboard=True, one_time_keyboard=True
        )
    )
    return WAITING_FOR_CONFIRMATION

# 🔹 פונקציה לבחירת מיקום
async def choose_location(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "ועכשיו אפשר לעבור לעניינו. איפה אני תופס אותך כעת?",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("בבית"), KeyboardButton("במשרד")]], resize_keyboard=True, one_time_keyboard=True
        )
    )
    return WAITING_FOR_LOCATION

# 🔹 פונקציה לבחירת זמן תרגול
async def choose_duration(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text(
        "מושלם! וכמה זמן יש לך לתרגול?",
        reply_markup=ReplyKeyboardMarkup(
            [[KeyboardButton("5 דקות"), KeyboardButton("10 דקות"), KeyboardButton("15 דקות")]], 
            resize_keyboard=True, one_time_keyboard=True
        )
    )
    return WAITING_FOR_DURATION

# 🔹 פונקציה לשליחת הווידאו לאחר בחירת זמן
async def handle_duration_choice(update: Update, context: CallbackContext) -> int:
    choice = update.message.text
    
    if choice == "5 דקות":
        response = "מעולה! ממוקד, קצר וקולע. 5 דקות שיחזירו אותך לשגרה באנרגיה מחודשת."
        await update.message.reply_text(response)
        await update.message.reply_video(VIDEO_URL, caption="🎥 הנה התרגול שלך!")

    elif choice == "10 דקות":
        response = "לא ארוך מדי ולא קצר מדי, בול במידה :)"
        await update.message.reply_text(response)

    elif choice == "15 דקות":
        response = "זה הולך להיות מדהים, הנה המדיטציה:"
        await update.message.reply_text(response)

    else:
        response = "לא הבנתי את הבחירה שלך. בבקשה בחר אחת מהאפשרויות."
        await update.message.reply_text(response)

    return ConversationHandler.END

# 🔹 פונקציה לשיחה עם GPT עבור הודעות חופשיות
import openai

# הכנס את המפתח החדש שלך מ-OpenRouter
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")  # לוקח את ה-API Key מהסביבה


async def chat_with_gpt(update: Update, context: CallbackContext):
    user_message = update.message.text
    try:
        client = openai.OpenAI(api_key=openai.api_key, base_url="https://openrouter.ai/api/v1")

        response = client.chat.completions.create(
            model="google/gemini-2.0-flash-001",  # שימוש ב-Gemini
            messages=[
                {"role": "system", "content": "אתה עוזר אישי שמתמקד רק במיינדפולנס, יוגה, מדיטציה ורוגע. אתה לא עונה על שאלות בנושאים אחרים."},
                {"role": "user", "content": user_message}
            ]
        )

        if response and response.choices and len(response.choices) > 0:
            gpt_reply = response.choices[0].message.content
            await update.message.reply_text(gpt_reply)
        else:
            await update.message.reply_text("❌ לא התקבלה תשובה מ-Gemini.")

    except Exception as e:
        await update.message.reply_text(f"❌ שגיאה: {str(e)}")


# 🔹 פונקציה לסיום השיחה
async def cancel(update: Update, context: CallbackContext) -> int:
    await update.message.reply_text("הבוט סיים את השיחה.")
    return ConversationHandler.END

# 🔹 פונקציה ראשית שמפעילה את הבוט
def main():
    token = "8053544037:AAEqLfh930a6rYLbeLgAShCV-yJM9Y4d1eE"

    application = Application.builder().token(token).build()

    # ConversationHandler לניהול השיחה על המדיטציה
    conversation_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            WAITING_FOR_CONFIRMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_location)],
            WAITING_FOR_LOCATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, choose_duration)],
            WAITING_FOR_DURATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_duration_choice)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    # הוספת ConversationHandler לבוט
    application.add_handler(conversation_handler)

    # הוספת MessageHandler כללי לשאלות חופשיות עם GPT
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_gpt))

    # הפעלת הבוט
    application.run_polling()

if __name__ == '__main__':
    main()
