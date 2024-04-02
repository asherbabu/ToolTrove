from flask import Flask, render_template, request, flash
from flask_sqlalchemy import SQLAlchemy
import os
from werkzeug.utils import secure_filename
import cv2
import img2pdf
from PIL import Image, ImageEnhance
import mysql.connector

UPLOAD_FOLDER = 'Uploads'

ALLOWED_EXTENSIONS = {'webp', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__, template_folder='Templates', static_folder='Static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:tiger@localhost/'
app.config['SECRET_KEY'] = "something complex"
#db = SQLAlchemy(app)

mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "tiger",
    database = "ToolTrove"
)

my_cursor = mydb.cursor()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def enhancingImg(filename):
    input_img = f"Uploads/{filename}"
    output_img = f"Static/{filename}"
    operation_type = "ImageEnhance"
    print(f"Image Enhancing for {filename}")
    OrginalImg = Image.open(f"Uploads/{filename}")
    EnhancedImg = ImageEnhance.Color(OrginalImg).enhance(1.5)
    EnhancedImg = ImageEnhance.Contrast(OrginalImg).enhance(1.5)
    EnhancedImg = ImageEnhance.Sharpness(OrginalImg).enhance(1.5)
    newfilename = f"Static/{filename}"
    EnhancedImg.save(newfilename, "JPEG", optimize=True)
    #cv2.imwrite(newfilename, EnhancedImg)
    sql_statement = "INSERT INTO OPERATIONS (CDATE, CTIME, INPUT_IMG, OUTPUT_IMG, operation_type) VALUES (CURDATE(), NOW(), %s, %s, %s);"
    my_cursor.execute(sql_statement, (input_img, output_img, operation_type))
    return newfilename

def grayScale(filename):
    input_img = f"Uploads/{filename}"
    output_img = f"Static/{filename}"
    operation_type = "grayscale"
    print(f"Image Gray Scale for {filename}")
    img = cv2.imread(f"Uploads/{filename}")
    imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    newFilename = f"Static/{filename}"
    cv2.imwrite(newFilename, imgProcessed)
    sql_statement = "INSERT INTO OPERATIONS (CDATE, CTIME, INPUT_IMG, OUTPUT_IMG, operation_type) VALUES (CURDATE(), NOW(), %s, %s, %s);"
    my_cursor.execute(sql_statement, (input_img, output_img, operation_type))
    mydb.commit()
    return newFilename

