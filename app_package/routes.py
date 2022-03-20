from asyncio.windows_events import NULL
from flask import render_template, url_for, request, redirect, flash
from werkzeug.utils import secure_filename
from app_package import app
import base64
import os

@app.route('/', methods= ['GET', 'POST'])
def showFullscreenImage():
    return render_template('content-1x1.html')


@app.route('/content/set', methods= ['GET', 'POST'])
def setContent():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash("Content Failed to upload, file not found")
            return redirect(request.url)

        file = request.files['file']
        
        if file.filename == '':
            flash("Content Failed to upload")
            return redirect(request.url)

        if file:
            dir = os.path.join(app.static_folder, "content")
            images = os.listdir(dir)

            for image in images:
                os.remove(os.path.join(dir, image))

            newImageFilename = secure_filename(file.filename)
            file.save(os.path.join(dir, newImageFilename))

            flash("Content Saved")

            return redirect(url_for('setContent'))

        return


    return render_template('uploadImage.html')


@app.route('/content/get', methods= ['GET'])
def getContent():
    dir = os.path.join(app.static_folder, "content")
    content = os.listdir(dir)[0]

    contentPath = os.path.join(dir, content)
    name, extension = os.path.splitext(contentPath)
    print (extension)

    with open(os.path.join(dir, content), "rb") as contentFile:
        encodedContent = base64.b64encode(contentFile.read())
        encodingAsString = encodedContent.decode('ascii')

        contentHeaderMimetype = getHeaderMimetype(extension)

        return {'mimeType': contentHeaderMimetype, 'data': encodingAsString}


def getHeaderMimetype(extension):
    if extension in ['.jpg', '.jpeg']:
        return "image/jpeg"

    elif extension == '.png':
        return "image/png"

    elif extension == ".mp4":
        return "video/mp4"
    elif extension == ".gif":
        return "image/gif"
        
    else:
        return NULL