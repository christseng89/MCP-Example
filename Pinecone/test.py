from pinecone import Pinecone
import os
from dotenv import load_dotenv

load_dotenv()
pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
idx = pc.Index(os.getenv("PINECONE_INDEX_NAME"))
stats = idx.describe_index_stats()
print(stats)  # should show total vector count and namespaces
