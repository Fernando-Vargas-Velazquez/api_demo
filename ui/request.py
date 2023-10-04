import requests

URI = "https://8000-fernandovargasv-apidemo-j3n8e2m2yyu.ws-us105.gitpod.io/v1/contactos"

response = requests.get(URI)

print(f"GET : {response.text}")
print(f"GET : {response.status_code}")

data = {
  "nombre": "Nando",
  "email": "preuba@gmail.com"
}
response = requests.post(URI, json=data)

print(f"POST : {response.text}")
print(f"POST : {response.status_code}")

