from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler

# 🛠 שלבי השיחה של הבוט
WAITING_FOR_CONFIRMATION = 1
WAITING_FOR_LOCATION = 2
WAITING_FOR_DURATION = 3

# 🔹 קישור ישיר לסרטון
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
        "ועכשוו אפשר לעבור לעניינו. איפה אני תופס אותך כעת?",
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

# 🔹 פונקציה לשליחת הווידאו אחר בחירת זמן
async def handle_duration_choice(update: Update, context: CallbackContext) -> int:
    choice = update.message.text
    
    if choice == "5 דקות":
        response = "מעולה! ממוקד, קצר וקולע."
        await update.message.reply_text(response)
        await update.message.reply_video(VIDEO_URL, caption="🎥 הנה התרגול שלך!")

    return ConversationHandler.END
