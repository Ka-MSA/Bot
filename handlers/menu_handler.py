from file_data import files_by_section, download_file
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ... other code ...

@bot.callback_query_handler(func=lambda call: call.data.startswith("get|"))
def send_file(call):
    filename = call.data.split("|", 1)[1]

    for section in files_by_section.values():
        if filename in section:
            file_info = section[filename]
            file_bytes = download_file(file_info['id'])  # Download the file as BytesIO
            bot.send_document(
                chat_id=call.message.chat.id,
                document=file_bytes,
                caption=f"**{file_info['name']}**",
                parse_mode="Markdown"
            )
            return

    bot.send_message(call.message.chat.id, "File not found.")
