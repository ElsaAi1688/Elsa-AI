from datetime import datetime
from services.cloudinary_service import upload_image
from services.line_service import send_line_image

today = datetime.now().strftime("%Y-%m-%d")

image_path = f"images/dashboard_{today}.png"

image_url = upload_image(image_path)

print("✅ 圖片已上傳：", image_url)

send_line_image(image_url)
