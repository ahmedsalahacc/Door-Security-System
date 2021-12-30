import requests

filename = "C:\\Users\\DELL\\Downloads\\DataBase\\WIN_20211221_15_50_36_Pro.jpg"

req = {
    'id':9,
    'password':"1234"
}

file = {'image':open(filename, 'rb')}
url = 'http://127.0.0.1:3000/auth'
r = requests.post(url,files=file, data=req)
print(r.status_code)