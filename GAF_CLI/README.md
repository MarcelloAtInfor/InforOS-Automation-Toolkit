# Infor OS GenAI Agent Factory

A Python CLI toolkit for creating and managing Infor OS GenAI tools and agents programmatically. The Factory Agent uses a two-step DRAFT -> CONFIRM PUBLISH workflow for safe, validated asset creation.

## What This Is

The Agent Factory is a self-referential system that creates, updates, and manages Infor OS GenAI assets. It consists of:

- **Factory Tools** (5 API_DOCS type tools): ListAssets, GetAsset, CreateTool, CreateAgent, UpdateAsset
- **Factory Agent** (1 TOOLKIT type agent): Orchestrates the Factory Tools with a safety workflow

**Who it's for:** Python developers who want to publish GenAI tools to Infor OS without manual JSON editing or direct API calls.

**What you can do:**
- Create API_DOCS tools from JSON specifications
- Create TOOLKIT agents that orchestrate multiple tools
- Update existing assets with version control
- Validate naming conventions and portability rules automatically
- Invoke agents programmatically or interactively

## Quick Start

### 1. Prerequisites

- Python 3.11+
- Infor OS .ionapi credentials file
- Network access to Infor OS tenant

### 2. Setup

```bash
# Clone repository
git clone <repo-url>
cd agent-factory

# Install dependencies
pip install -r requirements.txt

# Set credentials (Windows)
set IONAPI_FILE=C:\path\to\your\credentials.ionapi

# Set credentials (Linux/Mac)
export IONAPI_FILE=/path/to/your/credentials.ionapi
```

### 3. Verify Setup

```bash
python -m src.cli.list_assets --prefix GAF
```

**Expected output:**
```
Found 6 tools:
- GAF_GenAI_ListAssets_Tool_v1 (<GUID>)
- GAF_GenAI_GetAsset_Tool_v1 (<GUID>)
- GAF_GenAI_CreateTool_Tool_v1 (<GUID>)
- GAF_GenAI_CreateAgent_Tool_v1 (<GUID>)
- GAF_GenAI_UpdateAsset_Tool_v1 (<GUID>)
- GAF_GenAI_AgentFactory_Agent_v1 (<GUID>)
```

### 4. Create Your First Tool

```bash
python -m src.cli.invoke_agent "Create a tool called GAF_GenAI_HelloWorld_Tool_v1 that returns a greeting"
```

The agent shows a DRAFT. Type `CONFIRM PUBLISH` to create the tool.

## Factory Workflow

```
User Request
     |
     v
+-------------------+
|  Factory Agent    |
|  - Validates name |
|  - Checks rules   |
|  - Generates spec |
+--------+----------+
         |
         v
+-------------------+
|   DRAFT shown     |
| "Type CONFIRM     |
|  PUBLISH to       |
|  proceed"         |
+--------+----------+
         |
    +----+----+
    | Confirm?|
    +----+----+
         |
    +----+--------+
    |             |
   YES            NO
    |             |
    v             v
+-------+     +------+
|Publish|     | End  |
|  API  |     |(safe)|
+-------+     +------+
```

**Why two-step?** Safety without external approval workflow. DRAFT shows exactly what will be created; nothing publishes without explicit CONFIRM PUBLISH.

## CLI Commands

| Command | Purpose |
|---------|---------|
| `python -m src.cli.list_assets` | List tools/agents with filtering |
| `python -m src.cli.publish_tool <spec>` | Publish tool from JSON spec |
| `python -m src.cli.publish_agent <spec>` | Publish agent from JSON spec |
| `python -m src.cli.update_asset <spec>` | Update existing asset |
| `python -m src.cli.invoke_agent "<prompt>"` | Chat with Factory Agent |
| `python scripts/smoke_test.py` | Run end-to-end verification |

See [docs/usage.md](docs/usage.md) for complete command reference with examples.

## Infor OS GenAI Concepts

New to Infor OS GenAI? Here's what you need to know:

