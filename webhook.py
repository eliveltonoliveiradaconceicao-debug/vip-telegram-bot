from flask import Flask, request
import stripe
import config
from telegram import Bot

stripe.api_key = config.STRIPE_SECRET_KEY
bot = Bot(token=config.TELEGRAM_TOKEN)

app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")

    event = stripe.Webhook.construct_event(
        payload, sig_header, config.STRIPE_WEBHOOK_SECRET
    )

    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        telegram_id = int(session["metadata"]["telegram_id"])

        invite = bot.create_chat_invite_link(
            chat_id=config.VIP_GROUP_ID,
            member_limit=1
        )

        bot.send_message(
            chat_id=telegram_id,
            text=(
                "✅ Payment confirmed!\n\n"
                "🎉 Welcome to the VIP Group!\n\n"
                f"🔗 Join here:\n{invite.invite_link}"
            )
        )

    return "OK", 200
