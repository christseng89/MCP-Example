#!/usr/bin/env python3
"""
Folder Embedding Script for Pinecone

- Fixes: Pinecone vector IDs must be ASCII -> slugify filename stems
- Uses recursive file discovery without duplicates
- Optional: send vectors to a specific namespace
"""

import os
import sys
import json
import hashlib
import re
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from datetime import datetime

from dotenv import load_dotenv
import tiktoken

# OpenAI and Pinecone
from openai import OpenAI
from pinecone import Pinecone

# Text splitting
from langchain_text_splitters import RecursiveCharacterTextSplitter

# File processing
import pypdf
from docx import Document

# Optional transliteration (nice-to-have)
try:
    from unidecode import unidecode  # pip install Unidecode
except Exception:
    unidecode = None


# =========================
# Config (edit if you like)
# =========================

load_dotenv()

FOLDER_PATH = os.getenv("PINECONE_FOLDER_PATH", r"C:\Users\samfi\Downloads\Tesla-N8N-Course")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "tesla-index")     # must exist already
NAMESPACE  = os.getenv("PINECONE_NAMESPACE", "tesla")     # ASCII only; comment out to use default

# OpenAI Embedding Configuration (matching the interface settings)
EMBED_MODEL = "text-embedding-3-small"
EMBED_DIMENSIONS = 1536  # Vector dimensions
EMBED_BATCH_SIZE = 128   # Batch size for processing
EMBED_TIMEOUT = 300000   # Timeout in milliseconds (300 seconds)

# Recursive Character Text Splitter Configuration (matching the interface settings)
CHUNK_SIZE = 1000        # Chunk size in characters
CHUNK_OVERLAP = 120      # Chunk overlap in characters

def load_environment():
    """Load environment variables from .env file if it exists."""
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        load_dotenv(env_file)
        print("✅ Loaded environment variables from .env file")
    else:
        print("ℹ️  No .env file found, using system environment variables")


def initialize_clients() -> Tuple[Optional[OpenAI], Optional[Pinecone]]:
    """Initialize OpenAI and Pinecone clients."""
    try:
        openai_api_key = os.getenv('OPENAI_API_KEY')
        pinecone_api_key = os.getenv('PINECONE_API_KEY')

        if not openai_api_key:
            print("❌ Error: OPENAI_API_KEY not found!")
            return None, None
        if not pinecone_api_key:
            print("❌ Error: PINECONE_API_KEY not found!")
            return None, None

        print("🔄 Initializing OpenAI client...")
        openai_client = OpenAI(api_key=openai_api_key)

        print("🔄 Initializing Pinecone client...")
        pinecone_client = Pinecone(api_key=pinecone_api_key)

        return openai_client, pinecone_client
    except Exception as e:
        print(f"❌ Error initializing clients: {e}")
        return None, None


def count_tokens(text: str, model: str = EMBED_MODEL) -> int:
    """Count tokens for the given model (rough fallback if needed)."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except Exception:
        return int(len(text.split()) * 1.3)


def chunk_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Split text using Recursive Character Text Splitter with configurable parameters."""
    try:
        # Create the recursive character text splitter with specified parameters
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,  # Use character count
            separators=[
                "\n\n",    # Double newline (paragraphs)
                "\n",      # Single newline (lines)
                " ",       # Space (words)
                ".",       # Period
                ",",       # Comma
                "\u200b",  # Zero-width space
                "\uff0c",  # Full-width comma
                "\u3001",  # Ideographic comma
                "\uff0e",  # Full-width period
                "\u3002",  # Ideographic period
                "",        # Last resort - split by character
            ],
            keep_separator=True,
        )
        
        # Split the text
        chunks = text_splitter.split_text(text)
        
        # Filter out empty chunks
        chunks = [chunk.strip() for chunk in chunks if chunk.strip()]
        
        return chunks
        
    except Exception as e:
        print(f"⚠️  Warning: Error with RecursiveCharacterTextSplitter: {e}")
        print("   Falling back to simple text splitting...")
        
        # Fallback: Simple splitting if RecursiveCharacterTextSplitter fails
        return simple_chunk_text(text, chunk_size, chunk_overlap)


