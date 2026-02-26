# Infor GenAI API Documentation Summary

## Overview

Three APIs are available for working with Infor GenAI:

1. **GenAI Core Service** - Manages tools, evaluations, guardrails, settings
2. **GenAI Chat Service** - Handles chat sessions, prompts, and agent execution
3. **SyteLine REST API v2** - Backend API that tools call to interact with Infor data

## Base URLs

- **Core Service**: `https://mingle-ionapi.inforcloudsuite.com/<YOUR_TENANT>/GENAI/coresvc`
- **Chat Service**: `https://mingle-ionapi.inforcloudsuite.com/<YOUR_TENANT>/GENAI/chatsvc`
- **SyteLine REST**: `https://[server]/<YOUR_TENANT>/CSI/IDORequestService/ido`

## Authentication

All APIs use API Key authentication via the `Authorization` header:
```
Authorization: Bearer <token>
```

For SyteLine REST API specifically:
- Obtain token via `/token/{config}/{username}/{password}` or `/token/{config}` with credentials in headers
- Required header for ION API calls: `X-Infor-MongooseConfig` (configuration name)

---

## GenAI Core Service API

### Tools Management

#### GET `/api/v1/tools`
Get list of all tools.

**Response**: Array of `ToolResponse` objects

#### GET `/api/v1/tools/{tool_guid}`
Get specific tool by GUID.

**Parameters**:
- `tool_guid` (path) - Tool GUID

**Response**: `ToolResponse` object

#### PUT `/api/v1/tools`
Upsert (create or update) a tool.

**Request Body**: `ToolRequest` object
**Response**: `ToolResponse` object

#### POST `/api/v1/tools`
Add multiple tools at once.

**Request Body**: Array of `ToolRequest` objects
**Response**: Array of `ToolResponse` objects

#### DELETE `/api/v1/tools/{tool_guid}`
Delete a specific tool.

**Parameters**:
- `tool_guid` (path) - Tool GUID

#### DELETE `/api/v1/tools`
Bulk delete tools.

**Request Body**: `ToolBulkDeleteRequest`
**Response**: Array of `ToolBulkDeleteResponse`

#### PUT `/api/v1/tools/enable`
Enable or disable a tool.

**Request Body**: `ToolEnableRequest`

#### POST `/api/v1/tools/search`
Search for tools.

**Request Body**: `SearchRequest`

#### POST `/api/v1/tools/search/semantic`
Semantic search for tools.

**Request Body**: `SemanticSearchRequest`

#### POST `/api/v1/tools/duplicate`
Duplicate a tool.

#### POST `/api/v1/tools/export`
Export tools.

#### POST `/api/v1/tools/import`
Import tools.

### Other Core Service Endpoints

- **Suggestions**: `/api/v1/suggestions`
- **Evaluations**: `/api/v1/evaluations`
- **Guardrails**: `/api/v1/guardrails`
- **IFS Roles**: `/api/v1/ifs/roles`
- **Namespaces**: `/api/v1/namespaces`
- **Settings**: `/api/v1/settings/*`
- **Registry**: `/api/v1/registry/products`
- **MCP Tools**: `/api/v1/mcp/tools`

---

## GenAI Chat Service API

### Prompt Execution

#### POST `/api/v1/prompt`
Execute a single prompt (non-streaming).

**Headers**:
- `x-infor-logicalidprefix` (required) - Logical ID prefix for agent selection

**Request Body**: `PromptRequest`
```json
{
  "prompt": "string",
  "model": "string (optional, defaults to CLAUDE)",
  "version": "string (optional)",
  "config": {
    "temperature": 1.0,
    "max_response": 4096,
    "top_p": 0.9
  },
  "encoded_image": "base64string (optional)",
  "document": {
    "format": "pdf|docx|csv|html|txt|md|doc|xlsx|xls",
    "name": "filename",
    "data": "base64string"
  }
}
```

**Response**: `PromptResponse`

#### POST `/api/v1/prompt/stream`
Execute a prompt with streaming response.

### Messages API (Advanced)

#### POST `/api/v1/messages`
Run messages API (non-streaming).

**Headers**:
- `x-infor-logicalidprefix` (required)

**Request Body**: `MessagesRequest`
```json
{
  "model": "CLAUDE",
  "version": "specific-version-id",
  "system": "system prompt",
  "messages": [
    {
      "role": "user|assistant",
      "content": [
        {
          "type": "text|image|document",
          "data": "text or base64"
        }
      ]
    }
  ],
  "config": {
    "temperature": 1.0,
    "max_response": 4096
  }
}
```

#### POST `/api/v1/messages/stream`
Run messages API with streaming.

### Chat Sessions

#### POST `/api/v1/chat`
Run chat (streaming).

**Request Body**: `ChatRequest`
```json
{
  "prompt": "user message",
  "session": "session-id (optional)",
  "tools": ["tool1", "tool2"],
  "toolInfo": {
    "toolName": {
      "stub": false
    }
  }
}
```

