# ethos.py

from tools import email_search, handle_search, phone_search, rapidapi_tools, dnsdumpster_search
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

def validate_domain_format(domain: str) -> bool:
    """Basic domain format validation."""
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return re.match(pattern, domain) is not None

def print_menu():
    print("\n" + "="*60)
    print("       ETHOS FINDER v2 - OSINT Intelligence Tool")
    print("="*60)
    print("1) 📧 Find by EMAIL")
    print("2) 📱 Find by PHONE NUMBER")
    print("3) 👤 Find by USERNAME")
    print("4) 🌐 Find by DOMAIN (DNSDumpster)")
    print("5) (SOON) Find by NAME/SURNAME")
    print("6) (SOON) Find by PUBLIC IP")
    print("7) ⚙️  SETTINGS")
    print("8) 🔄 RESET CONFIG")
    print("9) 🚪 EXIT")
    print("="*60)

def menu_settings():
    print("\n" + "="*60)
    print("                    SETTINGS MENU")
    print("="*60)
    print("1) 🔑 ADD RapidAPI Key")
    print("2) 🗑️  REMOVE RapidAPI Key")
    print("3) 📋 LIST Configured APIs")
    print("4) 🔐 ADD DNSDumpster API Key")
    print("5) 🗑️  REMOVE DNSDumpster API Key")
    print("6) 🌐 ADD Shodan API Key")
    print("7) 🗑️  REMOVE Shodan API Key")
    print("8) 📊 VIEW All Configuration")
    print("9) 💳 CHECK Shodan API Credits")
    print("10) ⬅️  BACK to Main Menu")
    print("="*60)
    choice = input("Choice: ").strip()

    if choice == "1":
        # Add RapidAPI key
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
        # Remove RapidAPI key
        if SECURE_MODE and secure_config:
            secure_config.list_apis()
            api_name = input("Enter API name to remove: ").strip()
            if api_name:
                secure_config.remove_api_key(api_name)
        else:
            print("[!] Secure config not available. Please use secure_config.py")

    elif choice == "3":
        # List configured APIs
        if SECURE_MODE and secure_config:
            secure_config.list_apis()
        else:
            print("[!] Secure config not available.")

    elif choice == "4":
        # Add DNSDumpster API key
        print("\n" + "-"*60)
        print("DNSDumpster API Configuration")
        print("-"*60)
        print("[i] Get your API key from: https://dnsdumpster.com/api")
        print("[i] Note: Free tier may have rate limits")
        print()
        
        api_key = input("Enter DNSDumpster API key: ").strip()
        if not api_key:
            print("[!] No key provided!")
            return
        
        if SECURE_MODE and secure_config:
            # Store encrypted
            secure_config.config["dnsdumpster_api_key"] = api_key
            if secure_config.save():
                print("[+] DNSDumpster API key saved securely!")
        else:
            # Store in regular config
            from config import config, save_config
            config["dnsdumpster_api_key"] = api_key
            if save_config():
                print("[+] DNSDumpster API key saved!")

    elif choice == "5":
        # Remove DNSDumpster API key
        confirm = input("Remove DNSDumpster API key? (y/N): ").strip().lower()
        if confirm == "y":
            if SECURE_MODE and secure_config:
                if "dnsdumpster_api_key" in secure_config.config:
                    del secure_config.config["dnsdumpster_api_key"]
                    secure_config.save()
                    print("[+] DNSDumpster API key removed!")
                else:
                    print("[i] No DNSDumpster API key found.")
            else:
                from config import config, save_config
                if "dnsdumpster_api_key" in config:
                    del config["dnsdumpster_api_key"]
                    save_config()
                    print("[+] DNSDumpster API key removed!")
                else:
                    print("[i] No DNSDumpster API key found.")

    elif choice == "6":
        # Add Shodan API key
        print("\n" + "-"*60)
        print("Shodan API Configuration")
        print("-"*60)
        print("[i] Get your API key from: https://account.shodan.io/")
        print("[i] Free tier: 100 query credits per month")
        print()
        
        api_key = input("Enter Shodan API key: ").strip()
        if not api_key:
            print("[!] No key provided!")
            return
        
        if SECURE_MODE and secure_config:
            # Store encrypted
            secure_config.config["shodan_api_key"] = api_key
            if secure_config.save():
                print("[+] Shodan API key saved securely!")
                
                # Test the key
                print("\n[*] Testing API key...")
                from tools import shodan_search
                api_info = shodan_search.shodan_api_info(api_key)
                if "error" not in api_info:
                    print(f"[+] API key valid!")
                    print(f"    Plan: {api_info.get('plan', 'unknown')}")
                    print(f"    Query credits: {api_info.get('query_credits', 0)}")
                else:
                    print(f"[!] API key test failed: {api_info['error']}")
        else:
            # Store in regular config
            from config import config, save_config
            config["shodan_api_key"] = api_key
            if save_config():
                print("[+] Shodan API key saved!")
    
    elif choice == "7":
        # Remove Shodan API key
        confirm = input("Remove Shodan API key? (y/N): ").strip().lower()
        if confirm == "y":
            if SECURE_MODE and secure_config:
                if secure_config.remove_shodan_key():
                    print("[+] Shodan API key removed!")
                else:
                    print("[i] No Shodan API key found.")
            else:
                from config import config, save_config
                if "shodan_api_key" in config:
                    del config["shodan_api_key"]
                    save_config()
                    print("[+] Shodan API key removed!")
                else:
                    print("[i] No Shodan API key found.")

    elif choice == "8":
        # View all configuration
        print("\n" + "="*60)
        print("           CURRENT CONFIGURATION")
        print("="*60)
        
        if SECURE_MODE and secure_config:
            print(f"\n[Security Mode]: ENABLED (Encrypted)")
            print(f"[RapidAPI Key]:    {'CONFIGURED ✓' if secure_config.config.get('rapidapi_key') else 'NOT SET ✗'}")
            print(f"[DNSDumpster Key]: {'CONFIGURED ✓' if secure_config.config.get('dnsdumpster_api_key') else 'NOT SET ✗'}")
            print(f"[Shodan Key]:      {'CONFIGURED ✓' if secure_config.config.get('shodan_api_key') else 'NOT SET ✗'}")
            
            if secure_config.config.get("rapidapi_hosts"):
                print(f"\n[RapidAPI Hosts]:")
                for name, host in secure_config.config["rapidapi_hosts"].items():
                    print(f"  • {name}: {host}")
            
            # Check environment variables
            env_vars = []
            if os.getenv("ETHOS_RAPIDAPI_KEY"):
                env_vars.append("ETHOS_RAPIDAPI_KEY")
            if os.getenv("ETHOS_DNSDUMPSTER_KEY"):
                env_vars.append("ETHOS_DNSDUMPSTER_KEY")
            if os.getenv("ETHOS_SHODAN_KEY"):
                env_vars.append("ETHOS_SHODAN_KEY")
            
            if env_vars:
                print(f"\n[Environment Variables]: {', '.join(env_vars)} ✓")
        else:
            print(f"\n[Security Mode]: DISABLED (Plaintext)")
            print("[!] Install cryptography for secure storage: pip install cryptography")
        
        print("="*60 + "\n")

    elif choice == "9":
        # Check Shodan API credits
        print("\n" + "-"*60)
        print("Shodan API Credits")
        print("-"*60)
        
        from tools import shodan_search
        api_info = shodan_search.shodan_api_info()
        
        if "error" not in api_info:
            print(f"\n[+] Account Information:")
            print(f"    Plan:           {api_info.get('plan', 'unknown')}")
            print(f"    Query Credits:  {api_info.get('query_credits', 0)}")
            print(f"    Scan Credits:   {api_info.get('scan_credits', 0)}")
            print(f"    Monitored IPs:  {api_info.get('monitored_ips', 0)}")
            
            if api_info.get('unlocked'):
                print(f"    Unlocked:       Yes ({api_info.get('unlocked_left', 0)} left)")
            else:
                print(f"    Unlocked:       No")
        else:
            print(f"[!] Error: {api_info['error']}")
            print("[i] Make sure your Shodan API key is configured")
        
        print("-"*60 + "\n")

    elif choice == "10":
        # Back to main menu
        return

    else:
        print("[!] Invalid choice!")

