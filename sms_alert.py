from twilio.rest import Client

account_sid = "AC3c9e62ba587e5f81ad83c9199c6311ee"
auth_token = "485f9b4e7fe1709f277b326e4726a4ad"

client = Client(account_sid, auth_token)
def send_cpv_alert(dog_name, breed, age,  result):
    message = f"""
⚠️ CPV ALERT ⚠️


Dog Name: {dog_name}
Breed: {breed}
Age: {age}

Status: {result}

Please consult a veterinarian immediately.
"""

    message = client.messages.create(
        body=message,
        from_="+18704991348",   # Twilio number
        to= "+919042861280"  # Your verified number
    )

    print(message.sid)
