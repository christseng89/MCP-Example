# Embedding

## Vector Database 产品对比表

| Product                    | Free tier            | Queries per second (approx recall of 0.9) From ANN Benchmarks on glove-100-angular                                      | Cost at Scale per Month (Information and Not Comparison)                                                                                                                                                                                                                                                                                                                         | Is Current Database | Self-Host | Managed in Cloud          | SOC-2                         | HIPAA                         | Open Source | Notes                                                               |
| -------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------- | --------- | ------------------------- | ----------------------------- | ----------------------------- | ----------- | ------------------------------------------------------------------- |
| **Weaviate**               | Yes                  | 517                                                                                                                     | (Vector size 1,536, 10M vectors, 1,000,000 queries/month)<br>Standard: \$770/month (High Availability: \$1,700/month)<br>Enterprise: \$1,701/month (High Availability: \$3,300/month)<br>Business Critical: \$3,000/month (High Availability: \$5,900/month)                                                                                                                     | No                  | Yes       | Yes                       | Can be (Depending on hosting) | Can be (Depending on hosting) | Yes         |                                                                     |
| **Pinecone**               | Yes                  | From Pinecone website (queries per second for 1M vectors of size 768, top-10):<br>s1 pod: 1<br>p1 pod: 10<br>p2 pod: 17 | For 10M vectors of size 1,536 on AWS and one replica:<br>s1 pod (4 pods needed): standard \$384/month; enterprise \$480/month<br>p1 pod (20 pods needed): standard \$1,599/month; enterprise \$2,398/month<br>p2 pod (19 pods needed): standard \$2,278/month; enterprise \$3,417/month                                                                                          | No                  | No        | Yes                       | Yes                           | No                            | No          |                                                                     |
| **pgvector on PostgreSQL** | Depending on hosting | 84 (Supabase article claims around 470 with improvements)                                                               | (Each vector takes 4 \* dimensions + 8 bytes of storage)<br>10M vectors of size 1,536 occupy around 62 GB. Assuming using Azure PostgreSQL Flexible Server:<br>Burstable:<br>- 1 vCore: \$19.77/month<br>- 2 vCore: \$107/month<br>General purpose:<br>- 2 vCore: \$137/month<br>- 4 vCore: \$267/month<br>Memory optimized:<br>- 2 vCore: \$190/month<br>- 4 vCore: \$372/month | Yes                 | Yes       | Yes (various vendors)     | Can be (Depending on hosting) | Can be (Depending on hosting) | Yes         | Improvements to pgvector can improve pgvector’s requests per second |
| **Milvus**                 | Yes                  | ?                                                                                                                       | Capacity optimized on Zilliz cloud: \$450/month<br>Cost optimized: \$300/month<br>Performance optimized: \$1,375/month                                                                                                                                                                                                                                                           | No                  | Yes       | Yes                       | ? (Depending on hosting?)     | ? (Depending on hosting?)     | Yes         |                                                                     |
| **MongoDB**                | Yes                  | ? (There are ANN benchmarks on traditional MongoDB, but could not find vector part)                                     | MongoDB Atlas: Dedicated with 80 GB storage on AWS costs around \$750/month                                                                                                                                                                                                                                                                                                      | Yes                 | Yes       | Yes                       | Yes                           | Yes                           | Yes         | The vector search is new and not much tested yet                    |
| **Qdrant**                 | Self-hosted is free  | ? (Storage optimized: \$280/month; Not storage optimized: \$820/month)                                                  | Storage optimized: \$280/month<br>Not storage optimized: \$820/month                                                                                                                                                                                                                                                                                                             | No                  | Yes       | Yes                       | ? (Depending on hosting?)     | ? (Depending on hosting?)     | Yes         |                                                                     |
| **ChromaDB**               | In memory of server  | ?                                                                                                                       | Hosted product is under development                                                                                                                                                                                                                                                                                                                                              | No                  | Not Yet   | ? (Depending on hosting?) | ? (Depending on hosting?)     | ? (Depending on hosting?)     | Yes         |                                                                     |

---

## Qdrant Vector Database

<https://cloud.qdrant.io/>

* Login => Clusters => Create a Free Cluster (AI_autoWith_n8n) => Create Free Cluster

```bash
curl \
    -X GET 'https://ac7286b1-7cd1-484e-be93-1b95473e9615.us-east-1-1.aws.cloud.qdrant.io:6333' \
    --header 'api-key: eyJhbGciOiJIUzI1NiIsInR5c...'
```

* Endpoint: `https://ac7286b1-7cd1-484e-be93-1b95473e9615.us-east-1-1.aws.cloud.qdrant.io`

## Qdrant with n8n workflows

*02.1 Upserting Qdrant
*02.2 Upserting and Querying Qdrant v1 (LLMs)
*02.2 Upserting and Querying Qdrant v2 (AI Agents)
  
## PostgreSQL with pgvector

* Create n8n Database => n8n => Query Tool

```sql

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE n8n_vector (
    id bigserial PRIMARY KEY,
    "pageContent" text,          -- document text
    metadata jsonb,              -- extra metadata
    embedding vector(1536)       -- adjust dimension if using text-embedding-3-large (3072)
);
```

... to be continued ...
