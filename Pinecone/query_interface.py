#!/usr/bin/env python3
"""
Pinecone RAG Query Interface with Streamlit UI

This script provides a web-based interface to query your Pinecone knowledge base
using Retrieval Augmented Generation (RAG) with OpenAI's language models.
"""

import os
import sys
import json
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import re

import streamlit as st
from dotenv import load_dotenv
import tiktoken

# OpenAI and Pinecone
from openai import OpenAI
from pinecone import Pinecone


# =========================
# Configuration
# =========================
# INDEX_NAME = "biweekly-meeting"
# NAMESPACE = "biweekly-meeting"  # Set to None if using default namespace

load_dotenv()

INDEX_NAME = os.getenv("PINECONE_INDEX_NAME")     # must exist already
NAMESPACE  = os.getenv("PINECONE_NAMESPACE")   
INFO = "Tesla N8N Course"
# INFO = "BiWeekly Meeting Notes"
EMBED_MODEL = "text-embedding-3-small"
CHAT_MODEL = "gpt-4o-mini"  # or "gpt-3.5-turbo" for cheaper option
MAX_CONTEXT_LENGTH = 8000  # Max tokens for context


TOP_K = 5  # Number of similar chunks to retrieve


def load_environment():
    """Load environment variables from .env file."""
    env_file = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_file):
        load_dotenv(env_file)
        return True
    return False


@st.cache_resource
def initialize_clients():
    """Initialize and cache OpenAI and Pinecone clients."""
    try:
        openai_api_key = os.getenv('OPENAI_API_KEY')
        pinecone_api_key = os.getenv('PINECONE_API_KEY')
        
        if not openai_api_key or not pinecone_api_key:
            return None, None, "Missing API keys"
        
        openai_client = OpenAI(api_key=openai_api_key)
        pinecone_client = Pinecone(api_key=pinecone_api_key)
        
        return openai_client, pinecone_client, "success"
        
    except Exception as e:
        return None, None, str(e)


def count_tokens(text: str, model: str = CHAT_MODEL) -> int:
    """Count tokens in text."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except:
        return int(len(text.split()) * 1.3)


def create_query_embedding(openai_client: OpenAI, query: str) -> Optional[List[float]]:
    """Create embedding for the user query."""
    try:
        response = openai_client.embeddings.create(
            model=EMBED_MODEL,
            input=query
        )
        return response.data[0].embedding
    except Exception as e:
        st.error(f"Error creating query embedding: {e}")
        return None


def search_pinecone(pc: Pinecone, query_embedding: List[float], top_k: int = TOP_K) -> List[Dict]:
    """Search Pinecone index for similar content."""
    try:
        index = pc.Index(INDEX_NAME)
        
        search_kwargs = {
            "vector": query_embedding,
            "top_k": top_k,
            "include_metadata": True,
            "include_values": False
        }
        
        if NAMESPACE:
            search_kwargs["namespace"] = NAMESPACE
            
        results = index.query(**search_kwargs)
        
        # Format results
        formatted_results = []
        for match in results.matches:
            formatted_results.append({
                "id": match.id,
                "score": match.score,
                "metadata": match.metadata,
                "content": match.metadata.get("content", ""),
                "filename": match.metadata.get("filename", "Unknown"),
                "chunk_index": match.metadata.get("chunk_index", 0),
                "file_type": match.metadata.get("file_type", "unknown")
            })
        
        return formatted_results
        
    except Exception as e:
        st.error(f"Error searching Pinecone: {e}")
        return []


def build_context(search_results: List[Dict], max_tokens: int = MAX_CONTEXT_LENGTH) -> Tuple[str, List[str]]:
    """Build context string from search results while respecting token limits."""
    context_parts = []
    sources = []
    current_tokens = 0
    
    for i, result in enumerate(search_results):
        content = result["content"]
        filename = result["filename"]
        chunk_idx = result["chunk_index"]
        
        # Create a context entry
        context_entry = f"\n--- Source {i+1}: {filename} (chunk {chunk_idx}) ---\n{content}\n"
        entry_tokens = count_tokens(context_entry)
        
        if current_tokens + entry_tokens > max_tokens:
            if i == 0:  # Always include at least one result
                context_parts.append(context_entry[:max_tokens])
                sources.append(f"{filename} (chunk {chunk_idx})")
            break
            
        context_parts.append(context_entry)
        sources.append(f"{filename} (chunk {chunk_idx})")
        current_tokens += entry_tokens
    
    return "".join(context_parts), sources


def generate_answer(openai_client: OpenAI, query: str, context: str) -> Optional[str]:
    """Generate answer using OpenAI chat model with retrieved context."""
    try:
        system_prompt = f"""You are a helpful assistant that answers questions based on provided context from {INFO} and documents.

Instructions:
- Answer the question based ONLY on the provided context
- If the context doesn't contain enough information, say "I don't have enough information in the provided context to answer this question completely."
- Be specific and cite relevant details from the context
- If you find conflicting information, mention it
- Keep your answers concise but comprehensive
- Use bullet points or numbered lists when appropriate for clarity"""

        user_prompt = f"""Context from {INFO} documents:
{context}

Question: {query}

