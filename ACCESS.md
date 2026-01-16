# LangGraph Studio - Access Information

## 🚀 Server Running on Port 8888

**Status:** ✅ Running  
**Host:** 192.168.0.178  
**Port:** 8888  

---

## Access URLs

### SSH Port Forwarding (Recommended)

On your **local machine**, run:
```bash
ssh -L 8888:localhost:8888 markus@192.168.0.178
```

Then open:
```
https://smith.langchain.com/studio/?baseUrl=http://localhost:8888
```

### Direct Network Access

If on same network (192.168.0.x):
```
https://smith.langchain.com/studio/?baseUrl=http://192.168.0.178:8888
```

---

## Quick Test

1. Open Studio URL above
2. Click "New Thread"
3. Paste:
   ```json
   {
     "target_repo_path": "/tmp/ai-template-engine",
     "harness_org_id": "default",
     "harness_project_id": "AI_Orchestration",
     "hitl_required": true
   }
   ```
4. Click "Run"

---

## Server Management

**Check Status:**
```bash
curl http://localhost:8888/ok
```

**View Logs:**
```bash
tail -f /tmp/ai-template-engine/langgraph.log
```

**Stop:**
```bash
pkill -f "langgraph dev"
```

**Restart:**
```bash
cd /tmp/ai-template-engine
source venv/bin/activate
langgraph dev --no-browser --port 8888 > langgraph.log 2>&1 &
```

---

**API:** http://192.168.0.178:8888  
**Docs:** http://192.168.0.178:8888/docs  
**Health:** http://192.168.0.178:8888/ok
