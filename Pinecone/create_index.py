#!/usr/bin/env python3
"""
Pinecone Index Creation Script

This script creates a new Pinecone index with configurable parameters.
You'll need to set your Pinecone API key as an environment variable or pass it directly.
"""

import os
import sys
from pinecone import Pinecone, ServerlessSpec
from typing import Optional

from dotenv import load_dotenv

load_dotenv()

def create_pinecone_index(
    index_name: str,
    dimension: int = 1536,
    metric: str = "cosine",
    cloud: str = "aws",
    region: str = "us-east-1",
    api_key: Optional[str] = None
) -> bool:
    """
    Create a Pinecone index with specified parameters.
    
    Args:
        index_name (str): Name of the index to create
        dimension (int): Vector dimension (default: 1536 for OpenAI embeddings)
        metric (str): Distance metric - "cosine", "euclidean", or "dotproduct"
        cloud (str): Cloud provider - "aws", "gcp", or "azure"
        region (str): Region for the index
        api_key (str, optional): Pinecone API key (if not set as env var)
    
    Returns:
        bool: True if successful, False otherwise
    """
    
    try:
        # Get API key from parameter or environment variable
        if api_key is None:
            api_key = os.getenv('PINECONE_API_KEY')
        
        print("API Key: ", api_key[:8])

        if not api_key:
            print("❌ Error: Pinecone API key not found!")
            print("Please set PINECONE_API_KEY environment variable or pass api_key parameter.")
            print("You can get your API key from: https://app.pinecone.io/")
            return False
        
        # Initialize Pinecone client
        print(f"🔄 Initializing Pinecone client...")
        pc = Pinecone(api_key=api_key)
        
        # Check if index already exists
        existing_indexes = pc.list_indexes().names()
        if index_name in existing_indexes:
            print(f"⚠️  Index '{index_name}' already exists!")
            response = input("Do you want to delete and recreate it? (y/N): ").strip().lower()
            if response == 'y' or response == 'yes':
                print(f"🗑️  Deleting existing index '{index_name}'...")
                pc.delete_index(index_name)
                print("✅ Index deleted successfully!")
            else:
                print("❌ Aborted. Index creation cancelled.")
                return False
        
        # Create the index
        print(f"🔄 Creating index '{index_name}'...")
        print(f"   - Dimension: {dimension}")
        print(f"   - Metric: {metric}")
        print(f"   - Cloud: {cloud}")
        print(f"   - Region: {region}")
        
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(
                cloud=cloud,
                region=region
            )
        )
        
        print("✅ Index created successfully!")
        
        # Verify the index was created
        index_info = pc.describe_index(index_name)
        print(f"📊 Index Details:")
        print(f"   - Status: {index_info.status['ready']}")
        print(f"   - Host: {index_info.host}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creating index: {str(e)}")
        return False

def main():
    """Main function to run the index creation script."""
    
    print("🌲 Pinecone Index Creator")
    print("=" * 50)
    
    # Default configuration
    default_config = {
        "index_name": "biweekly-meeting",
        "dimension": 1536,  # OpenAI text-embedding-ada-002 dimension
        "metric": "cosine",
        "cloud": "aws",
        "region": "us-east-1"
    }
    
    # Interactive mode - ask user for configuration
    print("\n📝 Index Configuration:")
    print("Press Enter to use default values shown in [brackets]")
    
    index_name = input(f"Index name [{default_config['index_name']}]: ").strip()
    if not index_name:
        index_name = default_config['index_name']
    
    dimension_input = input(f"Vector dimension [{default_config['dimension']}]: ").strip()
    try:
        dimension = int(dimension_input) if dimension_input else default_config['dimension']
    except ValueError:
        print("⚠️  Invalid dimension, using default.")
        dimension = default_config['dimension']
    
    metric = input(f"Distance metric (cosine/euclidean/dotproduct) [{default_config['metric']}]: ").strip()
    if metric not in ["cosine", "euclidean", "dotproduct"]:
        metric = default_config['metric']
    
    cloud = input(f"Cloud provider (aws/gcp/azure) [{default_config['cloud']}]: ").strip()
    if cloud not in ["aws", "gcp", "azure"]:
        cloud = default_config['cloud']
    
    region = input(f"Region [{default_config['region']}]: ").strip()
    if not region:
        region = default_config['region']
    
    print(f"\n🚀 Creating index with the following configuration:")
    print(f"   - Name: {index_name}")
    print(f"   - Dimension: {dimension}")
    print(f"   - Metric: {metric}")
    print(f"   - Cloud: {cloud}")
    print(f"   - Region: {region}")
    
    confirmation = input("\nProceed? (Y/n): ").strip().lower()
    if confirmation == 'n' or confirmation == 'no':
        print("❌ Aborted.")
        return
    
    # Create the index
    success = create_pinecone_index(
        index_name=index_name,
        dimension=dimension,
        metric=metric,
        cloud=cloud,
        region=region
    )
    
    if success:
        print(f"\n🎉 Successfully created Pinecone index '{index_name}'!")
        print("\n📋 Next steps:")
        print("1. You can now connect to your index using:")
        print(f"   index = pc.Index('{index_name}')")
        print("2. Start adding vectors to your index")
        print("3. Perform similarity searches")
        
        # Example usage code
        print(f"\n💡 Example usage:")
        print(f"""
from pinecone import Pinecone

pc = Pinecone(api_key="your-api-key")
index = pc.Index("{index_name}")

# Add vectors (example)
vectors = [
    {{"id": "vec1", "values": [0.1, 0.2, 0.3, ...], "metadata": {{"text": "example"}}}},
    # ... more vectors
]
index.upsert(vectors=vectors)

# Query (example)
results = index.query(
    vector=[0.1, 0.2, 0.3, ...],
    top_k=5,
    include_metadata=True
)
        """)
    else:
        print("\n❌ Failed to create index. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
