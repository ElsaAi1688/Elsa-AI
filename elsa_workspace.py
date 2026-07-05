
from workspace.workspace_engine import WorkspaceEngine
from workspace.workspace_message import WorkspaceMessage
from services.line_service import send_line_message
import subprocess, sys

data = WorkspaceEngine().build()
msg = WorkspaceMessage().render(data)

print(msg)
send_line_message(msg)

subprocess.run([sys.executable, "workspace/workspace_renderer.py"], check=True)