def simple_chunk_text(text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP) -> List[str]:
    """Fallback simple text chunking method."""
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        # Calculate end position
        end = start + chunk_size
        
        if end >= len(text):
            # Last chunk
            chunks.append(text[start:])
            break
        
        # Try to end at a word boundary
        chunk = text[start:end]
        
        # Look for the last space before the end to avoid cutting words
        if end < len(text):
            last_space = chunk.rfind(' ')
            last_newline = chunk.rfind('\n')
            last_period = chunk.rfind('.')
            
            # Find the best breaking point
            break_point = max(last_space, last_newline, last_period)
            
            if break_point > chunk_size * 0.8:  # Only use if it's not too far back
                end = start + break_point + 1
                chunk = text[start:end]
        
        chunks.append(chunk.strip())
        
        # Move start position with overlap
        start = end - chunk_overlap
    
    return [chunk for chunk in chunks if chunk.strip()]


def read_pdf_file(file_path: str) -> str:
    """Extract text from PDF file."""
    try:
        with open(file_path, 'rb') as f:
            reader = pypdf.PdfReader(f)
            return "\n".join(page.extract_text() or "" for page in reader.pages).strip()
    except Exception as e:
        print(f"❌ Error reading PDF {file_path}: {e}")
        return ""


def read_docx_file(file_path: str) -> str:
    """Extract text from Word document."""
    try:
        doc = Document(file_path)
        return "\n".join(p.text for p in doc.paragraphs)
    except Exception as e:
        print(f"❌ Error reading DOCX {file_path}: {e}")
        return ""


def read_text_file(file_path: str) -> str:
    """Read text from various text file formats."""
    try:
        for enc in ['utf-8', 'utf-16', 'cp1252', 'iso-8859-1']:
            try:
                with open(file_path, 'r', encoding=enc) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
        print(f"⚠️  Could not decode {file_path} with common encodings")
        return ""
    except Exception as e:
        print(f"❌ Error reading text file {file_path}: {e}")
        return ""


def process_file(file_path: str) -> Optional[Dict]:
    """Process a single file and extract its content."""
    p = Path(file_path)
    if not p.exists():
        print(f"❌ File not found: {p}")
        return None

    info = {
        'filename': p.name,
        'filepath': str(p),
        'size': p.stat().st_size,
        'modified': datetime.fromtimestamp(p.stat().st_mtime).isoformat(),
        'extension': p.suffix.lower(),
        'content': "",
        'type': ""
    }
    print(f"📄 Processing: {info['filename']}")

    if info['extension'] == '.pdf':
        info['content'] = read_pdf_file(str(p))
        info['type'] = 'pdf'
    elif info['extension'] in ['.docx', '.doc']:
        info['content'] = read_docx_file(str(p))
        info['type'] = 'word'
    elif info['extension'] in ['.txt', '.md', '.rtf']:
        info['content'] = read_text_file(str(p))
        info['type'] = 'text'
    else:
        print(f"⚠️  Unsupported file type: {info['extension']}")
        return None

    if not info['content'].strip():
        print(f"⚠️  No content extracted from {info['filename']}")
        return None

    info['word_count'] = len(info['content'].split())
    info['char_count'] = len(info['content'])
    info['token_count'] = count_tokens(info['content'])
    print(f"   📊 Extracted: {info['word_count']} words, {info['token_count']} tokens")
    return info


def create_embedding(client: OpenAI, text: str, model: str = EMBED_MODEL) -> Optional[List[float]]:
    """Create embedding using OpenAI API with configured parameters."""
    try:
        # Create embedding with specified dimensions and timeout
        resp = client.embeddings.create(
            model=model,
            input=text,
            dimensions=EMBED_DIMENSIONS,
            # timeout=EMBED_TIMEOUT / 1000.0  # Convert milliseconds to seconds
        )
        return resp.data[0].embedding
    except Exception as e:
        print(f"❌ Error creating embedding: {e}")
        return None


