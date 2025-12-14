"""
Main Sentiment Analyzer with WSD Support
"""
from .wsd_engine import WSDEngine
from .sentiment_scorer import SentimentScorer
from modules.lexicon_manager import LexiconManager
from nltk.tokenize import word_tokenize
import json


class UniversalWSDAnalyzer:
    """Main analyzer combining WSD and Sentiment Analysis"""
    
    def __init__(self):
        self.lexicon = LexiconManager()
        self.wsd = WSDEngine()
        self.scorer = SentimentScorer(self.lexicon)
        self.version = "2.0"
    
    def analyze(self, text, mode='general'):
        """Main analysis method"""
        if not text or len(text.strip()) == 0:
            return {'error': 'Empty text', 'success': False}
        
        try:
            if mode == 'general':
                return self._analyze_general(text)
            elif mode == 'product':
                return self._analyze_product(text)
            elif mode == 'social':
                return self._analyze_social(text)
            else:
                return {'error': f'Unknown mode: {mode}', 'success': False}
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def _analyze_general(self, text):
        """General sentiment analysis"""
        try:
            # DO NOT lowercase here; WSD and scorer already handle case
            tokens = word_tokenize(text)
            senses = self.wsd.disambiguate(tokens)
            score = self.scorer.score_tokens(tokens, senses)
            confidence = self._calculate_confidence(score, senses)
            
            return {
                'success': True,
                'text': text,
                'score': round(score, 2),
                'sentiment': self._get_label(score),
                'confidence': round(confidence, 2),
                'intensity': self._get_intensity(score),
                'wsd_analysis': senses,
                'word_breakdown': self._breakdown_words(tokens)
            }
        except Exception as e:
            return {'error': str(e), 'success': False}
    
    def _analyze_product(self, text):
        """Product review analysis"""
        result = self._analyze_general(text)
        if not result.get('success', False):
            return result
        
        aspects = self._extract_aspects(text)
        recommendation = self._get_recommendation(result['score'])
        
        return {
            **result,
            'mode': 'product',
            'aspects': aspects,
            'recommend': recommendation
        }
    
    def _analyze_social(self, text):
        """Social media analysis"""
        result = self._analyze_general(text)
        if not result.get('success', False):
            return result
        
        hashtags = self._extract_hashtags(text)
        engagement = self._calculate_engagement(result, hashtags, text)
        emojis = self._analyze_emojis(text)
        
        return {
            **result,
            'mode': 'social',
            'hashtags': hashtags,
            'engagement_score': engagement,
            'emoji_analysis': emojis
        }
    
    def _get_label(self, score):
        """Get sentiment label from score"""
        if score > 1.0:
            return 'POSITIVE'
        elif score < -1.0:
            return 'NEGATIVE'
        else:
            return 'NEUTRAL'
    
    def _get_intensity(self, score):
        """Get intensity level"""
        abs_score = abs(score)
        if abs_score < 0.5:
            return 'low'
        elif abs_score < 1.5:
            return 'medium'
        elif abs_score < 3.0:
            return 'high'
        else:
            return 'extreme'
    
    def _calculate_confidence(self, score, senses):
        """Calculate confidence score"""
        base_confidence = min(100, max(0, abs(score) * 15))
        sense_confidence = sum(
            s.get('confidence', 0.5) for s in senses.values()
        ) / max(len(senses), 1)
        return (base_confidence + (sense_confidence * 100)) / 2
    
    def _breakdown_words(self, tokens):
        """Get word-by-word breakdown"""
        breakdown = {}
        for token in set(tokens):
            score = self.lexicon.get_sentiment_score(token)
            if score != 0:
                breakdown[token] = score
        return breakdown
    
    def _extract_aspects(self, text):
        """Extract product aspects"""
        aspects = {}
        product_keywords = [
            'quality', 'price', 'shipping', 'service', 
            'packaging', 'durability', 'design', 'value'
        ]
        for keyword in product_keywords:
            if keyword in text.lower():
                aspects[keyword] = 'detected'
        return aspects
    
    def _extract_hashtags(self, text):
        """Extract hashtags from text"""
        hashtags = []
        words = text.split()
        for word in words:
            if word.startswith('#'):
                hashtags.append(word)
        return hashtags
    
    def _calculate_engagement(self, result, hashtags, text):
        """Calculate social media engagement score"""
        engagement = 0
        engagement += len(hashtags) * 2
        engagement += text.count('!') * 1
        engagement += text.count('?') * 0.5
        engagement += abs(result['score']) * 5
        return min(10, round(engagement, 1))
    
    def _analyze_emojis(self, text):
        """Analyze emojis in text"""
        emoji_sentiments = self.lexicon.get_emoji_sentiments()
        emojis_found = {}
        for emoji, sentiment in emoji_sentiments.items():
            if emoji in text:
                emojis_found[emoji] = sentiment
        return emojis_found
    
    def _get_recommendation(self, score):
        """Get recommendation based on score"""
        return score > 0.5
