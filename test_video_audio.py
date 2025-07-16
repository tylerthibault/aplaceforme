#!/usr/bin/env python3
"""
Test script to verify video audio detection functionality.
"""

import os
import sys

# Add the project root to the Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src import create_app, db
from src.models.god_story import GodStory
from src.controllers.main import check_video_has_audio

def test_video_audio_detection():
    """Test the video audio detection function."""
    app = create_app()
    
    with app.app_context():
        print("Testing video audio detection...")
        
        # Get the first video story
        story = GodStory.query.filter(GodStory.video_data.isnot(None)).first()
        
        if story:
            print(f"\nTesting video from story: '{story.title}'")
            print(f"Video data size: {len(story.video_data)} bytes")
            
            has_audio = check_video_has_audio(story.video_data)
            print(f"Audio detected: {'✓ Yes' if has_audio else '✗ No'}")
            
            if not has_audio:
                print("\n🔍 Analysis: This video file does not contain audio tracks.")
                print("   This explains why you can see video but can't hear audio.")
                print("\n💡 Solutions:")
                print("   1. Upload a new video file that includes audio")
                print("   2. Record the video again with audio enabled")
                print("   3. Use video editing software to add audio to the existing video")
                
        else:
            print("No video files found in the database.")
            
        print("\n✅ Test completed!")

if __name__ == "__main__":
    test_video_audio_detection()
