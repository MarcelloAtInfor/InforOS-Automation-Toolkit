# Architecture: Infor OS GenAI Agent Factory

## Overview

The Infor OS GenAI Agent Factory is a self-referential system that creates and manages Tools and Agents programmatically on the Infor OS GenAI platform. The Factory itself is a TOOLKIT agent that orchestrates five API_DOCS tools to perform CRUD operations on GenAI assets. The core value proposition is a two-step DRAFT -> CONFIRM workflow that provides safety without requiring external approval processes.

## Infor OS GenAI Concepts

For developers new to Infor OS GenAI, understanding these platform concepts is essential:

### Tools

Tools are the atomic units of functionality in Infor OS GenAI. They come in multiple types:

- **API_DOCS**: Tools defined by JSON specification that make API calls or perform operations. Most common type for custom functionality.
- **OPENAPI_SCHEMA**: Tools generated from OpenAPI/Swagger specifications.
- **DOCUMENT_RETRIEVER**: Tools that query document stores.
- **SCRIPT**: Executable scripts.
- **API**: Direct API endpoint integrations.
- **TOOLKIT**: Special type for agents (see below).

Tools are defined by JSON specifications containing:
- `name`: Unique identifier following naming conventions
- `description`: What the tool does
- `type`: One of the ToolType enum values
- `instructions`: How to use the tool (for API_DOCS, this is the API request specification)
- `inputSchema`: JSON Schema defining expected inputs
- `guid`: Unique identifier assigned by platform (read-only after creation)

Tools are invoked via the Chat API (`/api/v1/chat/sync`) by passing their name in the request.

### Agents

Agents are orchestrators that chain multiple tools together to accomplish complex tasks. In Infor OS GenAI, agents are implemented as special tools with `type: "TOOLKIT"`.

Key characteristics:
- **Type**: Must be TOOLKIT (not API_DOCS or other types)
- **Tools Array**: Contains references to the tools the agent can use
- **Workflow**: Instructions for how to orchestrate tool invocations
- **State Management**: Can maintain conversation context across multiple user inputs

Agents are invoked the same way as tools - via the Chat API. The platform routes requests to the agent and provides access to its configured tools.

### Chat API

The Chat API (`/api/v1/chat/sync`) is the primary interface for invoking both tools and agents. It accepts:

```json
{
  "message": "User request or instruction",
  "tool": "ToolOrAgentName",
  "sessionId": "optional-session-id-for-context"
}
```

The API returns a synchronous response containing the tool/agent output.

### ServicePath

All GenAI API endpoints use relative `servicePath` values, not absolute URLs. This ensures portability across tenants:

- **Correct**: `/GENAI/coresvc/api/v1/tools`
- **Incorrect**: `https://mingle-ionapi.inforcloudsuite.com/TENANT/GENAI/coresvc/api/v1/tools`

The client library (GenAIClient) handles composing the full URL from the tenant's base URL and the relative service path.

### ToolType Enum

The platform recognizes these tool types:

```python
UNKNOWN = 0
API_DOCS = 1
OPENAPI_SCHEMA = 2
DOCUMENT_RETRIEVER = 3
TOOLKIT = 4
SCRIPT = 5
API = 6
```

For Factory Tools (CRUD operations), we use `API_DOCS`. For the Factory Agent (orchestrator), we use `TOOLKIT`.

## Factory Pattern

The Agent Factory uses a hierarchical pattern where a TOOLKIT agent orchestrates multiple API_DOCS tools.

### Factory Components

**Factory Agent (TOOLKIT type)**
- Name: `GAF_GenAI_AgentFactory_Agent_v1`
- Type: TOOLKIT
- Purpose: Orchestrates tool/agent creation workflow
- Tools: Uses 5 Factory Tools for CRUD operations

**Factory Tools (API_DOCS type)**
1. **ListAssets**: Query all tools and agents in the environment
2. **GetAsset**: Retrieve full specification of a specific tool/agent
3. **CreateTool**: Publish new API_DOCS tool specifications
4. **CreateAgent**: Publish new TOOLKIT agent specifications
5. **UpdateAsset**: Modify existing tool/agent specifications

### Why TOOLKIT for the Agent?

