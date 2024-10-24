from flask import Blueprint, request, jsonify
from tronpy import keys
import logging, json, os, httpx, asyncio
import concurrent.futures


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger()
main = Blueprint('main', __name__)
executor = concurrent.futures.ThreadPoolExecutor()

bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
notify_chat_id = os.getenv('TELEGRAM_CHAT_ID')
if not bot_token or not notify_chat_id:
    logger.error("Missing Telegram bot token or chat ID in environment variables.")
    raise EnvironmentError("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID is not set.")

bot_req_url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
tronscan_url = "https://tronscan.org/#/transaction/"


@main.route('/', methods=['GET', 'POST'])
def handle_request():
    try:
        data = request.get_json()
        if not data or not isinstance(data, list) or len(data) == 0:
            return jsonify({"error": "No data provided or data is not in expected format"}), 400

        result = parse_transaction_data(data[0])
        message = (
            f'🟢 Transaction Notification\n'
            f'Amount: {result["usdt"]}\n'
            f'From: {result["from_address"]}\n'
            f'To: {result["to_address"]}'
        )
        keyboard = {
            "inline_keyboard": [[{"text": "TRONSCAN", "url": result["url"]}]]
        }
        payload = {
            'chat_id': notify_chat_id,
            'text': message,
            'reply_markup': json.dumps(keyboard)
        }

        executor.submit(asyncio.run, send_telegram_message(payload))
        return '', 200

    except ValueError as e:
        return jsonify({"error": str(e)}), 400


def parse_transaction_data(receipt):
    try:
        transaction_hash = receipt.get("transactionHash", "")[2:]
        url = tronscan_url + transaction_hash
        log = receipt['logs'][0]

        usdt = int(log['data'], 16) / 1000000
        from_address = keys.to_base58check_address('41' + log['topics'][1][26:])
        to_address = keys.to_base58check_address('41' + log['topics'][2][26:])

        return {
            "transaction_hash": transaction_hash,
            "url": url,
            "usdt": usdt,
            "from_address": from_address,
            "to_address": to_address
        }
    except (IndexError, KeyError, ValueError) as e:
        logger.error(f"Failed to parse transaction data: {e}")
        raise ValueError("Invalid transaction data")


async def send_telegram_message(payload):
    async with httpx.AsyncClient() as client:
        response = await client.post(bot_req_url, json=payload)
        if response.status_code == 200:
            logger.info('Message sent successfully')
        else:
            error_message = response.json().get('description', 'No error description available')
            logger.error(f'Failed to send message: {response.status_code}, {error_message}')
