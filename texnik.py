import requests

url = "http://10.190.7.22:55550/api/construction/view"
data = {
    "inn": 200459808,
    "certificate_number": 2340979
}

# POST so'rovnoma yuborish
response = requests.post(url, data=data)

# XML javobni chop etish
print(response.text)
