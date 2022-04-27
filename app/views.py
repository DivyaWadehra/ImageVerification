from app import app
from flask import request, render_template
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image

#Add path to config
app.config['INITIAL_FILE_UPLOAD']="app/static/uploads"
app.config['EXISTING_FILE']="app/static/original"
app.config['GENERATED_FILE']="app/static/generated"

#route to home page
@app.route('/',methods=["GET","POST"])
def index():
    if request.method=="GET":
        return render_template("index.html")
    if request.method=="POST":
        file_upload=request.files['file_upload']
        filename=file_upload.filename
        uploaded_image=Image.open(file_upload).resize((250,160))
        uploaded_image.save(os.path.join(app.config['INITIAL_FILE_UPLOAD'],'image.jpg'))
        #to ensure that original and uploaded are of same size    
        original_image=Image.open(os.path.join(app.config['EXISTING_FILE']),'image.jpg').resize((250,160))
        original_image.save(os.path.join(app.config['EXISTING_FILE'],'image.jpg'))

        #Read uploaded and original image as array
        original_image=cv2.imread(os.path.join(app.config['EXISTING_FILE'],'image.jpg'))
        uploaded_image=cv2.imread(os.path.join(app.config['INITIAL_FILE_UPLOAD'],'image.jpg'))

        #Convert image to grayscale
        original_gray=cv2.cvtColor(original_image,cv2.COLOR_BGR2GRAY)
        uploaded_gray=cv2.cvtColor(uploaded_image,cv2.COLOR_BGR2GRAY)

        (score,diff)=structural_similarity(original_gray,uploaded_gray,full=True)
        diff=(diff*255).astype("unit8")

        #calculate threshold and contours
        thresh=cv2.threshold(diff,0,255,cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        cnts=cv2.findContours(thresh.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        cnts=imutils.grab_contours(cnts)

        #Create bounding rectange of the image using contours
        for c in cnts:
            (x,y,w,h)=cv2.boundingRect(c)
            cv2.rectangle(original_image,(x,y),(x+w,y+h),(0,0,255),2)
            cv2.rectangle(uploaded_image,(x,y),(x+w,y+h),(0,0,255),2)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'],'image_original.jpg'),original_image)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'],'image_uploaded.jpg'),uploaded_image)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'],'image_uploaded.jpg'),diff)
        cv2.imwrite(os.path.join(app.config['GENERATED_FILE'],'image_thersh.jpg'),thresh)
        return render_template("index.html",pred=str(round(score*100,2))+"%"+" correct")
        






