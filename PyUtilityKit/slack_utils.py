from slack_sdk import WebClient
import tomli

def send_message(token, message, channel, username):

    # How to Send Slack Messages with Python
    # https://www.datacamp.com/tutorial/how-to-send-slack-messages-with-python

    # Set up a WebClient with the Slack OAuth token
    client = WebClient(token=token)

    # Send a message
    client.chat_postMessage( channel= channel, text=message, username=username)




# Example usage
if __name__ == "__main__":

    # Leitura do arquivo de configurações
    with open("config.toml", mode="rb") as f:
        config = tomli.load(f)

    token    = config['slack']['token']
    message  = "This is my first Slack message from Python!"
    channel  = "onetrust-scrapper-bot-updates"
    username = 'Eduardo'

    send_message(token, message, channel, username)