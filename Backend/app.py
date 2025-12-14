"""
Flask REST API for Sentiment Analyzer
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
from core.analyzer import UniversalWSDAnalyzer
from modules.validator import InputValidator
from modules.url_extractor import URLTextExtractor
import logging
from datetime import datetime

app = Flask(__name__)
CORS(app)

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize analyzer
analyzer = UniversalWSDAnalyzer()
validator = InputValidator()
url_extractor = URLTextExtractor()

# ============= ROOT ENDPOINT =============

@app.route('/', methods=['GET'])
def root():
    """Root endpoint - API info"""
    return jsonify({
        'message': 'Universal WSD Sentiment Analyzer API',
        'version': '2.0',
        'status': 'running',
        'endpoints': {
            'analyze': 'POST /api/analyze',
            'analyze_product': 'POST /api/analyze-product',
            'analyze_social': 'POST /api/analyze-social',
            'analyze_url': 'POST /api/analyze-url',
            'batch': 'POST /api/analyze-batch',
            'health': 'GET /api/health',
            'version': 'GET /api/version'
        }
    }), 200

# ============= ANALYSIS ENDPOINTS =============

@app.route('/api/analyze', methods=['POST'])
def analyze_general():
    """General sentiment analysis"""
    try:
        data = request.json or {}
        text = (data.get('text') or '').strip()

        if not validator.validate_text(text):
            return jsonify({'error': 'Invalid text', 'success': False}), 400

        result = analyzer.analyze(text, mode='general')
        logger.info(f"Analyzed: {text[:30]}...")

        return jsonify({
            'success': result.get('success', True),
            'data': result,
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/analyze-product', methods=['POST'])
def analyze_product():
    """Product review analysis"""
    try:
        data = request.json or {}
        text = (data.get('text') or '').strip()

        if not validator.validate_text(text):
            return jsonify({'error': 'Invalid text', 'success': False}), 400

        result = analyzer.analyze(text, mode='product')
        logger.info(f"Product analysis: {text[:30]}...")

        return jsonify({
            'success': result.get('success', True),
            'data': result,
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/analyze-social', methods=['POST'])
def analyze_social():
    """Social media analysis"""
    try:
        data = request.json or {}
        text = (data.get('text') or '').strip()

        if not validator.validate_text(text):
            return jsonify({'error': 'Invalid text', 'success': False}), 400

        result = analyzer.analyze(text, mode='social')
        logger.info(f"Social analysis: {text[:30]}...")

        return jsonify({
            'success': result.get('success', True),
            'data': result,
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/analyze-batch', methods=['POST'])
def analyze_batch():
    """Batch analysis"""
    try:
        data = request.json or {}
        texts = data.get('texts', [])

        if not validator.validate_texts(texts):
            return jsonify({'error': 'Invalid texts', 'success': False}), 400

        results = []
        for text in texts:
            result = analyzer.analyze(text, mode='general')
            results.append(result)

        positive = len([r for r in results if r.get('sentiment') == 'POSITIVE'])
        negative = len([r for r in results if r.get('sentiment') == 'NEGATIVE'])
        neutral = len([r for r in results if r.get('sentiment') == 'NEUTRAL'])
        avg_confidence = sum(r.get('confidence', 0) for r in results) / len(results)

        logger.info(f"Batch: {len(results)} texts")

        return jsonify({
            'success': True,
            'total': len(results),
            'results': results,
            'summary': {
                'positive': positive,
                'negative': negative,
                'neutral': neutral,
                'average_confidence': round(avg_confidence, 2)
            },
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"Error: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500


@app.route('/api/analyze-url', methods=['POST'])
def analyze_url():
    """
    NEW: URL-based analysis.
    1) Fetch page HTML
    2) Extract main text
    3) Run same analyzer as text mode
    """
    try:
        data = request.json or {}
        url = (data.get('url') or '').strip()

        if not url:
            return jsonify({'error': 'No URL provided', 'success': False}), 400

        page_text = url_extractor.extract_from_url(url)

        if not page_text or len(page_text.split()) < 20:
            return jsonify({
                'error': 'Could not extract enough text from the URL for analysis.',
                'success': False
            }), 400

        result = analyzer.analyze(page_text, mode='general')
        logger.info(f"URL analysis: {url} -> {page_text[:30]}...")

        result['source_url'] = url
        result['snippet'] = " ".join(page_text.split()[:60]) + "..."

        return jsonify({
            'success': result.get('success', True),
            'data': result,
            'timestamp': datetime.now().isoformat()
        }), 200

    except Exception as e:
        logger.error(f"URL analysis error: {str(e)}")
        return jsonify({'error': str(e), 'success': False}), 500

# ============= HEALTH ENDPOINTS =============

@app.route('/api/health', methods=['GET'])
def health():
    """Health check"""
    return jsonify({
        'status': 'healthy',
        'version': '2.0',
        'timestamp': datetime.now().isoformat()
    }), 200


@app.route('/api/version', methods=['GET'])
def version():
    """API version"""
    return jsonify({
        'version': '2.0',
        'name': 'Universal WSD Sentiment Analyzer',
        'features': [
            'WSD-based sentiment',
            'Product review analysis',
            'Social media analysis',
            'Batch processing',
            'Modern slang support',
            'Emoji processing',
            'URL-based article analysis'
        ]
    }), 200

# ============= ERROR HANDLERS =============

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found', 'success': False}), 404


@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal error: {str(error)}")
    return jsonify({'error': 'Internal server error', 'success': False}), 500

# ============= MAIN =============

if __name__ == '__main__':
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   Universal WSD Sentiment Analyzer v2.0                   ║
    ║   Starting Flask API Server                               ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    print("Available endpoints:")
    print("  GET  /")
    print("  POST /api/analyze")
    print("  POST /api/analyze-product")
    print("  POST /api/analyze-social")
    print("  POST /api/analyze-batch")
    print("  POST /api/analyze-url")
    print("  GET  /api/health")
    print("  GET  /api/version")
    print("\nServer running at http://localhost:5000")

    app.run(debug=True, host='0.0.0.0', port=5000)
