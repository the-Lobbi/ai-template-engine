# LangGraph Studio - Access Instructions

## 🚀 Your Orchestrator is Live!

The AI Template Engine LangGraph orchestrator is now running with visual Studio access.

### Access URLs

**LangGraph Studio UI:**
```
https://muslim-soon-engines-liable.trycloudflare.com
```

**API Documentation:**
```
https://muslim-soon-engines-liable.trycloudflare.com/docs
```

**API Endpoint:**
```
https://muslim-soon-engines-liable.trycloudflare.com/api
```

### Server Details

- **Status:** Running via Cloudflare Tunnel
- **Local Port:** 8123
- **Process ID:** Check `/tmp/ai-template-engine/langgraph.pid`
- **Logs:** `/tmp/ai-template-engine/langgraph.log`

### Workflow Visualization

The Studio UI shows the complete 7-phase orchestration workflow:

```
init → analyze → extract → generate → approval → setup → verify
```

With a **human-in-the-loop interrupt** at the `approval` node.

### How to Use Studio

1. **Open the Studio URL** in your browser (works from any device!)

2. **Create a New Thread**
   - Click "New Thread" in the Studio interface

3. **Provide Initial State:**
   ```json
   {
     "target_repo_path": "/path/to/your/repository",
     "target_repo_url": "https://github.com/org/repo",
     "harness_org_id": "your_org_id",
     "harness_project_id": "your_project_id",
     "hitl_required": true
   }
   ```

4. **Run the Workflow:**
   - Click "Run" to start execution
   - Watch each node execute in real-time
   - See state updates at each phase

5. **Approve at Interrupt:**
   - Workflow pauses at `approval` node
   - Review generated templates
   - Update state to approve:
     ```json
     {"hitl_approved": true}
     ```
   - Continue execution

### Server Management

**Check Status:**
```bash
cd /tmp/ai-template-engine
ps aux | grep langgraph | grep -v grep
```

**View Logs:**
```bash
tail -f /tmp/ai-template-engine/langgraph.log
```

**Stop Server:**
```bash
pkill -f "langgraph dev"
```

**Restart Server:**
```bash
cd /tmp/ai-template-engine
source venv/bin/activate
langgraph dev --no-browser --tunnel --port 8123 > langgraph.log 2>&1 &
echo $! > langgraph.pid
```

### Features Available

- **Visual Workflow Graph:** See all nodes and edges
- **Real-time Execution:** Watch nodes execute live
- **State Inspection:** View state at each step
- **Interrupt Points:** Interactive human approval
- **Message History:** See all AI messages
- **Error Tracking:** View errors and warnings
- **Replay:** Re-run workflows from any point

### Workflow Phases Explained

| Phase | Node | Purpose |
|-------|------|---------|
| 1 | `init` | Initialize workflow metadata and validate inputs |
| 2 | `analyze` | Analyze repository using MCP tools (Scaffold, Repomix) |
| 3 | `extract` | Extract CI/CD patterns and requirements with Claude |
| 4 | `generate` | Generate Harness pipeline templates with Claude |
| 5 | `approval` | **⏸ Human review and approval** |
| 6 | `setup` | Create Harness resources (connectors, secrets, pipeline) |
| 7 | `verify` | Verify deployment with test execution |

### Graph Structure

```python
from orchestrator import graph

# Graph nodes
assert "init" in graph.nodes
assert "analyze" in graph.nodes
assert "extract" in graph.nodes
assert "generate" in graph.nodes
assert "approval" in graph.nodes  # Interrupt point
assert "setup" in graph.nodes
assert "verify" in graph.nodes

# Interrupts (pause points)
assert "approval" in graph.interrupt_before
```

### Troubleshooting

**Studio not loading?**
- Check if server is running: `ps aux | grep langgraph`
- Check logs for errors: `tail -50 langgraph.log`
- Verify tunnel is active: `ps aux | grep cloudflared`

**Graph not appearing?**
- Verify installation: `pip show langgraph-cli`
- Check langgraph.json: `cat langgraph.json`
- Test import: `python -c "from orchestrator import graph; print('OK')"`

**Tunnel URL changed?**
- Cloudflare tunnels are temporary and URL changes on restart
- Check latest URL: `grep trycloudflare.com langgraph.log | tail -1`

### Security Note

⚠️ **Cloudflare Tunnels are temporary and public!**

- These tunnels have no auth and are publicly accessible
- Do not use in production
- Tunnels expire and URLs change on restart
- For production, use:
  - Named Cloudflare Tunnels with auth
  - SSH port forwarding
  - VPN access
  - LangGraph Cloud deployment

### Next Steps

1. **Open Studio** and explore the workflow visualization
2. **Run a test workflow** with a sample repository
3. **Experiment with state** at each phase
4. **Test approval workflow** by pausing and resuming
5. **Deploy to production** using LangGraph Cloud or containerization

---

**Generated:** 2026-01-16
**Server:** markus-server (Ubuntu Linux)
**LangGraph Version:** 0.6.39
**Runtime:** langgraph-runtime-inmem 0.22.1
