# SysMLv2 MCP Server

A Model Context Protocol (MCP) server that provides access to the SysMLv2 API. 

## Features

- **Streamable HTTP Protocol**: Uses FastMCP's streamable HTTP transport for efficient bidirectional communication
- **Authorization Forwarding**: Forwards Bearer tokens from MCP clients to the SysMLv2 API
- **Read-Only Mode**: Optional read-only mode that only exposes GET endpoints

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

The server is configured via environment variables:

- `SYSMLV2_URL`: The base URL of the SysMLv2 API (default: `http://localhost:8080`)
- `READ_ONLY`: Enable read-only mode, only exposing GET endpoints (default: `true`)
  - Accepted values: `true`, `1`, `yes` (case-insensitive)

## Usage

### Starting the Server

```bash
# Default configuration
python server.py

# With custom SysMLv2 API URL
SYSMLV2_URL=https://api.example.com python server.py

# In read-only mode
READ_ONLY=true python server.py

# Combined configuration
SYSMLV2_URL=https://api.example.com READ_ONLY=true python server.py
```

The server will start on `http://0.0.0.0:8000` and the MCP endpoint will be available at `http://0.0.0.0:8000/mcp`.

### Connecting Clients

Clients can connect to the MCP server using the streamable HTTP transport. Example using FastMCP client:

```python
from fastmcp.client import Client

# Without authentication
client = Client("http://localhost:8000/mcp")

# With Bearer token authentication
client = Client(
    "http://localhost:8000/mcp",
    headers={"Authorization": "Bearer your-token-here"}
)
```

## Docker

### Building the Image

```bash
docker build -t flexo-mms-sysmlv2-mcp .
```

### Running the Container

Run with custom MMS URL:

```bash
docker run -d \
  -p 8000:8000 \
  -e MMS_URL=https://your-flexo-mms-server \
  flexo-mms-sysmlv2-mcp
```

Run in read-write mode (enables create/update/delete operations):

```bash
docker run -d \
  -p 8000:8000 \
  -e MMS_URL=https://your-mms-server \
  -e READ_ONLY=false \
  flexo-mms-sysmlv2-mcp
```

## Available Tools

The server exposes all operations from the OpenAPI specification as MCP tools. Each tool corresponds to a REST API endpoint:

### Projects
- `getProjects` - Get projects
- `postProject` - Create project
- `getProjectById` - Get project by ID
- `putProjectById` - Update project by ID
- `deleteProjectById` - Delete project by ID

### Branches
- `getBranchesByProject` - Get branches by project
- `postBranchByProject` - Create branch by project
- `getBranchesByProjectAndId` - Get branch by project and ID
- `deleteBranchByProjectAndId` - Delete branch by project and ID
- `merge` - Merge source commit(s) into a target branch

### Commits
- `getCommitsByProject` - Get commits by project
- `postCommitByProject` - Create commit by project
- `getCommitByProjectAndId` - Get commit by project and ID

### Elements
- `getElementsByProjectCommit` - Get elements by project and commit
- `getElementByProjectCommitId` - Get element by project, commit and ID
- `getProjectUsageByProjectCommitElement` - Get ProjectUsage for an element
- `getRelationshipsByProjectCommitRelatedElement` - Get relationships for an element
- `getRootsByProjectCommit` - Get root elements

### Queries
- `getQueriesByProject` - Get queries by project
- `postQueryByProject` - Create query by project
- `getQueryByProjectAndId` - Get query by project and ID
- `putQueryByProjectAndId` - Update query by project and ID
- `deleteQueryByProjectAndId` - Delete query by project and ID
- `getQueryResultsByProjectIdQueryId` - Get query results
- `getQueryResultsByProjectIdQuery` - Get query results

### Tags
- `getTagsByProject` - Get tags by project
- `postTagByProject` - Create tag by project
- `getTagByProjectAndId` - Get tag by project and ID
- `deleteTagByProjectAndId` - Delete tag by project and ID


## Read-Only Mode

When `READ_ONLY=true`, only GET operations are exposed as tools. This is useful for:
- Providing safe, read-only access to the API
- Preventing accidental modifications
- Compliance with security policies

## Authentication

The server forwards Bearer tokens from MCP clients to the SysMLv2 API. To authenticate:

1. Client sends request with `Authorization: Bearer <token>` header
2. Server extracts the token from the MCP request context
3. Server forwards the token in the `Authorization` header to the SysMLv2 API

This allows the SysMLv2 API to handle authentication and authorization independently.

## Architecture

```
MCP Client → [Streamable HTTP] → MCP Server → [REST API] → SysMLv2 API
              (with Bearer token)              (with Bearer token)
```

The server:
1. Defines 35 explicit MCP tools corresponding to SysMLv2 API operations
2. Extracts Bearer tokens from MCP request context
3. Forwards requests to the SysMLv2 API with proper authentication
4. Returns responses back to the MCP client
5. Conditionally registers write operations based on READ_ONLY mode

## Error Handling

The server includes comprehensive error handling:
- HTTP errors are caught and returned with status code and message
- Connection errors are caught and returned with error details
- Invalid requests are handled gracefully

## Development

The server uses:
- **FastMCP 2.x**: For MCP server implementation with streamable HTTP support
- **httpx**: For async HTTP client functionality
- **Python 3.7+**: Required for async/await support

## License

See the project license for details.
