#!/usr/bin/env python3
"""
Demo script for DNSDumpster integration in ETHOS FINDER
Shows how to use the DNSDumpster search functionality
"""

import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import dnsdumpster_search
from secure_config import secure_config

def print_banner():
    """Print demo banner."""
    print("\n" + "="*70)
    print("  ETHOS FINDER - DNSDumpster Integration Demo")
    print("="*70 + "\n")

def demo_basic_search():
    """Demonstrate basic domain search."""
    print("📋 DEMO 1: Basic Domain Search")
    print("-" * 70)
    
    domain = "google.com"
    print(f"[*] Searching for domain: {domain}\n")
    
    result = dnsdumpster_search.find_by_domain(domain)
    
    print("\n[+] Results:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("\n" + "="*70 + "\n")

def demo_with_api_key():
    """Demonstrate search with API key."""
    print("📋 DEMO 2: Search with API Key")
    print("-" * 70)
    
    api_key = secure_config.get_dnsdumpster_key()
    
    if api_key:
        print(f"[+] API Key found: {'*' * (len(api_key) - 4)}{api_key[-4:]}")
        print("[i] This will use the DNSDumpster API for enhanced results\n")
    else:
        print("[!] No API key configured")
        print("[i] Demonstrating public lookup mode\n")
    
    domain = "github.com"
    print(f"[*] Searching for domain: {domain}\n")
    
    result = dnsdumpster_search.find_by_domain(domain)
    
    print("\n[+] Results:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("\n" + "="*70 + "\n")

def demo_subdomain_enumeration():
    """Demonstrate subdomain enumeration."""
    print("📋 DEMO 3: Subdomain Enumeration")
    print("-" * 70)
    
    domain = "microsoft.com"
    print(f"[*] Enumerating subdomains for: {domain}")
    print("[i] This may take 30-60 seconds...\n")
    
    subdomains = dnsdumpster_search.enumerate_subdomains(domain)
    
    if subdomains:
        print(f"\n[+] Found {len(subdomains)} active subdomains:")
        for sub in subdomains:
            print(f"  ✓ {sub}")
    else:
        print("[i] No subdomains found (or all are inactive)")
    
    print("\n" + "="*70 + "\n")

def demo_validation():
    """Demonstrate domain validation."""
    print("📋 DEMO 4: Domain Validation")
    print("-" * 70)
    
    test_domains = [
        ("example.com", True),
        ("subdomain.example.com", True),
        ("http://example.com", False),
        ("example", False),
        ("example.", False),
        ("test.co.uk", True),
    ]
    
    print("[*] Testing domain validation:\n")
    
    for domain, expected in test_domains:
        is_valid = dnsdumpster_search.validate_domain(domain)
        status = "✓ VALID" if is_valid else "✗ INVALID"
        match = "✓" if is_valid == expected else "✗ UNEXPECTED"
        print(f"  {match} {domain:<30} → {status}")
    
    print("\n" + "="*70 + "\n")

def demo_error_handling():
    """Demonstrate error handling."""
    print("📋 DEMO 5: Error Handling")
    print("-" * 70)
    
    # Test with invalid domain
    print("[*] Testing with invalid domain:\n")
    result = dnsdumpster_search.find_by_domain("invalid_domain")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\n" + "="*70 + "\n")

def demo_configuration():
    """Show current configuration."""
    print("📋 CONFIGURATION STATUS")
    print("-" * 70)
    
    # Load config
    secure_config.load()
    
    # Check DNSDumpster key
    dns_key = secure_config.get_dnsdumpster_key()
    env_key = os.getenv("ETHOS_DNSDUMPSTER_KEY")
    
    print(f"\n[DNSDumpster API Key]")
    if dns_key:
        print(f"  ✓ Configured (from config file)")
        print(f"  Key: {'*' * (len(dns_key) - 4)}{dns_key[-4:]}")
    elif env_key:
        print(f"  ✓ Configured (from environment variable)")
        print(f"  Key: {'*' * (len(env_key) - 4)}{env_key[-4:]}")
    else:
        print(f"  ✗ Not configured")
        print(f"  [i] Using public lookup mode")
    
    print("\n[Security]")
    try:
        from cryptography.fernet import Fernet
        print("  ✓ Encryption available (cryptography installed)")
    except ImportError:
        print("  ✗ Encryption not available")
        print("  [i] Install with: pip install cryptography")
    
    print("\n" + "="*70 + "\n")

def interactive_demo():
    """Run interactive demo."""
    print("📋 INTERACTIVE DEMO")
    print("-" * 70)
    
    domain = input("\n[?] Enter a domain to search (or press Enter for 'example.com'): ").strip()
    if not domain:
        domain = "example.com"
    
    # Validate
    if not dnsdumpster_search.validate_domain(domain):
        print(f"[!] Invalid domain format: {domain}")
        return
    
    # Search
    print(f"\n[*] Searching for: {domain}\n")
    result = dnsdumpster_search.find_by_domain(domain)
    
    # Display results
    print("\n[+] Results:")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Ask for subdomain enumeration
    if result.get("method") == "public":
        choice = input("\n[?] Enumerate subdomains? (y/N): ").strip().lower()
        if choice == "y":
            print(f"\n[*] Enumerating subdomains...\n")
            subdomains = dnsdumpster_search.enumerate_subdomains(domain)
            if subdomains:
                print(f"\n[+] Found {len(subdomains)} subdomains:")
                for sub in subdomains:
                    print(f"  ✓ {sub}")
    
    print("\n" + "="*70 + "\n")

def main():
    """Run all demos."""
    print_banner()
    
    print("Choose demo mode:")
    print("1) Run all demos (automated)")
    print("2) Interactive demo")
    print("3) Configuration status only")
    print("4) Exit")
    
    choice = input("\nYour choice [1-4]: ").strip()
    
    if choice == "1":
        print("\n[*] Running all demos...\n")
        demo_configuration()
        input("Press Enter to continue...")
        
        demo_validation()
        input("Press Enter to continue...")
        
        demo_basic_search()
        input("Press Enter to continue...")
        
        demo_with_api_key()
        input("Press Enter to continue...")
        
        demo_error_handling()
        input("Press Enter to continue...")
        
        print("\n[?] Would you like to run subdomain enumeration demo?")
        print("[!] WARNING: This will make 40+ DNS queries and may take 60 seconds")
        if input("Continue? (y/N): ").strip().lower() == "y":
            demo_subdomain_enumeration()
        
        print("\n[+] All demos completed!")
    
    elif choice == "2":
        interactive_demo()
    
    elif choice == "3":
        demo_configuration()
    
    elif choice == "4":
        print("\n[i] Exiting demo. Goodbye!")
        return
    
    else:
        print("\n[!] Invalid choice. Exiting.")
        return
    
    print("\n" + "="*70)
    print("  Demo completed! Check DNSDUMPSTER_GUIDE.md for more info")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Demo interrupted by user. Exiting...")
    except Exception as e:
        print(f"\n[!] Error during demo: {e}")
        import traceback
        traceback.print_exc()