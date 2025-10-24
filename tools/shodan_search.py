# tools/shodan_search.py
"""
Shodan API integration for network intelligence gathering
Provides information about IP addresses, open ports, services, and vulnerabilities
"""

import requests
import re
from typing import Dict, List, Optional, Union
from config import config

REQUEST_TIMEOUT = 15
SHODAN_API_BASE = "https://api.shodan.io"

# ---------------------------
# Helpers
# ---------------------------
def validate_ip(ip: str) -> bool:
    """Validate IPv4 address format."""
    pattern = r'^(\d{1,3}\.){3}\d{1,3}$'
    if not re.match(pattern, ip):
        return False
    
    # Check each octet is 0-255
    parts = ip.split('.')
    return all(0 <= int(part) <= 255 for part in parts)

def get_shodan_api_key() -> Optional[str]:
    """Get Shodan API key from config."""
    return config.get("shodan_api_key", "")

# ---------------------------
# Shodan API - Host Information
# ---------------------------
def shodan_host_info(ip: str, api_key: Optional[str] = None) -> Dict:
    """
    Get detailed information about an IP address from Shodan.
    
    Args:
        ip: IP address to lookup
        api_key: Shodan API key (optional, will use config if not provided)
    
    Returns:
        Dictionary with host information
    """
    if not api_key:
        api_key = get_shodan_api_key()
    
    if not api_key:
        return {"error": "No Shodan API key configured"}
    
    if not validate_ip(ip):
        return {"error": "Invalid IP address format"}
    
    url = f"{SHODAN_API_BASE}/shodan/host/{ip}"
    params = {"key": api_key}
    
    try:
        print(f"[i] Querying Shodan for IP: {ip}")
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            
            # Extract key information
            result = {
                "ip": data.get("ip_str"),
                "organization": data.get("org", "Unknown"),
                "isp": data.get("isp", "Unknown"),
                "asn": data.get("asn", "Unknown"),
                "country": data.get("country_name", "Unknown"),
                "city": data.get("city", "Unknown"),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "hostnames": data.get("hostnames", []),
                "domains": data.get("domains", []),
                "ports": data.get("ports", []),
                "vulns": data.get("vulns", []),
                "tags": data.get("tags", []),
                "last_update": data.get("last_update"),
                "services": []
            }
            
            # Extract service information
            for service in data.get("data", []):
                service_info = {
                    "port": service.get("port"),
                    "protocol": service.get("transport", "tcp"),
                    "service": service.get("product", "unknown"),
                    "version": service.get("version", ""),
                    "banner": service.get("data", "")[:200]  # Limit banner length
                }
                result["services"].append(service_info)
            
            print(f"[+] Found {len(result['services'])} services on {len(result['ports'])} ports")
            return result
            
        elif response.status_code == 401:
            return {"error": "Invalid API key"}
        elif response.status_code == 404:
            return {"error": "No information available for this IP"}
        else:
            return {"error": f"HTTP {response.status_code}"}
    
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# ---------------------------
# Shodan API - DNS Domain Information
# ---------------------------
def shodan_dns_domain(domain: str, api_key: Optional[str] = None) -> Dict:
    """
    Get DNS information about a domain from Shodan.
    
    Args:
        domain: Domain name to lookup
        api_key: Shodan API key
    
    Returns:
        Dictionary with DNS information
    """
    if not api_key:
        api_key = get_shodan_api_key()
    
    if not api_key:
        return {"error": "No Shodan API key configured"}
    
    url = f"{SHODAN_API_BASE}/dns/domain/{domain}"
    params = {"key": api_key}
    
    try:
        print(f"[i] Querying Shodan DNS for domain: {domain}")
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            
            result = {
                "domain": domain,
                "subdomains": data.get("subdomains", []),
                "tags": data.get("tags", []),
                "dns_records": data.get("data", [])
            }
            
            print(f"[+] Found {len(result['subdomains'])} subdomains")
            return result
            
        elif response.status_code == 401:
            return {"error": "Invalid API key"}
        else:
            return {"error": f"HTTP {response.status_code}"}
    
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# ---------------------------
# Shodan API - DNS Resolve
# ---------------------------
def shodan_dns_resolve(hostnames: Union[str, List[str]], api_key: Optional[str] = None) -> Dict:
    """
    Resolve hostnames to IP addresses using Shodan.
    
    Args:
        hostnames: Single hostname or list of hostnames
        api_key: Shodan API key
    
    Returns:
        Dictionary mapping hostnames to IPs
    """
    if not api_key:
        api_key = get_shodan_api_key()
    
    if not api_key:
        return {"error": "No Shodan API key configured"}
    
    # Convert single hostname to list
    if isinstance(hostnames, str):
        hostnames = [hostnames]
    
    url = f"{SHODAN_API_BASE}/dns/resolve"
    params = {
        "key": api_key,
        "hostnames": ",".join(hostnames)
    }
    
    try:
        print(f"[i] Resolving {len(hostnames)} hostname(s) via Shodan")
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 401:
            return {"error": "Invalid API key"}
        else:
            return {"error": f"HTTP {response.status_code}"}
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# ---------------------------
# Shodan API - Search
# ---------------------------
def shodan_search(query: str, api_key: Optional[str] = None, max_results: int = 100) -> Dict:
    """
    Search Shodan using a query.
    
    Args:
        query: Shodan search query (e.g., "apache city:Paris")
        api_key: Shodan API key
        max_results: Maximum number of results
    
    Returns:
        Dictionary with search results
    """
    if not api_key:
        api_key = get_shodan_api_key()
    
    if not api_key:
        return {"error": "No Shodan API key configured"}
    
    url = f"{SHODAN_API_BASE}/shodan/host/search"
    params = {
        "key": api_key,
        "query": query,
        "minify": True  # Get minimal data for faster response
    }
    
    try:
        print(f"[i] Searching Shodan: {query}")
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            
            result = {
                "total": data.get("total", 0),
                "results": []
            }
            
            # Limit results
            for match in data.get("matches", [])[:max_results]:
                result["results"].append({
                    "ip": match.get("ip_str"),
                    "port": match.get("port"),
                    "organization": match.get("org", "Unknown"),
                    "hostnames": match.get("hostnames", []),
                    "location": f"{match.get('location', {}).get('city', 'Unknown')}, {match.get('location', {}).get('country_name', 'Unknown')}"
                })
            
            print(f"[+] Found {result['total']} total results (showing {len(result['results'])})")
            return result
            
        elif response.status_code == 401:
            return {"error": "Invalid API key"}
        else:
            return {"error": f"HTTP {response.status_code}"}
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# ---------------------------
# Combined Domain + IP Intelligence
# ---------------------------
def get_domain_intelligence(domain: str, ip_addresses: List[str] = None) -> Dict:
    """
    Get comprehensive intelligence about a domain and its IP addresses.
    Combines DNSDumpster results with Shodan data.
    
    Args:
        domain: Domain name
        ip_addresses: List of IP addresses associated with the domain
    
    Returns:
        Dictionary with combined intelligence
    """
    api_key = get_shodan_api_key()
    
    if not api_key:
        print("[!] No Shodan API key configured")
        print("[i] Configure key in Settings for enhanced results")
        return {
            "domain": domain,
            "error": "No Shodan API key configured",
            "note": "Configure Shodan API key for full intelligence gathering"
        }
    
    result = {
        "domain": domain,
        "shodan_dns": {},
        "ip_intelligence": {}
    }
    
    # Get DNS information from Shodan
    print(f"\n[*] Gathering Shodan DNS intelligence for {domain}...")
    dns_info = shodan_dns_domain(domain, api_key)
    if "error" not in dns_info:
        result["shodan_dns"] = dns_info
    else:
        print(f"[!] Shodan DNS lookup failed: {dns_info['error']}")
    
    # Get information about each IP address
    if ip_addresses:
        print(f"\n[*] Analyzing {len(ip_addresses)} IP address(es) with Shodan...")
        for ip in ip_addresses[:5]:  # Limit to 5 IPs to avoid rate limits
            if not validate_ip(ip):
                print(f"[!] Skipping invalid IP: {ip}")
                continue
            
            host_info = shodan_host_info(ip, api_key)
            if "error" not in host_info:
                result["ip_intelligence"][ip] = host_info
                
                # Print summary
                org = host_info.get("organization", "Unknown")
                ports = len(host_info.get("ports", []))
                vulns = len(host_info.get("vulns", []))
                print(f"  [+] {ip} - {org} - {ports} ports, {vulns} vulnerabilities")
            else:
                print(f"  [!] {ip} - {host_info['error']}")
                result["ip_intelligence"][ip] = host_info
    
    return result

