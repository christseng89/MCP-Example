#!/usr/bin/env python3
"""
Launch script for the Pinecone Query Interface

This script launches the Streamlit web interface for querying your Pinecone knowledge base.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Launch the Streamlit interface."""
    print("🚀 Launching N8N Course Q&A Interface...")
    print("=" * 60)
    
    # Check if we're in the right directory
    current_dir = Path(__file__).parent
    interface_file = current_dir / "query_interface.py"
    
    if not interface_file.exists():
        print("❌ query_interface.py not found!")
        print(f"   Expected at: {interface_file}")
        sys.exit(1)
    
    # Check environment
    env_file = current_dir / ".env"
    if not env_file.exists():
        print("⚠️  No .env file found!")
        print("   Please create .env with your API keys:")
        print("   OPENAI_API_KEY=your-openai-key")
        print("   PINECONE_API_KEY=your-pinecone-key")
        print()
    else:
        print("✅ Found .env file")
    
    # Launch Streamlit
    try:
        print("🌐 Starting Streamlit server...")
        print("   The interface will open in your web browser")
        print("   Press Ctrl+C to stop the server")
        print()
        
        # Run streamlit with UV
        cmd = ["uv", "run", "streamlit", "run", str(interface_file), "--server.headless=false"]
        
        subprocess.run(cmd, cwd=current_dir)
        
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error running Streamlit: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
