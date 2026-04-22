
from flask import Flask, render_template, request, redirect, url_for, flash, session
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
from predict import predict_cpv
from sms_alert import send_cpv_alert
import csv


app = Flask(__name__)
app.secret_key = "supersecretkey"

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["cpv_prediction"]
collection = db["users"]

collection.insert_one({"test":"ok"})


# Home
@app.route("/")
def home():
    return render_template("index.html")

# Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        contact = request.form['contact']
        password = request.form['password']
        address = request.form['address']


        if collection.find_one({"email": email}):
            return "Email already exists"


        collection.insert_one({
            'email': email,
            'contact': contact,
            'address': address,

            'password': generate_password_hash(password)
        })

        return redirect('/login')

    return render_template('register.html')



@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = collection.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            session["email"] = email
            flash("Login successful!", "success")
            return redirect(url_for('dogdetails'))
        else:
            flash("Invalid email or password!", "error")
            return redirect(url_for('login'))

    return render_template('login.html')




@app.route("/dogdetails", methods=["GET", "POST"])
def dogdetails():

    if "email" not in session:
        flash("Please login first!", "error")
        return redirect(url_for("login"))

    if request.method == "POST":

        dog_name = request.form.get("dog_name")
        breed = request.form.get("breed")
        age = request.form.get("age")
        weight = request.form.get("weight")
        gender = request.form.get("gender")

        symptoms = [
            int(request.form.get("vomiting", 0)),
            int(request.form.get("diarrhea", 0)),
            int(request.form.get("bloody_diarrhea", 0)),
            int(request.form.get("fever", 0)),
            int(request.form.get("loss_appetite", 0)),
            int(request.form.get("lethargy", 0)),
            int(request.form.get("dehydration", 0)),
            int(request.form.get("weight_loss", 0)),
            int(request.form.get("abdominal_pain", 0)),
            int(request.form.get("vaccination_status", 0)),
            int(request.form.get("white_blood_cell_low", 0))
        ]

        # ✅ Prediction INSIDE POST
        result = predict_cpv(symptoms)

        # ✅ Store in MongoDB
        collection.insert_one({
            "email": session["email"],
            "dog_name": dog_name,
            "breed": breed,
            "age": age,
            "weight": weight,
            "gender": gender,
            "symptoms": symptoms,
            "result": result
        })

        # ✅ Send SMS if CPV
        if "CPV" in result:
            send_cpv_alert(
                dog_name=dog_name,
                breed=breed,
                age=age,
                result=result
            )

        # ✅ Tips
        tips = []
        if "CPV" in result:
            tips = [
                "Keep your dog isolated to avoid spreading infection.",
                "Provide plenty of clean water to prevent dehydration.",
                "Feed easily digestible food recommended by vet.",
                "Monitor temperature and watch for vomiting/diarrhea.",
                "Take your dog to a veterinarian immediately.",
                "Maintain strict hygiene of bedding and feeding areas."
            ]

          


        return render_template(
           "result.html",
            result=result,
            dog_name=dog_name,
            breed=breed,
            age=age,
            weight=weight,
            gender=gender,
            tips=tips
            
            )

   

    # ✅ GET request
    return render_template("dogdetails.html")


@app.route("/nearby", methods=["GET","POST"])
def nearby():
    hospitals = []

    if request.method == "POST":
        district = request.form.get("district")

        with open("hospitals.csv", newline="", encoding="utf-8") as file:

            reader = csv.DictReader(file)
            for row in reader:
                if row["district"].lower() == district.lower():
                    hospitals.append(row)

    return render_template("nearby.html", hospitals=hospitals)


# Logout
@app.route("/logout")
def logout():
    session.pop("email", None)
    flash("Logged out successfully!", "success")
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True)
