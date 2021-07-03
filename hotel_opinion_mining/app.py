from flask import Flask, render_template, request
import os
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
nltk.download('punkt')
import tensorflow as tf
import pickle
from tensorflow import keras
from tensorflow.keras.preprocessing.sequence import pad_sequences

physical_devices = tf.config.list_physical_devices('GPU') 
tf.config.experimental.set_memory_growth(physical_devices[0], True)

with open('tokenizer.pickle' , 'rb') as pickle_file:
    tokenizer = pickle.load(pickle_file)
lstm_model = keras.models.load_model('sentimentmodel.h5')
IMAGE_FOLDER = os.path.join('static', 'img_pool')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/sentiment_analysis', methods = ['POST', "GET"])

def sentiment_analysis():
    #TODO read the messeage and encode tokenize and get prediction
    
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']
        review = [message]
        review =  review[0].split(' ')
        stop = stopwords.words('english')
        review = [item for item in review if item not in stop]
        review = tokenizer.texts_to_sequences([review])
        review = pad_sequences(review, padding='post', maxlen= 100)
        prediction = lstm_model.predict_classes(review)
        
    ## 0 is negative, 1 is positive
    #if positive, add the image and the message to that awesome css page
        if(prediction[[0]] == 0):
            import smtplib 
            from email.message import EmailMessage
    
            source_email = "hotelopiniominingproject@gmail.com" #senders Gmail id over here
            password = "hot3lopiniominingproj3ct" #senders Gmail's Password over here 
            msg = EmailMessage()
            msg['Subject'] = 'Negative Hotel Review'  # Subject of Email
            msg['From'] = source_email
            msg['To'] = 'tendaimmutamba@gmail.com'
            email_body = "A negative review has been entered by "+name+ " with email address " +email+" and text "+message
            msg.set_content(email_body) # Email body or Content
            
            with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp: 
                smtp.login(source_email,password) 
                smtp.send_message(msg)
            return render_template('index.html')
        
        else:
            return render_template('about.html', positive=True, message = message)
        
if __name__ == "__main__":
    app.run()
