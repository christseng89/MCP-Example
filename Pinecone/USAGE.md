# Usage Guide

## Quick Start with Environment Variables

### 1. Set up your configuration

Create a `.env` file (copy from `example.env`):

```bash
# Required
OPENAI_API_KEY=your-openai-api-key
PINECONE_API_KEY=your-pinecone-api-key

# Optional - customize for your use case
PINECONE_FOLDER_PATH=C:\path\to\your\documents
PINECONE_INDEX_NAME=your-index-name
PINECONE_NAMESPACE=your-namespace
```

### 2. Run the embedding script

```bash
uv run python embed_folder.py
```

The script will:
1. Show your current configuration
2. Validate that the index exists
3. Ask for confirmation before processing
4. Process all supported files in your folder
5. Upload embeddings to Pinecone

### 3. Launch the query interface

```bash
# Windows
run_ui.bat

# Or directly
uv run streamlit run query_interface.py
```

## Configuration Examples

### For Tesla N8N Course
```bash
PINECONE_FOLDER_PATH=C:\Users\samfi\Downloads\Tesla-N8N-Course
PINECONE_INDEX_NAME=n8n-course-tsla
PINECONE_NAMESPACE=n8n-tsla
```

### For BiWeekly Meeting Notes
```bash
PINECONE_FOLDER_PATH=C:\Users\samfi\Downloads\BiWeekly-MeetingNotes
PINECONE_INDEX_NAME=biweekly-meeting
PINECONE_NAMESPACE=biweekly-meeting
```

### For Custom Documents
```bash
PINECONE_FOLDER_PATH=C:\MyDocuments\Knowledge-Base
PINECONE_INDEX_NAME=my-knowledge-base
PINECONE_NAMESPACE=my-docs
```

## Advanced Usage

### Command Line Environment Variables

You can also set variables temporarily:

```bash
# Windows
set PINECONE_INDEX_NAME=my-custom-index
set PINECONE_FOLDER_PATH=C:\MyDocs
uv run python embed_folder.py

# Linux/Mac
export PINECONE_INDEX_NAME=my-custom-index
export PINECONE_FOLDER_PATH=/path/to/docs
uv run python embed_folder.py
```

### Multiple Configurations

For different projects, create separate `.env` files:

```bash
# .env.tesla
PINECONE_INDEX_NAME=tesla-docs
PINECONE_NAMESPACE=tesla
PINECONE_FOLDER_PATH=C:\Tesla\Documents

# .env.meetings
PINECONE_INDEX_NAME=meeting-notes
PINECONE_NAMESPACE=meetings
PINECONE_FOLDER_PATH=C:\Meetings\Notes
```

Then copy the appropriate one to `.env` when needed.

## Troubleshooting

### Configuration Issues

If you get "No index name specified" error:
1. Check that `PINECONE_INDEX_NAME` is set in your `.env` file
2. Make sure the index exists in Pinecone (create with `create_index.py`)

If you get "No folder path specified" error:
1. Set `PINECONE_FOLDER_PATH` in your `.env` file
2. Verify the folder exists and contains supported files

### Supported File Types

- PDF: `.pdf`
- Word: `.docx`, `.doc`
- Text: `.txt`, `.md`, `.rtf`

### Index Management

Always create the index first:
```bash
uv run python create_index.py
```

The index name you create must match `PINECONE_INDEX_NAME` in your configuration.
