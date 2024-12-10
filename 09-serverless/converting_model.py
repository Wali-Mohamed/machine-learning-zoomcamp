#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('wget https://github.com/DataTalksClub/machine-learning-zoomcamp/releases/download/chapter7-model/xception_v4_large_08_0.894.h5 -O clothing-model.h5')


# In[ ]:


get_ipython().system('python -V')


# In[ ]:


pip install numpy==1.24


# In[ ]:


import numpy as np

import tensorflow as tf
from tensorflow import keras

tf.__version__


# In[ ]:


get_ipython().system('wget http://bit.ly/mlbookcamp-pants -O pants.jpg')


# In[ ]:


from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.xception import preprocess_input


# In[ ]:


model = keras.models.load_model('clothing-model.h5')


# In[ ]:


img = load_img('pants.jpg', target_size=(299, 299))

x = np.array(img)
X = np.array([x])

X = preprocess_input(X)


# In[ ]:


preds = model.predict(X)


# In[ ]:


preds


# In[ ]:


classes = [
    'dress',
    'hat',
    'longsleeve',
    'outwear',
    'pants',
    'shirt',
    'shoes',
    'shorts',
    'skirt',
    't-shirt'
]


# In[ ]:


dict(zip(classes, preds[0]))


# In[ ]:


converter = tf.lite.TFLiteConverter.from_keras_model(model)

tflite_model = converter.convert()

with open('clothing-model.tflite', 'wb') as f_out:
    f_out.write(tflite_model)


# In[ ]:


get_ipython().system('ls -lh')


# In[ ]:


import tensorflow.lite as tflite


# In[ ]:


interpreter = tflite.Interpreter(model_path='clothing-model.tflite')
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']


# In[ ]:


interpreter.get_input_details()


# In[ ]:


interpreter.get_output_details()


# In[ ]:


interpreter.set_tensor(input_index, X)
interpreter.invoke()
preds = interpreter.get_tensor(output_index)


# In[ ]:


classes = [
    'dress',
    'hat',
    'longsleeve',
    'outwear',
    'pants',
    'shirt',
    'shoes',
    'shorts',
    'skirt',
    't-shirt'
]

dict(zip(classes, preds[0]))


# ## Removing tensorflow dependency

# In[ ]:


from PIL import Image


# In[ ]:


with Image.open('pants.jpg') as img:
    img = img.resize((299, 299), Image.NEAREST)


# In[ ]:


img


# In[ ]:


def preprocess_input(x):
    x /= 127.5
    x -= 1.
    return x


# In[ ]:


x = np.array(img, dtype='float32')
X = np.array([x])

X = preprocess_input(X)


# In[ ]:


interpreter.set_tensor(input_index, X)
interpreter.invoke()
preds = interpreter.get_tensor(output_index)


# In[ ]:


classes = [
    'dress',
    'hat',
    'longsleeve',
    'outwear',
    'pants',
    'shirt',
    'shoes',
    'shorts',
    'skirt',
    't-shirt'
]

dict(zip(classes, preds[0]))


# # Simpler way of doing
# # from Alex Gregorev github we install keras-image-helper

# In[ ]:


get_ipython().system('pip install keras-image-helper')


# In[ ]:


get_ipython().system('pip install --extra-index-url https://google-coral.github.io/py-repo/ tflite_runtime')


# In[1]:


#import tensorflow.lite as tflite
import tflite_runtime.interpreter as tflite
from keras_image_helper import create_preprocessor


# In[6]:


interpreter = tflite.Interpreter(model_path='clothing-model.tflite')
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']


# In[7]:


preprocessor = create_preprocessor('xception', target_size=(299, 299))


# In[8]:


url = 'http://bit.ly/mlbookcamp-pants'
X = preprocessor.from_url(url)


# In[ ]:


interpreter.set_tensor(input_index, X)
interpreter.invoke()
preds = interpreter.get_tensor(output_index)


# In[ ]:


classes = [
    'dress',
    'hat',
    'longsleeve',
    'outwear',
    'pants',
    'shirt',
    'shoes',
    'shorts',
    'skirt',
    't-shirt'
]

dict(zip(classes, preds[0]))


# In[5]:


# converting to python file


# In[4]:


get_ipython().system('jupyter nbconvert --to script converting_model.ipynb')


# In[ ]:




