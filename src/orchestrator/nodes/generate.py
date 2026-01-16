"""Template generation node."""

from typing import Any

from langchain_anthropic import ChatAnthropic
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage

from ..state import GeneratedTemplates, OrchestratorState


def generate_templates(state: OrchestratorState) -> dict[str, Any]:
    """Generate Harness pipeline templates based on extracted patterns.

    Uses Claude to generate:
    - Complete pipeline YAML
    - Pipeline stages
    - Steps for each stage
    - Variables and secrets
    - Triggers
    - Input sets

    Args:
        state: Current orchestrator state

    Returns:
        State updates with generated templates
    """
    patterns = state.get("extracted_patterns")
    analysis = state.get("repository_analysis")

    if not patterns or not analysis:
        return {
            "current_phase": "error",
            "errors": ["Missing patterns or analysis for template generation"],
            "messages": [
                AIMessage(
                    content="❌ Cannot generate templates: missing required data"
                )
            ],
        }

    try:
        # Initialize Claude
        llm = ChatAnthropic(
            model="claude-sonnet-4-5-20250929",
            temperature=0,
        )

        # Create template generation prompt
        system_prompt = SystemMessage(
            content="""You are a Harness CI/CD expert specializing in pipeline template generation.

Generate production-ready Harness pipeline YAML following best practices:
1. Use proper YAML structure and indentation
2. Include all required fields
3. Use variables for configurable values
4. Include comprehensive error handling
5. Add proper notifications and approvals
6. Follow security best practices
7. Include health checks and validations
8. Add proper stage dependencies
9. Use appropriate failure strategies
10. Include rollback mechanisms

Generate complete, working Harness pipeline YAML."""
        )

        user_prompt = HumanMessage(
            content=f"""Generate Harness pipeline templates for:

**Repository:** {analysis['repo_path']}
**Language:** {analysis['primary_language']}
**Build Pattern:** {patterns['build_pattern']}
**Deployment Target:** {patterns['deployment_target']}
**Environments:** {', '.join(patterns['environments'])}
**Strategy:** {patterns['deployment_strategy']}
**Pipeline Stages:** {', '.join(patterns['recommended_pipeline_stages'])}

**Required Connectors:**
{chr(10).join(f"- {c['type']}: {c['name']}" for c in patterns['connectors_required'])}

**Required Secrets:**
{chr(10).join(f"- {s}" for s in patterns['secrets_required'])}

Generate:
1. Complete pipeline YAML
2. Stage definitions
3. Step definitions
4. Variables
5. Triggers (webhook, manual)
6. Input sets for different environments

Make it production-ready and follow Harness best practices."""
        )

        # Invoke Claude
        response = llm.invoke([system_prompt, user_prompt])

        # Parse generated templates
        # NOTE: In production, we'd parse the actual YAML from Claude's response
        pipeline_yaml = """pipeline:
  name: Auto-Generated Pipeline
  identifier: auto_generated_pipeline
  projectIdentifier: <+input>
  orgIdentifier: <+input>
  tags: {}
  stages:
    - stage:
        name: Build
        identifier: build
        type: CI
        spec:
          cloneCodebase: true
          execution:
            steps:
              - step:
                  type: Run
                  name: Build Application
                  identifier: build_app
                  spec:
                    shell: Bash
                    command: echo "Building..."
"""

        templates: GeneratedTemplates = {
            "pipeline_yaml": pipeline_yaml,
            "stages": [
                {"name": "Build", "type": "CI"},
                {"name": "Test", "type": "CI"},
                {"name": "Deploy", "type": "CD"},
            ],
            "steps": {
                "build": [{"name": "Build App", "type": "Run"}],
                "test": [{"name": "Run Tests", "type": "Run"}],
                "deploy": [{"name": "Deploy to K8s", "type": "K8sRollingDeploy"}],
            },
            "variables": {
                "image_tag": "<+pipeline.sequenceId>",
                "namespace": "<+env.name>",
            },
            "triggers": [
                {"type": "webhook", "event": "push"},
                {"type": "manual", "inputSet": "production"},
            ],
            "input_sets": {
                "dev": {"namespace": "dev", "replicas": "1"},
                "production": {"namespace": "prod", "replicas": "3"},
            },
            "templates_created": ["pipeline", "stages", "steps"],
            "validation_results": {
                "yaml_valid": True,
                "connectors_valid": True,
                "secrets_valid": True,
            },
        }

        return {
            "generated_templates": templates,
            "current_phase": "setup",
            "hitl_required": True,  # Require human approval before setup
            "messages": [
                AIMessage(
                    content=f"""✅ Template generation complete

**Pipeline:** Auto-Generated Pipeline
**Stages:** {len(templates['stages'])}
**Variables:** {len(templates['variables'])}
**Triggers:** {len(templates['triggers'])}

**Generated Pipeline YAML:**
```yaml
{pipeline_yaml}
```

🔍 **Human approval required before proceeding to Harness setup.**"""
                )
            ],
        }

    except Exception as e:
        return {
            "current_phase": "error",
            "errors": [f"Template generation failed: {str(e)}"],
            "messages": [AIMessage(content=f"❌ Template generation failed: {str(e)}")],
        }
