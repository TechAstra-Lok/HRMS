"""AI Chats and ML Models"""

import pickle
import json
from datetime import datetime

class ChurnPredictionModel:
    """Employee churn prediction model"""
    
    def __init__(self):
        self.model = None
        self.features = [
            'age', 'tenure', 'attendance_rate', 
            'performance_rating', 'overtime_hours'
        ]
    
    def predict(self, employee_data):
        """Predict churn probability for employee"""
        
        # Simulated prediction
        age = employee_data.get('age', 30)
        tenure = employee_data.get('tenure', 5)
        attendance = employee_data.get('attendance_rate', 95)
        performance = employee_data.get('performance_rating', 3.5)
        overtime = employee_data.get('overtime_hours', 10)
        
        # Simple scoring logic
        score = 0
        if age > 50:
            score += 0.1
        if tenure < 2:
            score += 0.2
        if attendance < 90:
            score += 0.15
        if performance < 3:
            score += 0.25
        if overtime > 20:
            score += 0.15
        
        churn_probability = min(score, 1.0)
        
        # Determine risk level
        if churn_probability < 0.3:
            risk_level = 'low'
        elif churn_probability < 0.7:
            risk_level = 'medium'
        else:
            risk_level = 'high'
        
        return {
            'churn_probability': round(churn_probability, 3),
            'risk_level': risk_level,
            'factors': self._get_risk_factors(employee_data),
            'recommendations': self._get_recommendations(risk_level)
        }
    
    def _get_risk_factors(self, employee_data):
        """Get contributing factors"""
        factors = []
        if employee_data.get('tenure', 0) < 2:
            factors.append('Low tenure')
        if employee_data.get('attendance_rate', 100) < 90:
            factors.append('Low attendance')
        if employee_data.get('performance_rating', 5) < 3:
            factors.append('Poor performance')
        if employee_data.get('overtime_hours', 0) > 20:
            factors.append('High overtime')
        return factors
    
    def _get_recommendations(self, risk_level):
        """Get retention recommendations"""
        if risk_level == 'high':
            return ['Schedule one-on-one meeting', 'Review compensation', 'Career development plan']
        elif risk_level == 'medium':
            return ['Quarterly check-in', 'Performance review', 'Training opportunities']
        else:
            return ['Continue regular monitoring', 'Career growth opportunities']


class NLPChatbot:
    """HR Assistant Chatbot"""
    
    def __init__(self):
        self.intents = {
            'attendance': ['check attendance', 'attendance report', 'when did i come', 'my attendance'],
            'leave': ['apply leave', 'leave status', 'cancel leave', 'my leaves'],
            'payroll': ['payslip', 'salary', 'pay date', 'my salary'],
            'employee': ['employee list', 'find employee', 'team members'],
            'policy': ['policy', 'rules', 'guidelines'],
            'general': ['hello', 'help', 'what can you do']
        }
    
    def process_message(self, message):
        """Process user message and return response"""
        
        message_lower = message.lower()
        intent = self._detect_intent(message_lower)
        
        response = self._generate_response(intent, message_lower)
        
        return {
            'response': response,
            'intent': intent,
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def _detect_intent(self, message):
        """Detect message intent"""
        for intent, keywords in self.intents.items():
            for keyword in keywords:
                if keyword in message:
                    return intent
        return 'general'
    
    def _generate_response(self, intent, message):
        """Generate response based on intent"""
        
        responses = {
            'attendance': 'I can help you check your attendance. What date would you like to check?',
            'leave': 'To apply for leave, please provide the dates and type of leave.',
            'payroll': 'Your latest payslip is available in the Payroll section.',
            'employee': 'You can search for employees in the Employee section.',
            'policy': 'Company policies are available in the Settings section.',
            'general': 'Hello! I\'m your HR Assistant. How can I help you today?'
        }
        
        return responses.get(intent, 'I didn\'t understand. Could you please rephrase?')


class ResumeParser:
    """Resume parsing and analysis"""
    
    def __init__(self):
        self.skills_db = {
            'technical': ['Python', 'Java', 'JavaScript', 'SQL', 'AWS', 'Docker', 'Kubernetes'],
            'business': ['Project Management', 'Team Leadership', 'Strategic Planning', 'Business Analysis']
        }
    
    def parse_resume(self, file_path):
        """Parse resume file and extract information"""
        
        # Simulated resume parsing
        return {
            'name': 'Extracted Name',
            'email': 'extracted@email.com',
            'phone': '+1234567890',
            'skills': ['Python', 'Project Management'],
            'experience_years': 5,
            'companies': ['Company 1', 'Company 2'],
            'education': ['Bachelor in CS', 'Master in Business'],
            'languages': ['English', 'Spanish'],
            'summary': 'Experienced professional with strong technical background',
            'completeness_score': 85,
            'recommendations': ['Add more specific skills', 'Quantify achievements']
        }
    
    def score_resume(self, resume_data):
        """Score resume for completeness"""
        
        score = 0
        checks = [
            (bool(resume_data.get('name')), 10),
            (bool(resume_data.get('email')), 10),
            (bool(resume_data.get('phone')), 5),
            (len(resume_data.get('skills', [])) > 3, 15),
            (resume_data.get('experience_years', 0) > 0, 15),
            (len(resume_data.get('companies', [])) > 0, 15),
            (len(resume_data.get('education', [])) > 0, 15),
            (bool(resume_data.get('summary')), 10)
        ]
        
        for check, points in checks:
            if check:
                score += points
        
        return min(score, 100)
