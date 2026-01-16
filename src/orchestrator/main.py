"""CLI interface for the AI Template Engine orchestrator."""

import datetime
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from .graph import graph
from .state import OrchestratorState

app = typer.Typer(
    name="ai-template-engine",
    help="LangGraph-based orchestration for automated Harness CI/CD setup",
)
console = Console()


@app.command()
def orchestrate(
    repo_path: str = typer.Argument(..., help="Path to the target repository"),
    repo_url: Optional[str] = typer.Option(None, help="Repository URL (optional)"),
    org_id: str = typer.Option(..., "--org", "-o", help="Harness organization ID"),
    project_id: str = typer.Option(..., "--project", "-p", help="Harness project ID"),
    no_approval: bool = typer.Option(
        False, "--no-approval", help="Skip human approval step"
    ),
) -> None:
    """Run the complete orchestration workflow.

    This will:
    1. Analyze the repository
    2. Extract CI/CD patterns
    3. Generate Harness templates
    4. Request human approval (unless --no-approval)
    5. Setup Harness platform
    6. Verify deployment

    Example:
        ai-template-engine /path/to/repo --org my-org --project my-project
    """
    console.print(
        Panel.fit(
            "🚀 AI Template Engine - Harness Orchestration",
            border_style="bold blue",
        )
    )

    # Create initial state
    initial_state: OrchestratorState = {
        "messages": [],
        "current_phase": "init",
        "target_repo_path": repo_path,
        "target_repo_url": repo_url,
        "harness_org_id": org_id,
        "harness_project_id": project_id,
        "repository_analysis": None,
        "extracted_patterns": None,
        "generated_templates": None,
        "harness_setup": None,
        "deployment_verification": None,
        "hitl_required": not no_approval,
        "hitl_approved": no_approval,  # Auto-approve if flag set
        "hitl_feedback": None,
        "errors": [],
        "warnings": [],
        "workflow_id": "",
        "started_at": "",
        "completed_at": None,
        "total_duration_seconds": None,
    }

    # Run the workflow
    config = {"configurable": {"thread_id": "orchestration-session"}}

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
        ) as progress:
            task = progress.add_task("Initializing workflow...", total=None)

            # Stream the graph execution
            for event in graph.stream(initial_state, config=config, stream_mode="values"):
                phase = event.get("current_phase", "unknown")
                progress.update(task, description=f"Phase: {phase}")

                # Print any new messages
                messages = event.get("messages", [])
                if messages:
                    last_message = messages[-1]
                    console.print(f"\n{last_message.content}\n")

                # Check for errors
                errors = event.get("errors", [])
                if errors:
                    console.print(f"[bold red]Errors: {', '.join(errors)}[/bold red]")
                    sys.exit(1)

                # Handle approval interrupt
                if phase == "approval" and not event.get("hitl_approved"):
                    console.print(
                        "\n[yellow]⏸ Workflow paused for human approval[/yellow]"
                    )
                    console.print(
                        "[dim]To approve: Update the graph state with hitl_approved=True[/dim]"
                    )
                    console.print(
                        "[dim]In LangGraph Studio, you can interact with the paused workflow[/dim]\n"
                    )
                    # In CLI mode, we can't interactively approve, so exit
                    sys.exit(0)

                # Check for completion
                if phase == "complete":
                    break

        console.print(
            Panel.fit(
                "✅ Orchestration Complete!",
                border_style="bold green",
            )
        )

    except Exception as e:
        console.print(f"[bold red]Orchestration failed: {str(e)}[/bold red]")
        sys.exit(1)


@app.command()
def studio() -> None:
    """Launch LangGraph Studio for visual workflow management.

    This will start the LangGraph development server which includes
    the Studio UI for visualizing and debugging the workflow.
    """
    console.print(
        Panel.fit(
            "🎨 Launching LangGraph Studio\n\n"
            "Run: langgraph dev\n"
            "Then open: http://localhost:8123",
            border_style="bold blue",
        )
    )
    console.print("\n[dim]Starting LangGraph dev server...[/dim]\n")

    import subprocess

    try:
        subprocess.run(["langgraph", "dev"], check=True)
    except FileNotFoundError:
        console.print(
            "[bold red]Error: langgraph CLI not found[/bold red]\n"
            "Install with: pip install langgraph-cli"
        )
        sys.exit(1)
    except KeyboardInterrupt:
        console.print("\n[yellow]Studio server stopped[/yellow]")


@app.command()
def version() -> None:
    """Show version information."""
    from . import __version__

    console.print(f"AI Template Engine v{__version__}")


def main() -> None:
    """Entry point for the CLI."""
    app()


if __name__ == "__main__":
    main()