def processImage(filename, operation):
    print(f"the operation is {operation} and file name is {filename}")
    img = cv2.imread(f"Uploads/{filename}")
    input_img = f"Uploads/{filename}"
    output_img = f"Static/{filename}"
    match operation:
        #case "imgEnhance":
            #imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            #OrginalImg = Image.open(f"Uploads/{filename}")
            #EnhancedImg = ImageEnhance.Color(OrginalImg).enhance(1.5)
            #EnhancedImg = ImageEnhance.Contrast(OrginalImg).enhance(1.5)
            #EnhancedImg = ImageEnhance.Sharpness(OrginalImg).enhance(1.5)
            #img.close()
            #newfilename = f"Static/{filename}"
            #cv2.imwrite(newfilename, EnhancedImg)
            #EnhancedImg.save(newfilename)
            #EnhancedImg.save(newfilename, optimize=True)
            #EnhancedImg = open(newfilename, "wb")
            #EnhancedImg.save(newfilename)
            #return newfilename
        case "cwebp":
            operation_type = "Convert to WEBP"
            newfilename = f"Static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newfilename, img)
            sql_statement = "INSERT INTO OPERATIONS (CDATE, CTIME, INPUT_IMG, OUTPUT_IMG, operation_type) VALUES (CURDATE(), NOW(), %s, %s, %s);"
            my_cursor.execute(sql_statement, (input_img, output_img, operation_type))
            mydb.commit()
            return newfilename
        case "cjpg":
            operation_type = "Convert to JPG"
            newfilename = f"Static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newfilename, img)
            sql_statement = "INSERT INTO OPERATIONS (CDATE, CTIME, INPUT_IMG, OUTPUT_IMG, operation_type) VALUES (CURDATE(), NOW(), %s, %s, %s);"
            my_cursor.execute(sql_statement, (input_img, output_img, operation_type))
            mydb.commit()
            return newfilename
        case "cpng":
            operation_type = "Convert to PNG"
            newfilename = f"Static/{filename.split('.')[0]}.png"
            cv2.imwrite(newfilename, img)
            sql_statement = "INSERT INTO OPERATIONS (CDATE, CTIME, INPUT_IMG, OUTPUT_IMG, operation_type) VALUES (CURDATE(), NOW(), %s, %s, %s);"
            my_cursor.execute(sql_statement, (input_img, output_img, operation_type))
            mydb.commit()
            return newfilename
        case "cpdf":
            operation_type = "Convert to PDF"
            img_path = f"Uploads/{filename}"
            newfilename = f"Static/{filename.split('.')[0]}.pdf"
            image = Image.open(img_path)
            pdf_bytes = img2pdf.convert(image.filename)
            file = open(newfilename, "wb")
            file.write(pdf_bytes)
            image.close()
            file.close()
            sql_statement = "INSERT INTO OPERATIONS (CDATE, CTIME, INPUT_IMG, OUTPUT_IMG, operation_type) VALUES (CURDATE(), NOW(), %s, %s, %s);"
            my_cursor.execute(sql_statement, (input_img, output_img, operation_type))
            mydb.commit()
            return newfilename
    pass

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/about')
def about():
    return render_template("about.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/signup')
def signup():
    return render_template("signup.html")

@app.route('/texttohandwriting')
def texttohandwriting():
    return render_template("texttohandwriting.html")

@app.route('/imageconverter')
def imageconverter():
   return render_template("imageconverter.html")

@app.route('/imageEnhancer')
def imageEnhancer():
    return render_template("imageEnhancer.html")

@app.route('/imageCompressor')
def imageCompressor():
    return render_template("imageCompressor.html")

@app.route('/attendanceCalc')
def attendanceCalc():
    return render_template("attendanceCalc.html")

@app.route('/imgToText')
def imgToText():
    return render_template("imgToText.html")

@app.route('/backgroundRemover')
def backgroundRemover():
    return render_template("backgroundRemover.html")

@app.route('/plagerismChecker')
def plagerismChecker():
    return render_template("plagerismChecker.html")

@app.route('/textToSpeech')
def textToSpeech():
    return render_template("textToSpeech.html")

@app.route('/audioTranscriber')
def audioTranscriber():
    return render_template("audioTranscriber.html")

@app.route('/audioConverter')
def audioConverter():
    return render_template("audioConverter.html")

@app.route('/pdfTranslator')
def pdfTranslator():
    return render_template("pdfTranslator.html")

@app.route('/imgToGrayscale')
def imgToGrayscale():
    return render_template("imgToGrayscale.html")

@app.route('/unitConverter')
def unitConverter():
    return render_template("unitConverter.html")

@app.route('/qrCodeGenerator')
def qrCodeGenerator():
    return render_template("qrCodeGenerator.html")

@app.route('/urlShortner')
def urlShortner():
    return render_template("urlShortner.html")

@app.route('/imageconverterfunc', methods=["GET", "POST"])
def imageconverterfunc():
    if request.method == "POST":
        operation = request.form.get("operation")
        #return "POST REQUEST IS HERE"
     # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template("error.html")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "error no seleceted file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"your image has been processed and is available <a href='/{new}' target='_blank'>HERE</a>")
            return render_template("imageconverter.html")
    return render_template("imageconverter.html")

@app.route('/imageEnhancerfunc', methods=["GET", "POST"])
def imageEnhancerfunc():
    if request.method == "POST":
        operation = request.form.get("operation")
        #return "POST REQUEST IS HERE"
     # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template("error.html")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "error no seleceted file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = enhancingImg(filename)
            flash(f"your image has been processed and is available <a href='/{new}' target='_blank'>HERE</a>")
            return render_template("imageEnhancer.html")
    return render_template("imageEnhancer.html")

@app.route('/imgToGrayscalefunc', methods=["GET", "POST"])
def imgToGrayscalefunc():
    if request.method == "POST":
        operation = request.form.get("operation")
        #return "POST REQUEST IS HERE"
     # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return render_template("error.html")
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return "error no seleceted file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = grayScale(filename)
            flash(f"your image has been processed and is available <a href='/{new}' target='_blank'>HERE</a>")
            return render_template("imgToGrayscale.html")
    return render_template("imgToGrayscale.html")

if __name__ == '__main__':
    app.run(debug=True, port=5000)
