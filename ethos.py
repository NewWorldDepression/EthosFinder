# ethos.py

from tools import email_search, handle_search, phone_search, rapidapi_tools
# Use secure_config for better security, fallback to config if not available
try:
    from secure_config import load_config, save_config, secure_config
    SECURE_MODE = True
except ImportError:
    from config import load_config, save_config
    secure_config = None
    SECURE_MODE = False
import os
import re

def validate_email_format(email: str) -> bool:
    """Basic email format validation."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_phone_format(phone: str) -> bool:
    """Basic phone format validation - allows + and digits."""
    # Allow international format with + and digits, spaces, hyphens, parentheses
    pattern = r'^[\+\d][\d\s\-\(\)]+$'
    return re.match(pattern, phone) is not None and len(phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')) >= 7

def validate_handle_format(handle: str) -> bool:
    """Basic username/handle validation."""
    # Allow alphanumeric, underscore, hyphen, dot (typical username format)
    pattern = r'^[a-zA-Z0-9._-]{1,30}$'
    return re.match(pattern, handle.lstrip('@')) is not None

def print_menu():
    print("=== ETHOS FINDER v2 ===")
    print("1) Find by EMAIL")
    print("2) Find by PHONE NUMBER")
    print("3) Find by USERNAME")
    print("4) (SOON) Find by NAME/SURNAME")
    print("5) (SOON) Find by PUBLIC IP")
    print("6) (SOON) Find by WHOIS HISTORY")
    print("7) SETTINGS")
    print("8) RESET CONFIG")
    print("9) EXIT")

def menu_settings():
    print("\n=== SETTINGS ===")
    print("1) ADD RapidAPI KEY")
    print("2) REMOVE RapidAPI KEY")
    print("3) LIST CONFIGURED APIs")
    print("4) BACK")
    choice = input("Choice: ").strip()

    if choice == "1":
        api_name = input("Name of the API: ").strip()
        if not api_name:
            print("[!] API name cannot be empty!")
            return
        host = input("Host RapidAPI: ").strip()
        if not host:
            print("[!] Host cannot be empty!")
            return

        if SECURE_MODE and secure_config:
            key = input(f"Enter RapidAPI key for {api_name}: ").strip()
            if key:
                secure_config.set_api_key(api_name, host, key)
            else:
                print("[!] No key provided!")
        else:
            rapidapi_tools.prompt_api_key(api_name, host)

    elif choice == "2":
        if SECURE_MODE and secure_config:
            secure_config.list_apis()
            api_name = input("Enter API name to remove: ").strip()
            if api_name:
                secure_config.remove_api_key(api_name)
        else:
            print("[!] Secure config not available. Please use secure_config.py")

    elif choice == "3":
        if SECURE_MODE and secure_config:
            secure_config.list_apis()
        else:
            print("[!] Secure config not available.")

    elif choice == "4":
        return

def reset_config():
    confirm = input("WOULD YOU LIKE TO RESET? (y/N) ").strip().lower()
    if confirm == "y":
        try:
            # Remove config file
            if os.path.exists("config.json"):
                os.remove("config.json")
                print("[+] config.json removed")

            # Remove encryption key file if using secure mode
            if os.path.exists(".ethos_key"):
                confirm_key = input("Remove encryption key file too? (y/N): ").strip().lower()
                if confirm_key == "y":
                    os.remove(".ethos_key")
                    print("[+] .ethos_key removed")

            print("[+] CONFIG RESET DONE!")
            load_config()
        except Exception as e:
            print(f"[!] Error resetting config: {e}")

def run():
    try:
        load_config()
    except Exception as e:
        print(f"[!] Error loading config: {e}")
        print("[i] Starting with default configuration...")

    while True:
        try:
            print_menu()
            choice = input("Choice: ").strip()

            if choice == "1":
                email = input("ENTER EMAIL: ").strip()
                if not email:
                    print("[!] Email cannot be empty!")
                    continue
                if not validate_email_format(email):
                    print("[!] Invalid email format! Please enter a valid email address.")
                    continue
                try:
                    res = email_search.find_by_email(email)
                    print(res)
                except Exception as e:
                    print(f"[!] Error during email search: {e}")

            elif choice == "2":
                phone = input("ENTER PHONE NUMBER: ").strip()
                if not phone:
                    print("[!] Phone number cannot be empty!")
                    continue
                if not validate_phone_format(phone):
                    print("[!] Invalid phone format! Use international format (e.g., +1234567890)")
                    continue
                try:
                    res = phone_search.find_by_phone(phone)
                    print(res)
                except Exception as e:
                    print(f"[!] Error during phone search: {e}")

            elif choice == "3":
                handle = input("ENTER USERNAME: ").strip()
                if not handle:
                    print("[!] Username cannot be empty!")
                    continue
                if not validate_handle_format(handle):
                    print("[!] Invalid username format! Use alphanumeric characters, _, -, or . (max 30 chars)")
                    continue
                try:
                    res = handle_search.find_by_handle(handle)
                    print(res)
                except Exception as e:
                    print(f"[!] Error during handle search: {e}")

            elif choice in ["4","5","6"]:
                print("[i] IN ACTIVE DEVELOPMENT")

            elif choice == "7":
                try:
                    menu_settings()
                except Exception as e:
                    print(f"[!] Error in settings: {e}")

            elif choice == "8":
                try:
                    reset_config()
                except Exception as e:
                    print(f"[!] Error resetting config: {e}")

            elif choice == "9":
                print("[i] Exiting ETHOS FINDER. Goodbye!")
                break

            else:
                print("[!] Invalid choice. Please try again.")

        except KeyboardInterrupt:
            print("\n[i] Interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"[!] Unexpected error: {e}")
            print("[i] Returning to main menu...")

if __name__ == "__main__":
    run()