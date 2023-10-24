from flask import Flask, request, render_template, redirect, url_for
import os
from process_image import process_image

app = Flask(__name__)

UPLOAD_FOLDER = 'upload'
PROCESSED_FOLDER = 'processed'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# Route to the home page
@app.route('/')
def index():
    return render_template('index.html')


# Route to handle the login form submission
@app.route('/login', methods=['POST'])
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')

    if username == 'test' and password == 'test':
        # If the credentials are correct, redirect to the file upload page
        return redirect(url_for('file_upload'))
    else:
        # Redirect back to the login page with an error message
        return redirect(url_for('index'))


# Route for the file upload page
@app.route('/file_upload')
def file_upload():
    return render_template('Fileupload.html')


# Route for the upload processing
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'image' not in request.files:
        return redirect(request.url)

    file = request.files['image']

    if file.filename == '':
        return redirect(request.url)

    if file and allowed_file(file.filename):
        # Save the uploaded image
        filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filename)

        process_image(filename)

        # After processing, show a confirmation screen with a link to the processed image
        processed_filename = 'try_hnr_new.jpg'  # Adjust the filename as needed
        return render_template('confirmation.html', processed_filename=processed_filename)

        return redirect(request.url)

        return redirect(url_for('index'))

    return redirect(request.url)


# Initiate the app
if __name__ == '__main__':
    app.run(debug=True)
