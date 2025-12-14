"""
URL Text Extractor - Extract main text content from a webpage URL
Educational/demo use only. Always respect site terms/robots.txt.
"""

import requests
from bs4 import BeautifulSoup

class URLTextExtractor:
    """Extract main text from a webpage URL"""

    def __init__(self, timeout=8):
        self.timeout = timeout
        # Simple headers to look like a browser (still must respect terms)
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0 Safari/537.36"
            )
        }

    def fetch_html(self, url: str) -> str:
        """Download raw HTML for a URL"""
        try:
            resp = requests.get(url, headers=self.headers, timeout=self.timeout)
            if resp.status_code != 200:
                return ""
            return resp.text
        except Exception:
            return ""

    def extract_main_text(self, html: str) -> str:
        """Extract main article-like text from HTML (simple heuristic)"""
        if not html:
            return ""

        soup = BeautifulSoup(html, "html.parser")

        # Remove script/style/meta tags
        for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "form"]):
            tag.decompose()

        # Try common article/content containers first
        candidates = []

        selectors = [
            "article",
            "main",
            "div[id*=content]",
            "div[class*=content]",
            "div[id*=article]",
            "div[class*=article]",
            "div[id*=post]",
            "div[class*=post]",
        ]

        for sel in selectors:
            for el in soup.select(sel):
                text = el.get_text(separator="\n", strip=True)
                if text and len(text.split()) > 40:  # at least ~40 words
                    candidates.append(text)

        # Fallback: all <p> tags
        if not candidates:
            paragraphs = [p.get_text(separator=" ", strip=True) for p in soup.find_all("p")]
            paragraphs = [p for p in paragraphs if len(p.split()) > 5]
            text = "\n".join(paragraphs)
            return text.strip()

        # Pick the longest candidate (naive heuristic for "main content")
        candidates.sort(key=lambda t: len(t.split()), reverse=True)
        return candidates[0].strip()

    def extract_from_url(self, url: str) -> str:
        """Full pipeline: URL -> HTML -> main text"""
        html = self.fetch_html(url)
        if not html:
            return ""
        text = self.extract_main_text(html)
        return text
