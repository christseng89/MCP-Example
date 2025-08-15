#!/usr/bin/env python3
"""
Folder Embedding Script for Pinecone

This script reads files from a local folder, processes them, creates embeddings using OpenAI,
and uploads them to a specified Pinecone index.
"""

import os
import sys
import json
import hashlib
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

# Core libraries
from dotenv import load_dotenv
import tiktoken

# OpenAI and Pinecone
from openai import OpenAI
from pinecone import Pinecone

# File processing libraries
import pypdf
from docx import Document
import re

def load_environment():
    """Load environment variables from .env file if it exists."""
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print("✅ Loaded environment variables from .env file")
    else:
        print("ℹ️  No .env file found, using system environment variables")

def initialize_clients() -> Tuple[Optional[OpenAI], Optional[Pinecone]]:
    """
    Initialize OpenAI and Pinecone clients.
    
    Returns:
        Tuple[OpenAI, Pinecone]: Initialized clients or None if failed
    """
    try:
        # Get API keys
        openai_api_key = os.getenv('OPENAI_API_KEY')
        pinecone_api_key = os.getenv('PINECONE_API_KEY')
        
        if not openai_api_key:
            print("❌ Error: OPENAI_API_KEY not found!")
            print("Please set OPENAI_API_KEY in your environment or .env file")
            return None, None
            
        if not pinecone_api_key:
            print("❌ Error: PINECONE_API_KEY not found!")
            print("Please set PINECONE_API_KEY in your environment or .env file")
            return None, None
        
        print("🔄 Initializing OpenAI client...")
        openai_client = OpenAI(api_key=openai_api_key)
        
        print("🔄 Initializing Pinecone client...")
        pinecone_client = Pinecone(api_key=pinecone_api_key)
        
        return openai_client, pinecone_client
        
    except Exception as e:
        print(f"❌ Error initializing clients: {str(e)}")
        return None, None

def count_tokens(text: str, model: str = "text-embedding-3-small") -> int:
    """
    Count tokens in text for the given model.
    
    Args:
        text (str): Text to count tokens for
        model (str): Model name for tokenizer
    
    Returns:
        int: Number of tokens
    """
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except:
        # Fallback to rough estimation if tiktoken fails
        return len(text.split()) * 1.3  # Rough approximation

def chunk_text(text: str, max_tokens: int = 8000, overlap: int = 200) -> List[str]:
    """
    Split text into chunks that fit within token limits.
    
    Args:
        text (str): Text to chunk
        max_tokens (int): Maximum tokens per chunk
        overlap (int): Number of tokens to overlap between chunks
    
    Returns:
        List[str]: List of text chunks
    """
    if count_tokens(text) <= max_tokens:
        return [text]
    
    # Split by paragraphs first
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ""
    
    for paragraph in paragraphs:
        test_chunk = current_chunk + ("\n\n" if current_chunk else "") + paragraph
        
        if count_tokens(test_chunk) <= max_tokens:
            current_chunk = test_chunk
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
                # Start new chunk with overlap
                words = current_chunk.split()
                overlap_text = " ".join(words[-overlap:]) if len(words) > overlap else current_chunk
                current_chunk = overlap_text + "\n\n" + paragraph
            else:
                # Paragraph itself is too long, split by sentences
                sentences = re.split(r'[.!?]+', paragraph)
                temp_chunk = ""
                for sentence in sentences:
                    if sentence.strip():
                        test_sentence = temp_chunk + sentence + ". "
                        if count_tokens(test_sentence) <= max_tokens:
                            temp_chunk = test_sentence
                        else:
                            if temp_chunk:
                                chunks.append(temp_chunk.strip())
                            temp_chunk = sentence + ". "
                current_chunk = temp_chunk
    
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    
    return chunks

def read_pdf_file(file_path: str) -> str:
    """Extract text from PDF file."""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = pypdf.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        print(f"❌ Error reading PDF {file_path}: {str(e)}")
        return ""

def read_docx_file(file_path: str) -> str:
    """Extract text from Word document."""
    try:
        doc = Document(file_path)
        text = []
        for paragraph in doc.paragraphs:
            text.append(paragraph.text)
        return "\n".join(text)
    except Exception as e:
        print(f"❌ Error reading DOCX {file_path}: {str(e)}")
        return ""

def read_text_file(file_path: str) -> str:
    """Read text from various text file formats."""
    try:
        encodings = ['utf-8', 'utf-16', 'cp1252', 'iso-8859-1']
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as file:
                    return file.read()
            except UnicodeDecodeError:
                continue
        print(f"⚠️  Could not decode {file_path} with common encodings")
        return ""
    except Exception as e:
        print(f"❌ Error reading text file {file_path}: {str(e)}")
        return ""

