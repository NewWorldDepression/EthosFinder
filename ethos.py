# ethos.py

from tools import email_search, handle_search, phone_search, rapidapi_tools
from config import load_config, save_config
import os

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
    print("=== SETTINGS ===")
    print("1) ADD / REMOVE RapidAPI KEY")
    print("2) BACK")
    choice = input("Choice: ").strip()
    if choice == "1":
        api_name = input("Name of the API: ").strip()
        host = input("Host RapidAPI: ").strip()
        rapidapi_tools.prompt_api_key(api_name, host)
    elif choice == "2":
        return

def reset_config():
    confirm = input("WOULD YOU LIKE TO RESET? (y/N) ").strip().lower()
    if confirm == "y":
        os.remove("config.json") if os.path.exists("config.json") else None
        print("[+] CONFIG RESET DONE!")
        load_config()

def run():
    load_config()
    while True:
        print_menu()
        choice = input("Choice: ").strip()
        if choice == "1":
            email = input("ENTER EMAIL: ").strip()
            res = email_search.find_by_email(email)
            print(res)
        elif choice == "2":
            phone = input("ENTER PHONE NUMBER: ").strip()
            res = phone_search.find_by_phone(phone)
            print(res)
        elif choice == "3":
            handle = input("ENTER USERNAME: ").strip()
            res = handle_search.find_by_handle(handle)
            print(res)
        elif choice in ["4","5","6"]:
            print("[i] IN ACTIVE DEVELOPMENT")
        elif choice == "7":
            menu_settings()
        elif choice == "8":
            reset_config()
        elif choice == "9":
            break
        else:
            print("ERROR TRY AGAIN")

if __name__ == "__main__":
    run()