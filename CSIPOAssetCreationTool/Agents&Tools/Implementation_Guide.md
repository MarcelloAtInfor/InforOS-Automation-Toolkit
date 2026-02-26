# Infor GenAI - Complete Implementation Guide

## Overview

This guide documents the complete process of creating and testing GenAI tools and agents programmatically via REST API.

**Status**: ✅ Successfully implemented and tested end-to-end

**Demo**: CustomerSearch_Agent using CustomerSearch_Tool to query SyteLine customer data

---

## Prerequisites

1. **ION API Credentials** (`.ionapi` file with OAuth credentials)
2. **Python 3.x** with `requests` library
3. **Access to Infor GenAI platform** (Core Service & Chat Service)

---

## Step 1: Authentication

### Obtain OAuth Token

```python
import requests
import base64
import json

# Load credentials from .ionapi file
with open('path/to/credentials.ionapi', 'r') as f:
    creds = json.load(f)

# Token endpoint
token_url = f"{creds['pu']}{creds['ot']}"

# Basic Auth header
auth_string = f"{creds['ci']}:{creds['cs']}"
encoded_auth = base64.b64encode(auth_string.encode()).decode()

headers = {
    'Authorization': f'Basic {encoded_auth}',
    'Content-Type': 'application/x-www-form-urlencoded'
}

# Request body - OAuth password grant with service account keys
data = {
    'grant_type': 'password',
    'username': creds['saak'],  # Service Account Access Key
    'password': creds['sask']   # Service Account Secret Key
}

response = requests.post(token_url, headers=headers, data=data)
token_data = response.json()
access_token = token_data['access_token']  # Valid for 120 minutes
```

**Key Points**:
- Use OAuth password grant type (not client_credentials)
- Service account keys go in username/password fields
- Client ID/Secret go in Basic Auth header
- Token expires after 7200 seconds (2 hours)

---

## Step 2: Create a Tool

### Tool Structure

Tools wrap backend APIs and tell the LLM how to use them.

```python
tool_definition = {
    "name": "CustomerSearch_Tool",
    "description": "Search for customers in CSI/Syteline by customer number or name",
    "type": "API_DOCS",  # Tools are type API_DOCS
    "inputs": None,
    "data": {
        "servicePath": "CSI/IDORequestService/ido",  # Backend API path
        "api_docs": """Method: GET
ENDPOINT: /load/SLCustomers

Headers:
X-Infor-MongooseConfig: <YOUR_SITE>

Query Parameters:
Parameter: properties
Format: STRING
Required: True
Description: Comma-separated list of properties (e.g., CustNum,Name,CustSeq)

Parameter: filter
Format: STRING
Required: False
Description: SQL WHERE clause (e.g., CustNum='CUST001' or Name LIKE 'ABC%')

Parameter: recordCap
Format: INTEGER
Required: False
Description: Max records to return (default: -1)""",
        "headers": {},
        "responseInstructions": """Returns JSON with Items array containing customer objects.
If found: Items contains customer data
If not found: Items is empty array
Success field indicates API call status""",
        "returnDirect": False,
        "model": {
            "model": "CLAUDE",
            "version": "claude-3-7-sonnet-20250219-v1:0"
        }
    },
    "status": 1,  # 1 = enabled, 0 = disabled
    "ignoreSearch": False,
    "utterances": [],
    "stubResponse": "",
    "instructions": "Use this tool to search for customers in CSI/Syteline by customer number or name. [MAX 900 CHARS]",
    "security": None
}
```

### Create Tool via API

```python
tools_url = "https://mingle-ionapi.inforcloudsuite.com/<YOUR_TENANT>/GENAI/coresvc/api/v1/tools"

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

response = requests.put(tools_url, headers=headers, json=tool_definition)
tool_response = response.json()
tool_guid = tool_response['guid']  # Save this GUID
```

