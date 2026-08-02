"""Encryption and decryption utilities"""

import base64
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import os
from typing import Dict, Any

class EncryptionManager:
    """Manage encryption and decryption operations"""
    
    def __init__(self, key: str = None):
        if key is None:
            key = os.getenv('ENCRYPTION_KEY', 'default-encryption-key-change-in-production')
        self.key = self._derive_key(key)
        self.fernet = Fernet(self.key)
    
    def _derive_key(self, password: str) -> bytes:
        """Derive encryption key from password"""
        salt = b'hrms_salt_2024'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        return base64.urlsafe_b64encode(kdf.derive(password.encode()))
    
    def encrypt(self, data: str) -> str:
        """Encrypt data"""
        if not data:
            return ""
        return self.fernet.encrypt(data.encode()).decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Decrypt data"""
        if not encrypted_data:
            return ""
        try:
            return self.fernet.decrypt(encrypted_data.encode()).decode()
        except Exception:
            return ""
    
    def encrypt_dict(self, data: dict, exclude_keys: list = None) -> dict:
        """Encrypt dictionary values"""
        exclude_keys = exclude_keys or ['id', 'created_at', 'updated_at', 'is_deleted']
        return {
            k: self.encrypt(v) if isinstance(v, str) and k not in exclude_keys else v 
            for k, v in data.items()
        }
    
    def decrypt_dict(self, data: dict, exclude_keys: list = None) -> dict:
        """Decrypt dictionary values"""
        exclude_keys = exclude_keys or ['id', 'created_at', 'updated_at', 'is_deleted']
        return {
            k: self.decrypt(v) if isinstance(v, str) and k not in exclude_keys else v 
            for k, v in data.items()
        }


# Global instance
encryption_manager = EncryptionManager()
