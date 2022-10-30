import requests
url="http://127.0.0.1:4444/getAudio"
with open("sample.mp3",'rb') as file:
    files={"audio":file}
    req=requests.post(url,files=files)
    print(req.status_code)
    print(req.text)