def _ascii_slug(s: str, max_len: int = 64) -> str:
    """Transliterate & sanitize to ASCII for Pinecone IDs."""
    # transliterate if possible (turns '会议记录' -> 'Hui Yi Ji Lu')
    if unidecode:
        try:
            s = unidecode(s)
        except Exception:
            pass
    # keep only allowed characters
    s = re.sub(r'[^A-Za-z0-9._:-]+', '-', s)
    s = re.sub(r'-{2,}', '-', s).strip('-._:')
    return (s[:max_len] or 'file')


def generate_chunk_id(content: str, file_path: str, chunk_index: int) -> str:
    """Generate a Pinecone-safe ASCII ID for a content chunk."""
    content_hash = hashlib.md5(content.encode('utf-8')).hexdigest()[:12]
    stem = Path(file_path).stem
    safe_stem = _ascii_slug(stem)
    return f"{safe_stem}_{chunk_index}_{content_hash}"


def upload_to_pinecone(pc: Pinecone, index_name: str, vectors: List[Dict], namespace: Optional[str] = None) -> bool:
    """Upload vectors to Pinecone index."""
    try:
        print(f"🔄 Connecting to Pinecone index '{index_name}'...")
        index = pc.Index(index_name)

        # sanity: ensure IDs are ASCII
        for v in vectors[:3]:
            if not all(ord(c) < 128 for c in v['id']):
                raise ValueError(f"Non-ASCII ID detected: {v['id']}")

        # batch upload
        batch_size = 100
        total = len(vectors)
        for start in range(0, total, batch_size):
            batch = vectors[start:start + batch_size]
            print(f"📤 Uploading batch {start // batch_size + 1}/{(total + batch_size - 1) // batch_size} ({len(batch)} vectors)...")
            if namespace:
                index.upsert(vectors=batch, namespace=namespace)
            else:
                index.upsert(vectors=batch)

        print(f"✅ Successfully uploaded {total} vectors to '{index_name}'")
        return True

    except Exception as e:
        print(f"❌ Error uploading to Pinecone: {e}")
        return False


def create_embeddings_batch(client: OpenAI, texts: List[str], model: str = EMBED_MODEL) -> List[Optional[List[float]]]:
    """Create embeddings for multiple texts in batches for efficiency."""
    embeddings = []
    
    # Process texts in batches according to configured batch size
    for i in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = texts[i:i + EMBED_BATCH_SIZE]
        batch_size = len(batch)
        
        try:
            print(f"   🔄 Creating embeddings for batch of {batch_size} texts...")
            resp = client.embeddings.create(
                model=model,
                input=batch,
                dimensions=EMBED_DIMENSIONS,
                # timeout=EMBED_TIMEOUT / 1000.0  # Convert milliseconds to seconds
            )
            
            # Extract embeddings from response
            batch_embeddings = [data.embedding for data in resp.data]
            embeddings.extend(batch_embeddings)
            
        except Exception as e:
            print(f"   ❌ Error creating batch embeddings: {e}")
            # Add None for each failed embedding in the batch
            embeddings.extend([None] * batch_size)
    
    return embeddings


