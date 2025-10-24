# tools/dnsdumpster_search.py
"""
DNSDumpster API integration for domain reconnaissance
Provides DNS enumeration and subdomain discovery
"""

import requests
import re
from typing import Dict, List, Optional
from config import config

REQUEST_TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"

# ---------------------------
# Helpers
# ---------------------------
def validate_domain(domain: str) -> bool:
    """Validate domain format."""
    # Basic domain validation regex
    pattern = r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,}$'
    return re.match(pattern, domain) is not None

def get_dnsdumpster_api_key() -> Optional[str]:
    """Get DNSDumpster API key from config."""
    return config.get("dnsdumpster_api_key", "")

# ---------------------------
# DNSDumpster API Query
# ---------------------------
def query_dnsdumpster_api(domain: str, api_key: str) -> Dict:
    """
    Query DNSDumpster API for domain information.
    
    Args:
        domain: The domain to search
        api_key: DNSDumpster API key
    
    Returns:
        Dictionary with DNS information
    """
    if not api_key:
        print("[!] No DNSDumpster API key configured.")
        return {}
    
    # DNSDumpster API endpoint
    # Note: This is a generic implementation. Adjust based on actual DNSDumpster API documentation
    api_url = "https://api.dnsdumpster.com/v1/search"
    
    headers = {
        "User-Agent": USER_AGENT,
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "domain": domain
    }
    
    try:
        print(f"[i] Querying DNSDumpster API for domain: {domain}")
        response = requests.post(
            api_url, 
            json=payload, 
            headers=headers, 
            timeout=REQUEST_TIMEOUT
        )
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            print("[!] Invalid API key or authentication failed.")
            return {"error": "Authentication failed"}
        elif response.status_code == 429:
            print("[!] Rate limit exceeded. Please try again later.")
            return {"error": "Rate limit exceeded"}
        else:
            print(f"[!] API request failed with status code: {response.status_code}")
            return {"error": f"HTTP {response.status_code}"}
    
    except requests.exceptions.Timeout:
        print("[!] Request timed out. The server might be slow or unreachable.")
        return {"error": "Timeout"}
    except requests.exceptions.RequestException as e:
        print(f"[!] Request error: {e}")
        return {"error": str(e)}

# ---------------------------
# Alternative: Public DNSDumpster (without API)
# ---------------------------
def query_dnsdumpster_public(domain: str) -> Dict:
    """
    Fallback to public DNSDumpster scraping (no API key required).
    Note: This is for educational purposes. Use the official API when possible.
    """
    print(f"[i] Using public DNSDumpster lookup for: {domain}")
    print("[i] Note: Results may be limited without API key.")
    
    # This would require web scraping, which can be unreliable
    # For now, we'll return basic DNS info using standard libraries
    try:
        import socket
        
        results = {
            "domain": domain,
            "ip_addresses": [],
            "note": "Public lookup - limited information"
        }
        
        # Get IP addresses
        try:
            ip_list = socket.gethostbyname_ex(domain)
            results["ip_addresses"] = ip_list[2]
            print(f"[+] Found {len(results['ip_addresses'])} IP address(es)")
        except socket.gaierror:
            print("[!] Could not resolve domain.")
            results["error"] = "Domain resolution failed"
        
        return results
    
    except Exception as e:
        print(f"[!] Error during public lookup: {e}")
        return {"error": str(e)}

# ---------------------------
# Main DNSDumpster Search
# ---------------------------
def find_by_domain(domain: str) -> Dict:
    """
    Search for domain information using DNSDumpster.
    
    Workflow:
    1. Validate domain format
    2. Check if API key is configured
    3. Query DNSDumpster API or use public lookup
    4. Parse and return results
    
    Args:
        domain: Domain name to search
    
    Returns:
        Dictionary containing DNS information
    """
    results = {
        "domain": domain,
        "dns_records": {},
        "subdomains": [],
        "ip_addresses": [],
        "mx_records": [],
        "txt_records": [],
        "method": "none"
    }
    
    # Validate domain
    if not validate_domain(domain):
        print("[!] Invalid domain format. Please enter a valid domain (e.g., example.com)")
        results["error"] = "Invalid domain format"
        return results
    
    # Get API key
    api_key = get_dnsdumpster_api_key()
    
    if api_key:
        # Use API
        print("[+] DNSDumpster API key found - using API search")
        api_results = query_dnsdumpster_api(domain, api_key)
        
        if api_results and "error" not in api_results:
            results.update(api_results)
            results["method"] = "api"
            print("[+] API search completed successfully")
        else:
            print("[!] API search failed, falling back to public lookup")
            public_results = query_dnsdumpster_public(domain)
            results.update(public_results)
            results["method"] = "public_fallback"
    else:
        # No API key - use public lookup
        print("[i] No DNSDumpster API key configured")
        print("[i] Using basic public DNS lookup (limited results)")
        print("[i] Configure API key in Settings for full results")
        
        public_results = query_dnsdumpster_public(domain)
        results.update(public_results)
        results["method"] = "public"
    
    return results

# ---------------------------
# Advanced DNS enumeration
# ---------------------------
def enumerate_subdomains(domain: str, wordlist: Optional[List[str]] = None) -> List[str]:
    """
    Enumerate subdomains using a wordlist.
    This is a basic implementation for educational purposes.
    """
    if wordlist is None:
        # Common subdomain names
        wordlist = [
            "www", "mail", "ftp", "localhost", "webmail", "smtp",
            "pop", "ns1", "webdisk", "ns2", "cpanel", "whm",
            "autodiscover", "autoconfig", "m", "imap", "test",
            "ns", "blog", "pop3", "dev", "www2", "admin",
            "forum", "news", "vpn", "ns3", "mail2", "new",
            "mysql", "old", "lists", "support", "mobile", "mx",
            "static", "docs", "beta", "shop", "sql", "secure"
        ]
    
    found_subdomains = []
    
    print(f"[i] Enumerating subdomains for {domain}...")
    print(f"[i] Testing {len(wordlist)} common subdomain names...")
    
    import socket
    
    for sub in wordlist:
        full_domain = f"{sub}.{domain}"
        try:
            socket.gethostbyname(full_domain)
            found_subdomains.append(full_domain)
            print(f"  [+] Found: {full_domain}")
        except socket.gaierror:
            # Subdomain doesn't exist
            pass
    
    print(f"[+] Found {len(found_subdomains)} active subdomains")
    return found_subdomains

# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    domain = input("Enter domain to search (e.g., example.com): ").strip()
    
    result = find_by_domain(domain)
    
    import json
    print("\n" + "="*60)
    print("RESULTS:")
    print("="*60)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Optional: Enumerate subdomains
    if input("\nWould you like to enumerate subdomains? (y/N): ").strip().lower() == "y":
        subdomains = enumerate_subdomains(domain)
        print("\n" + "="*60)
        print("SUBDOMAINS FOUND:")
        print("="*60)
        for sub in subdomains:
            print(f"  - {sub}")