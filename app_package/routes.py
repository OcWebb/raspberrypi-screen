from flask import render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
from app_package import app
import base64
import os

@app.route('/', methods= ['GET', 'POST'])
def showFullscreenImage():
    image = getImage()

    return render_template('image.html', encodedImage=image)


@app.route('/image/set', methods= ['GET', 'POST'])
def setImage():

    print('\n\n')
    print(request.method)
    print(request.files)
    print('\n\n')
    
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Image Failed to upload, file not found")
            return redirect(request.url)

        file = request.files['file']
        
        if file.filename == '':
            flash("Image Failed to upload")
            return redirect(request.url)

        if file:
            dir = os.path.join(app.static_folder, "images")
            images = os.listdir(dir)

            for image in images:
                os.remove(os.path.join(dir, image))

            newImageFilename = secure_filename(file.filename)
            file.save(os.path.join(dir, newImageFilename))

            flash("Image Saved")

            return redirect(url_for('setImage'))

        return


    return render_template('uploadImage.html')


@app.route('/image/get', methods= ['GET'])
def getImage():
    dir = os.path.join(app.static_folder, "images")
    images = os.listdir(dir)

    with open(os.path.join(dir, images[0]), "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        return encoded_string