**Key Points**:
- Use `PUT /api/v1/tools` to create or update tools
- `type: "API_DOCS"` designates this as a tool (not an agent)
- `instructions` field limited to 900 characters
- `api_docs` field contains full API documentation for the LLM
- `responseInstructions` tells LLM how to interpret API responses

---

## Step 3: Create an Agent

### Agent Structure

Agents orchestrate tools and manage workflows.

```python
agent_definition = {
    "name": "CustomerSearch_Agent",
    "description": "Agent to help users search for customer information",
    "type": "TOOLKIT",  # Agents are type TOOLKIT (not API_DOCS!)
    "inputs": None,
    "data": {
        "workflow": """You are a customer search assistant.

When users ask about customers:
1. Use the CustomerSearch_Tool
2. For exact matches: filter=CustNum='NUMBER'
3. For partial matches: filter=Name LIKE 'PARTIAL%'
4. Request properties: CustNum, Name, CustSeq

Present results clearly with customer number, name, and sequence.""",
        "tools": [
            "CustomerSearch_Tool"  # Array of tool names this agent can use
        ],
        "logicalIds": [
            "lid://infor.syteline.customer-search"  # Used to invoke this agent
        ],
        "model": {
            "model": "CLAUDE",
            "version": "claude-3-7-sonnet-20250219-v1:0"
        }
    },
    "status": 1,
    "ignoreSearch": False,
    "utterances": [
        "Find customer {customer_number}",
        "Search for customers",
        "Look up customer information"
    ],
    "stubResponse": "",
    "instructions": "Agent to search for customers using CustomerSearch_Tool. [MAX 900 CHARS]",
    "security": {
        "roles": []
    }
}
```

### Create Agent via API

```python
# Same endpoint as tools!
agents_url = "https://mingle-ionapi.inforcloudsuite.com/<YOUR_TENANT>/GENAI/coresvc/api/v1/tools"

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}

response = requests.put(agents_url, headers=headers, json=agent_definition)
agent_response = response.json()
agent_guid = agent_response['guid']
logical_id = agent_response['data']['logicalIds'][0]  # Save this!
```

**Key Points**:
- Agents created through same endpoint as tools: `/api/v1/tools`
- `type: "TOOLKIT"` designates this as an agent
- `data.workflow` contains agent workflow instructions
- `data.tools` array lists which tools the agent can use
- `data.logicalIds` array contains IDs for invoking the agent
- `utterances` provides sample phrases that trigger the agent

---

## Step 4: Test the Agent

### Invoke Agent via Chat API

```python
chat_url = "https://mingle-ionapi.inforcloudsuite.com/<YOUR_TENANT>/GENAI/chatsvc/api/v1/chat/sync"

headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
    'x-infor-logicalidprefix': 'lid://infor.syteline.customer-search'  # Critical!
}

chat_request = {
    "prompt": "Search for customers with name containing 'Corp'",
    "session": None  # Start new session, or provide existing session ID
}

response = requests.post(chat_url, headers=headers, json=chat_request, timeout=60)
chat_response = response.json()

print(f"Session ID: {chat_response['session']}")
print(f"Response: {chat_response['content']}")
print(f"Follow-ups: {chat_response['followups']}")
```

**Example Response**:
```
Based on the search, I found two customers with 'Corp' in their name:

1. Customer Number: AUCHRY1
   Name: Chrysler Corporation

2. Customer Number: AUCHRY1
   Name: Chrysler Corp, Windsor Plant

Both customers share the same customer number (AUCHRY1) but represent
different locations or entities within the Chrysler organization.
```

**Key Points**:
- Use `POST /api/v1/chat/sync` for synchronous responses
- Use `POST /api/v1/chat` for streaming responses
- **Critical**: `x-infor-logicalidprefix` header routes request to specific agent
- Session ID enables conversation continuity
- Agent automatically uses assigned tools
- Response includes content, followups, and optional links/screen navigation

---

## Complete Architecture

