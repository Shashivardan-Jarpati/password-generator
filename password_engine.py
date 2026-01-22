"""
Password Generator Engine Module
Handles password generation with various complexity levels and options
"""

import random
import string
import secrets
import json
import os
from typing import List, Dict, Tuple


class PasswordGenerator:
    """Core password generation engine with multiple complexity levels"""
    
    # Character sets
    LOWERCASE = string.ascii_lowercase
    UPPERCASE = string.ascii_uppercase
    DIGITS = string.digits
    SPECIAL = string.punctuation
    
    # Ambiguous characters that can be confused
    AMBIGUOUS = 'il1Lo0O'
    
    def __init__(self):
        self.history_file = "password_history.json"
        self.history = self.load_history()
    
    def generate_password(self, length: int = 12, use_uppercase: bool = True,
                         use_lowercase: bool = True, use_digits: bool = True,
                         use_special: bool = True, exclude_ambiguous: bool = False,
                         custom_chars: str = "") -> str:
        """
        Generate a password with specified criteria
        
        Args:
            length: Password length
            use_uppercase: Include uppercase letters
            use_lowercase: Include lowercase letters
            use_digits: Include numbers
            use_special: Include special characters
            exclude_ambiguous: Exclude ambiguous characters (il1Lo0O)
            custom_chars: Additional custom characters to include
        
        Returns:
            Generated password string
        """
        if length < 4:
            raise ValueError("Password length must be at least 4 characters")
        
        # Build character pool
        char_pool = ""
        required_chars = []
        
        if use_lowercase:
            chars = self.LOWERCASE
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS)
            char_pool += chars
            required_chars.append(secrets.choice(chars))
        
        if use_uppercase:
            chars = self.UPPERCASE
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS)
            char_pool += chars
            required_chars.append(secrets.choice(chars))
        
        if use_digits:
            chars = self.DIGITS
            if exclude_ambiguous:
                chars = ''.join(c for c in chars if c not in self.AMBIGUOUS)
            char_pool += chars
            required_chars.append(secrets.choice(chars))
        
        if use_special:
            char_pool += self.SPECIAL
            required_chars.append(secrets.choice(self.SPECIAL))
        
        if custom_chars:
            char_pool += custom_chars
        
        if not char_pool:
            raise ValueError("At least one character type must be selected")
        
        # Generate password
        password_chars = required_chars.copy()
        remaining_length = length - len(required_chars)
        
        for _ in range(remaining_length):
            password_chars.append(secrets.choice(char_pool))
        
        # Shuffle to avoid predictable patterns
        secrets.SystemRandom().shuffle(password_chars)
        
        password = ''.join(password_chars)
        return password
    
    def generate_easy_password(self, length: int = 12) -> str:
        """Generate an easy-to-type password (lowercase + digits only)"""
        return self.generate_password(
            length=length,
            use_uppercase=False,
            use_lowercase=True,
            use_digits=True,
            use_special=False,
            exclude_ambiguous=True
        )
    
    def generate_medium_password(self, length: int = 12) -> str:
        """Generate a medium-strength password (letters + digits)"""
        return self.generate_password(
            length=length,
            use_uppercase=True,
            use_lowercase=True,
            use_digits=True,
            use_special=False,
            exclude_ambiguous=False
        )
    
    def generate_strong_password(self, length: int = 16) -> str:
        """Generate a strong password (all character types)"""
        return self.generate_password(
            length=length,
            use_uppercase=True,
            use_lowercase=True,
            use_digits=True,
            use_special=True,
            exclude_ambiguous=False
        )
    
    def generate_pin(self, length: int = 4) -> str:
        """Generate a numeric PIN"""
        if length < 4:
            raise ValueError("PIN length must be at least 4 digits")
        return ''.join(secrets.choice(self.DIGITS) for _ in range(length))
    
    def generate_passphrase(self, num_words: int = 4, separator: str = '-') -> str:
        """Generate a memorable passphrase using common words"""
        # Common word list for passphrases
        words = [
            'apple', 'banana', 'cherry', 'dragon', 'elephant', 'forest', 'garden',
            'happy', 'island', 'jungle', 'kitten', 'lemon', 'mountain', 'ninja',
            'ocean', 'panda', 'queen', 'rabbit', 'sunset', 'tiger', 'umbrella',
            'valley', 'wizard', 'yellow', 'zebra', 'anchor', 'bridge', 'castle',
            'diamond', 'eagle', 'flame', 'galaxy', 'hammer', 'igloo', 'jasper',
            'knight', 'lantern', 'marble', 'nectar', 'oasis', 'puzzle', 'quartz',
            'rocket', 'shadow', 'thunder', 'universe', 'victory', 'wonder', 'xenon'
        ]
        
        selected_words = [secrets.choice(words) for _ in range(num_words)]
        # Capitalize first letter of each word for better security
        selected_words = [word.capitalize() for word in selected_words]
        # Add a random number at the end
        selected_words.append(str(secrets.randbelow(100)))
        
        return separator.join(selected_words)
    
    def generate_multiple(self, count: int, length: int = 12, **kwargs) -> List[str]:
        """Generate multiple passwords at once"""
        return [self.generate_password(length, **kwargs) for _ in range(count)]
    
    def check_strength(self, password: str) -> Dict:
        """
        Analyze password strength
        
        Returns:
            Dictionary with strength analysis
        """
        length = len(password)
        has_lowercase = any(c in self.LOWERCASE for c in password)
        has_uppercase = any(c in self.UPPERCASE for c in password)
        has_digits = any(c in self.DIGITS for c in password)
        has_special = any(c in self.SPECIAL for c in password)
        
        # Calculate strength score (0-100)
        score = 0
        
        # Length scoring
        if length >= 16:
            score += 30
        elif length >= 12:
            score += 20
        elif length >= 8:
            score += 10
        
        # Character variety scoring
        if has_lowercase:
            score += 10
        if has_uppercase:
            score += 15
        if has_digits:
            score += 15
        if has_special:
            score += 20
        
        # Bonus for using all types
        if has_lowercase and has_uppercase and has_digits and has_special:
            score += 10
        
        # Determine strength level
        if score >= 80:
            strength = "Very Strong"
            color = "green"
        elif score >= 60:
            strength = "Strong"
            color = "blue"
        elif score >= 40:
            strength = "Medium"
            color = "orange"
        elif score >= 20:
            strength = "Weak"
            color = "red"
        else:
            strength = "Very Weak"
            color = "darkred"
        
        return {
            'score': score,
            'strength': strength,
            'color': color,
            'length': length,
            'has_lowercase': has_lowercase,
            'has_uppercase': has_uppercase,
            'has_digits': has_digits,
            'has_special': has_special,
            'feedback': self._get_strength_feedback(score, length, has_lowercase, 
                                                    has_uppercase, has_digits, has_special)
        }
    
    def _get_strength_feedback(self, score: int, length: int, has_lower: bool,
                               has_upper: bool, has_digits: bool, has_special: bool) -> List[str]:
        """Generate feedback for password strength"""
        feedback = []
        
        if length < 12:
            feedback.append("Consider using at least 12 characters")
        if not has_lower:
            feedback.append("Add lowercase letters")
        if not has_upper:
            feedback.append("Add uppercase letters")
        if not has_digits:
            feedback.append("Add numbers")
        if not has_special:
            feedback.append("Add special characters for maximum security")
        
        if not feedback:
            feedback.append("Excellent! This is a strong password")
        
        return feedback
    
    def save_to_history(self, password: str, description: str = ""):
        """Save password to history"""
        entry = {
            'password': password,
            'description': description,
            'created_at': self._get_timestamp(),
            'strength': self.check_strength(password)['strength']
        }
        self.history.append(entry)
        self._save_history()
    
    def load_history(self) -> List[Dict]:
        """Load password history from file"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []
    
    def _save_history(self):
        """Save history to file"""
        try:
            with open(self.history_file, 'w') as f:
                json.dump(self.history, f, indent=2)
        except IOError:
            pass
    
    def clear_history(self):
        """Clear password history"""
        self.history = []
        if os.path.exists(self.history_file):
            os.remove(self.history_file)
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def copy_to_clipboard(text: str) -> bool:
        """
        Attempt to copy text to clipboard
        Returns True if successful, False otherwise
        """
        try:
            # Try using pyperclip if available
            import pyperclip
            pyperclip.copy(text)
            return True
        except ImportError:
            # pyperclip not available
            return False
