"""
Lexicon Manager - Manage sentiment words and emojis
"""


class LexiconManager:
    """Manage sentiment lexicon and emoji mappings"""
    
    def __init__(self):
        self.positive_words = {
            'good': 1.0, 'great': 1.5, 'excellent': 1.5, 'amazing': 1.5,
            'awesome': 1.5, 'wonderful': 1.5, 'fantastic': 1.5,
            'fire': 1.5, 'lit': 1.4, 'dope': 1.4, 'healthy': 1.2,
            'sick': 1.4,  # slang for cool/awesome (WSD will handle context)
            'slay': 1.5, 'bussin': 1.4, 'iconic': 1.3, 'slaps': 1.4,
            'love': 1.4, 'perfect': 1.5, 'beautiful': 1.3, 'brilliant': 1.4,
            'superb': 1.4, 'lovely': 1.3, 'nice': 1.0, 'best': 1.5,
            'incredible': 1.5, 'outstanding': 1.5, 'fantastic': 1.5,
            'wonderful': 1.5, 'marvelous': 1.5, 'magnificent': 1.5,
            'splendid': 1.4, 'terrific': 1.4, 'delightful': 1.4,
            'favorable': 1.2, 'positive': 1.2, 'appealing': 1.2, 
            'attractive': 1.2, 'charming': 1.2, 'pleasant': 1.2, 
            'delightful': 1.3, 'joyful': 1.3, 'happy': 1.2, 'glad': 1.2, 
            'pleased': 1.2, 'satisfied': 1.1, 'impressed': 1.3, 
            'inspired': 1.2, 'energetic': 1.1, 'vibrant': 1.1, 'lively': 1.1
        }
        
        self.negative_words = {
            # Basic negative
            'bad': -1.0, 'terrible': -1.5, 'awful': -1.5, 'horrible': -1.5,
            'disgusting': -1.5, 'hate': -1.4, 'worst': -1.5,
            'trash': -1.3, 'wack': -1.3, 'cringe': -1.3, 'mid': -1.0,
            'weak': -1.2, 'lame': -1.2, 'poor': -1.0, 'disappointing': -1.3, 
            'useless': -1.4, 'pathetic': -1.4, 'dreadful': -1.4, 'atrocious': -1.5,
            
            # Health/Medical
            'sick': -1.3,  # health issue (WSD will handle context)
            'illness': -1.3, 'ill': -1.3, 'fever': -1.2,
            'disease': -1.4, 'pain': -1.2, 'hurt': -1.2, 'ache': -1.1,
            'nausea': -1.3, 'headache': -1.2, 'tired': -1.0, 'exhausted': -1.2,
            'dizzy': -1.2, 'cold': -1.1, 'cough': -1.1, 'injured': -1.2,
            'broken': -1.1, 'bleeding': -1.3, 'wound': -1.2, 'suffer': -1.2,
            'unwell': -1.2, 'ailment': -1.2, 'infection': -1.3, 'virus': -1.2,
            
            # Emotion negative
            'annoying': -1.1, 'irritating': -1.1, 'frustrating': -1.1,
            'confusing': -1.0, 'boring': -1.1, 'tedious': -1.2,
            'unfavorable': -1.1, 'negative': -1.1, 'unfriendly': -1.1,
            'hostile': -1.3, 'harsh': -1.2, 'sad': -1.1, 'miserable': -1.4, 
            'unhappy': -1.2, 'depressed': -1.3, 'gloomy': -1.2, 'dismal': -1.3,
            
            # Worry/Fear
            'worried': -1.0, 'anxious': -1.0, 'nervous': -0.9,
            'afraid': -1.1, 'scared': -1.2, 'terrified': -1.4,
            
            # Anger
            'angry': -1.3, 'furious': -1.5, 'enraged': -1.5,
            'upset': -1.1, 'troubled': -1.0, 'disturbed': -1.2,
            'mad': -1.2, 'irritated': -1.1, 'livid': -1.4,
        }
        
        self.emoji_sentiments = {
            '🔥': 1.5, '❤️': 1.4, '😍': 1.5, '💯': 1.5, '✨': 1.3,
            '🎉': 1.3, '👍': 1.2, '😊': 1.2, '🙌': 1.3, '💪': 1.2,
            '😂': 1.2, '🤣': 1.2, '😆': 1.1, '🥳': 1.4, '😎': 1.2,
            '😭': -1.2, '😡': -1.3, '🤦': -1.1, '😤': -1.1, '💔': -1.3,
            '😞': -1.2, '😢': -1.2, '🙅': -1.1, '😠': -1.3,
            '🤬': -1.4, '💀': -1.0, '👎': -1.2, '🚫': -1.1
        }
    
    def get_sentiment_score(self, word):
        """Get sentiment score for a word"""
        word = word.lower()
        word = word.strip('.,!?;:\'"')
        
        if word in self.positive_words:
            return self.positive_words[word]
        elif word in self.negative_words:
            return self.negative_words[word]
        else:
            return 0.0
    
    def get_emoji_sentiments(self):
        """Get emoji sentiment mappings"""
        return self.emoji_sentiments