```
┌─────────────────┐
│  User Request   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Chat API                           │
│  POST /api/v1/chat/sync             │
│  Header: x-infor-logicalidprefix    │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Agent (CustomerSearch_Agent)       │
│  Type: TOOLKIT                      │
│  Logical ID: lid://...              │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Tool (CustomerSearch_Tool)         │
│  Type: API_DOCS                     │
│  Wraps SyteLine REST API            │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────┐
│  Backend API                        │
│  GET /load/SLCustomers              │
│  SyteLine REST v2                   │
└────────┬────────────────────────────┘
         │
         ▼
┌─────────────────┐
│  Response Flow  │
│  Backend →      │
│  Tool →         │
│  Agent →        │
│  User           │
└─────────────────┘
```

---

## API Endpoints Summary

| Purpose | Method | Endpoint | Headers |
|---------|--------|----------|---------|
| Get OAuth Token | POST | `{pu}{ot}` | Basic Auth |
| List Tools/Agents | GET | `/api/v1/tools` | Bearer Token |
| Get Tool/Agent | GET | `/api/v1/tools/{guid}` | Bearer Token |
| Create/Update Tool/Agent | PUT | `/api/v1/tools` | Bearer Token |
| Delete Tool/Agent | DELETE | `/api/v1/tools/{guid}` | Bearer Token |
| Chat with Agent | POST | `/api/v1/chat/sync` | Bearer Token + Logical ID |
| Stream Chat | POST | `/api/v1/chat` | Bearer Token + Logical ID |

---

## Key Differences: Tools vs Agents

| Aspect | Tool (API_DOCS) | Agent (TOOLKIT) |
|--------|-----------------|-----------------|
| **Type** | `API_DOCS` | `TOOLKIT` |
| **Purpose** | Wraps a single API endpoint | Orchestrates multiple tools |
| **Instructions Field** | `data.api_docs` | `data.workflow` |
| **Can Use Tools?** | No | Yes (via `data.tools` array) |
| **Invocation** | Called by agents | Called via logical ID header |
| **Logical ID** | N/A | Required (`data.logicalIds`) |
| **Response Handling** | `data.responseInstructions` | Formats tool outputs for user |

---

## Common Gotchas

1. **Instructions Limit**: Both tool and agent `instructions` fields are limited to 900 characters
2. **Same Endpoint**: Tools and agents use the same `/api/v1/tools` endpoint
3. **Type Matters**: `type: "API_DOCS"` for tools, `type: "TOOLKIT"` for agents
4. **Logical ID Required**: Agents need logical IDs to be invoked via Chat API
5. **Tool Names**: Agent's `data.tools` array uses tool names (not GUIDs)
6. **Authentication**: Service account keys go in OAuth request, not as direct Bearer tokens
7. **Mongoose Config**: Backend tools need `X-Infor-MongooseConfig` header

---

## Testing Checklist

- [ ] OAuth token obtained successfully
- [ ] Tool created and shows in UI/API list
- [ ] Tool has correct `type: "API_DOCS"`
- [ ] Agent created and shows in UI/API list
- [ ] Agent has correct `type: "TOOLKIT"`
- [ ] Agent has logical ID defined
- [ ] Agent's `data.tools` array includes your tool name
- [ ] Chat API returns 200 status
- [ ] Agent response includes expected data
- [ ] Backend API called successfully (check agent response)
- [ ] Follow-up suggestions generated

---

## Next Steps

1. **Add More Tools**: Create tools for other SyteLine operations (orders, items, vendors)
2. **Create Complex Agents**: Build agents that use multiple tools in sequence
3. **Error Handling**: Add error handling and validation to tools
4. **Testing**: Create automated tests for tools and agents
5. **Documentation**: Document custom tools and agents for team use
6. **Monitoring**: Track agent usage and performance

---

## Resources

- **API Documentation**: See `API_Documentation.md`
- **Scripts**: Located in `/scripts/` directory
- **Credentials**: `.ionapi` file in `/APIs/Creds/`
- **Swagger Files**: `/APIs/*.json`

---

**Status**: Production-ready implementation validated end-to-end
**Last Updated**: 2026-01-27
