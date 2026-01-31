import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from config import BOT_TOKEN
from processor import process_scores

# Handler for receiving Excel files
async def run_program(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document

    # Check file extension
    if not document.file_name.endswith(".xlsx"):
        await update.message.reply_text("Please upload a valid Excel (.xlsx) file.")
        return

    # Download file from Telegram
    file = await document.get_file()
    input_file = f"input_{update.message.from_user.id}.xlsx"
    await file.download_to_drive(input_file)

    try:
        # Process Excel and get output files
        success_file, failed_file = process_scores(input_file)

        # Send results back to user
        await update.message.reply_document(open(success_file, "rb"))
        await update.message.reply_document(open(failed_file, "rb"))

                # ✅ Prompt user for another file
        await update.message.reply_text(
            "Here are your results.\n"
            "If you want to process another file, please upload it now."
        )

    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

    finally:
        # Clean up temporary files
        for f in [input_file, success_file, failed_file]:
            if os.path.exists(f):
                os.remove(f)

# Optional /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hello! Please upload an Excel file with participant scores.\n"
    )
async def upload(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Please upload an Excel file with participant scores.\n"
    )


# Main function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Handlers
    app.add_handler(MessageHandler(filters.Document.ALL, run_program))
    app.add_handler(MessageHandler(filters.COMMAND & filters.Regex("^/start$"), start))
    app.add_handler(MessageHandler(filters.COMMAND & filters.Regex("^/upload$"), upload))

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
