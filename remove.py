from flask import Flask, render_template, request, jsonify
from rembg import remove
import base64
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-background', methods=['POST'])
def remove_bg():
    # Get the base64 image data from the POST request
    data = request.get_json()
    image_data = data.get('image')

    # Decode the base64 string
    img_data = base64.b64decode(image_data.split(',')[1])
    img = Image.open(BytesIO(img_data))

    # Remove the background using rembg
    result = remove(img)

    # Save the image with the background removed
    output_path = os.path.join(UPLOAD_FOLDER, 'processed_image.png')
    result.save(output_path)

    # Convert the result to a base64 string
    buffered = BytesIO()
    result.save(buffered, format="PNG")
    result_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

    # Send the processed image back to the client
    return jsonify({"image": f"data:image/png;base64,{result_base64}"})


if _name_ == '_main_':
    app.run(debug=True, host='0.0.0.0', port=5000)