import requests

url = 'http://localhost:9000/2015-03-31/functions/function/invocations'



data = {'url':'http://bit.ly/mlbookcamp-pants'}

result = requests.post(url, json=data).json()
print(result)