def process_file(file_path: str) -> Optional[Dict]:
    """
    Process a single file and extract its content.
    
    Args:
        file_path (str): Path to the file
    
    Returns:
        Dict: File information and content, or None if processing failed
    """
    file_path = Path(file_path)
    
    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        return None
    
    # Get file info
    file_info = {
        'filename': file_path.name,
        'filepath': str(file_path),
        'size': file_path.stat().st_size,
        'modified': datetime.fromtimestamp(file_path.stat().st_mtime).isoformat(),
        'extension': file_path.suffix.lower(),
        'content': ""
    }
    
    print(f"📄 Processing: {file_info['filename']}")
    
    # Process based on file type
    if file_info['extension'] == '.pdf':
        file_info['content'] = read_pdf_file(str(file_path))
        file_info['type'] = 'pdf'
    elif file_info['extension'] in ['.docx', '.doc']:
        file_info['content'] = read_docx_file(str(file_path))
        file_info['type'] = 'word'
    elif file_info['extension'] in ['.txt', '.md', '.rtf']:
        file_info['content'] = read_text_file(str(file_path))
        file_info['type'] = 'text'
    else:
        print(f"⚠️  Unsupported file type: {file_info['extension']}")
        return None
    
    if not file_info['content'].strip():
        print(f"⚠️  No content extracted from {file_info['filename']}")
        return None
    
    # Add content statistics
    file_info['word_count'] = len(file_info['content'].split())
    file_info['char_count'] = len(file_info['content'])
    file_info['token_count'] = count_tokens(file_info['content'])
    
    print(f"   📊 Extracted: {file_info['word_count']} words, {file_info['token_count']} tokens")
    
    return file_info

def create_embedding(client: OpenAI, text: str, model: str = "text-embedding-3-small") -> Optional[List[float]]:
    """
    Create embedding using OpenAI API.
    
    Args:
        client (OpenAI): OpenAI client
        text (str): Text to embed
        model (str): Embedding model to use
    
    Returns:
        List[float]: Embedding vector or None if failed
    """
    try:
        response = client.embeddings.create(
            model=model,
            input=text
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"❌ Error creating embedding: {str(e)}")
        return None

def generate_chunk_id(content: str, file_path: str, chunk_index: int) -> str:
    """Generate a unique ID for a content chunk."""
    # Create a hash of the content and metadata
    content_hash = hashlib.md5(content.encode()).hexdigest()[:12]
    filename = Path(file_path).stem
    return f"{filename}_{chunk_index}_{content_hash}"

def upload_to_pinecone(pc: Pinecone, index_name: str, vectors: List[Dict]) -> bool:
    """
    Upload vectors to Pinecone index.
    
    Args:
        pc (Pinecone): Pinecone client
        index_name (str): Name of the index
        vectors (List[Dict]): List of vectors with metadata
    
    Returns:
        bool: True if successful
    """
    try:
        print(f"🔄 Connecting to Pinecone index '{index_name}'...")
        index = pc.Index(index_name)
        
        # Upload in batches of 100
        batch_size = 100
        for i in range(0, len(vectors), batch_size):
            batch = vectors[i:i + batch_size]
            print(f"📤 Uploading batch {i//batch_size + 1}/{(len(vectors) + batch_size - 1)//batch_size} ({len(batch)} vectors)...")
            
            index.upsert(vectors=batch)
        
        print(f"✅ Successfully uploaded {len(vectors)} vectors to '{index_name}'")
        return True
        
    except Exception as e:
        print(f"❌ Error uploading to Pinecone: {str(e)}")
        return False

