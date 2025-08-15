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
FOLDER_PATH = r"C:\Users\samfi\Downloads\BiWeekly-MeetingNotes"
INDEX_NAME = "biweekly-meeting"     # must exist already
NAMESPACE  = "biweekly-meeting"     # ASCII only; comment out to use default
EMBED_MODEL = "text-embedding-3-small"  # 1536 dims


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


def chunk_text(text: str, max_tokens: int = 8000, overlap: int = 200) -> List[str]:
    """Split text into chunks that fit within token limits."""
    if count_tokens(text) <= max_tokens:
        return [text]

    paragraphs = text.split('\n\n')
    chunks: List[str] = []
    current_chunk = ""

    for paragraph in paragraphs:
        test_chunk = current_chunk + ("\n\n" if current_chunk else "") + paragraph
        if count_tokens(test_chunk) <= max_tokens:
            current_chunk = test_chunk
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
                # overlap by words
                words = current_chunk.split()
                overlap_text = " ".join(words[-overlap:]) if len(words) > overlap else current_chunk
                current_chunk = overlap_text + "\n\n" + paragraph
            else:
                # paragraph too long -> split by sentences
                sentences = re.split(r'(?<=[.!?])\s+', paragraph)
                temp_chunk = ""
                for sentence in sentences:
                    if not sentence.strip():
                        continue
                    test_sentence = (temp_chunk + " " + sentence).strip()
                    if count_tokens(test_sentence) <= max_tokens:
                        temp_chunk = test_sentence
                    else:
                        if temp_chunk:
                            chunks.append(temp_chunk.strip())
                        temp_chunk = sentence
                current_chunk = temp_chunk
    if current_chunk.strip():
        chunks.append(current_chunk.strip())
    return chunks


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
    """Create embedding using OpenAI API."""
    try:
        resp = client.embeddings.create(model=model, input=text)
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

    for file_path in files:
        print("\n" + "=" * 60)
        info = process_file(str(file_path))
        if not info:
            continue

        chunks = chunk_text(info['content'])
        print(f"📝 Split into {len(chunks)} chunk(s)")

        for chunk_idx, chunk in enumerate(chunks):
            print(f"   🔄 Processing chunk {chunk_idx + 1}/{len(chunks)}...")
            emb = create_embedding(openai_client, chunk)
            if not emb:
                print(f"   ❌ Failed to create embedding for chunk {chunk_idx + 1}")
                continue

            vector_id = generate_chunk_id(chunk, str(file_path), chunk_idx)
            vector = {
                "id": vector_id,
                "values": emb,
                "metadata": {
                    "filename": info['filename'],
                    "filepath": info['filepath'],
                    "file_type": info['type'],
                    "file_size": info['size'],
                    "file_modified": info['modified'],
                    "chunk_index": chunk_idx,
                    "total_chunks": len(chunks),
                    # keep metadata < 40KB; trim content
                    "content": chunk[:1000],
                    "word_count": len(chunk.split()),
                    "char_count": len(chunk),
                    "processed_at": datetime.now().isoformat()
                }
            }
            all_vectors.append(vector)
            total_chunks += 1
            print(f"   ✅ Created embedding (dimension: {len(emb)})")

        processed_files += 1
        print(f"✅ Completed {info['filename']} ({len(chunks)} chunks)")

    if not all_vectors:
        print("❌ No embeddings were created. Check the files and try again.")
        return

    print("\n" + "=" * 60)
    print("📊 Processing Summary:")
    print(f"   📁 Files processed: {processed_files}/{len(files)}")
    print(f"   📄 Total chunks: {total_chunks}")
    print(f"   🧠 Total embeddings: {len(all_vectors)}")

    # quick peek at IDs to confirm ASCII
    print("🔎 Example IDs:", [v["id"] for v in all_vectors[:3]])

    print(f"\n🔄 Uploading embeddings to Pinecone index '{INDEX_NAME}'...")
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
    print(f"📁 Target folder: {FOLDER_PATH}")
    print(f"🎯 Target index: {INDEX_NAME}")
    if NAMESPACE:
        print(f"🧱 Namespace: {NAMESPACE}")

    load_environment()

    openai_client, pc = initialize_clients()
    if not openai_client or not pc:
        sys.exit(1)

    # Verify index exists
    try:
        indexes = pc.list_indexes().names()
        if INDEX_NAME not in indexes:
            print(f"❌ Index '{INDEX_NAME}' not found!")
            print(f"Available indexes: {', '.join(indexes) if indexes else 'None'}")
            print("Please create the index first.")
            sys.exit(1)
        else:
            print(f"✅ Found index '{INDEX_NAME}'")
    except Exception as e:
        print(f"❌ Error checking indexes: {e}")
        sys.exit(1)

    print("\n⚠️  This will process all supported files in:")
    print(f"   {FOLDER_PATH}")
    print(f"   And upload embeddings to index '{INDEX_NAME}'")
    confirmation = input("\nProceed? (y/N): ").strip().lower()
    if confirmation not in ("y", "yes"):
        print("❌ Operation cancelled by user.")
        return

    process_folder(FOLDER_PATH, openai_client, pc, INDEX_NAME, namespace=NAMESPACE)


if __name__ == "__main__":
    main()
