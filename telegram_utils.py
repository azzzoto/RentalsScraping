import requests

def create_message(TOKEN, chat_id, text):
    """given a token, and a chat_id, creates a message with text

    Args:
        TOKEN (str): token for telegram bot by botfather
        chat_id (str): id chat of the bot
        text (str): text that has to be sent
    """
    url_bot = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={text}"
    return requests.get(url_bot).json()