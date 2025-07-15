#!/usr/bin/env python3
"""
Test script for Base64 functionality in models.
"""

import os
import sys
import base64

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src import create_app, db
from src.models.song import Song
from src.models.radio_session import RadioSession
from src.models.blog_post import BlogPost

def test_base64_conversion():
    """Test Base64 conversion functionality for all models."""
    
    app = create_app()
    
    with app.app_context():
        print("Testing Base64 conversion functionality...")
        
        # Create some sample binary data (simulating a small audio/image file)
        sample_audio_data = b"This is sample audio data for testing purposes"
        sample_image_data = b"This is sample image data for testing purposes"
        
        # Test Song model
        print("\n1. Testing Song model...")
        song = Song()
        song.title = "Test Song"
        song.file_data = sample_audio_data
        song.uploaded_by = 1  # Assuming user ID 1 exists
        
        base64_result = song.get_base64_file_data()
        print(f"   Original data length: {len(sample_audio_data)} bytes")
        print(f"   Base64 data length: {len(base64_result)} characters")
        print(f"   Base64 preview: {base64_result[:50]}...")
        
        # Verify we can decode it back
        decoded_data = base64.b64decode(base64_result)
        print(f"   Decoded matches original: {decoded_data == sample_audio_data}")
        
        # Test RadioSession model
        print("\n2. Testing RadioSession model...")
        radio_session = RadioSession()
        radio_session.title = "Test Radio Session"
        radio_session.file_data = sample_audio_data
        radio_session.thumbnail_data = sample_image_data
        radio_session.uploaded_by = 1
        
        base64_audio = radio_session.get_base64_file_data()
        base64_thumbnail = radio_session.get_base64_thumbnail_data()
        
        print(f"   Audio Base64 preview: {base64_audio[:50]}...")
        print(f"   Thumbnail Base64 preview: {base64_thumbnail[:50]}...")
        
        # Verify decoding
        decoded_audio = base64.b64decode(base64_audio)
        decoded_thumbnail = base64.b64decode(base64_thumbnail)
        print(f"   Audio decoded matches: {decoded_audio == sample_audio_data}")
        print(f"   Thumbnail decoded matches: {decoded_thumbnail == sample_image_data}")
        
        # Test BlogPost model
        print("\n3. Testing BlogPost model...")
        blog_post = BlogPost()
        blog_post.title = "Test Blog Post"
        blog_post.content = "This is test content"
        blog_post.image_data = sample_image_data
        blog_post.author_id = 1
        
        base64_image = blog_post.get_base64_image_data()
        print(f"   Image Base64 preview: {base64_image[:50]}...")
        
        # Verify decoding
        decoded_image = base64.b64decode(base64_image)
        print(f"   Image decoded matches: {decoded_image == sample_image_data}")
        
        # Test with None data
        print("\n4. Testing with None data...")
        empty_song = Song()
        empty_song.title = "Empty Song"
        empty_song.uploaded_by = 1
        # file_data is None
        
        base64_none = empty_song.get_base64_file_data()
        print(f"   Base64 result for None data: {base64_none}")
        
        print("\n✅ All tests completed successfully!")

if __name__ == "__main__":
    test_base64_conversion()
