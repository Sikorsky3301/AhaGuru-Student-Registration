"""
Encryption utility for encrypting and decrypting sensitive student data.
Uses Fernet symmetric encryption from the cryptography library.
"""
from cryptography.fernet import Fernet
from django.conf import settings
import base64
import os


def get_encryption_key():
    """
    Get or generate encryption key from Django settings.
    If not set, generates a new key (for development only).
    """
    if hasattr(settings, 'ENCRYPTION_KEY') and settings.ENCRYPTION_KEY:
        return settings.ENCRYPTION_KEY.encode()
    
    # For development: generate a key if not set
    # In production, this should be set in settings.py
    key = Fernet.generate_key()
    print(f"WARNING: Generated new encryption key. Add this to settings.py:")
    print(f"ENCRYPTION_KEY = {key.decode()}")
    return key


def encrypt_data(data):
    """
    Encrypt string data and return as bytes (for VARBINARY storage).
    
    Args:
        data: String to encrypt
        
    Returns:
        bytes: Encrypted data ready for VARBINARY storage
    """
    if not data:
        return b''
    
    key = get_encryption_key()
    fernet = Fernet(key)
    encrypted = fernet.encrypt(data.encode('utf-8'))
    return encrypted


def decrypt_data(encrypted_data):
    """
    Decrypt bytes data (from VARBINARY) and return as string.
    
    Args:
        encrypted_data: Encrypted bytes from database
        
    Returns:
        str: Decrypted string
    """
    if not encrypted_data:
        return ''
    
    try:
        key = get_encryption_key()
        fernet = Fernet(key)
        decrypted = fernet.decrypt(encrypted_data)
        return decrypted.decode('utf-8')
    except Exception as e:
        raise ValueError(f"Decryption failed: {str(e)}")