#### POST `/api/v1/chat/sync`
Run chat (synchronous, non-streaming).

**Response**: `ChatResponse`

#### GET `/api/v1/sessions`
Get all chat sessions.

**Response**: Array of `ChatSession` objects

#### GET `/api/v1/sessions/{session_id}/messages`
Get messages for a specific session.

**Query Parameters**:
- `page` (default: 1)
- `size` (default: 50)

#### PUT `/api/v1/sessions/{session_id}`
Update session (rename).

**Request Body**: `UpdateSessionRequest`

#### DELETE `/api/v1/sessions/{session_id}`
Delete a session.

### Models

#### GET `/api/v1/models`
Get list of available models.

**Response**: Array of `ModelDetail` objects

#### GET `/api/v1/models/tools`
Get list of models available for tools and agents.

**Response**: `ToolModelResponse`

---

## SyteLine REST API v2

This is the backend API that GenAI tools will call to interact with Infor data.

### Collections (IDO Operations)

#### GET `/load/{ido}`
Load records from a collection (IDO).

**Headers**:
- `Authorization`: Bearer token
- `X-Infor-MongooseConfig`: Configuration name (required for ION API)

**Parameters**:
- `ido` (path, required) - IDO name (e.g., "SLItems", "SLCoItem")
- `properties` (query, required) - Comma-delimited list or `*` for all
- `filter` (query, optional) - SQL WHERE clause
- `orderBy` (query, optional) - SQL ORDER BY
- `recordCap` (query, optional) - Max records (-1=default, 0=unlimited)
- `distinct` (query, optional) - SQL DISTINCT flag

**Response**: `LoadCollectionResponse`
```json
{
  "Success": true,
  "Message": "",
  "Items": [
    { /* item properties */ }
  ],
  "Bookmark": "",
  "MoreRowsExist": false
}
```

**Example**:
```
GET /load/SLItems?properties=Item,Description,UnitOfMeasure&filter=Item LIKE 'A%'&recordCap=10
```

#### POST `/update/{ido}`
Insert, update, or delete records.

**Parameters**:
- `ido` (path, required) - IDO name
- `refresh` (query, optional) - Refresh after update

**Request Body**: `UpdateCollectionRequest`
```json
{
  "IDOName": "SLItems",
  "RefreshAfterSave": true,
  "Changes": [
    {
      "Action": 1,  // 1=Insert, 2=Update, 4=Delete
      "ItemId": "",
      "Properties": [
        {
          "Name": "Item",
          "Value": "NEW001",
          "Modified": true
        }
      ]
    }
  ]
}
```

#### GET `/info/{ido}`
Get IDO metadata (property info).

**Response**: `GetPropertyInfoResponse` - includes property names, types, required fields, etc.

#### POST `/invoke/{ido}`
Invoke an IDO method.

**Parameters**:
- `ido` (path, required) - IDO name
- `method` (query, required) - Method name

**Request Body**: Array of parameter strings

### Configuration

#### GET `/configurations`
Get available configurations.

**Query Parameters**:
- `configGroup` (optional) - Filter by configuration group

### Security Token

#### GET `/token/{config}/{username}/{password}`
Get security token for API access.

#### GET `/token/{config}`
Get security token with credentials in headers.

**Headers**:
- `username`
- `password`

---

## Agent Execution Model

Based on the APIs, here's how agents work:

1. **Agents are not directly managed via REST API** - They appear to be configured through the UI and referenced via Logical IDs
2. **Agent invocation** happens through the Chat Service:
   - Use `/api/v1/chat` or `/api/v1/chat/sync`
   - Pass the Logical ID prefix in the `x-infor-logicalidprefix` header
   - The agent automatically has access to its configured tools
3. **Tool execution** is managed by the agent - when you chat with an agent, it decides which tools to use

## Tool Structure (from API)

Based on the schema references, a Tool likely contains:
- `name` - Tool name
- `description` - What the tool does
- `enabled` - Active status
- `model` - LLM model to use
- API connection details (source, method, endpoint)
- Request parameters schema
- Response interpretation instructions

## Key Insights

1. **Tools are managed via API** - Full CRUD operations available
2. **Agents are configured via UI** - Referenced by Logical ID in API calls
3. **Chat execution is flexible** - Can specify tools explicitly or use agent's default tools
4. **Authentication flows**:
   - For direct Mongoose calls: Get token via `/token` endpoint
   - For ION API calls: Use OAuth 2.0 Bearer token + `X-Infor-MongooseConfig` header
5. **Tools call backend APIs** - Typically SyteLine REST v2 or other Infor APIs

## Next Steps for Development

1. **Create a tool via API** using POST `/api/v1/tools`
2. **Test the tool** by invoking it through the Chat Service
3. **Create an agent via UI** that uses the tool (Logical ID assignment)
4. **Test the agent** via Chat Service with the Logical ID prefix
5. **Iterate and refine** based on results
