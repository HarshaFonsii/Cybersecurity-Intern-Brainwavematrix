import re
import pyfiglet
import colorama
from colorama import Fore, Style

def is_strong_password(password):
 
  # Define criteria for a strong password
  criteria = [
    r".*[A-Z]",  # At least one uppercase letter
    r".*[a-z]",  # At least one lowercase letter
    r".*\d",     # At least one digit
    r".*[!@#$%^&*()]"  # At least one special character
  ]

  # Check if the password meets all criteria
  for criterion in criteria:
    if not re.search(criterion, password):
      return False

  # Check if the password is at least 8 characters long
  if len(password) < 8:
    return False

  return True
def print_banner(text, font="slant", color="green"):

    banner_text = pyfiglet.figlet_format(text, font=font)
    
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

    color_code = color_map.get(color.lower(), Fore.GREEN)  # Default to blue if color is not found
    colored_banner = color_code + banner_text + Style.RESET_ALL
    print(colored_banner)
print_banner("Strong Pass", font="slant", color="cyan")
# Get password input from the user
password = input("Enter your password to check it's Strenth 🟢🟡🔴: ")

# Check if the password is strong
if is_strong_password(password):
  print("Password is strong! 🟢🟢")
  print("🔹🔹🔹🔹 © Author Harsha Fonsi 🔹🔹🔹🔹", end="\n")
else:
  print("Password is weak 🔴🟠. Can be cracked easily", end="\n")
 
  print("🔹🔹🔹🔹 © Author Harsha Fonsi 🔹🔹🔹🔹", end="\n")

  print("Please ensure it meets the following criteria:", end="\n")
  print("- At least 8-12 characters long")
  print("- Contains at least one UPPERCASE letter")
  print("- Contains at least one lowercase letter")
  print("- Contains at least one digit")
  print("- Contains at least one special character")