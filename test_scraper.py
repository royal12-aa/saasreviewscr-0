#!/usr/bin/env python3
"""
Unit tests for the review scraper
Run with: pytest tests/test_scraper.py -v
"""

import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.scraper import ReviewScraper, Review, Source


class TestReviewScraper:
    """Test cases for ReviewScraper"""
    
    def setup_method(self):
        """Setup before each test"""
        self.scraper = ReviewScraper(delay=0)  # No delay for tests
    
    def test_validate_inputs_valid(self):
        """Test valid inputs"""
        assert self.scraper.validate_inputs("Slack", "2023-01-01", "2023-12-31", "g2") == True
    
    def test_validate_inputs_invalid_date(self):
        """Test invalid date format"""
        assert self.scraper.validate_inputs("Slack", "2023-13-01", "2023-12-31", "g2") == False
    
    def test_validate_inputs_date_range(self):
        """Test invalid date range"""
        assert self.scraper.validate_inputs("Slack", "2023-12-31", "2023-01-01", "g2") == False
    
    def test_validate_inputs_invalid_source(self):
        """Test invalid source"""
        assert self.scraper.validate_inputs("Slack", "2023-01-01", "2023-12-31", "invalid") == False
    
    def test_parse_date_various_formats(self):
        """Test date parsing with various formats"""
        test_cases = [
            ("2023-06-15", "2023-06-15"),
            ("15/06/2023", "2023-06-15"),
            ("June 15, 2023", "2023-06-15"),
            ("15 June 2023", "2023-06-15"),
            ("", ""),
        ]
        
        for input_date, expected in test_cases:
            result = self.scraper.parse_date(input_date)
            assert result == expected
    
    def test_is_date_in_range(self):
        """Test date range checking"""
        assert self.scraper._is_date_in_range("2023-06-15", "2023-01-01", "2023-12-31") == True
        assert self.scraper._is_date_in_range("2022-06-15", "2023-01-01", "2023-12-31") == False
        assert self.scraper._is_date_in_range("", "2023-01-01", "2023-12-31") == True  # Empty date included
    
    def test_extract_rating(self):
        """Test rating extraction"""
        from bs4 import BeautifulSoup
        
        # Test with text
        html_text = '<div>4.5 out of 5 stars</div>'
        soup = BeautifulSoup(html_text, 'html.parser')
        rating = self.scraper.extract_rating(soup.div)
        assert rating == 4.5
        
        # Test with aria-label
        html_text = '<div aria-label="4.2 stars out of 5"></div>'
        soup = BeautifulSoup(html_text, 'html.parser')
        rating = self.scraper.extract_rating(soup.div)
        assert rating == 4.2
    
    def test_review_dataclass(self):
        """Test Review dataclass"""
        review = Review(
            title="Great product",
            description="Very useful",
            date="2023-06-15",
            reviewer_name="John Doe",
            rating=4.5,
            source="g2"
        )
        
        assert review.title == "Great product"
        assert review.rating == 4.5
        assert review.date == "2023-06-15"
        
        # Test to_dict
        review_dict = review.to_dict()
        assert review_dict["title"] == "Great product"
        assert review_dict["rating"] == 4.5
        assert "source" in review_dict
    
    def test_scraper_initialization(self):
        """Test scraper initialization"""
        scraper = ReviewScraper(user_agent="TestAgent", delay=2.0)
        assert scraper.delay == 2.0
        assert "TestAgent" in scraper.session.headers["User-Agent"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])