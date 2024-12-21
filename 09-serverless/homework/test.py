import requests

url = 'http://localhost:8899/2015-03-31/functions/function/invocations'
#url = 'http://localhost:8899'

#data = {'url': 'https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg'}
data = {'url': 'https://pixabay.com/illustrations/girl-woman-portrait-face-fashion-8726241/'}

result = requests.post(url, json=data).json()
print(result)