The Infor OS GenAI platform requires agents to be type TOOLKIT. This is the designated type for orchestrators that coordinate multiple tools. When you invoke a TOOLKIT agent via the Chat API, the platform:
1. Routes the request to the agent's workflow logic
2. Provides access to the tools configured in the agent's `data.tools` array
3. Manages the conversation context and state

### Why API_DOCS for the Tools?

API_DOCS is the appropriate type for Factory Tools because:
- They perform specific, well-defined operations (list, get, create, update)
- They interact with the GenAI Core API endpoints
- They accept structured inputs and return structured outputs
- They fit the request/response pattern of API_DOCS tools

Other types (OPENAPI_SCHEMA, DOCUMENT_RETRIEVER, etc.) are for specialized use cases that don't match our CRUD requirements.

## Two-Step Workflow

The Factory Agent implements a safety mechanism: users review generated specifications before they're published.

### Workflow Diagram

```
   User Request ("Create a HelloWorld tool")
        |
        v
+-------------------+
| Factory Agent     |
| - Validates name  |
| - Checks rules    |
| - Generates spec  |
+--------+----------+
         |
         v
+-------------------+
|    DRAFT shown    |
| "Type CONFIRM     |
|  PUBLISH to       |
|  proceed"         |
+--------+----------+
         |
    +----+----+
    | Confirm?|
    +----+----+
         |
    +----+----+
    |         |
   YES        NO
    |         |
    v         v
+-------+  +------+
|Publish|  | End  |
| via   |  |(safe)|
| Create|  +------+
| Tool  |
+-------+
```

### Why Two-Step?

The two-step workflow addresses a critical safety requirement:

1. **Prevents Accidental Creates**: Users might ask exploratory questions like "What would a tool look like for X?" Without the confirmation step, the agent might misinterpret this as a creation request.

2. **Enables Review**: Complex specifications may have subtle issues (naming violations, portability problems, incorrect schemas). The draft review catches these before publication.

3. **No External Approval Needed**: Some organizations require external approval workflows (tickets, manager sign-off, etc.). The two-step workflow provides safety without infrastructure overhead.

4. **Clear Intent Signal**: The exact phrase "CONFIRM PUBLISH" (case-insensitive) is unambiguous. There's no confusion about whether the user wants to proceed.

### Confirmation Phrase

The trigger is: **CONFIRM PUBLISH** (case-insensitive)

Examples that work:
- "confirm publish"
- "CONFIRM PUBLISH"
- "Confirm Publish"

Examples that don't trigger:
- "yes"
- "ok"
- "publish"
- "go ahead"

The specificity is intentional - generic affirmations might appear in exploratory conversation.

## Versioning Strategy

Factory-created assets follow a consistent naming and versioning approach.

### Naming Convention

Format: `GAF_<Product>_<Capability>_<Type>_v<N>`

- **GAF**: "GenAI Agent Factory" prefix identifies factory-created assets
- **Product**: Product domain (GenAI, IPA, Lawson, etc.)
- **Capability**: What the asset does (HelloWorld, InvoiceValidator, etc.)
- **Type**: Tool or Agent
- **vN**: Version number (v1, v2, etc.)

Examples:
- `GAF_GenAI_ListAssets_Tool_v1`
- `GAF_GenAI_AgentFactory_Agent_v1`
- `GAF_IPA_InvoiceValidator_Tool_v1`

### Update vs New Version

**Update in place (same version):**
- Bug fixes (incorrect logic, wrong error messages)
- Clarifications (better descriptions, clearer instructions)
- Non-breaking changes (adding optional fields, expanding accepted values)

**Create new version (_v2):**
- Breaking changes to input schema (removing fields, changing field types, making optional fields required)
- Instruction changes that alter behavior (different API endpoints, changed validation rules)
- Type changes (API_DOCS to TOOLKIT, though this is rare)

### Breaking Change Definition

A change is breaking if:
1. Existing clients would fail with the new version
2. The input schema changes in incompatible ways
3. The behavior changes such that previous valid inputs produce different outputs

Examples:
- **Breaking**: Removing a field from inputSchema
- **Breaking**: Changing field type from string to number
- **Breaking**: Changing API endpoint in instructions
- **Non-breaking**: Adding optional field to inputSchema
- **Non-breaking**: Fixing bug that caused incorrect output
- **Non-breaking**: Clarifying description text

