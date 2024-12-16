#import tensorflow.lite as tflite
import numpy as np 
import tflite_runtime.interpreter as tflite
from keras_image_helper import create_preprocessor



interpreter = tflite.Interpreter(model_path='hairstyle-model.tflite')
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']


from io import BytesIO
from urllib import request

from PIL import Image

def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img
def preprocess_input(x):
    
    return x/255.0

#url='https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg'


def predict(url):
    img=download_image(url)
    img=prepare_image(img, target_size=(200,200))

    x = np.array(img, dtype='float32')
    X = np.array([x])
    X = preprocess_input(X)

    interpreter.set_tensor(input_index, X)
    interpreter.invoke()
    preds = interpreter.get_tensor(output_index)
    
    return float(preds[0,0])


def lambda_handler(event, context):
    url = event['url']
    pred = predict(url)

    result ={
        'prediction':pred
    }


    return result