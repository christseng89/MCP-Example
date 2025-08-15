# BiWeekly Meeting Notes RAG System

This project provides a complete Retrieval Augmented Generation (RAG) system for your BiWeekly meeting notes using OpenAI embeddings and Pinecone vector database.

## 🚀 Features

- **File Processing**: Supports PDF, Word documents (.docx/.doc), and text files (.txt/.md/.rtf)
- **Advanced Text Splitting**: Uses RecursiveCharacterTextSplitter with configurable chunk size (1000) and overlap (120)
- **Vector Embeddings**: Uses OpenAI's `text-embedding-3-small` model for high-quality embeddings
- **Batch Processing**: Efficient batch embedding creation for optimal performance
- **Web Interface**: Beautiful Streamlit-based Q&A interface
- **RAG Pipeline**: Retrieves relevant context and generates accurate answers
- **Source Attribution**: Always shows which documents were used to generate answers

## 📋 Requirements

- Python 3.12+
- OpenAI API key
- Pinecone API key
- UV package manager (recommended) or pip

## 🛠️ Setup

1. **Install Dependencies**:
   ```bash
   cd Pinecone
   uv sync
   ```

2. **Set API Keys and Configuration**:
   Create a `.env` file in the Pinecone directory:
   ```
   # Required API Keys
   OPENAI_API_KEY=your-openai-api-key-here
   PINECONE_API_KEY=your-pinecone-api-key-here
   
   # Optional: Custom configuration (uses defaults if not specified)
   PINECONE_FOLDER_PATH=C:\path\to\your\documents
   PINECONE_INDEX_NAME=your-index-name
   PINECONE_NAMESPACE=your-namespace
   ```

3. **Get API Keys**:
   - OpenAI: [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
   - Pinecone: [https://app.pinecone.io/](https://app.pinecone.io/)

## 📚 Usage

### Step 1: Create Pinecone Index

```bash
uv run python create_index.py
```

This will:
- Guide you through creating a new Pinecone index
- Configure dimensions (1536 for OpenAI embeddings)
- Set up the index with proper settings

### Step 2: Upload Documents

```bash
uv run python embed_folder.py
```

This will:
- Process all supported files in your configured folder (default: `C:\Users\samfi\Downloads\BiWeekly-MeetingNotes`)
- Create embeddings for document chunks
- Upload them to your Pinecone index

**💡 Tip**: Set `PINECONE_FOLDER_PATH` in your `.env` file to customize the source folder

### Step 3: Query with UI

**Option A - Quick Launch (Windows)**:
```bash
run_ui.bat
```

**Option B - Python Script**:
```bash
uv run python run_ui.py
```

**Option C - Direct Streamlit**:
```bash
uv run streamlit run query_interface.py
```

## 🖥️ Web Interface Features

### Chat Interface
- **Natural Questions**: Ask questions in plain English
- **Context-Aware**: Maintains conversation history
- **Real-time Search**: Instant results from your knowledge base

### Advanced Features
- **Source Attribution**: See exactly which documents were used
- **Relevance Scoring**: Shows how relevant each source is
- **Configurable Search**: Adjust number of sources and context length
- **Model Selection**: Choose between different OpenAI models

### Search Configuration
- **Top-K Results**: Choose how many similar documents to retrieve (1-10)
- **Context Length**: Adjust maximum tokens for context (2000-12000)
- **Chat Models**: Select from GPT-4o-mini, GPT-4o, or GPT-3.5-turbo

## 📁 File Support

| Format | Extension | Notes |
|--------|-----------|-------|
| PDF | `.pdf` | Full text extraction |
| Word | `.docx`, `.doc` | Paragraphs and formatting preserved |
| Text | `.txt`, `.md`, `.rtf` | Multiple encoding support |

## 🔧 Configuration

Edit these variables in the scripts to customize:

**embed_folder.py** (via environment variables):
```bash
# Set in .env file or environment
PINECONE_FOLDER_PATH=C:\path\to\your\documents
PINECONE_INDEX_NAME=your-index-name
PINECONE_NAMESPACE=your-namespace

# OpenAI Embedding Settings (optional - uses optimized defaults)
OPENAI_EMBED_MODEL=text-embedding-3-small
OPENAI_EMBED_DIMENSIONS=1536
OPENAI_EMBED_BATCH_SIZE=128
OPENAI_EMBED_TIMEOUT=300000

# Text Splitter Settings (optional - uses optimized defaults)
TEXT_CHUNK_SIZE=1000
TEXT_CHUNK_OVERLAP=120

# Built-in defaults:
# Model: text-embedding-3-small (1536 dimensions)  
# Batch Size: 128 texts per API call
# Timeout: 300,000ms (5 minutes)
# Chunk Size: 1000 characters
# Chunk Overlap: 120 characters
```

**query_interface.py**:
```python
INDEX_NAME = "biweekly-meeting"
NAMESPACE = "biweekly-meeting"
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"
TOP_K = 5  # Number of sources to retrieve
```

## 🐛 Troubleshooting

### Common Issues

**API Key Errors**:
- Ensure `.env` file exists with correct keys
- Check API key validity on respective platforms
- Verify environment variables are loaded

**Import Errors**:
- Run `uv sync` to install dependencies
- Check Python version (3.12+ required)

**Empty Results**:
- Verify documents were uploaded successfully
- Check if index name matches configuration
- Ensure namespace is configured correctly

**File Processing Issues**:
- Check file permissions
- Verify file formats are supported
- Look for encoding issues in text files

### Debug Mode

Add this to your `.env` file for verbose logging:
```
STREAMLIT_LOGGER_LEVEL=DEBUG
```

## 💡 Tips

1. **Better Questions**: Be specific in your questions for better results
2. **Context Length**: Increase context length for complex questions
3. **Source Review**: Always check the sources to verify answer accuracy
4. **Chunk Strategy**: Large documents are automatically chunked for better retrieval

## 📊 Example Questions

Try asking questions like:
- "What were the main decisions made in the last quarter?"
- "Who is responsible for the new project implementation?"
- "What are the key deadlines mentioned in recent meetings?"
- "Summarize the budget discussions from the meeting notes"

## 🔒 Security

- API keys are stored locally in `.env` files
- No data is sent to external services except OpenAI and Pinecone APIs
- Documents remain in your local environment during processing

---

*Built with ❤️ using OpenAI, Pinecone, and Streamlit*
