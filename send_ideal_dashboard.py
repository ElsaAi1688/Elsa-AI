from services.cloudinary_service import upload_image
from services.line_service import send_line_image

image_path = "reports/output/elsa_ideal_dashboard.png"

image_url = upload_image(image_path)

print("✅ 圖片已上傳：", image_url)

send_line_image(image_url)
