import requests
import time

url = "https://biashara-connect-backend.onrender.com/api/auth/register/buyer/"

data = {
    "first_name": "Test",
    "last_name": "Buyer",
    "email": f"test{int(time.time())}@example.com",
    "password": "Test12345",
    "confirm_password": "Test12345",  # ← ADD THIS
    "phone": "+254700000001",
    "location": "Nairobi"
}

print("Sending:", data)
response = requests.post(url, json=data)

print("Status Code:", response.status_code)
print("Response:", response.text)