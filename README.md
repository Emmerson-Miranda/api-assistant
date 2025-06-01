# api-assistant
AI Project Demo.

A FastAPI-based AI-powered service to **ingest**, **embed**, and **search OpenAPI specifications** using semantic similarity. This platform allows users to search and discover APIs by meaning, not just keywords.

## Purpose

Enable developers or systems to search across a catalog of OpenAPI specifications using **natural language** or **semantic intent**, powered by modern **embedding models**.


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

- **Script**  
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

```mermaid
erDiagram
    APIs ||--o{ APIEndpoints : has
    APIEndpoints ||--o{ Embeddings : stores

    APIs {
        int id PK
        string name
        string version
    }

    APIEndpoints {
        int id PK
        int api_id FK
        string method
        string path
        string summary
        string description
    }

    Embeddings {
        int id PK
        int endpoint_id FK
        string type 
        string model 
        vector embedding
        datetime created_at
    }

```
 type : summary, description, parameters, response schemas ...
