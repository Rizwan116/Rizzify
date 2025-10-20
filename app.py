from flask import Flask, render_template, request
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import os
import io

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    photo = request.files['photo']
    name = request.form.get('name', 'Guest')
    location = request.form.get('location', 'Unknown Location')

    if not photo:
        return "❌ No photo received!"

    # Save photo with timestamped filename
    filename = datetime.now().strftime("photo_%Y%m%d_%H%M%S.jpg")
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    # Read image into Pillow
    img = Image.open(photo.stream).convert("RGB")

    # Add overlay text
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    date_str = datetime.now().strftime("%d/%m/%Y")
    time_str = datetime.now().strftime("%I:%M %p")

    text = f"Name: {name}\nLocation: {location}\nDate: {date_str}\nTime: {time_str}"

    # Position text (bottom-left)
    x, y = 20, img.height - 100
    draw.rectangle([(x - 10, y - 10), (x + 330, y + 80)], fill=(0, 0, 0, 120))
    draw.multiline_text((x, y), text, fill=(255, 255, 255), font=font, spacing=4)

    # Save image
    img.save(filepath)

    return f"✅ Photo saved successfully with details: {filepath}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