def process_folder(folder_path: str, openai_client: OpenAI, pc: Pinecone, index_name: str, namespace: Optional[str]):
    """Process all files in a folder and upload embeddings to Pinecone."""
    root = Path(folder_path)
    if not root.exists():
        print(f"❌ Folder not found: {root}")
        return

    print(f"📁 Processing folder: {root}")

    # Recursive, unique file list
    supported_ext = {'.pdf', '.docx', '.doc', '.txt', '.md', '.rtf'}
    files = sorted({
        p.resolve()
        for p in root.rglob('*')
        if p.is_file() and p.suffix.lower() in supported_ext
    })

    if not files:
        print(f"❌ No supported files found in {root}")
        print(f"   Supported: {', '.join(sorted(supported_ext))}")
        return

    print(f"📊 Found {len(files)} file(s) to process")

    all_vectors: List[Dict] = []
    processed_files = 0
    total_chunks = 0
    truncated_chunks = 0
    all_chunks_for_batch = []  # Store all chunks for batch processing
    all_metadata = []  # Store corresponding metadata

    for file_path in files:
        print("\n" + "=" * 60)
        info = process_file(str(file_path))
        if not info:
            continue

        chunks = chunk_text(info['content'])
        print(f"📝 Split into {len(chunks)} chunk(s)")

        # Prepare chunks and metadata for batch processing
        for chunk_idx, chunk in enumerate(chunks):
            vector_id = generate_chunk_id(chunk, str(file_path), chunk_idx)
            
            # Calculate available space for content (Pinecone has ~40KB metadata limit)
            max_content_size = 38000  # bytes
            full_content = chunk
            
            # Truncate content only if it exceeds metadata limit
            if len(full_content.encode('utf-8')) > max_content_size:
                truncated = full_content.encode('utf-8')[:max_content_size].decode('utf-8', errors='ignore')
                last_space = truncated.rfind(' ')
                if last_space > max_content_size * 0.8:
                    truncated = truncated[:last_space]
                stored_content = truncated + "... [TRUNCATED]"
                content_truncated = True
            else:
                stored_content = full_content
                content_truncated = False

            # Store chunk and metadata for batch processing
            all_chunks_for_batch.append(chunk)
            all_metadata.append({
                "vector_id": vector_id,
                "info": info,
                "chunk_idx": chunk_idx,
                "total_chunks": len(chunks),
                "stored_content": stored_content,
                "content_truncated": content_truncated,
                "chunk": chunk
            })
            
            total_chunks += 1
            if content_truncated:
                truncated_chunks += 1

        processed_files += 1
        print(f"✅ Prepared {info['filename']} ({len(chunks)} chunks for batch processing)")

    if not all_chunks_for_batch:
        print("❌ No chunks were prepared for embedding. Check the files and try again.")
        return

    print(f"\n📊 Batch Processing Summary:")
    print(f"   📁 Files prepared: {processed_files}/{len(files)}")
    print(f"   📄 Total chunks for embedding: {total_chunks}")
    print(f"   🧠 Embedding model: {EMBED_MODEL}")
    print(f"   📐 Dimensions: {EMBED_DIMENSIONS}")
    print(f"   📦 Batch size: {EMBED_BATCH_SIZE}")
    print(f"   ⏱️  Timeout: {EMBED_TIMEOUT}ms")
    if truncated_chunks > 0:
        print(f"   ⚠️  Chunks with truncated content: {truncated_chunks}/{total_chunks}")

    # Create embeddings in batches
    print(f"\n🔄 Creating embeddings for {len(all_chunks_for_batch)} chunks...")
    embeddings = create_embeddings_batch(openai_client, all_chunks_for_batch)

    # Create vectors with embeddings
    successful_embeddings = 0
    for i, (embedding, metadata) in enumerate(zip(embeddings, all_metadata)):
        if embedding is None:
            print(f"   ⚠️  Skipping chunk {i+1} due to embedding failure")
            continue

        vector = {
            "id": metadata["vector_id"],
            "values": embedding,
            "metadata": {
                "filename": metadata["info"]['filename'],
                "filepath": metadata["info"]['filepath'],
                "file_type": metadata["info"]['type'],
                "file_size": metadata["info"]['size'],
                "file_modified": metadata["info"]['modified'],
                "chunk_index": metadata["chunk_idx"],
                "total_chunks": metadata["total_chunks"],
                "content": metadata["stored_content"],
                "content_truncated": metadata["content_truncated"],
                "word_count": len(metadata["chunk"].split()),
                "char_count": len(metadata["chunk"]),
                "processed_at": datetime.now().isoformat()
            }
        }
        all_vectors.append(vector)
        successful_embeddings += 1

    print(f"✅ Successfully created {successful_embeddings}/{len(all_chunks_for_batch)} embeddings")

    if not all_vectors:
        print("❌ No embeddings were created. Check the files and try again.")
        return

    print("\n" + "=" * 60)
    print("📊 Final Processing Summary:")
    print(f"   📁 Files processed: {processed_files}/{len(files)}")
    print(f"   📄 Total chunks: {total_chunks}")
    print(f"   🧠 Successful embeddings: {len(all_vectors)}")
    print(f"   📐 Vector dimensions: {EMBED_DIMENSIONS}")
    if truncated_chunks > 0:
        print(f"   ⚠️  Chunks with truncated content: {truncated_chunks}/{total_chunks}")
        print(f"       (Content was too large for Pinecone metadata limits)")

    # quick peek at IDs to confirm ASCII
    print("🔎 Example IDs:", [v["id"] for v in all_vectors[:3]])

    print(f"\n🔄 Uploading embeddings to Pinecone index '{index_name}'...")
    ok = upload_to_pinecone(pc, index_name, all_vectors, namespace=namespace)
    if ok:
        print("\n🎉 Successfully processed and uploaded all files!")
        print(f"   📊 Index '{index_name}' now contains embeddings from {processed_files} files")
        print("   🔍 You can now search and query this knowledge base")
    else:
        print("\n❌ Failed to upload embeddings to Pinecone")


