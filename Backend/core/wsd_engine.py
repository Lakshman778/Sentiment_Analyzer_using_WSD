"""
Word Sense Disambiguation Engine
Context-aware word sense detection
"""
from typing import List, Dict


class WSDEngine:
    """Word Sense Disambiguation Engine"""

    def __init__(self, window_size: int = 5):
        self.window_size = window_size

        # Context keywords for each ambiguous word and sense
        self.context_clues = {
            'sick': {
                'health': [
                    'i', 'am', 'is', 'are', 'was', 'were',
                    'feel', 'feeling', 'felt',
                    'got', 'have', 'having', 'getting',
                    'ill', 'illness', 'fever', 'cold',
                    'doctor', 'hospital', 'medicine',
                    'pain', 'hurt', 'body', 'nurse',
                    'tired', 'weak'
                ],
                'positive': [
                    'movie', 'film', 'song', 'track', 'album',
                    'beat', 'game', 'skills', 'talent',
                    'dope', 'fire', 'awesome', 'amazing',
                    'performance', 'show', 'dance',
                    'bro', 'dude', 'guy', 'girl',
                    'lit', 'cool'
                ]
            },
            'bad': {
                'negative': [
                    'very', 'really', 'extremely', 'so',
                    'terrible', 'awful', 'horrible',
                    'not', 'never'
                ],
                'positive': [
                    'so', 'amazing', 'awesome', 'talented',
                    'skills', 'really', 'very'
                ]
            },
            'fire': {
                'positive': [
                    'track', 'song', 'beat', 'game', 'movie',
                    'dope', 'awesome', 'lit', 'sick',
                    'performance', 'show'
                ],
                'danger': [
                    'house', 'building', 'burn', 'burning',
                    'danger', 'warning', 'on', 'started',
                    'emergency', 'call', 'alarm', 'spread'
                ]
            },
            'cool': {
                'positive': [
                    'so', 'very', 'really', 'awesome',
                    'amazing', 'love', 'person', 'dude',
                    'guy', 'girl', 'movie', 'trick'
                ],
                'temperature': [
                    'cold', 'temperature', 'weather', 'hot',
                    'freezing', 'ice', 'chilly'
                ]
            }
        }

        self.sense_inventory = self._load_sense_inventory()

    def disambiguate(self, tokens: List[str]) -> Dict[int, Dict]:
        """Disambiguate word senses in context for a token list."""
        senses: Dict[int, Dict] = {}

        for i, token in enumerate(tokens):
            # Context window
            context_start = max(0, i - self.window_size)
            context_end = min(len(tokens), i + self.window_size + 1)
            context = tokens[context_start:context_end]
            context_lower = [t.lower().strip('.,!?;:\'"') for t in context]

            token_lower = token.lower().strip('.,!?;:\'"')
            possible_senses = self.sense_inventory.get(token_lower, [token_lower])

            if len(possible_senses) == 1:
                senses[i] = {
                    'word': token,
                    'sense': possible_senses[0],
                    'confidence': 1.0,
                    'context': context
                }
            else:
                best_sense = self._select_sense_by_context(
                    token_lower,
                    context_lower,
                    possible_senses
                )
                confidence = self._calculate_sense_confidence(
                    best_sense,
                    context_lower,
                    token_lower
                )

                senses[i] = {
                    'word': token,
                    'sense': best_sense,
                    'confidence': confidence,
                    'context': context
                }

        return senses

    def _select_sense_by_context(
        self,
        word: str,
        context: List[str],
        possible_senses: List[str]
    ) -> str:
        """Select best sense using context clues."""
        if word in self.context_clues:
            clues = self.context_clues[word]

            # Initialise scores only for real possible senses
            sense_scores = {sense: 0 for sense in possible_senses}

            # Accumulate matches for each sense
            for sense_type, sense_keywords in clues.items():
                score = sum(1 for c in context if c in sense_keywords)
                if sense_type in sense_scores:
                    sense_scores[sense_type] += score

            # If any sense has > 0 score, choose best
            if max(sense_scores.values()) > 0:
                return max(sense_scores, key=sense_scores.get)

            # No explicit clue match: prefer 'positive' if available
            if 'positive' in possible_senses:
                return 'positive'

        # Fallback: first sense in inventory
        return possible_senses[0]

    def _calculate_sense_confidence(
        self,
        sense: str,
        context: List[str],
        word: str
    ) -> float:
        """Calculate confidence in sense selection."""
        if not context:
            return 0.6

        match_count = len([c for c in context if c == sense or c.startswith(sense)])

        if word in self.context_clues:
            sense_keywords = self.context_clues[word].get(sense, [])
            keyword_matches = sum(1 for c in context if c in sense_keywords)
            match_count += keyword_matches

        base_confidence = min(1.0, max(0.55, match_count / max(len(context), 1)))

        return round(base_confidence, 2)

    def _load_sense_inventory(self) -> Dict[str, List[str]]:
        """Load sense inventory - words with multiple meanings."""
        return {
            'sick': ['health', 'positive'],       # health issue OR cool/awesome
            'bad': ['negative', 'positive'],      # bad thing OR cool thing
            'fire': ['danger', 'positive'],       # fire danger OR awesome
            'cool': ['temperature', 'positive'],  # cool temp OR awesome
            'hot': ['temperature', 'positive'],   # hot temperature OR attractive/popular
            'bank': ['financial', 'river'],       # bank account OR river bank
            'book': ['novel', 'reserve'],         # book to read OR book a table
        }


