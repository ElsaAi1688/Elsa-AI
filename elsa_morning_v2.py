from elsa_rc1a import msg as portfolio_msg
from elsa_build004 import msg as market_msg
from elsa_rc1f import msg as teacher_msg
from services.line_service import send_line_message

final_msg = "\n\n".join([
    "🌅 Elsa AI Morning Brief 2.0",
    "==============================",
    portfolio_msg,
    market_msg,
    teacher_msg
])

print(final_msg)
send_line_message(final_msg)
