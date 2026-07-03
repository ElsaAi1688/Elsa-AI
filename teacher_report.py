from services.teacher_service import get_daily_lesson
from services.line_service import send_line_message

lesson = get_daily_lesson()

print(lesson)

send_line_message(lesson)
