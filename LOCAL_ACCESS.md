# LangGraph Studio - Local Network Access

## 🚀 Server Running Locally

The AI Template Engine is running on your local network without external tunnels.

### Local Access URLs

**From the Server (localhost):**
```
Studio UI: https://smith.langchain.com/studio/?baseUrl=http://127.0.0.1:8123
API: http://127.0.0.1:8123
API Docs: http://127.0.0.1:8123/docs
```

**From Other Devices on Network:**
```
Studio UI: https://smith.langchain.com/studio/?baseUrl=http://192.168.0.178:8123
API: http://192.168.0.178:8123
API Docs: http://192.168.0.178:8123/docs
```

### Server Status

```bash
# Check if server is running
ps aux | grep "langgraph dev" | grep -v grep

# Test server response
curl http://localhost:8123/ok
# Should return: {"ok":true}

# View logs
tail -f /tmp/ai-template-engine/langgraph.log
```

**Current Status:**
- ✅ Server running (PID in `/tmp/ai-template-engine/langgraph.pid`)
- ✅ Port: 8123
- ✅ Host: 0.0.0.0 (accessible from network)
- ✅ Graph loaded: `harness_orchestrator`

### Access from Your Machine via SSH

Since you're SSH'd into the server, you have two options to access Studio:

#### Option 1: SSH Port Forwarding (Recommended)

On your **local machine**, create an SSH tunnel:

```bash
ssh -L 8123:localhost:8123 markus@192.168.0.178
```

Then open on your local machine:
```
https://smith.langchain.com/studio/?baseUrl=http://localhost:8123
```

#### Option 2: Direct Network Access

If your local machine is on the same network (192.168.0.x):

```
https://smith.langchain.com/studio/?baseUrl=http://192.168.0.178:8123
```

### LangGraph Studio Interface

The Studio UI is hosted by LangChain at `smith.langchain.com/studio` and connects to your local API server via the `baseUrl` parameter.

**Features Available:**
- Visual workflow graph
- Real-time execution monitoring
- State inspection at each node
- Human-in-the-loop approval workflow
- Message history
- Execution replay
- Error tracking

### Workflow Visualization

Once in Studio, you'll see the complete orchestration graph:

```
┌─────────┐
│  init   │ → Initialize workflow metadata
└────┬────┘
     │
┌──────────┐
│ analyze  │ → Analyze repository with MCP tools
└────┬─────┘
     │
┌──────────┐
│ extract  │ → Extract CI/CD patterns
└────┬─────┘
     │
┌──────────┐
│ generate │ → Generate Harness templates
└────┬─────┘
     │
┌──────────┐
│ approval │ → ⏸ HUMAN APPROVAL (interrupt)
└────┬─────┘
     │
┌──────────┐
│  setup   │ → Create Harness resources
└────┬─────┘
     │
┌──────────┐
│  verify  │ → Verify deployment
└──────────┘
```

### Running a Workflow

1. **Open Studio** with the baseUrl pointing to your server
2. **Create New Thread**
3. **Provide Initial Input:**
   ```json
   {
     "target_repo_path": "/tmp/ai-template-engine",
     "target_repo_url": "https://github.com/the-Lobbi/ai-template-engine",
     "harness_org_id": "default",
     "harness_project_id": "AI_Orchestration",
     "hitl_required": true
   }
   ```
4. **Click "Run"** to start the workflow
5. **Watch Execution** in real-time
6. **At Approval Node**: Update state with `{"hitl_approved": true}` to continue

### Server Management

**Stop Server:**
```bash
pkill -f "langgraph dev"
```

**Restart Server:**
```bash
cd /tmp/ai-template-engine
source venv/bin/activate
langgraph dev --no-browser --port 8123 > langgraph.log 2>&1 &
echo $! > langgraph.pid
```

**Check Server Health:**
```bash
curl http://localhost:8123/ok
curl http://localhost:8123/info
```

### API Endpoints

**Health Check:**
```bash
GET http://192.168.0.178:8123/ok
```

**List Graphs:**
```bash
GET http://192.168.0.178:8123/graphs
```

**Get Graph Info:**
```bash
GET http://192.168.0.178:8123/graphs/harness_orchestrator
```

**API Documentation:**
```bash
GET http://192.168.0.178:8123/docs
```

### Firewall Configuration

If you can't access from other devices on the network, you may need to open port 8123:

```bash
# For UFW (Ubuntu)
sudo ufw allow 8123/tcp

# For firewalld (CentOS/RHEL)
sudo firewall-cmd --permanent --add-port=8123/tcp
sudo firewall-cmd --reload
```

### Troubleshooting

**Server not responding?**
```bash
# Check if process is running
ps aux | grep langgraph

# Check logs for errors
tail -50 /tmp/ai-template-engine/langgraph.log

# Test connectivity
curl -v http://localhost:8123/ok
```

**Studio UI not loading?**
- Verify the baseUrl in the Studio URL matches your server
- Check browser console for CORS errors
- Ensure server is accessible from your machine
- Try SSH port forwarding if direct access doesn't work

**Graph not appearing?**
```bash
# Verify graph loaded successfully
curl http://localhost:8123/graphs | jq

# Should show: {"graphs": ["harness_orchestrator"]}
```

### Security Notes

🔒 **Local Network Only**
- Server is accessible to anyone on your local network (192.168.0.x)
- No authentication configured (dev mode)
- For production, use LangGraph Cloud or add authentication

### System Resources

**Memory Usage:**
```bash
ps aux | grep langgraph | awk '{print $6/1024 " MB"}'
```

**Logs Disk Space:**
```bash
ls -lh /tmp/ai-template-engine/langgraph.log
```

---

**Server:** markus-server (192.168.0.178)
**Port:** 8123
**Protocol:** HTTP (no TLS in dev mode)
**LangGraph API:** 0.6.39
**Graph:** harness_orchestrator (7 nodes)
**Started:** 2026-01-16 23:45:45
