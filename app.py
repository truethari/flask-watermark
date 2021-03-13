import os
from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__, static_folder="templates")

app.config['WATERMARK_UPLOAD_FOLDER'] = 'templates/images/input/watermark/'
app.config['MAIN_IMAGE_UPLOAD_FOLDER'] = 'templates/images/input/main/'
app.config['OUTPUT_FOLDER'] = 'templates/images/output/'

for folder in [app.config['WATERMARK_UPLOAD_FOLDER'], app.config['MAIN_IMAGE_UPLOAD_FOLDER'], app.config['OUTPUT_FOLDER']]:
        for item in os.listdir(folder):
            os.remove(os.path.join(folder, item))

@app.route('/', methods=['POST', 'GET'])
def index():
    for folder in [app.config['WATERMARK_UPLOAD_FOLDER'], app.config['MAIN_IMAGE_UPLOAD_FOLDER']]:
        for item in os.listdir(folder):
            os.remove(os.path.join(folder, item))

    if request.method == 'POST':
        for item in os.listdir(app.config['OUTPUT_FOLDER']):
            os.remove(os.path.join(app.config['OUTPUT_FOLDER'], item))

        watermark_image = request.files['watermark_image']
        main_image = request.files['main_image']
        filename_watermark_image = secure_filename(watermark_image.filename)
        filename_main_image = secure_filename(main_image.filename)
        watermark_image.save(os.path.join(app.config['WATERMARK_UPLOAD_FOLDER'], filename_watermark_image))
        main_image.save(os.path.join(app.config['MAIN_IMAGE_UPLOAD_FOLDER'], filename_main_image))

        #watermark process
        watermark_files = os.listdir(app.config['WATERMARK_UPLOAD_FOLDER'])
        logo_path = app.config['WATERMARK_UPLOAD_FOLDER'] + watermark_files[0]
        logo = Image.open(logo_path)
        imageList = os.listdir(app.config['MAIN_IMAGE_UPLOAD_FOLDER'])

        for imageName in imageList:
            image = Image.open(app.config['MAIN_IMAGE_UPLOAD_FOLDER'] + imageName)
            image.paste(logo, (0, 0), logo)
            image.save(app.config['OUTPUT_FOLDER'] + imageName)
        #-------------------------------------------

        filelist = os.listdir(app.config['OUTPUT_FOLDER'])
        return render_template('index.html', images=filelist)
    else:
        filelist = os.listdir(app.config['OUTPUT_FOLDER'])
        return render_template('index.html', images=filelist)

if __name__ == "__main__":
    app.run(debug=True)