Please answer the question based on the context provided above."""

        response = openai_client.chat.completions.create(
            model=CHAT_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.1,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        st.error(f"Error generating answer: {e}")
        return None


def format_search_results(results: List[Dict]) -> str:
    """Format search results for display."""
    if not results:
        return "No relevant documents found."
    
    formatted = []
    for i, result in enumerate(results, 1):
        filename = result["filename"]
        chunk_idx = result["chunk_index"]
        score = result["score"]
        content = result["content"]
        
        # Check if content was truncated during storage
        metadata = result.get("metadata", {})
        was_truncated = metadata.get("content_truncated", False)
        
        # Show preview of content
        content_preview = content[:300] + "..." if len(content) > 300 else content
        
        truncation_note = ""
        if was_truncated:
            truncation_note = " ⚠️ *Content was truncated during storage*"
        
        formatted.append(f"""
**{i}. {filename}** (chunk {chunk_idx}) - Relevance: {score:.3f}{truncation_note}
```
{content_preview}
```
""")
    
    return "\n".join(formatted)


def main():
    st.set_page_config(
        page_title=f"{INFO} Q&A",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title(f"🧠 {INFO} Q&A System")
    st.markdown(f"Ask questions about your {INFO} and get AI-powered answers!")
    
    # Load environment
    env_loaded = load_environment()
    if not env_loaded:
        st.warning("No .env file found. Make sure your API keys are set as environment variables.")
    
    # Initialize clients
    openai_client, pc, init_status = initialize_clients()
    
    if init_status != "success":
        st.error(f"Failed to initialize clients: {init_status}")
        st.info("Please ensure your OPENAI_API_KEY and PINECONE_API_KEY are set correctly.")
        
        with st.expander("Setup Instructions"):
            st.markdown(f"""
            Create a `.env` file in the Pinecone directory with:
            ```
            OPENAI_API_KEY=your-openai-api-key
            PINECONE_API_KEY=your-pinecone-api-key
            ```
            
            Or set them as environment variables:
            ```bash
            set OPENAI_API_KEY=your-openai-api-key
            set PINECONE_API_KEY=your-pinecone-api-key
            ```
            """)
        return
    
    # Verify index exists
    try:
        indexes = pc.list_indexes().names()
        if INDEX_NAME not in indexes:
            st.error(f"Pinecone index '{INDEX_NAME}' not found!")
            st.info(f"Available indexes: {', '.join(indexes) if indexes else 'None'}")
            return
    except Exception as e:
        st.error(f"Error checking Pinecone indexes: {e}")
        return
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Search parameters
        search_top_k = st.slider("Number of sources to retrieve", 1, 10, TOP_K)
        max_context_tokens = st.slider("Max context tokens", 2000, 12000, MAX_CONTEXT_LENGTH, step=500)
        
        # Model selection
        chat_model = st.selectbox(
            "Chat Model",
            ["gpt-4o-mini", "gpt-4o", "gpt-3.5-turbo"],
            index=0
        )
        
        # Show index info
        st.header("📊 Index Info")
        st.info(f"""
        **Index:** {INDEX_NAME}
        **Namespace:** {NAMESPACE or "Default"}
        **Embed Model:** {EMBED_MODEL}
        """)
        
        # Clear chat button
        if st.button("🗑️ Clear Chat History"):
            if "messages" in st.session_state:
                st.session_state.messages = []
            st.rerun()
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        st.session_state.messages.append({
            "role": "assistant", 
            "content": f"👋 Hello! I'm here to help you find information from your {INFO}. What would you like to know?",
            "sources": [],
            "search_results": []
        })
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
            
            # Show sources if available
            if message.get("sources"):
                with st.expander(f"📚 Sources ({len(message['sources'])})"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"{i}. {source}")
            
            # Show detailed search results if available
            if message.get("search_results"):
                with st.expander("🔍 Detailed Search Results"):
                    st.markdown(format_search_results(message["search_results"]))
    
    # Chat input
    if prompt := st.chat_input(f"Ask a question about your {INFO}..."):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Searching through your meeting notes..."):
                
                # Create query embedding
                query_embedding = create_query_embedding(openai_client, prompt)
                if not query_embedding:
                    st.error("Failed to create query embedding.")
                    return
                
                # Search Pinecone
                search_results = search_pinecone(pc, query_embedding, top_k=search_top_k)
                if not search_results:
                    response = f"I couldn't find any relevant information in your {INFO} for this question."
                    sources = []
                else:
                    # Build context and generate answer
                    context, sources = build_context(search_results, max_context_tokens)
                    response = generate_answer(openai_client, prompt, context)
                    
                    if not response:
                        response = "I encountered an error while generating the response. Please try again."
                
                # Display response
                st.markdown(response)
                
                # Show sources
                if sources:
                    with st.expander(f"📚 Sources ({len(sources)})"):
                        for i, source in enumerate(sources, 1):
                            st.markdown(f"{i}. {source}")
                
                # Show detailed search results
                if search_results:
                    with st.expander("🔍 Detailed Search Results"):
                        st.markdown(format_search_results(search_results))
                
                # Add to chat history
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": response,
                    "sources": sources,
                    "search_results": search_results
                })
    
    # Footer
    st.markdown("---")
    st.markdown(f"*Powered by OpenAI {EMBED_MODEL} embeddings and {chat_model} chat model*")


if __name__ == "__main__":
    main()
