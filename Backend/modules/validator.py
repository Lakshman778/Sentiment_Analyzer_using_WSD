"""
Input Validator
"""

class InputValidator:
    """Validate inputs"""
    
    @staticmethod
    def validate_text(text):
        """Validate text input"""
        if not text:
            return False
        if not isinstance(text, str):
            return False
        if len(text.strip()) == 0:
            return False
        return True
    
    @staticmethod
    def validate_texts(texts):
        """Validate texts array"""
        if not isinstance(texts, list):
            return False
        if len(texts) == 0:
            return False
        return all(InputValidator.validate_text(t) for t in texts)