## Component Architecture

The Agent Factory is implemented as a Python CLI application with these layers:

```
+------------------+
|   CLI Scripts    |  (invoke_agent.py, publish_tool.py, list_assets.py, etc.)
+--------+---------+
         |
         v
+------------------+
|   GenAI Client   |  (src/infor_os/genai_client.py)
| - list_tools()   |
| - get_tool()     |
| - create_tools() |
| - update_tool()  |
| - delete_tool()  |
| - chat_sync()    |
+--------+---------+
         |
         v
+------------------+
|   HTTP Client    |  (src/infor_os/http_client.py)
| - Retry logic    |
| - Backoff        |
+--------+---------+
         |
         v
+------------------+
|   OAuth Auth     |  (src/infor_os/oauth_client.py)
| - Token fetch    |
| - Token cache    |
| - Expiry check   |
+--------+---------+
         |
         v
+------------------+
|  Infor OS APIs   |
| - Token endpoint |
| - GenAI Core API |
| - GenAI Chat API |
+------------------+
```

### Layer Responsibilities

**CLI Scripts** (`scripts/`)
- User-facing commands
- Argument parsing
- Output formatting
- Error handling for end users

**GenAI Client** (`src/infor_os/genai_client.py`)
- High-level operations (list, get, create, update, delete, chat)
- Request/response mapping
- Error translation

**HTTP Client** (`src/infor_os/http_client.py`)
- HTTP operations (GET, POST, PUT, DELETE)
- Retry with exponential backoff
- Timeout handling

**OAuth Client** (`src/infor_os/oauth_client.py`)
- Token acquisition using password grant flow
- Token caching with 60-second expiry margin
- Automatic refresh

**Configuration** (`src/infor_os/config.py`)
- .ionapi file parsing
- Environment variable support
- Credential validation and redaction

**Validation** (`src/shared/validation.py`)
- Naming convention enforcement
- Portability checks (servicePath, no tenant URLs)
- Input schema validation

## Key Files

| File | Purpose |
|------|---------|
| `scripts/invoke_agent.py` | CLI for invoking Factory Agent or other agents |
| `scripts/publish_tool.py` | CLI for publishing tool specifications |
| `scripts/publish_agent.py` | CLI for publishing agent specifications |
| `scripts/list_assets.py` | CLI for listing all tools and agents |
| `scripts/update_asset.py` | CLI for updating existing assets |
| `scripts/smoke_test.py` | End-to-end factory loop verification |
| `src/infor_os/genai_client.py` | GenAI API client with CRUD operations |
| `src/infor_os/http_client.py` | HTTP client with retry logic |
| `src/infor_os/oauth_client.py` | OAuth token manager |
| `src/infor_os/config.py` | Configuration parser for .ionapi files |
| `src/shared/validation.py` | Naming and portability validation |
| `src/shared/errors.py` | Structured error responses |
| `specs/factory_agent.json` | Factory Agent TOOLKIT specification |
| `specs/tools/*.json` | Factory Tool API_DOCS specifications |

## Security Considerations

### Credential Management

- Never log credentials (SAAK/SASK)
- Redaction patterns catch 95%+ of leak scenarios
- .ionapi files rejected if > 1MB (injection defense)
- Tokens cached in memory only (not persisted to disk)

### Input Validation

- Naming convention enforcement prevents malicious names
- ServicePath validation ensures portability and prevents tenant URL leakage
- Input schema validation catches type mismatches before API calls

### API Safety

- OAuth password grant flow (platform requirement)
- 60-second token expiry margin prevents mid-request expiry
- Retry with exponential backoff respects platform rate limits
- 300-second timeout prevents hung operations

## Future Extensions

Potential enhancements to the Factory Agent:

1. **Version Management**: Automatic version bumping based on change analysis
2. **Dependency Tracking**: Track which tools an agent uses, suggest updates
3. **Batch Operations**: Create multiple related tools in one request
4. **Template Library**: Pre-built templates for common tool patterns
5. **Validation Extensions**: Custom validation rules per product domain
6. **Rollback**: Revert to previous version if new version fails
7. **Testing Integration**: Automated test generation for new tools

---

*Generated: 2026-02-02*
*Part of Phase 5: Documentation*