def main():
    print("🧠 Folder Embedding Script for Pinecone")
    print("=" * 60)
    
    # Load environment first
    load_environment()
    
    # Get configuration values with fallbacks
    final_folder_path = FOLDER_PATH
    final_index_name = INDEX_NAME 
    final_namespace = NAMESPACE 
    
    # Validate required configuration
    if not final_folder_path:
        print("❌ Error: No folder path specified!")
        print("   Set PINECONE_FOLDER_PATH environment variable")
        sys.exit(1)
    
    if not final_index_name:
        print("❌ Error: No index name specified!")
        print("   Set PINECONE_INDEX_NAME environment variable")
        sys.exit(1)
    
    # Display configuration
    print(f"📁 Target folder: {final_folder_path}")
    if FOLDER_PATH:
        print("   (📌 Using PINECONE_FOLDER_PATH environment variable)")
    else:
        print("   (⚠️  Using default path - set PINECONE_FOLDER_PATH to customize)")
    
    print(f"🎯 Target index: {final_index_name}")
    if INDEX_NAME:
        print("   (📌 Using PINECONE_INDEX_NAME environment variable)")
    else:
        print("   (⚠️  Using default index - set PINECONE_INDEX_NAME to customize)")
    
    if final_namespace:
        print(f"🧱 Namespace: {final_namespace}")
        if NAMESPACE:
            print("   (📌 Using PINECONE_NAMESPACE environment variable)")
        else:
            print("   (⚠️  Using default namespace - set PINECONE_NAMESPACE to customize)")
    else:
        print("🧱 Namespace: Default (no namespace)")
    
    print(f"🧠 Embedding configuration:")
    print(f"   Model: {EMBED_MODEL}")
    print(f"   Dimensions: {EMBED_DIMENSIONS}")
    print(f"   Batch Size: {EMBED_BATCH_SIZE}")
    print(f"   Timeout: {EMBED_TIMEOUT}ms")
    
    print(f"📝 Text Splitter configuration:")
    print(f"   Type: Recursive Character Text Splitter")
    print(f"   Chunk Size: {CHUNK_SIZE} characters")
    print(f"   Chunk Overlap: {CHUNK_OVERLAP} characters")
    print()

    openai_client, pc = initialize_clients()
    if not openai_client or not pc:
        sys.exit(1)

    # Verify index exists
    try:
        indexes = pc.list_indexes().names()
        if final_index_name not in indexes:
            print(f"❌ Index '{final_index_name}' not found!")
            print(f"Available indexes: {', '.join(indexes) if indexes else 'None'}")
            print("Please create the index first using create_index.py")
            sys.exit(1)
        else:
            print(f"✅ Found index '{final_index_name}'")
    except Exception as e:
        print(f"❌ Error checking indexes: {e}")
        sys.exit(1)

    print("\n⚠️  This will process all supported files in:")
    print(f"   {final_folder_path}")
    print(f"   And upload embeddings to index '{final_index_name}'")
    if final_namespace:
        print(f"   Using namespace: '{final_namespace}'")
    
    confirmation = input("\nProceed? (y/N): ").strip().lower()
    if confirmation not in ("y", "yes"):
        print("❌ Operation cancelled by user.")
        return

    process_folder(final_folder_path, openai_client, pc, final_index_name, namespace=final_namespace)


if __name__ == "__main__":
    main()
