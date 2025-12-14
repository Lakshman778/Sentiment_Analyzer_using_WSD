"""
Unit Tests for Analyzer
"""
import pytest
import sys
from pathlib import Path


# Add Backend to path
backend_path = Path(__file__).parent.parent / 'Backend'
sys.path.insert(0, str(backend_path))


from core.analyzer import UniversalWSDAnalyzer


@pytest.fixture
def analyzer():
    return UniversalWSDAnalyzer()


def test_positive_sentiment(analyzer):
    """Test positive sentiment"""
    result = analyzer.analyze("This song is fire bro!")
    assert result.get('sentiment') == 'POSITIVE'
    assert result.get('success') == True


def test_negative_sentiment(analyzer):
    """Test negative sentiment"""
    result = analyzer.analyze("This is terrible!")
    assert result.get('sentiment') == 'NEGATIVE'
    assert result.get('success') == True


def test_neutral_sentiment(analyzer):
    """Test neutral sentiment"""
    result = analyzer.analyze("The weather is cloudy.")
    assert result.get('sentiment') == 'NEUTRAL'


def test_emoji_support(analyzer):
    """Test emoji processing"""
    result = analyzer.analyze("I love this 🔥❤️")
    assert result.get('success') == True


def test_negation_handling(analyzer):
    """Test negation - basic test"""
    result = analyzer.analyze("I hate this")
    assert result.get('sentiment') == 'NEGATIVE'
    assert result.get('success') == True


def test_product_mode(analyzer):
    """Test product review mode"""
    result = analyzer.analyze("Great quality! Fast shipping!", mode='product')
    assert result.get('mode') == 'product'
    assert 'aspects' in result
    assert result.get('success') == True


def test_social_mode(analyzer):
    """Test social media mode"""
    result = analyzer.analyze("Just got new phone! #blessed", mode='social')
    assert result.get('mode') == 'social'
    assert '#blessed' in result.get('hashtags', [])


def test_confidence_scoring(analyzer):
    """Test confidence"""
    result = analyzer.analyze("This is absolutely fantastic!")
    assert 0 <= result.get('confidence', 0) <= 100


def test_empty_text(analyzer):
    """Test empty text"""
    result = analyzer.analyze("")
    assert result.get('success') == False or result.get('error') is not None


def test_general_mode(analyzer):
    """Test general mode"""
    result = analyzer.analyze("This is amazing!", mode='general')
    assert result.get('success') == True
    assert 'sentiment' in result


def test_intensity_level(analyzer):
    """Test intensity"""
    result = analyzer.analyze("This is absolutely perfect!")
    assert result.get('intensity') in ['low', 'medium', 'high', 'extreme']


def test_word_breakdown(analyzer):
    """Test word breakdown"""
    result = analyzer.analyze("Good movie")
    assert 'word_breakdown' in result
    assert result.get('success') == True


def test_multiple_emojis(analyzer):
    """Test multiple emojis"""
    result = analyzer.analyze("Amazing! 🔥🎉❤️")
    assert result.get('success') == True


def test_long_text(analyzer):
    """Test long text"""
    long_text = "This is a great product! " * 10
    result = analyzer.analyze(long_text)
    assert result.get('success') == True
