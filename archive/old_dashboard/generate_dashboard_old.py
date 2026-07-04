from PIL import Image, ImageDraw, ImageFont

W,H = 1080,1920

img = Image.new("RGB",(W,H),"#F5F7FB")
draw = ImageDraw.Draw(img)

title = ImageFont.load_default()
font = ImageFont.load_default()

draw.text((40,40),"🚀 Elsa AI Morning Brief",fill="black",font=title)

draw.rectangle((40,120,1040,260),outline="blue",width=3)
draw.text((70,150),"🔥 Top10",fill="black",font=font)

draw.rectangle((40,300,1040,440),outline="green",width=3)
draw.text((70,330),"⭐ Watch List",fill="black",font=font)

draw.rectangle((40,480,1040,620),outline="orange",width=3)
draw.text((70,510),"🏆 Elite",fill="black",font=font)

draw.rectangle((40,660,1040,800),outline="red",width=3)
draw.text((70,690),"🚫 Avoid",fill="black",font=font)

img.save("reports/dashboard.png")

print("✅ reports/dashboard.png")
