# api-assistant
AI Project Demo.

A FastAPI-based AI-powered service to **ingest**, **embed**, and **search OpenAPI specifications** using semantic similarity. This platform allows users to search and discover APIs by meaning, not just keywords.

## Purpose

Enable developers or systems to search across a catalog of OpenAPI specifications using **natural language** or **semantic intent**, powered by modern **embedding models**.

## Out-of-scope

- Authentication and Authorization
- Loging and audit
- Session management


## Example Flow

1. **User uploads** OpenAPI JSON/YAML.
2. Ingestion service:
   - Parses and normalizes the data.
   - Sends descriptions to the embedding engine.
   - Stores the resulting vectors in PgVector.
3. User performs a **semantic search query** via Webpage.
4. Query is embedded and compared to stored vectors.
5. Top-k similar API endpoints are returned.


## Solution

```mermaid
---
title: API Assitant Solution
mermaid:
  theme: neutral
---
graph TD

    subgraph Script 
        E1[Upload local schemas] 
    end

    subgraph Browser
        A2[Chat Frontend <br> e.g. React]
    end

    subgraph Development Environment
        A1[VS Code<br>e.g. copiot]
    end

    subgraph MCP Server
        B1[MCP Server<br>FastAPI]
        B2[Semantic Client<br>HTTP client for /ask]
    end

    subgraph Semantic Search API
        C1[Semantic Search API<br>FastAPI /ask]
        C2[LangChain Agent<br>API Search]
        C4[Embeddings Generator<br>OpenAI]
    end

    subgraph API Ingestion
        D1[Uploader API<br> FastAPI]
        D2[Data Extraction]
        D3[Embeddings Generation<br>OpenAI]
        D4[Save embeddings]
    end

    subgraph Vector Database
        C3[PostgreSQL + pgvector]
    end

    %% User interaction paths
    A1 -->|chat message| B1
    A2 -->|chat message| C1
    B1 --> B2
    B2 -->|POST /ask| C1
    C1 --> C2
    C2 -->|semantic search| C3
    C2 -->|embed user query| C4
    C3 -->|filtered matches| C2
    C2 -->|response| C1
    C1 -->|reply| B2
    B2 --> B1 -->|answer| A1
    B2 --> C1 -->|answer| A2
    D4 -->|embeddings and data| C3
    E1 -->|POST /upload| D1

    %% Indexing path
    D1 --> D2 --> D3 --> D4

```

## Components

- **Client Script**  
  Read local OpenAPI specifications and upload to the system.
  
- **OpenAPI Ingestion Service (FastAPI)**  
  Accepts raw OpenAPI specs (JSON/YAML), parses endpoints, and extracts semantic descriptions.

- **Embedding Engine (via OpenAI API)**  
  Converts API endpoint descriptions into high-dimensional embeddings using models like `text-embedding-3-small`.

- **Vector Store (PostgreSQL + PgVector)**  
  Stores API metadata and endpoint embeddings in a relational and vector-aware format. Supports efficient similarity search.

- **Semantic Search API (AI Agent via FastAPI)**  
  Accepts user queries, converts them to embeddings, and retrieves the most relevant endpoints using cosine similarity.

- **Chat Frontend (Webpage powered by React)**  
  Allows users to interact with the search API using a web page.

- **MCP Server**  
  Allows AI agent to interact with the search API using the [Model Control Protocol (MCP)].

- **Developer Environment**  
  Visual studio code with copilot pluging configured in agent mode the connect to MCP Server using MCP.
  

## Model

| Table | Description |
|-------|-------------|
| `apis` | OpenAPI documents (name, version) |
| `api_endpoints` | Parsed endpoints (`GET /users`) |
| `embeddings` | Stores vector representation per endpoint |

Supports standard relational normalization and indexing for fast lookup.

```mermaid
erDiagram

    APIs {
        int id PK
        string title
        string version
        json spec
        vector embedding
        string model
        string uploaded_at
    }
```
*type* : summary, description, parameters, response schemas ...

This model can be improved to support multiple embeddings per API, key benefits are:

1. Embedding Versioning
    - re-embed content when:
      - Switch to a newer model (e.g., text-embedding-3-small → text-embedding-3-large)
      - Refine your embedding strategy (e.g., different preprocessing)

    - Historical embeddings allows:
       - Compare models - helps to ensure you're using the best embedding representation for your accuracy, performance, and cost trade-offs.
       - Re-rank results
       - Roll back mistakes

2. Fine-tuned Use Cases
    - You could store different embeddings for:
      - Endpoint description
      - Endpoint parameters
      - Endpoint response schemas

3. Multi-language Support
    - Embed descriptions in multiple languages if your API is multilingual.



## Technologies Used

| Layer | Tech |
|-------|------|
| API | FastAPI |
| Embedding | OpenAI Embeddings API |
| Vector Search | PgVector (PostgreSQL extension) |
| ORM | SQLAlchemy |
| CLI/Agent | MCP or Python script |
| Infra | Docker, Kubernetes/Kind |
