# Tron Event Handler

## Project Description 📝
This is a Flask API system designed to handle **QuickNode** EVM events from the Tron blockchain. When a transaction event is received, the system parses the transaction details and sends the result as a notification to a specified Telegram group. This project is specifically designed to monitor USDT transfers and provide automated notifications.

---

## Features 🌟
- **Real-time transaction notifications**: Events from QuickNode are processed immediately.
- **Multi-address parsing**: Supports converting `from` and `to` addresses to readable Base58 format.
- **Automated notifications**: Sends transaction details to a Telegram group.
- **Extensibility**: Simple Flask API, easy to extend for additional features.

## Environment Variables 🌐

Make sure your environment variables are set correctly. You can use a `.env` file or export them directly:

```bash
export TELEGRAM_BOT_TOKEN=your-telegram-bot-token
export TELEGRAM_CHAT_ID=your-chat-id
```

## API Documentation 📡

#### 1. Receive Transaction Event
**Endpoint**: `/`  
**Method**: `POST`

**Sample Request Body:**
```json
[
  {
    "transactionHash": "0x1234567890abcdef...",
    "logs": [
      {
        "data": "0x0000000000000000000000000000000000000000000000000000000000989680",
        "topics": [
          "0x...",
          "0x000000000000000000000000abcdef1234567890",
          "0x000000000000000000000000fedcba0987654321"
        ]
      }
    ]
  }
]
```

## Example Notification Message 📱

```
🟢 Transaction Notification
Amount: 10.0 USDT
From: TXYZ...Abc123
To: TABC...Xyz987
```