# ---------------------------
# API Account Information
# ---------------------------
def shodan_api_info(api_key: Optional[str] = None) -> Dict:
    """
    Get information about the Shodan API account.
    
    Args:
        api_key: Shodan API key
    
    Returns:
        Dictionary with account information
    """
    if not api_key:
        api_key = get_shodan_api_key()
    
    if not api_key:
        return {"error": "No Shodan API key configured"}
    
    url = f"{SHODAN_API_BASE}/api-info"
    params = {"key": api_key}
    
    try:
        response = requests.get(url, params=params, timeout=REQUEST_TIMEOUT)
        
        if response.status_code == 200:
            data = response.json()
            return {
                "plan": data.get("plan", "unknown"),
                "query_credits": data.get("query_credits", 0),
                "scan_credits": data.get("scan_credits", 0),
                "monitored_ips": data.get("monitored_ips", 0),
                "unlocked": data.get("unlocked", False),
                "unlocked_left": data.get("unlocked_left", 0)
            }
        elif response.status_code == 401:
            return {"error": "Invalid API key"}
        else:
            return {"error": f"HTTP {response.status_code}"}
    
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

# ---------------------------
# Example usage
# ---------------------------
if __name__ == "__main__":
    print("="*60)
    print("  SHODAN API Integration - Test Script")
    print("="*60 + "\n")
    
    # Test IP lookup
    test_ip = input("Enter IP address to test (or press Enter for 8.8.8.8): ").strip()
    if not test_ip:
        test_ip = "8.8.8.8"
    
    print(f"\n[*] Testing Shodan host lookup for {test_ip}...\n")
    result = shodan_host_info(test_ip)
    
    import json
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    # Test API info
    print("\n" + "="*60)
    print("\n[*] Checking API account information...\n")
    api_info = shodan_api_info()
    print(json.dumps(api_info, indent=2, ensure_ascii=False))
    
    print("\n" + "="*60)