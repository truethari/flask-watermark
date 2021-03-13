import os
from flask import Flask, render_template, url_for, request
from werkzeug.utils import secure_filename
from PIL import Image

app = Flask(__name__, static_folder="templates")

app.config['WATERMARK_UPLOAD_FOLDER'] = 'templates/images/input/watermark/'
app.config['MAIN_IMAGE_UPLOAD_FOLDER'] = 'templates/images/input/main/'
app.config['OUTPUT_FOLDER'] = 'templates/images/output/'

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        watermark_image = request.files['watermark_image']
        main_image = request.files['main_image']
        filename_watermark_image = secure_filename(watermark_image.filename)
        filename_main_image = secure_filename(main_image.filename)
        watermark_image.save(os.path.join(app.config['WATERMARK_UPLOAD_FOLDER'], filename_watermark_image))
        main_image.save(os.path.join(app.config['MAIN_IMAGE_UPLOAD_FOLDER'], filename_main_image))

        #watermark process
        watermark_files = os.listdir(app.config['WATERMARK_UPLOAD_FOLDER'])
        logo_path = app.config['WATERMARK_UPLOAD_FOLDER'] + watermark_files[0]
        print(logo_path)
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