| Concept | Description |
|---------|-------------|
| **Tool** | A GenAI capability defined by JSON spec. Type: API_DOCS for CRUD operations. |
| **Agent** | A TOOLKIT-type tool that orchestrates other tools. |
| **Chat API** | `/api/v1/chat/sync` - invoke agents with natural language. |
| **servicePath** | Relative path to API (e.g., "GENAI/coresvc"). Never hardcode tenant URLs. |
| **.ionapi** | Infor credential file containing OAuth client_id, secret, and endpoints. |

## Naming Convention

All assets MUST follow this pattern:
```
GAF_<product>_<Capability>_(Tool|Agent)_v<N>
```

Examples:
- `GAF_GenAI_ListAssets_Tool_v1`
- `GAF_GenAI_AgentFactory_Agent_v1`
- `GAF_SyteLine_InventoryLookup_Tool_v1`

## Example: Full Tool Specification

```json
{
  "name": "GAF_GenAI_HelloWorld_Tool_v1",
  "description": "Returns a greeting message",
  "type": "API_DOCS",
  "instructions": "Call this tool to get a greeting. No parameters required.",
  "inputs": [],
  "data": {
    "servicePath": "GENAI/coresvc",
    "api_docs": "Method: GET\nEndpoint: /api/v1/tools\nReturns: List of tools as greeting example",
    "headers": {},
    "responseInstructions": "Return the greeting message from the response",
    "returnDirect": false,
    "model": {
      "model": "CLAUDE",
      "version": "claude-3-7-sonnet-20250219-v1:0"
    }
  },
  "status": 1,
  "utterances": ["say hello", "greet me"]
}
```

**Key fields:**
- 
ame`: Must follow naming convention
- `type`: `"API_DOCS"` for tools, `"TOOLKIT"` for agents
- `servicePath`: Relative path (no tenant URL for portability)
- `instructions`: Brief description (<200 chars recommended)

## Project Structure

```
agent-factory/
├── README.md              # This file
├── CLAUDE.md              # AI assistant rules
├── requirements.txt       # Python dependencies
├── docs/
│   ├── architecture.md    # Factory pattern explanation
│   └── usage.md           # CLI reference and tutorials
├── log.md                 # Decision log
├── specs/
│   ├── tools/             # Factory Tool specifications
│   ├── agents/            # Factory Agent specification
│   └── examples/          # Example specs (HelloWorld)
├── scripts/
│   └── smoke_test.py      # End-to-end verification
└── src/
    ├── cli/               # CLI scripts
    ├── infor_os/          # GenAI API client
    └── shared/            # Config, auth, logging, validation
```

## Documentation

- [Architecture](docs/architecture.md) - Factory pattern, two-step workflow, versioning
- [Usage Guide](docs/usage.md) - Tutorials and CLI reference
- [Decision Log](log.md) - Design decisions and rationale

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| IONAPI_FILE | Yes | Path to .ionapi credentials file |
| LOG_LEVEL | No | DEBUG, INFO, WARNING, ERROR (default: INFO) |

## Troubleshooting

**"Invalid name format"**
- Name doesn't match `GAF_<product>_<Capability>_(Tool|Agent)_v<N>` pattern

**"Token acquisition failed"**
- Check IONAPI_FILE path and .ionapi file contents

**"API returned 500"**
- Transient platform error. Retry after a few seconds.

See [docs/usage.md#common-errors](docs/usage.md#common-errors) for more.

## Contributing

1. Follow naming convention strictly
2. Test with smoke_test.py before committing
3. Verify in Infor OS GenAI UI
4. Document decisions in log.md

## License

[Specify license here]


## Agent-Agnostic Usage (Claude + Codex)

This folder is designed to work with both Claude Code and Codex.

Shared guide:
- AGENT_GUIDE.md

Agent adapter files:
- AGENTS.md (Codex)
- CLAUDE.md (Claude)

Read order:
1. AGENT_GUIDE.md
2. CLAUDE.md
3. log.md



