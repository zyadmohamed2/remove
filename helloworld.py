from flask import Flask, request, send_file
from PIL import Image
from rembg import remove
import io

app = Flask(__name__)

@app.route('/process-image', methods=['POST'])
def process_image():
    # التحقق من وجود الصورة في الطلب
    if 'user_image' not in request.files:
        return {'error': 'Please provide the user_image.'}, 400

    # استلام الصورة من الطلب
    user_image_file = request.files['user_image']

    try:
        # فتح الصورة وتحويلها إلى صيغة RGBA
        user_image = Image.open(user_image_file).convert('RGBA')

        # إزالة الخلفية باستخدام rembg
        user_image_bytes = io.BytesIO()
        user_image.save(user_image_bytes, format='PNG')
        user_image_no_bg = remove(user_image_bytes.getvalue())
        user_image_no_bg = Image.open(io.BytesIO(user_image_no_bg))

        # حفظ الصورة المعالجة إلى كائن BytesIO
        output = io.BytesIO()
        user_image_no_bg.save(output, format='PNG')
        output.seek(0)

        # تنظيف الذاكرة
        del user_image, user_image_no_bg

        # إعادة الصورة بدون خلفية
        return send_file(output, mimetype='image/png')

    except Exception as e:
        # معالجة الأخطاء
        return {'error': str(e)}, 500

if __name__ == '__main__':
    app.run(debug=False)
