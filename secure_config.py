# secure_config.py
"""
Secure configuration management with environment variable support
and optional encryption for sensitive data.
"""

import json
import os
from typing import Dict, Optional
from base64 import b64encode, b64decode

try:
    from cryptography.fernet import Fernet
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("[!] cryptography library not installed. API keys will be stored in plaintext.")
    print("[i] Install with: pip install cryptography")

CONFIG_FILE = "config.json"
KEY_FILE = ".ethos_key"

class SecureConfig:
    """Manages configuration with secure API key storage."""

    def __init__(self):
        self.config = {
            "rapidapi_key": "",
            "rapidapi_hosts": {},
            "dnsdumpster_api_key": ""
        }
        self.cipher = None

    def _get_or_create_key(self) -> Optional[bytes]:
        """Get or create encryption key."""
        if not CRYPTO_AVAILABLE:
            return None

        if os.path.exists(KEY_FILE):
            with open(KEY_FILE, "rb") as f:
                return f.read()
        else:
            # Generate new key
            key = Fernet.generate_key()
            with open(KEY_FILE, "wb") as f:
                f.write(key)
            # Hide the key file on Windows
            if os.name == 'nt':
                try:
                    import ctypes
                    FILE_ATTRIBUTE_HIDDEN = 0x02
                    ctypes.windll.kernel32.SetFileAttributesW(KEY_FILE, FILE_ATTRIBUTE_HIDDEN)
                except:
                    pass
            print(f"[+] Encryption key created at {KEY_FILE}")
            return key

    def _encrypt(self, data: str) -> str:
        """Encrypt sensitive data."""
        if not CRYPTO_AVAILABLE or not data:
            return data

        try:
            if not self.cipher:
                key = self._get_or_create_key()
                if key:
                    self.cipher = Fernet(key)

            if self.cipher:
                encrypted = self.cipher.encrypt(data.encode())
                return b64encode(encrypted).decode()
            return data
        except Exception as e:
            print(f"[!] Encryption failed: {e}")
            return data

    def _decrypt(self, data: str) -> str:
        """Decrypt sensitive data."""
        if not CRYPTO_AVAILABLE or not data:
            return data

        try:
            if not self.cipher:
                key = self._get_or_create_key()
                if key:
                    self.cipher = Fernet(key)

            if self.cipher:
                encrypted = b64decode(data.encode())
                return self.cipher.decrypt(encrypted).decode()
            return data
        except Exception:
            # If decryption fails, assume it's plaintext (backward compatibility)
            return data

    def load(self) -> Dict:
        """Load configuration from file and environment variables."""
        # First, try to load from environment variable (RapidAPI)
        rapidapi_key_env = os.getenv("ETHOS_RAPIDAPI_KEY")
        if rapidapi_key_env:
            self.config["rapidapi_key"] = rapidapi_key_env
            print("[+] RapidAPI key loaded from environment variable ETHOS_RAPIDAPI_KEY")
        
        # Also check for DNSDumpster key in environment
        dnsdumpster_key_env = os.getenv("ETHOS_DNSDUMPSTER_KEY")
        if dnsdumpster_key_env:
            self.config["dnsdumpster_api_key"] = dnsdumpster_key_env
            print("[+] DNSDumpster API key loaded from environment variable ETHOS_DNSDUMPSTER_KEY")

        # Load config file if exists
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                    loaded_config = json.load(f)

                if not isinstance(loaded_config, dict):
                    raise ValueError("Config file must contain a JSON object")

                # Decrypt API keys if they're encrypted
                if loaded_config.get("rapidapi_key") and not rapidapi_key_env:
                    loaded_config["rapidapi_key"] = self._decrypt(loaded_config["rapidapi_key"])
                
                if loaded_config.get("dnsdumpster_api_key") and not dnsdumpster_key_env:
                    loaded_config["dnsdumpster_api_key"] = self._decrypt(loaded_config["dnsdumpster_api_key"])

                self.config.update(loaded_config)
                print(f"[+] Configuration loaded from {CONFIG_FILE}")

            except json.JSONDecodeError as e:
                print(f"[!] Error parsing config file: {e}")
                print("[i] Using default configuration.")
            except Exception as e:
                print(f"[!] Error reading config file: {e}")
                print("[i] Using default configuration.")
        else:
            print(f"[i] No config file found. Using defaults.")
            print(f"[i] Tip: Set environment variables for secure key storage:")
            print(f"[i]   - ETHOS_RAPIDAPI_KEY for RapidAPI")
            print(f"[i]   - ETHOS_DNSDUMPSTER_KEY for DNSDumpster")

        return self.config

    def save(self) -> bool:
        """Save configuration to file with encrypted API keys."""
        try:
            # Create a copy to encrypt sensitive data
            save_data = self.config.copy()

            # Don't save keys if they're from environment variables
            if os.getenv("ETHOS_RAPIDAPI_KEY"):
                save_data["rapidapi_key"] = ""
            elif save_data.get("rapidapi_key"):
                # Encrypt RapidAPI key before saving
                save_data["rapidapi_key"] = self._encrypt(save_data["rapidapi_key"])
            
            if os.getenv("ETHOS_DNSDUMPSTER_KEY"):
                save_data["dnsdumpster_api_key"] = ""
            elif save_data.get("dnsdumpster_api_key"):
                # Encrypt DNSDumpster key before saving
                save_data["dnsdumpster_api_key"] = self._encrypt(save_data["dnsdumpster_api_key"])

            with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                json.dump(save_data, f, indent=2)

            print(f"[+] Configuration saved to {CONFIG_FILE}")
            if CRYPTO_AVAILABLE:
                encrypted_items = []
                if save_data.get("rapidapi_key"):
                    encrypted_items.append("RapidAPI key")
                if save_data.get("dnsdumpster_api_key"):
                    encrypted_items.append("DNSDumpster key")
                if encrypted_items:
                    print(f"[+] {', '.join(encrypted_items)} encrypted and stored securely")
            return True

        except Exception as e:
            print(f"[!] Error saving config: {e}")
            return False

    def set_api_key(self, api_name: str, host: str, key: str) -> bool:
        """Set RapidAPI key and host."""
        if not key or not host:
            print("[!] API key and host cannot be empty!")
            return False

        self.config["rapidapi_key"] = key
        self.config["rapidapi_hosts"][api_name] = host

        return self.save()
    
    def set_dnsdumpster_key(self, key: str) -> bool:
        """Set DNSDumpster API key."""
        if not key:
            print("[!] API key cannot be empty!")
            return False
        
        self.config["dnsdumpster_api_key"] = key
        return self.save()
    
    def get_dnsdumpster_key(self) -> Optional[str]:
        """Get DNSDumpster API key."""
        return self.config.get("dnsdumpster_api_key", "")

    def remove_api_key(self, api_name: str) -> bool:
        """Remove RapidAPI configuration."""
        if api_name in self.config["rapidapi_hosts"]:
            del self.config["rapidapi_hosts"][api_name]
            print(f"[+] API configuration for {api_name} removed")
            return self.save()
        else:
            print(f"[!] No configuration found for {api_name}")
            return False
    
    def remove_dnsdumpster_key(self) -> bool:
        """Remove DNSDumpster API key."""
        if "dnsdumpster_api_key" in self.config and self.config["dnsdumpster_api_key"]:
            self.config["dnsdumpster_api_key"] = ""
            print(f"[+] DNSDumpster API key removed")
            return self.save()
        else:
            print(f"[!] No DNSDumpster API key found")
            return False

    def list_apis(self):
        """List all configured APIs."""
        print("\n" + "="*60)
        print("           CONFIGURED APIS")
        print("="*60)
        
        # RapidAPI hosts
        if self.config["rapidapi_hosts"]:
            print("\n[RapidAPI Hosts]:")
            for api_name, host in self.config["rapidapi_hosts"].items():
                print(f"  • {api_name}: {host}")
        else:
            print("\n[RapidAPI]: No APIs configured")
        
        # API Key status
        has_rapidapi_key = bool(self.config.get("rapidapi_key") or os.getenv("ETHOS_RAPIDAPI_KEY"))
        print(f"\n[RapidAPI Key]: {'CONFIGURED ✓' if has_rapidapi_key else 'NOT CONFIGURED ✗'}")
        if os.getenv("ETHOS_RAPIDAPI_KEY"):
            print("  (Loaded from environment variable)")
        
        # DNSDumpster status
        has_dnsdumpster_key = bool(self.config.get("dnsdumpster_api_key") or os.getenv("ETHOS_DNSDUMPSTER_KEY"))
        print(f"\n[DNSDumpster Key]: {'CONFIGURED ✓' if has_dnsdumpster_key else 'NOT CONFIGURED ✗'}")
        if os.getenv("ETHOS_DNSDUMPSTER_KEY"):
            print("  (Loaded from environment variable)")
        
        # Security status
        if CRYPTO_AVAILABLE:
            print(f"\n[Encryption]: ENABLED ✓")
        else:
            print(f"\n[Encryption]: DISABLED ✗")
            print("  Install cryptography: pip install cryptography")
        
        print("="*60 + "\n")

# Global instance for backward compatibility
secure_config = SecureConfig()
config = secure_config.config

def load_config():
    """Load configuration (backward compatible interface)."""
    return secure_config.load()

def save_config():
    """Save configuration (backward compatible interface)."""
    return secure_config.save()