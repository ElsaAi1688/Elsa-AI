from workspace.workspace_engine import WorkspaceEngine
from workspace.workspace_message import WorkspaceMessage
from services.line_service import send_line_message
from memory.investment_journal import InvestmentJournal
import subprocess
import sys

data = WorkspaceEngine().build()
InvestmentJournal().record_daily(data)
msg = WorkspaceMessage().render(data)

print(msg)
send_line_message(msg)

try:
    result = subprocess.run(
        [sys.executable, "workspace/workspace_renderer.py"],
        check=True,
        capture_output=True,
        text=True
    )
    print(result.stdout)

except subprocess.CalledProcessError as e:
    print(e.stdout)
    print(e.stderr)

    send_line_message(
        "⚠️ Workspace Renderer Error\n\n"
        + (e.stderr if e.stderr else e.stdout)
    )
