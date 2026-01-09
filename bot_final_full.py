from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import os

# التوكين الجديد للبوت
TOKEN = "7752865738:AAFw-gqzqIHpp2iDcZAe0BSE__c_rcKAMtM"

# مجلد حفظ الفيديوهات على الهاتف
DOWNLOAD_FOLDER = "/storage/emulated/0/"

# لتخزين اختيار المنصة لكل مستخدم
user_platform = {}

# رابط مباشر للبوت (جاهز للمشاركة)
BOT_LINK = "https://t.me/GenieAhmadBot"

# /start مع الأزرار
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("TikTok 🎵", callback_data='tiktok')],
        [InlineKeyboardButton("Instagram 📸", callback_data='instagram')],
        [InlineKeyboardButton("YouTube 🎥", callback_data='youtube')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"أهلاً! اختر المنصة لتحميل الفيديو أو شارك هذا الرابط مع أصدقائك:\n{BOT_LINK}",
        reply_markup=reply_markup
    )

# اختيار المنصة
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if query.data == "tiktok":
        user_platform[user_id] = "tiktok"
        await query.edit_message_text("أرسل لي رابط الفيديو من TikTok 📥")
    elif query.data == "instagram":
        user_platform[user_id] = "instagram"
        await query.edit_message_text("أرسل لي رابط الفيديو من Instagram 📥")
    elif query.data == "youtube":
        user_platform[user_id] = "youtube"
        await query.edit_message_text("أرسل لي رابط الفيديو من YouTube 📥")

# استقبال رابط الفيديو وتحميله
async def receive_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    link = update.message.text.strip()
    platform = user_platform.get(user_id)

    if not platform:
        await update.message.reply_text(
            "أولاً اختر المنصة باستخدام /start ثم الزر المناسب."
        )
        return

    await update.message.reply_text("⏳ جاري تحميل الفيديو...")

    try:
        # إعداد yt-dlp
        ydl_opts = {
            'outtmpl': os.path.join(DOWNLOAD_FOLDER, '%(title)s.%(ext)s'),
            'format': 'mp4',
            'noplaylist': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            filename = ydl.prepare_filename(info)

        # إرسال الفيديو مباشرة في Telegram
        with open(filename, 'rb') as video:
            await update.message.reply_video(video)

        await update.message.reply_text("✅ تم التحميل بنجاح!")

    except Exception as e:
        await update.message.reply_text(f"❌ حدث خطأ أثناء التحميل:\n{e}")

    # الاختيار يبقى محفوظًا → يمكن إرسال روابط أخرى مباشرة
    # user_platform.pop(user_id, None)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, receive_link))

    print("البوت النهائي شغال بالكامل ✅")
    app.run_polling()

if __name__ == "__main__":
    main()