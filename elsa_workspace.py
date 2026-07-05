from workspace.workspace_engine import WorkspaceEngine
from workspace.workspace_message import WorkspaceMessage
from services.line_service import send_line_message
import subprocess, sys, traceback

data = WorkspaceEngine().build()
msg = WorkspaceMessage().render(data)

print(msg)
send_line_message(msg)

try:
    subprocess.run(
        [sys.executable, "workspace/workspace_renderer.py"],
        check=True,
        capture_output=True,
        text=True
    )
except Exception as e:
    err = traceback.format_exc()
    print("⚠️ Workspace 圖片失敗")
    print(err)
    send_line_message("⚠️ Elsa Workspace 圖片產生失敗\n文字已正常送出\n\n錯誤：\n" + str(e))
