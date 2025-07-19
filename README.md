# Balance-Update-Bot

A lightweight Discord bot to manage balance tracking with a SQLite database, implemented in Python using discord.py.
It allows users to add or subtract amounts via simple messages and query the current balance.

---

Features

- Add or subtract amounts by sending messages like +10 or -5.25
- Check current balance with the !balance command
- Persistent balance stored locally in a SQLite database
- Automatically creates the necessary database and folder structure
- Dockerized for easy deployment
- Supports automatic restart with Docker's restart policies

---

Prerequisites

- Python 3.8 or higher
- Discord Bot Token (https://discord.com/developers/applications)
- Docker (optional, but recommended for easy deployment)
- A Discord channel ID where the bot will operate
- .env file for environment variables

---

Setup Instructions

1. Clone the Repository

git clone https://github.com/yourusername/balance-update-bot.git
cd balance-update-bot

2. Create .env File

Create a .env file in the root directory with your Discord bot token and channel ID:

DISCORD_TOKEN=your_discord_bot_token_here
CHANNEL_ID=your_discord_channel_id_here

Note: Replace your_discord_bot_token_here and your_discord_channel_id_here with your actual token and channel ID.

3. Install Dependencies

Install the required Python packages:

pip install -r requirements.txt

---

Running the Bot

Run Locally (Without Docker)

python bot.py

The bot will connect to Discord, and you can interact with it in the specified channel.

Run with Docker

Build the Docker image:

docker build -t balance-update-bot .

Run the container with auto-restart enabled:

docker run -d --name balance-update-bot-container --restart unless-stopped --env-file .env balance-update-bot

---

Usage

- Add or subtract balance: Send messages like +10 to add $10 or -5 to subtract $5 in the designated Discord channel.
- Check balance: Send !balance to receive the current balance.
- The bot responds with an embedded message showing the previous balance, the transaction amount, and the updated balance.

---

Folder Structure

balance-update-bot/
├── bot.py               # Main bot script
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker image build instructions
├── .env                 # Environment variables (not committed)
└── data/                # SQLite database stored here (created automatically)
    └── balance2.db

---

Notes

- The bot must have permission to read and send messages in the configured Discord channel.
- The SQLite database (balance2.db) is stored in the data/ directory.
- To reset the balance, simply delete the data/balance2.db file.
- Make sure your .env file is never committed to source control (add to .gitignore).

---

Troubleshooting

- If the bot fails to connect, verify your Discord token and channel ID in the .env file.
- Check Discord permissions for the bot in the specified channel.
- Review the script_error.log file for unexpected errors.

---

Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

---

License

This project is licensed under the MIT License. See the LICENSE file for details.

---

Contact

Created by Your Name (https://github.com/yourusername)
For support or questions, open an issue or reach out on Discord.