def process_folder(folder_path: str, openai_client: OpenAI, pc: Pinecone, index_name: str):
    """
    Process all files in a folder and upload embeddings to Pinecone.
    
    Args:
        folder_path (str): Path to the folder containing files
        openai_client (OpenAI): OpenAI client
        pc (Pinecone): Pinecone client
        index_name (str): Pinecone index name
    """
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"❌ Folder not found: {folder_path}")
        return
    
    print(f"📁 Processing folder: {folder_path}")
    
    # Find all supported files
    supported_extensions = ['.pdf', '.docx', '.doc', '.txt', '.md', '.rtf']
    files = []
    
    for ext in supported_extensions:
        files.extend(folder_path.glob(f'*{ext}'))
        files.extend(folder_path.glob(f'**/*{ext}'))  # Include subdirectories
    
    if not files:
        print(f"❌ No supported files found in {folder_path}")
        print(f"   Supported formats: {', '.join(supported_extensions)}")
        return
    
    print(f"📊 Found {len(files)} file(s) to process")
    
    all_vectors = []
    processed_files = 0
    total_chunks = 0
    
    for file_path in files:
        print(f"\n{'='*60}")
        
        # Process file
        file_info = process_file(file_path)
        if not file_info:
            continue
        
        # Chunk the content
        chunks = chunk_text(file_info['content'])
        print(f"📝 Split into {len(chunks)} chunk(s)")
        
        # Create embeddings for each chunk
        for chunk_index, chunk in enumerate(chunks):
            print(f"   🔄 Processing chunk {chunk_index + 1}/{len(chunks)}...")
            
            # Create embedding
            embedding = create_embedding(openai_client, chunk)
            if not embedding:
                print(f"   ❌ Failed to create embedding for chunk {chunk_index + 1}")
                continue
            
            # Create vector with metadata
            vector_id = generate_chunk_id(chunk, str(file_path), chunk_index)
            
            vector = {
                'id': vector_id,
                'values': embedding,
                'metadata': {
                    'filename': file_info['filename'],
                    'filepath': file_info['filepath'],
                    'file_type': file_info['type'],
                    'file_size': file_info['size'],
                    'file_modified': file_info['modified'],
                    'chunk_index': chunk_index,
                    'total_chunks': len(chunks),
                    'content': chunk[:1000],  # Store first 1000 chars for reference
                    'word_count': len(chunk.split()),
                    'char_count': len(chunk),
                    'processed_at': datetime.now().isoformat()
                }
            }
            
            all_vectors.append(vector)
            total_chunks += 1
            
            print(f"   ✅ Created embedding (dimension: {len(embedding)})")
        
        processed_files += 1
        print(f"✅ Completed {file_info['filename']} ({len(chunks)} chunks)")
    
    if not all_vectors:
        print("❌ No embeddings were created. Check the files and try again.")
        return
    
    print(f"\n{'='*60}")
    print(f"📊 Processing Summary:")
    print(f"   📁 Files processed: {processed_files}/{len(files)}")
    print(f"   📄 Total chunks: {total_chunks}")
    print(f"   🧠 Total embeddings: {len(all_vectors)}")
    
    # Upload to Pinecone
    print(f"\n🔄 Uploading embeddings to Pinecone index '{index_name}'...")
    success = upload_to_pinecone(pc, index_name, all_vectors)
    
    if success:
        print(f"\n🎉 Successfully processed and uploaded all files!")
        print(f"   📊 Index '{index_name}' now contains embeddings from {processed_files} files")
        print(f"   🔍 You can now search and query this knowledge base")
    else:
        print(f"\n❌ Failed to upload embeddings to Pinecone")

def main():
    """Main function."""
    print("🧠 Folder Embedding Script for Pinecone")
    print("=" * 60)
    
    # Configuration
    FOLDER_PATH = r"C:\Users\samfi\Downloads\BiWeekly-MeetingNotes"
    INDEX_NAME = "biweekly-meeting"
    
    print(f"📁 Target folder: {FOLDER_PATH}")
    print(f"🎯 Target index: {INDEX_NAME}")
    
    # Load environment
    load_environment()
    
    # Initialize clients
    openai_client, pc = initialize_clients()
    if not openai_client or not pc:
        sys.exit(1)
    
    # Verify index exists
    try:
        indexes = pc.list_indexes().names()
        if INDEX_NAME not in indexes:
            print(f"❌ Index '{INDEX_NAME}' not found!")
            print(f"Available indexes: {', '.join(indexes) if indexes else 'None'}")
            print(f"Please create the index first using create_index.py")
            sys.exit(1)
        else:
            print(f"✅ Found index '{INDEX_NAME}'")
    except Exception as e:
        print(f"❌ Error checking indexes: {str(e)}")
        sys.exit(1)
    
    # Confirm processing
    print(f"\n⚠️  This will process all supported files in:")
    print(f"   {FOLDER_PATH}")
    print(f"   And upload embeddings to index '{INDEX_NAME}'")
    
    confirmation = input(f"\nProceed? (y/N): ").strip().lower()
    if confirmation not in ['y', 'yes']:
        print("❌ Operation cancelled by user.")
        return
    
    # Process folder
    process_folder(FOLDER_PATH, openai_client, pc, INDEX_NAME)

if __name__ == "__main__":
    main()
