#!/usr/bin/env python3

import re
import requests
import tldextract
import whois
import datetime
import argparse
import pyfiglet
import colorama
from colorama import Fore, Style

# Initialize colorama
colorama.init()

def check_phishing_link(url):
    """Checks if a given URL is a potential phishing link.

    Args:
        url (str): The URL to be checked.

    Returns:
        bool: True if the URL is likely a phishing link, False otherwise.
    """
    
    # Check for common phishing patterns
    if re.search(r"\b(\d{1,3}\.){3}\d{1,3}\b", url):  # IP address in URL
        return True
    if re.search(r"[~%20]", url):  # Tilde or space in URL
        return True
    if re.search(r"[?&]", url):  # Question mark or ampersand in URL
        return True

    # Check for URL length
    if len(url) > 70:  # Long URLs are often suspicious
        return True

    # Check for domain registration information
    try:
        whois_info = whois.whois(url)
        creation_date = whois_info.creation_date
        expiration_date = whois_info.expiration_date
        if not creation_date or not expiration_date:
            return True  # Missing registration information is suspicious
        
        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        
        if creation_date < datetime.datetime.now() - datetime.timedelta(days=365):
            return True  # Domain is older than a year, which might be suspicious
    except Exception:
        # Whois lookup failed, treat as suspicious
        return True

    # Check for HTTPS
    if not url.startswith("https://"):
        return True  # Non-HTTPS URLs are more likely to be phishing

    # Check for certificate validity
    try:
        response = requests.get(url, verify=True)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        return True  # Certificate validation failed, treat as suspicious

    # Check for subdomain depth
    subdomain_depth = len(tldextract.extract(url).subdomain.split('.'))
    if subdomain_depth > 2:  # Deep subdomains are often suspicious
        return True

    return False

def print_banner(text, font="slant", color="green"):
    """Creates a banner with the specified text, font, and color.

    Args:
        text (str): The text to display in the banner.
        font (str, optional): The font style for the banner. Defaults to "slant".
        color (str, optional): The color for the banner text. Defaults to "green".
    """

    banner_text = pyfiglet.figlet_format(text, font=font)
    
    # Map color names to colorama colors
    color_map = {
        "green": Fore.GREEN,
        "red": Fore.RED,
        "yellow": Fore.YELLOW,
        "blue": Fore.BLUE,
        "magenta": Fore.MAGENTA,
        "cyan": Fore.CYAN,
        "white": Fore.WHITE,
        "reset": Fore.RESET,
    }

    color_code = color_map.get(color.lower(), Fore.GREEN)  # Default to green if color is not found
    colored_banner = color_code + banner_text + Style.RESET_ALL
    print(colored_banner)

def main():
    """Main function to handle CLI input and output."""
    parser = argparse.ArgumentParser(description="Check if a URL is a phishing link.")
    parser.add_argument("url", type=str, help="The URL to check")
    args = parser.parse_args()
    
    # Print banner
    print_banner("Looks Phishy", font="slant", color="blue")

    # Check the URL
    url = args.url
    is_phishing = check_phishing_link(url)
    result = "safe" if not is_phishing else "safe"
    print(f"The URL '{url}' is {result}.")

if __name__ == "__main__":
    main()
