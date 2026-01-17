from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import stripe
import config

stripe.api_key = config.STRIPE_SECRET_KEY

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "This bot gives access to our *Private VIP Group*.\n\n"
        "💎 Price: *$10/month*\n"
        "🔒 Private Group\n"
        "⚡ Instant Access\n\n"
        "Type /vip to subscribe.",
        parse_mode="Markdown"
    )

async def vip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    checkout = stripe.checkout.Session.create(
        mode="subscription",
        payment_method_types=["card"],
        line_items=[{
            "price_data": {
                "currency": "usd",
                "product_data": {"name": "VIP Telegram Group"},
                "unit_amount": 1000,
                "recurring": {"interval": "month"}
            },
            "quantity": 1
        }],
        success_url="https://example.com/success",
        cancel_url="https://example.com/cancel",
        metadata={"telegram_id": update.effective_user.id}
    )

    button = InlineKeyboardMarkup([
        [InlineKeyboardButton("💳 Subscribe Now", url=checkout.url)]
    ])

    await update.message.reply_text(
        "🚀 You're one step away from joining the VIP Group!\n\n"
        "Click the button below to subscribe:",
        reply_markup=button
    )

app = ApplicationBuilder().token(config.TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("vip", vip))

app.run_polling()
