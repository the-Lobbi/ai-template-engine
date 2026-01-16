# AI Template Engine

> **LangGraph-based orchestration system for automated repository analysis and Harness CI/CD setup**

[![GitHub](https://img.shields.io/badge/GitHub-the--Lobbi-blue)](https://github.com/the-Lobbi/ai-template-engine)
[![Harness](https://img.shields.io/badge/Harness-lobbi--ai-orange)](https://app.harness.io)
[![Python](https://img.shields.io/badge/Python-3.11+-green)](https://python.org)

## Overview

The AI Template Engine is an intelligent orchestration system that:

1. 📊 **Analyzes** source repositories to understand structure, technologies, and deployment patterns
2. 🔍 **Extracts** deployment requirements and CI/CD patterns automatically
3. 🎯 **Generates** optimized Harness templates (pipelines, stages, steps)
4. 🚀 **Automates** complete Harness platform setup (connectors, secrets, environments, services)
5. ✅ **Verifies** deployment with initial test executions

All powered by **LangGraph** multi-agent workflows with **Claude Sonnet 4.5** and **MCP (Model Context Protocol)** tool integration.

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                        LangGraph Orchestrator                                │
│                                                                              │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌────────┐   ┌─────────┐     │
│  │ Analyze │-->│  Extract │-->│ Generate │-->│  Setup │-->│ Verify  │     │
│  │  Repo   │   │ Patterns │   │Templates │   │Harness │   │ Deploy  │     │
│  └─────────┘   └──────────┘   └──────────┘   └────────┘   └─────────┘     │
│       │             │              │              │             │           │
│       ▼             ▼              ▼              ▼             ▼           │
│  ┌─────────┐   ┌──────────┐   ┌──────────┐   ┌────────┐   ┌─────────┐     │
│  │  Repo   │   │ Pattern  │   │Template  │   │Harness │   │ Deploy  │     │
│  │  Agent  │   │  Agent   │   │  Agent   │   │ Setup  │   │  Agent  │     │
│  │         │   │          │   │          │   │  Agent │   │         │     │
│  └─────────┘   └──────────┘   └──────────┘   └────────┘   └─────────┘     │
│                                                                              │
│                         MCP Integration Layer                                │
│          ┌──────────────┬───────────────┬──────────────────┐                │
│          │  Harness MCP │ Scaffold MCP  │   GitHub MCP     │                │
│          │    Server    │    Server     │     Server       │                │
│          └──────────────┴───────────────┴──────────────────┘                │
└──────────────────────────────────────────────────────────────────────────────┘
```

---

## Key Features

### 🤖 **Multi-Agent Orchestration**

- **Repository Analysis Agent**: Deep code analysis with Repomix integration
- **Pattern Extraction Agent**: Intelligent deployment pattern detection
- **Template Generation Agent**: Harness-optimized template creation
- **Harness Setup Agent**: Automated platform configuration
- **Deployment Agent**: Verification and validation

### 🔧 **MCP Tool Integration**

- **Harness MCP**: Direct Harness API access for all operations
- **Scaffold MCP**: Repository analysis and code pattern detection
- **GitHub MCP**: Git operations and repository management
- **Filesystem MCP**: Local file operations

### 🧠 **Intelligent Pattern Detection**

Automatically detects:
- Project types (microservice, monolith, library, ETL, frontend, infrastructure)
- Deployment targets (Kubernetes, ECS, Lambda, VM, static hosting)
- CI requirements (build, test, scan, publish)
- CD requirements (environments, strategies, approvals)
- Infrastructure needs (connectors, secrets, delegates)

### 🎯 **Complete Harness Automation**

Creates and configures:
- ✅ Organizations and Projects
- ✅ Connectors (Git, Docker, Cloud Providers, K8s)
- ✅ Secrets (tokens, credentials, API keys)
- ✅ Delegates (Kubernetes, Docker)
- ✅ Services (with manifests and artifacts)
- ✅ Environments (Dev, Staging, Production)
- ✅ Infrastructure Definitions
- ✅ Templates (Step, Stage, Pipeline)
- ✅ Pipelines (CI, CD, CI/CD combined)

### 👤 **Human-in-the-Loop**

- Approval gates before critical changes
- Plan modification capabilities
- Progress streaming with real-time updates
- Error recovery with detailed reporting

---

## Installation

### Prerequisites

- Python 3.11+
- Docker (for MCP servers)
- Node.js 18+ (for Scaffold and GitHub MCP servers)
- Harness account with API access
- GitHub account (optional, for source repositories)

### Install Dependencies

```bash
# Clone the repository
git clone https://github.com/the-Lobbi/ai-template-engine.git
cd ai-template-engine

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install MCP servers
npm install -g @agiflowai/scaffold-mcp
npm install -g @modelcontextprotocol/server-github
```

### Configure Environment

```bash
# Copy example environment file
cp .env.example .env

# Edit .env and add your credentials
# Required:
export HARNESS_API_KEY="pat.ErW8whvyRY22hTaA3uAESA.xxx.yyy"
export HARNESS_ORG_ID="default"
export ANTHROPIC_API_KEY="sk-ant-xxx"

# Optional:
export GITHUB_TOKEN="ghp_xxx"
export HARNESS_BASE_URL="https://app.harness.io"
```

---

## Usage

### CLI Interface

```bash
# Basic usage - analyze and setup with approval
python -m orchestrator.main https://github.com/myorg/my-service

# Auto-approve (skip approval step)
python -m orchestrator.main https://github.com/myorg/my-service --auto-approve

# Target specific project
python -m orchestrator.main https://github.com/myorg/my-service \
  --project-id my_project \
  --org-id my_org

# Full example
python -m orchestrator.main \
  https://github.com/acme/payment-service \
  --project-id payments \
  --org-id production \
  --auto-approve
```

### Python API

```python
from orchestrator import HarnessAutomationOrchestrator

# Initialize orchestrator
orchestrator = HarnessAutomationOrchestrator(
    harness_api_key="pat.xxx",
    harness_org_id="default"
)

# Run complete automation
result = await orchestrator.run(
    source_repo="https://github.com/myorg/my-service",
    target_project_id="my_project",
    auto_approve=False,
    stream=True
)

# Check result
if result["current_phase"] == "complete":
    print(f"✅ Created {len(result['harness_setup'].pipelines_created)} pipelines")
else:
    print(f"❌ Errors: {result['errors']}")
```

### Interactive Approval Mode

```python
# Start automation (will pause for approval)
result = await orchestrator.run(
    source_repo="https://github.com/myorg/my-service",
    auto_approve=False
)

# Review proposed changes
print(result["approval_context"])

# Approve and continue
final = await orchestrator.resume(
    approval_decision="approve",
    modifications=None
)

# Or reject
final = await orchestrator.resume(
    approval_decision="reject",
    modifications={"reason": "Need different deployment strategy"}
)
```

### Claude Code Integration

The orchestrator can be used within Claude Code as a plugin:

```
> Analyze https://github.com/acme/payment-service and set up Harness
> with canary deployments to production

[Orchestrator analyzes repository]
[Detects: Go microservice with Kubernetes deployment]
[Proposes: CI/CD pipeline with canary deployment strategy]
[Requests approval]

> Approve

[Creates complete Harness setup]
[Configures canary deployment]
[Verifies with test execution]

✅ Complete! Pipeline available at: https://app.harness.io/...
```

---

## Project Structure

```
ai-template-engine/
├── src/
│   └── orchestrator/
│       ├── __init__.py           # Package initialization
│       ├── state.py              # LangGraph state definitions
│       ├── graph.py              # Workflow graph construction
│       ├── main.py               # CLI interface
│       ├── agents/
│       │   ├── __init__.py
│       │   ├── repo_analysis.py  # Repository analysis agent
│       │   ├── pattern_extraction.py  # Pattern extraction agent
│       │   ├── template_generation.py # Template generation agent
│       │   ├── harness_setup.py  # Harness setup agent
│       │   └── deployment.py     # Deployment verification agent
│       ├── tools/
│       │   ├── __init__.py
│       │   └── mcp_registry.py   # MCP tool registry
│       └── claude_code_integration.py  # Claude Code plugin bridge
├── tests/
│   ├── test_state.py
│   ├── test_graph.py
│   ├── test_agents.py
│   └── test_tools.py
├── docs/
│   ├── ARCHITECTURE.md           # Detailed architecture
│   ├── AGENTS.md                 # Agent documentation
│   ├── MCP_INTEGRATION.md        # MCP server setup
│   ├── WORKFLOWS.md              # Workflow examples
│   └── CONTRIBUTING.md           # Contribution guidelines
├── examples/
│   ├── basic_automation.py       # Basic example
│   ├── custom_patterns.py        # Custom pattern rules
│   └── advanced_workflows.py     # Advanced usage
├── requirements.txt              # Python dependencies
├── pyproject.toml                # Project configuration
├── .env.example                  # Example environment file
├── .gitignore
└── README.md
```

---

## Workflow Phases

### Phase 1: Repository Analysis

**Agent**: `RepoAnalysisAgent`

- Clones source repository
- Runs Repomix for compressed code analysis
- Detects languages, frameworks, build tools
- Identifies configuration files (Docker, K8s, Terraform)
- Analyzes dependencies and package managers
- Detects test frameworks and coverage

**Output**: `RepositoryAnalysis` dataclass

### Phase 2: Pattern Extraction

**Agent**: `PatternExtractionAgent`

- Classifies project type
- Determines optimal deployment strategy
- Suggests pipeline stages
- Identifies required connectors
- Determines secrets needed
- Maps dependencies

**Output**: `ExtractedPatterns` dataclass

### Phase 3: Template Generation

**Agent**: `TemplateGenerationAgent`

- Generates step templates
- Creates stage templates
- Builds pipeline templates
- Defines service configurations
- Creates environment definitions
- Generates infrastructure definitions

**Output**: `GeneratedTemplates` dataclass

### Phase 4: Approval (Optional)

**Human-in-the-Loop**

- Presents proposed setup
- Lists all resources to be created
- Requests approval/modification/rejection
- Updates plan based on user feedback

**Output**: User decision + modifications

### Phase 5: Harness Setup

**Agent**: `HarnessSetupAgent`

- Creates/verifies organization and project
- Creates all connectors
- Stores secrets securely
- Sets up delegates
- Creates services
- Creates environments
- Creates infrastructure definitions
- Creates templates (step, stage, pipeline)
- Creates pipelines

**Output**: `HarnessSetupResult` dataclass

### Phase 6: Deployment Verification

**Agent**: `DeploymentAgent`

- Triggers test pipeline execution
- Monitors execution progress
- Validates deployment success
- Captures logs and metrics
- Verifies endpoints

**Output**: `DeploymentVerification` dataclass

---

## Configuration

### MCP Servers

```json
{
  "mcpServers": {
    "harness": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "harness/mcp-server", "stdio"],
      "env": {
        "HARNESS_API_KEY": "${HARNESS_API_KEY}",
        "HARNESS_DEFAULT_ORG_ID": "${HARNESS_ORG_ID}"
      }
    },
    "scaffold": {
      "command": "npx",
      "args": ["-y", "@agiflowai/scaffold-mcp"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Pattern Detection Rules

Custom pattern rules can be defined in `patterns.yaml`:

```yaml
patterns:
  microservice:
    indicators:
      - fastapi
      - flask
      - express
      - spring-boot
    deployment: kubernetes
    pipeline_type: ci-cd
    stages:
      - build
      - test
      - scan
      - deploy-dev
      - deploy-staging
      - approval
      - deploy-prod

  frontend:
    indicators:
      - react
      - vue
      - angular
      - next.js
    deployment: static
    pipeline_type: ci-cd
    stages:
      - build
      - test
      - deploy-preview
      - approval
      - deploy-prod
```

---

## Examples

### Example 1: Python FastAPI Microservice

**Repository**: https://github.com/acme/api-service

**Detected**:
- Language: Python 3.11
- Framework: FastAPI
- Database: PostgreSQL
- Tests: pytest with 85% coverage
- Deployment: Kubernetes with Helm

**Generated**:
- 3 connectors (GitHub, DockerHub, Kubernetes)
- 5 secrets (GitHub token, Docker creds, DB connection, API keys)
- 3 environments (dev, staging, prod)
- 1 service definition with K8s manifests
- 1 CI/CD pipeline (build → test → scan → deploy)

### Example 2: React Frontend Application

**Repository**: https://github.com/acme/web-app

**Detected**:
- Language: TypeScript
- Framework: React 18, Next.js 14
- Tests: Jest + React Testing Library
- Deployment: Static site (Vercel/Netlify pattern)

**Generated**:
- 2 connectors (GitHub, AWS S3)
- 2 secrets (GitHub token, AWS credentials)
- 2 environments (preview, production)
- 1 service definition for static assets
- 1 CI/CD pipeline (build → test → deploy-preview → approval → deploy-prod)

### Example 3: Terraform Infrastructure

**Repository**: https://github.com/acme/infrastructure

**Detected**:
- Language: HCL (Terraform)
- Cloud: AWS (EC2, RDS, S3, VPC)
- No runtime deployment, IaC only

**Generated**:
- 2 connectors (GitHub, AWS)
- 3 secrets (GitHub token, AWS credentials)
- 1 IaC pipeline (validate → plan → approval → apply)
- Approval gates for production changes

---

## Development

### Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run with coverage
pytest tests/ --cov=src --cov-report=html

# Run specific test file
pytest tests/test_agents.py -v

# Run integration tests (requires MCP servers)
pytest tests/integration/ -v --requires-mcp
```

### Adding New Agents

1. Create agent file in `src/orchestrator/agents/`
2. Implement agent class with required methods
3. Add agent to workflow graph in `src/orchestrator/graph.py`
4. Add tests in `tests/test_agents.py`

Example:

```python
# src/orchestrator/agents/my_agent.py
from langchain_anthropic import ChatAnthropic
from deepagents import create_deep_agent

class MyAgent:
    def __init__(self, mcp_registry):
        self.mcp_registry = mcp_registry
        self.model = ChatAnthropic(model_name="claude-sonnet-4-5-20250929")
        self.tools = self._create_tools()
        self.agent = create_deep_agent(
            model=self.model,
            tools=self.tools,
            system_prompt="..."
        )

    async def process(self, input_data):
        result = await self.agent.ainvoke({"messages": [...]})
        return self._parse_result(result)
```

### Adding New MCP Servers

1. Add server configuration to `mcp_registry.py`
2. Create tools that call the server
3. Register tools with agents
4. Update documentation

---

## Troubleshooting

### MCP Server Connection Issues

```bash
# Test MCP server manually
npx @agiflowai/scaffold-mcp

# Verify Docker MCP server
docker run -i --rm harness/mcp-server stdio

# Check environment variables
echo $HARNESS_API_KEY
echo $HARNESS_ORG_ID
```

### Authentication Errors

- Verify API keys are correct and not expired
- Check organization/project permissions
- Ensure API keys have required scopes

### Pattern Detection Issues

- Add custom pattern rules in `patterns.yaml`
- Review Repomix output for missing indicators
- Check agent logs for detection reasoning

### Template Generation Errors

- Verify extracted patterns are complete
- Check Harness API connectivity
- Review template syntax in generated YAML

---

## Roadmap

### Phase 1: Core Functionality ✅
- [x] LangGraph workflow orchestration
- [x] Multi-agent architecture
- [x] MCP integration layer
- [x] Repository analysis
- [x] Pattern extraction
- [x] Template generation
- [x] Harness setup automation

### Phase 2: Enhanced Intelligence 🚧
- [ ] ML-based pattern learning
- [ ] Historical data analysis
- [ ] Cost optimization suggestions
- [ ] Performance benchmarking
- [ ] Security best practices enforcement

### Phase 3: Advanced Features 📋
- [ ] Multi-cloud support (AWS, GCP, Azure)
- [ ] GitOps integration (Argo CD, Flux)
- [ ] Monitoring integration (Prometheus, Datadog)
- [ ] Incident response automation
- [ ] Rollback strategies

### Phase 4: Enterprise Features 📋
- [ ] RBAC and audit logging
- [ ] Policy as code integration
- [ ] Compliance checking
- [ ] Custom approval workflows
- [ ] Multi-tenancy support

---

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](docs/CONTRIBUTING.md) for guidelines.

### Quick Start

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is part of the Lobbi AI platform infrastructure.

---

## Support

- **GitHub Issues**: [https://github.com/the-Lobbi/ai-template-engine/issues](https://github.com/the-Lobbi/ai-template-engine/issues)
- **Documentation**: [docs/](docs/)
- **Harness Community**: [https://community.harness.io](https://community.harness.io)

---

## Acknowledgments

- **LangGraph**: State machine workflow orchestration
- **Anthropic Claude**: AI reasoning and code generation
- **Model Context Protocol (MCP)**: Tool integration framework
- **Harness**: CI/CD platform automation
- **Repomix**: Repository compression and analysis

---

**Built with ❤️ by the Lobbi team**

🚀 **Automate Everything. Deploy with Confidence.**
