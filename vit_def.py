from flask import Flask, render_template, request, current_app
from werkzeug.utils import secure_filename
import os
import label_image
import image_fuzzy_clustering as fem
from PIL import Image

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'img')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# Routes
@app.route('/')
@app.route('/first')
def first():
    return render_template('first.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/chart')
def chart():
    return render_template('chart.html')


@app.route('/upload')
def upload():
    return render_template('index1.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/success', methods=['POST'])
def success():
    if request.method == 'POST':
        clusters = request.form.get('cluster')
        file = request.files['file']
        _, file_ext = os.path.splitext(file.filename)

        original_pic_path = save_img(file, file.filename)
        fem.plot_cluster_img(original_pic_path, clusters)

        return render_template('success.html')


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['file']
        file_path = secure_filename(file.filename)
        file.save(file_path)

        result = load_image(file_path)
        result = result.title()

        info = {
            "Vitamin A": " → Deficiency of vitamin A is associated with significant morbidity and mortality from common childhood infections, and is the world's leading preventable cause of childhood blindness. Vitamin A deficiency also contributes to maternal mortality and other poor outcomes of pregnancy and lactation.",
            "Vitamin B": " → Vitamin B12 deficiency may lead to a reduction in healthy red blood cells (anaemia). The nervous system may also be affected. Symptoms include fatigue, breathlessness, numbness, poor balance, and memory trouble. Treatment includes dietary changes, B12 shots or supplements.",
            "Vitamin C": " → A condition caused by a severe lack of vitamin C (scurvy). Symptoms include bruising, bleeding gums, weakness, fatigue, and rash. Treatment involves taking vitamin C supplements and consuming fruits and vegetables.",
            "Vitamin D": " → Vitamin D deficiency can lead to loss of bone density, contributing to osteoporosis and fractures. In children, it can cause rickets—a rare disease that softens and bends the bones.",
            "Vitamin E": " → Vitamin E deficiency can cause nerve and muscle damage leading to loss of movement control, muscle weakness, vision problems, and a weakened immune system."
        }

        if result in info:
            result_text = result + info[result]
        else:
            result_text = f"{result} → No detailed description available."

        os.remove(file_path)
        return result_text

    return None


# Helper functions
def load_image(image_path):
    return label_image.main(image_path)


def save_img(img_file, filename):
    picture_path = os.path.join(current_app.root_path, 'static/images', filename)
    image = Image.open(img_file)
    image.save(picture_path)
    return picture_path


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
