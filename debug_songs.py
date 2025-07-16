#!/usr/bin/env python3
"""
Debug script to check song audio data.
"""
import os
import sys
import base64

# Add the project root to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src import create_app, db
from src.models.song import Song

def debug_songs():
    """Debug song audio data."""
    app = create_app()
    
    with app.app_context():
        print("=== Song Debug Information ===")
        
        # Get all songs
        songs = Song.query.all()
        print(f"Total songs in database: {len(songs)}")
        
        if not songs:
            print("❌ No songs found in database")
            return
        
        for i, song in enumerate(songs, 1):
            print(f"\n--- Song {i}: {song.title} ---")
            print(f"ID: {song.id}")
            print(f"Artist: {song.artist}")
            print(f"Status: {song.status}")
            print(f"Is Published: {song.is_published}")
            print(f"Has file_data: {song.file_data is not None}")
            if song.file_data:
                print(f"File data size: {len(song.file_data)} bytes")
                
                # Check file format by looking at file header
                file_header = song.file_data[:16]
                print(f"File header (hex): {file_header.hex()}")
                print(f"File header (ascii): {file_header}")
                
                # Detect file format
                if file_header.startswith(b'ID3') or file_header[6:10] == b'ftyp':
                    print("🎵 Detected: MP4/M4A file")
                elif file_header.startswith(b'\xff\xfb') or file_header.startswith(b'\xff\xf3') or file_header.startswith(b'\xff\xf2'):
                    print("🎵 Detected: MP3 file")
                elif file_header.startswith(b'RIFF') and file_header[8:12] == b'WAVE':
                    print("🎵 Detected: WAV file")
                elif file_header.startswith(b'OggS'):
                    print("🎵 Detected: OGG file")
                else:
                    print(f"❓ Unknown format. Header: {file_header}")
                
                # Test Base64 encoding
                try:
                    b64_data = base64.b64encode(song.file_data).decode('utf-8')
                    print(f"✅ Base64 encoding successful: {len(b64_data)} chars")
                    print(f"Base64 preview: {b64_data[:50]}...")
                    
                    # Test creating data URI
                    data_uri_mp3 = f"data:audio/mpeg;base64,{b64_data}"
                    data_uri_mp4 = f"data:audio/mp4;base64,{b64_data}"
                    print(f"Data URI length (MP3): {len(data_uri_mp3)}")
                    print(f"Data URI length (MP4): {len(data_uri_mp4)}")
                    
                    # Save a small test file to verify
                    test_file = f"test_audio_{song.id}.bin"
                    with open(test_file, 'wb') as f:
                        f.write(song.file_data[:1024])  # First 1KB
                    print(f"✅ Saved test file: {test_file}")
                    
                except Exception as e:
                    print(f"❌ Base64 encoding failed: {e}")
                
            print(f"has_audio() method: {song.has_audio()}")
            print(f"get_base64_audio_data() returns: {song.get_base64_audio_data() is not None}")
            if song.get_base64_audio_data():
                print(f"Base64 data length: {len(song.get_base64_audio_data())} chars")
        
        # Check published songs specifically
        published_songs = Song.query.filter_by(is_published=True).all()
        print(f"\nPublished songs: {len(published_songs)}")
        
        for song in published_songs:
            print(f"Published song: {song.title} - Has audio: {song.has_audio()}")

if __name__ == '__main__':
    debug_songs()
