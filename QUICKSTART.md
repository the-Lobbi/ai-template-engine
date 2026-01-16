# Quick Start - AI Template Engine with LangGraph Studio

This guide will get you up and running with the AI Template Engine in LangGraph Studio.

## Prerequisites

- Python 3.11+
- Node.js 18+ (for MCP servers)
- LangGraph CLI
- Anthropic API key
- Harness account credentials

## Installation

### 1. Install Dependencies

```bash
# Install Python dependencies
pip install -e .

# Install LangGraph CLI
pip install langgraph-cli

# Install MCP CLI (if needed for MCP servers)
npm install -g @modelcontextprotocol/cli
```

### 2. Configure Environment

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your credentials
nano .env
```

Required environment variables:
- `ANTHROPIC_API_KEY` - Your Anthropic API key
- `HARNESS_ACCOUNT_ID` - Your Harness account ID
- `HARNESS_API_KEY` - Your Harness API key
- `HARNESS_ORG_ID` - Your Harness organization ID
- `HARNESS_PROJECT_ID` - Your Harness project ID

## Launch LangGraph Studio

### Option 1: Using CLI Command

```bash
# From project root
orchestrator studio
```

### Option 2: Using LangGraph Dev Server

```bash
# From project root
langgraph dev
```

This will:
1. Start the LangGraph development server
2. Launch Studio UI at http://localhost:8123
3. Load the `harness_orchestrator` graph automatically

## Using the Studio

### 1. Open Studio

Navigate to http://localhost:8123 in your browser.

### 2. Create a New Thread

Click "New Thread" to start a workflow session.

### 3. Provide Initial Input

In the Studio chat interface, provide the initial state:

```json
{
  "target_repo_path": "/path/to/your/repository",
  "target_repo_url": "https://github.com/org/repo",
  "harness_org_id": "your_org_id",
  "harness_project_id": "your_project_id",
  "hitl_required": true
}
```

### 4. Start Workflow

Click "Run" to start the orchestration workflow.

### 5. Visualize the Flow

Studio will show you:
- **Graph Visualization**: See the workflow structure
- **Node Execution**: Watch each node execute in real-time
- **State Updates**: View state changes at each step
- **Messages**: Read AI-generated messages
- **Interrupts**: Interact at approval points

### 6. Handle Human Approval

When the workflow reaches the `approval` node:

1. Review the generated templates in the message
2. Check the extracted patterns
3. Decide to approve or reject

To approve:
```json
{
  "hitl_approved": true
}
```

To reject with feedback:
```json
{
  "hitl_approved": false,
  "hitl_feedback": "Please adjust X, Y, Z"
}
```

### 7. Monitor Completion

Watch as the workflow:
1. Sets up Harness connectors
2. Creates secrets
3. Creates environments and services
4. Creates the pipeline
5. Runs verification

## CLI Usage (Alternative)

For non-interactive execution:

```bash
orchestrator orchestrate \
  /path/to/repo \
  --org my-org \
  --project my-project \
  --no-approval  # Skip approval step
```

## Workflow Phases

The orchestrator follows this flow:

```
init → analyze → extract → generate → approval → setup → verify → complete
```

1. **init**: Initialize workflow metadata
2. **analyze**: Analyze repository using MCP tools
3. **extract**: Extract CI/CD patterns
4. **generate**: Generate Harness templates
5. **approval**: Human approval (interrupt point)
6. **setup**: Create Harness resources
7. **verify**: Verify with test execution
8. **complete**: Workflow finished

## Debugging in Studio

### View State

Click any node to see:
- Input state
- Output state
- Execution time
- Errors (if any)

### Replay Execution

1. Select a past thread
2. Click any node
3. View historical state
4. Re-run from that point

### Modify State

At any interrupt:
1. Click "Edit State"
2. Modify state JSON
3. Continue execution

## Troubleshooting

### MCP Servers Not Working

```bash
# Test MCP server manually
npx -y @scaffoldly/mcp-server --help
npx -y @elizaos/mcp-repomix --help
```

### Studio Not Loading Graph

Check `langgraph.json`:
```json
{
  "graphs": {
    "harness_orchestrator": "./src/orchestrator/graph.py:graph"
  }
}
```

Verify the graph is exported:
```python
# In src/orchestrator/graph.py
__all__ = ["graph"]
```

### Approval Not Working

The workflow should pause at the `approval` node. If it doesn't:

1. Check `interrupt_before` in graph compilation:
   ```python
   graph = workflow.compile(
       checkpointer=memory,
       interrupt_before=["approval"],
   )
   ```

2. Ensure `hitl_required=True` in initial state

### State Not Updating

Ensure you're using the checkpointer:
```python
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()
graph = workflow.compile(checkpointer=memory)
```

## Next Steps

- Read [ARCHITECTURE.md](docs/ARCHITECTURE.md) for detailed design
- Review [AGENTS.md](docs/AGENTS.md) for agent documentation
- Check [MCP_INTEGRATION.md](docs/MCP_INTEGRATION.md) for MCP details
- See [WORKFLOWS.md](docs/WORKFLOWS.md) for workflow patterns

## Support

- GitHub Issues: https://github.com/the-Lobbi/ai-template-engine/issues
- Documentation: https://github.com/the-Lobbi/ai-template-engine