"""
Sentiment Scoring Engine with WSD-aware scoring
"""


class SentimentScorer:
    """Sentiment Scoring Engine"""

    def __init__(self, lexicon_manager):
        self.lexicon = lexicon_manager

        # Degree adverbs/intensifiers
        self.intensifiers = {
            'very': 1.2, 'really': 1.2, 'extremely': 1.3,
            'super': 1.2, 'mega': 1.3, 'ultra': 1.4,
            'absolutely': 1.3, 'definitely': 1.2,
            'so': 1.1, 'rather': 1.1, 'quite': 1.1
        }

        # Simple negation list
        self.negations = [
            'not', 'never', 'hardly', 'barely', 'scarcely',
            'no', "don't", "doesn't", "didn't", "won't"
        ]

        # WSD Sentiment overrides - based on sense label
        self.wsd_overrides = {
            'sick': {
                'health': -1.3,      # I am sick = NEGATIVE
                'positive': 1.4      # Movie is sick = POSITIVE
            },
            'bad': {
                'negative': -1.0,    # bad thing = NEGATIVE
                'positive': 1.2      # bad in a good way = POSITIVE
            },
            'fire': {
                'danger': -1.2,      # fire danger = NEGATIVE
                'positive': 1.5      # fire beat = POSITIVE
            },
            'cool': {
                'temperature': -0.5,  # cool weather = slightly negative
                'positive': 1.2       # cool person = POSITIVE
            }
        }

    def score_tokens(self, tokens, senses):
        """
        Score sentiment of token sequence with WSD awareness.

        tokens: list of raw tokens
        senses: dict from WSDEngine.disambiguate(tokens)
        """
        total_score = 0.0
        word_count = 0

        for i, token in enumerate(tokens):
            word_lower = token.lower().strip('.,!?;:\'"')

            # Start neutral
            word_score = 0.0
            wsd_applied = False

            # 1) Try WSD override first (highest priority)
            if i in senses:
                sense_info = senses[i]
                sense = sense_info.get('sense')

                if word_lower in self.wsd_overrides:
                    overrides = self.wsd_overrides[word_lower]
                    if sense in overrides:
                        word_score = overrides[sense]
                        wsd_applied = True

            # 2) If no WSD override, fall back to lexicon
            if not wsd_applied:
                word_score = self.lexicon.get_sentiment_score(word_lower)

            # 3) Skip if word has no sentiment
            if word_score == 0:
                continue

            # 4) Check for negation in previous words (within 3 words)
            #    BUT: Do not negate if WSD override already applied
            if not wsd_applied:
                negation_flag = False
                for j in range(max(0, i - 3), i):
                    prev = tokens[j].lower().strip('.,!?;:\'"')
                    if prev in self.negations:
                        negation_flag = True
                        break

                if negation_flag:
                    word_score = -word_score

            # 5) Check for intensifier directly before this word
            intensifier = 1.0
            if i > 0:
                prev_word = tokens[i - 1].lower().strip('.,!?;:\'"')
                if prev_word in self.intensifiers:
                    intensifier = self.intensifiers[prev_word]

            # Apply intensifier
            word_score *= intensifier

            total_score += word_score
            word_count += 1

        # Normalize score
        return total_score / word_count if word_count > 0 else 0.0
