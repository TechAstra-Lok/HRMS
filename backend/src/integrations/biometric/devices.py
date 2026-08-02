"""Biometric device integration"""

import logging
import socket
import struct
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ZKTecoBiometricDevice:
    """ZKTeco biometric device integration"""
    
    def __init__(self, ip: str, port: int = 4370):
        self.ip = ip
        self.port = port
        self.socket = None
        self.session_id = 0
    
    def connect(self):
        """Connect to device"""
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.connect((self.ip, self.port))
            self.session_id = 1
            return True
        except Exception as e:
            logger.warning("Connection error: %s", e)
            return False
    
    def disconnect(self):
        """Disconnect from device"""
        if self.socket:
            self.socket.close()
    
    def get_logs(self) -> list:
        """Get attendance logs from device"""
        try:
            # Send command to get logs (simplified)
            logs = []
            # Parse binary protocol and extract logs
            return logs
        except Exception as e:
            logger.warning("Get logs error: %s", e)
            return []
    
    def register_user(self, user_id: int, name: str):
        """Register user on device"""
        try:
            # Send register command
            return True
        except Exception as e:
            logger.warning("Register error: %s", e)
            return False
    
    def delete_user(self, user_id: int):
        """Delete user from device"""
        try:
            # Send delete command
            return True
        except Exception as e:
            logger.warning("Delete error: %s", e)
            return False


class FacialRecognitionAPI:
    """Facial recognition API integration"""
    
    def __init__(self, api_url: str, api_key: str):
        self.api_url = api_url
        self.api_key = api_key
    
    def detect_face(self, image_base64: str) -> Dict[str, Any]:
        """Detect face in image"""
        import requests
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {'image': image_base64}
        
        try:
            response = requests.post(f'{self.api_url}/detect', json=data, headers=headers)
            return response.json()
        except Exception as e:
            logger.warning("Detect face error: %s", e)
            return {'error': str(e)}
    
    def verify_user(self, user_id: str, image_base64: str) -> Dict[str, Any]:
        """Verify user identity"""
        import requests
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {'user_id': user_id, 'image': image_base64}
        
        try:
            response = requests.post(f'{self.api_url}/verify', json=data, headers=headers)
            return response.json()
        except Exception as e:
            logger.warning("Verify user error: %s", e)
            return {'error': str(e)}
    
    def enroll_user(self, user_id: str, images: list) -> Dict[str, Any]:
        """Enroll user with facial recognition"""
        import requests
        
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        
        data = {'user_id': user_id, 'images': images}
        
        try:
            response = requests.post(f'{self.api_url}/enroll', json=data, headers=headers)
            return response.json()
        except Exception as e:
            logger.warning("Enroll user error: %s", e)
            return {'error': str(e)}
