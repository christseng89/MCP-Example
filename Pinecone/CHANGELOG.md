# Changelog

## Latest Updates

### 🔧 Fixed Content Truncation Issue (embed_folder.py)
- **Problem**: Previously only stored 1000 characters of each document chunk in Pinecone metadata
- **Solution**: Now stores full content (up to 38KB per chunk) with intelligent truncation
- **Improvements**:
  - Full content preservation where possible
  - Smart word-boundary truncation for oversized content
  - Clear indicators when content was truncated
  - Better reporting of content storage statistics

### 🎯 Configuration Updates (query_interface.py)
- **Updated for Tesla N8N Course index**: Changed default index from `biweekly-meeting` to `n8n-course-tsla`
- **Dynamic branding**: UI now adapts to the INFO variable for different knowledge bases
- **Enhanced error handling**: Better truncation detection and display

### 🌟 Key Features
1. **Smart Content Storage**:
   - Maximizes content storage within Pinecone's metadata limits
   - Preserves word boundaries when truncating
   - Tracks and reports truncation statistics

2. **Enhanced Query Interface**:
   - Configurable index and namespace
   - Dynamic branding based on content type
   - Better source attribution with truncation warnings

3. **Improved Processing**:
   - Real-time feedback on content storage
   - Detailed processing statistics
   - ASCII-safe ID generation for international filenames

### 🛠️ Technical Improvements
- Fixed syntax errors in query interface
- Proper indentation and code structure
- Enhanced error reporting
- Better token counting for context management

### 📊 Statistics Tracking
- Total files processed
- Chunks created per file
- Content truncation counts
- Embedding dimensions and storage info

### 🔍 Search Enhancements
- Full content available for RAG responses
- Better context building from retrieved chunks
- Improved source attribution in UI
- Truncation warnings in search results
