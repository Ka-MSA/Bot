from file_data import files_by_section
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def register_menu_handler(bot):
    @bot.message_handler(commands=['menu'])
    def show_menu(message):
        bot.send_message(message.chat.id, "Choose a section:", reply_markup=build_section_keyboard())

    def build_section_keyboard():
        keyboard = InlineKeyboardMarkup()
        for section in files_by_section:
            keyboard.add(InlineKeyboardButton(text=section, callback_data=f"section|{section}"))
        return keyboard

    def build_files_keyboard(section_name):
        keyboard = InlineKeyboardMarkup()
        for filename in files_by_section[section_name]:
            keyboard.add(InlineKeyboardButton(text=filename, callback_data=f"get|{filename}"))
        keyboard.add(InlineKeyboardButton(text="⬅ Back to Sections", callback_data="back"))
        return keyboard

    @bot.callback_query_handler(func=lambda call: call.data.startswith("section|"))
    def handle_section(call):
        section_name = call.data.split("|", 1)[1]
        if section_name not in files_by_section:
            bot.answer_callback_query(call.id, "Section not found.")
            return

        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=f"Files in *{section_name}*:",
            reply_markup=build_files_keyboard(section_name),
            parse_mode="Markdown"
        )

    @bot.callback_query_handler(func=lambda call: call.data == "back")
    def handle_back(call):
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="Choose a section:",
            reply_markup=build_section_keyboard()
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("get|"))
    def send_file(call):
        filename = call.data.split("|", 1)[1]
        
        # Loop through sections to find the file
        for section, files in files_by_section.items():
            if filename in files:
                file_path = files[filename]  # Assuming this stores the file path or link
                
                # Check if the file path is a valid file or a link
                if file_path.startswith("http"):  # Check if it's a URL
                    # Send the file via the URL (e.g., Google Drive link)
                    bot.send_document(call.message.chat.id, file_path, caption=f"Here’s your file: {filename}")
                else:
                    # Send the file from a local path
                    try:
                        with open(file_path, 'rb') as file:
                            bot.send_document(call.message.chat.id, file, caption=f"Here’s your file: {filename}")
                    except FileNotFoundError:
                        bot.send_message(call.message.chat.id, "Sorry, the file could not be found.")
                return

        # If the file is not found in any section
        bot.send_message(call.message.chat.id, "File not found.")
