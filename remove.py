from flask import Flask, request, send_file
from PIL import Image
from rembg import remove
import io

app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image():
    # Check if both user_image and background_image are provided
    if 'user_image' not in request.files or 'background_image' not in request.files:
        return {'error': 'Please provide both user_image and background_image.'}, 400

    # Get the images from the request
    user_image_file = request.files['user_image']
    background_image_file = request.files['background_image']

    # Open and process user_image (remove background)
    user_image = Image.open(user_image_file)
    user_image = user_image.convert('RGBA')
    user_image_bytes = io.BytesIO()
    user_image.save(user_image_bytes, format='PNG')
    user_image_no_bg = remove(user_image_bytes.getvalue())
    user_image_no_bg = Image.open(io.BytesIO(user_image_no_bg))

    # Open background_image
    background_image = Image.open(background_image_file)

    # Resize user_image to fit background_image dimensions
    user_image_no_bg = user_image_no_bg.resize(background_image.size, Image.Resampling.LANCZOS)

    # Merge user_image_no_bg onto background_image
    combined_image = background_image.copy()
    combined_image.paste(user_image_no_bg, (0, 0), user_image_no_bg)

    # Save the final image to a BytesIO object
    output = io.BytesIO()
    combined_image.save(output, format='PNG')
    output.seek(0)

    # Return the combined image
    return send_file(output, mimetype='image/png', as_attachment=True, download_name="processed_image.png")

if __name__ == '__main__':
    app.run(debug=True)
