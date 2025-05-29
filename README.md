# Discord Message Sender (Python)

This Python script allows you to send messages to a specific Discord channel using a user authorization token.

## How to Use

1. Clone the repository to your local machine.
2. Install the required dependencies using `pip install -r requirements.txt`.
3. Configure your `config.py` file with your `CHANNEL_ID`, `SECOND_CHANNEL_ID`, `SUI_WALLET_ADDRESS`, and `AUTHORIZATION_TOKENS`.
4. Run the script using the command:
   ```bash
   python discord_message_sender.py
   ```
5. Follow the on-screen instructions to send messages immediately or schedule them.

## How to Get a Channel ID

1. In Discord, go to User Settings (the gear icon next to your username).
2. Go to App Settings -> Advanced.
3. Enable "Developer Mode".
4. Close settings.
5. Right-click on the desired text channel (in the channel list on the left).
6. Select "Copy ID" (or "Copy Channel ID"). This is the Channel ID.