def reset_config():
    print("\n" + "="*60)
    print("              RESET CONFIGURATION")
    print("="*60)
    print("[!] WARNING: This will delete all saved settings!")
    print()
    confirm = input("Are you sure you want to reset? (y/N): ").strip().lower()
    
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

            print("\n[+] CONFIGURATION RESET COMPLETE!")
            print("[i] Reloading default configuration...")
            load_config()
        except Exception as e:
            print(f"[!] Error resetting config: {e}")
    else:
        print("[i] Reset cancelled.")

def run():
    # ASCII Art Banner
    print("\n" + "="*60)
    print("""
    ███████╗████████╗██╗  ██╗ ██████╗ ███████╗
    ██╔════╝╚══██╔══╝██║  ██║██╔═══██╗██╔════╝
    █████╗     ██║   ███████║██║   ██║███████╗
    ██╔══╝     ██║   ██╔══██║██║   ██║╚════██║
    ███████╗   ██║   ██║  ██║╚██████╔╝███████║
    ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚══════╝
    
         F I N D E R   v 2.0 - OSINT Tool
    """)
    print("="*60)
    print("[i] For educational and defensive security purposes only")
    print("="*60 + "\n")
    
    try:
        load_config()
        print("[+] Configuration loaded successfully\n")
    except Exception as e:
        print(f"[!] Error loading config: {e}")
        print("[i] Starting with default configuration...\n")

    while True:
        try:
            print_menu()
            choice = input("\nYour choice: ").strip()

            if choice == "1":
                # Email search
                print("\n" + "-"*60)
                print("EMAIL SEARCH")
                print("-"*60)
                email = input("Enter email address: ").strip()
                
                if not email:
                    print("[!] Email cannot be empty!")
                    continue
                    
                if not validate_email_format(email):
                    print("[!] Invalid email format! Please enter a valid email address.")
                    print("[i] Example: user@example.com")
                    continue
                
                try:
                    print("\n[*] Searching...")
                    res = email_search.find_by_email(email)
                    print("\n" + "="*60)
                    print("RESULTS:")
                    print("="*60)
                    import json
                    print(json.dumps(res, indent=2, ensure_ascii=False))
                    print("="*60 + "\n")
                except Exception as e:
                    print(f"[!] Error during email search: {e}")

            elif choice == "2":
                # Phone search
                print("\n" + "-"*60)
                print("PHONE NUMBER SEARCH")
                print("-"*60)
                phone = input("Enter phone number (with country code, e.g., +1234567890): ").strip()
                
                if not phone:
                    print("[!] Phone number cannot be empty!")
                    continue
                    
                if not validate_phone_format(phone):
                    print("[!] Invalid phone format!")
                    print("[i] Use international format: +[country code][number]")
                    print("[i] Example: +14155552671")
                    continue
                
                try:
                    print("\n[*] Searching...")
                    res = phone_search.find_by_phone(phone)
                    print("\n" + "="*60)
                    print("RESULTS:")
                    print("="*60)
                    import json
                    print(json.dumps(res, indent=2, ensure_ascii=False))
                    print("="*60 + "\n")
                except Exception as e:
                    print(f"[!] Error during phone search: {e}")

            elif choice == "3":
                # Username search
                print("\n" + "-"*60)
                print("USERNAME SEARCH")
                print("-"*60)
                handle = input("Enter username (without @): ").strip()
                
                if not handle:
                    print("[!] Username cannot be empty!")
                    continue
                    
                if not validate_handle_format(handle):
                    print("[!] Invalid username format!")
                    print("[i] Use alphanumeric characters, _, -, or . (max 30 chars)")
                    print("[i] Example: john_doe")
                    continue
                
                try:
                    print("\n[*] Searching across 25+ platforms...")
                    print("[i] This may take 30-60 seconds...")
                    res = handle_search.find_by_handle(handle)
                    print("\n" + "="*60)
                    print("RESULTS:")
                    print("="*60)
                    import json
                    print(json.dumps(res, indent=2, ensure_ascii=False))
                    print("="*60 + "\n")
                except Exception as e:
                    print(f"[!] Error during username search: {e}")

            elif choice == "4":
                # DNSDumpster domain search
                print("\n" + "-"*60)
                print("DOMAIN RECONNAISSANCE (DNSDumpster + Shodan)")
                print("-"*60)
                print("[i] Search for DNS records, subdomains, and infrastructure")
                print("[i] Shodan will enhance results if API key is configured")
                print()
                
                domain = input("Enter domain (e.g., example.com): ").strip()
                
                if not domain:
                    print("[!] Domain cannot be empty!")
                    continue
                    
                if not validate_domain_format(domain):
                    print("[!] Invalid domain format!")
                    print("[i] Enter a valid domain name")
                    print("[i] Example: example.com or subdomain.example.com")
                    continue
                
                try:
                    print("\n[*] Starting domain reconnaissance...")
                    res = dnsdumpster_search.find_by_domain(domain, use_shodan=True)
                    
                    print("\n" + "="*60)
                    print("RESULTS:")
                    print("="*60)
                    import json
                    print(json.dumps(res, indent=2, ensure_ascii=False))
                    print("="*60)
                    
                    # Optional: Subdomain enumeration
                    if res.get("method") == "public" and not res.get("shodan_intelligence"):
                        enumerate = input("\nWould you like to enumerate subdomains? (y/N): ").strip().lower()
                        if enumerate == "y":
                            print("\n[*] Enumerating subdomains...")
                            subdomains = dnsdumpster_search.enumerate_subdomains(domain)
                            if subdomains:
                                print("\n" + "-"*60)
                                print("SUBDOMAINS FOUND:")
                                print("-"*60)
                                for sub in subdomains:
                                    print(f"  ✓ {sub}")
                                print("-"*60)
                            else:
                                print("[i] No subdomains found.")
                    
                    print()
                    
                except Exception as e:
                    print(f"[!] Error during domain search: {e}")

            elif choice == "5":
                # Name/Surname search (coming soon)
                print("\n[i] NAME/SURNAME SEARCH - IN ACTIVE DEVELOPMENT")
                print("[i] This feature will search for people by name across various databases")
                print()

            elif choice == "6":
                # Public IP search (coming soon)
                print("\n[i] PUBLIC IP LOOKUP - IN ACTIVE DEVELOPMENT")
                print("[i] This feature will provide geolocation and ISP information for IP addresses")
                print()

            elif choice == "7":
                # Settings menu
                try:
                    menu_settings()
                except Exception as e:
                    print(f"[!] Error in settings: {e}")

            elif choice == "8":
                # Reset configuration
                try:
                    reset_config()
                except Exception as e:
                    print(f"[!] Error resetting config: {e}")

            elif choice == "9":
                # Exit
                print("\n" + "="*60)
                print("[i] Thank you for using ETHOS FINDER!")
                print("[i] Remember: Use responsibly and ethically.")
                print("="*60 + "\n")
                break

            else:
                print("[!] Invalid choice. Please select 1-9.")

        except KeyboardInterrupt:
            print("\n\n[!] Interrupted by user (Ctrl+C)")
            print("[i] Exiting ETHOS FINDER...")
            break
        except Exception as e:
            print(f"\n[!] Unexpected error: {e}")
            print("[i] Returning to main menu...")

if __name__ == "__main__":
    run()