"""
Sentiment Scoring Engine with WSD-aware scoring
"""


class SentimentScorer:
    """Sentiment Scoring Engine"""
    
    def __init__(self, lexicon_manager):
        self.lexicon = lexicon_manager
        self.intensifiers = {
            'very': 1.2, 'really': 1.2, 'extremely': 1.3,
            'super': 1.2, 'mega': 1.3, 'ultra': 1.4,
            'absolutely': 1.3, 'definitely': 1.2,
            'so': 1.1, 'rather': 1.1, 'quite': 1.1
        }
        self.negations = [
            'not', 'never', 'hardly', 'barely', 'scarcely',
            'no', "don't", "doesn't", "didn't", "won't"
        ]
        
        # WSD Sentiment overrides - based on sense
        self.wsd_overrides = {
            'sick': {
                'health': -1.3,      # I am sick = NEGATIVE
                'positive': 1.4       # Movie is sick = POSITIVE
            },
            'bad': {
                'negative': -1.0,     # bad thing = NEGATIVE
                'positive': 1.2       # bad in a good way = POSITIVE
            },
            'fire': {
                'danger': -1.2,       # fire danger = NEGATIVE
                'positive': 1.5       # fire beat = POSITIVE
            },
            'cool': {
                'temperature': -0.5,  # cool weather = slightly negative
                'positive': 1.2       # cool person = POSITIVE
            }
        }
    
    def score_tokens(self, tokens, senses):
        """Score sentiment of token sequence with WSD awareness"""
        total_score = 0
        word_count = 0
        
        for i, token in enumerate(tokens):
            word_lower = token.lower().strip('.,!?;:\'"')
            
            # Check for WSD sense FIRST (highest priority)
            word_score = 0
            wsd_applied = False
            
            if i in senses:
                sense_info = senses[i]
                sense = sense_info['sense']
                
                # Apply WSD override if available
                if word_lower in self.wsd_overrides:
                    overrides = self.wsd_overrides[word_lower]
                    if sense in overrides:
                        word_score = overrides[sense]
                        wsd_applied = True
            
            # If no WSD override, use lexicon
            if not wsd_applied:
                word_score = self.lexicon.get_sentiment_score(word_lower)
            
            # Skip if word has no sentiment
            if word_score == 0:
                continue
            
            # Check for negation in previous words (within 3 words)
            # BUT: Don't negate if WSD already handled it
            negation_flag = False
            if not wsd_applied:
                for j in range(max(0, i-3), i):
                    if tokens[j].lower() in self.negations:
                        negation_flag = True
                        break
                
                # Apply negation (flip sign)
                if negation_flag:
                    word_score = -word_score
            
            # Check for intensifier before this word
            intensifier = 1.0
            if i > 0:
                prev_word = tokens[i-1].lower().strip('.,!?;:\'"')
                if prev_word in self.intensifiers:
                    intensifier = self.intensifiers[prev_word]
            
            # Apply intensifier
            word_score *= intensifier
            
            total_score += word_score
            word_count += 1
        
        # Normalize
        if word_count > 0:
            return total_score / word_count
        return 0.0
