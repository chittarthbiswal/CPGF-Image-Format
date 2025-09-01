from flask import Flask, request, send_file, render_template
from PIL import Image
import io
from cpgf_tools import block_reduce, save_cpgf

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_png', methods=['POST'])
def upload_png():
    uploaded_file = request.files['image']
    block_size = int(request.form.get('block_size', 20))
    img = Image.open(uploaded_file).convert("RGB")
    reduced = block_reduce(img, block_size=block_size)

    cpgf_io = io.BytesIO()
    save_cpgf(reduced, cpgf_io)
    cpgf_io.seek(0)
    return send_file(cpgf_io,
                     mimetype='application/octet-stream',
                     download_name='image.cpgf')

if __name__ == "__main__":
    app.run(debug=True)
