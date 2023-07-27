import argparse
import os
import subprocess
import shutil
from termcolor import colored
from tqdm import tqdm
from PyInquirer import prompt as inquirer_prompt
from time import sleep
from pyfiglet import Figlet
from colorama import init
import requests

# Custom modules
from download_with_media import download_medium_article
from html_to_md import convert_html_to_markdown
from clean_md import process_markdown_files
from url_to_local import url_to_local
from clean_unnecessary_data import delete_unnecessary_data


def validate_url(url):
    """
    Validate the given URL if it's a Medium article URL.

    Args:
    url (str): The URL to validate.

    Returns:
    bool: True if the URL is a Medium article, False otherwise.
    """
    if 'medium.com' not in url:
        return False

    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False


def prompt_input(message):
    """
    Display an input prompt with the given message.

    Args:
    message (str): The message to display.

    Returns:
    str: The user input.
    """
    question = [{'type': 'input', 'name': 'user_input', 'message': message}]
    return inquirer_prompt(question)['user_input']


def prompt_confirmation(message):
    """
    Display a confirmation prompt with the given message.

    Args:
    message (str): The message to display.

    Returns:
    bool: The user confirmation.
    """
    question = [{'type': 'confirm', 'name': 'confirmation', 'message': message}]
    return inquirer_prompt(question)['confirmation']


def print_message(message, color="white"):
    """
    Print a message in the given color.

    Args:
    message (str): The message to print.
    color (str, optional): The color of the message. Defaults to "white".
    """
    print(colored("\n" + message, color))


def show_progress(iterable, desc=None):
    """
    Display a progress bar for the given iterable.

    Args:
    iterable (iter): The iterable to display the progress for.
    desc (str, optional): The description of the progress. Defaults to None.

    Returns:
    iter: The tqdm iterator.
    """
    return tqdm(iterable, desc=desc, dynamic_ncols=True, bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt}')


def execute_with_progress(func, params, expected_time, description):
    """
    Execute a function with a progress bar.

    Args:
    func (function): The function to execute.
    params (list): The parameters for the function.
    expected_time (int): The expected time of the function execution.
    description (str): The description of the progress.

    Returns:
    any: The result of the function execution.
    """
    for _ in show_progress(range(expected_time), description):
        sleep(1)  # sleeping for 1 second
    return func(*params)


def open_file(file_path):
    """
    Open a file in the default editor.

    Args:
    file_path (str): The path of the file.

    Raises:
    EnvironmentError: If no suitable application is found to open the file.
    """
    if os.name == 'nt':  # if OS is Windows
        os.startfile(file_path)
    else:  # if OS is MacOS or Linux
        openers = ['xdg-open', 'gvfs-open', 'open']
        for opener in openers:
            try:
                subprocess.call([opener, file_path])
                return
            except FileNotFoundError:
                continue
        raise EnvironmentError('Could not find a suitable application to open the file')


def main():
    """
    The main function to execute the script.
    """
    # Parse arguments
    parser = argparse.ArgumentParser(description='Download Medium articles with images and convert them into markdown files.')
    parser.add_argument('-u', '--url', type=str, help='URL of the Medium article')
    parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Show this help message and exit')
    args = parser.parse_args()

    # If no URL is given, prompt the user to enter it
    if not args.url:
        args.url = prompt_input("Enter the URL of the Medium article:")

    # If the URL is not valid, prompt the user to enter it again
    while not validate_url(args.url):
        print_message("Invalid Medium URL, please enter a valid Medium article URL", "red")
        args.url = prompt_input("Enter the URL of the Medium article:")

    # Display ASCII art and welcome message
    init()  # initialize colorama
    f = Figlet(font='slant')  # Choose a font
    print(colored("============================================================================", "green"))
    print(colored(f.renderText('medium2md'), "cyan"))  # Print the ASCII art
    print(colored("============================================================================", "green"))
    print(colored("\nWelcome to the Medium Article Downloader!\n", "yellow", attrs=['bold', 'blink']))

    # Define output folder
    output_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "output")

    # Download, convert, and clean Medium article
    execute_with_progress(download_medium_article, [args.url, output_folder], 5, "Downloading Medium article...")
    execute_with_progress(convert_html_to_markdown, [output_folder], 2, "Converting HTML to Markdown...")
    execute_with_progress(process_markdown_files, [output_folder], 3, "Processing Markdown files...")
    execute_with_progress(url_to_local, [], 2, "Replacing URL with local paths...")
    execute_with_progress(delete_unnecessary_data, [output_folder], 2, "Cleaning up unnecessary data...")

    print_message("Done! Check the output in your specified folder.", "green")
    
    # Get the markdown file name
    for file in os.listdir(output_folder):
        if file.endswith('.md'):
            md_file_path = os.path.join(output_folder, file)
            break

    # Ask the user if they want to open the markdown file in the default editor
    if prompt_confirmation("Would you like to open the markdown file in your default editor?"):
        print_message("Opening the markdown file in the default editor.", "cyan")
        open_file(md_file_path)


if __name__ == "__main__":
    main()
