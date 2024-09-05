from flask import Flask, render_template, request, jsonify
from keras.models import load_model
from keras.preprocessing import image
import numpy as np

import os
import pathlib

import requests
from flask import Flask, session, abort, redirect, request
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

app = Flask(__name__)

dic = {0: 'Benign', 1: 'Malignant'}

model = load_model('BreastCancerSVM.h5')

model.make_predict_function()

def predict_label(img_path):
    i = image.load_img(img_path, target_size=(224, 224))
    i = image.img_to_array(i) / 255.0
    i = i.reshape(1, 224, 224, 3)
    probabilities = model.predict(i)[0]
    predicted_class = int(np.argmax(probabilities))
    return dic[predicted_class]

@app.route("/", methods=['GET', 'POST'])
def main():
    return render_template("index.html")


# Route for the About Us page
@app.route("/about")
def about_page():
    return render_template("about.html")

# Route for the Doctors page
@app.route("/doctors")
def doctors_page():
    return render_template("doctors.html")

# Route for the News/Blog page
@app.route("/blog")
def blog_page():
    return render_template("blog.html")

@app.route("/blog_2")
def blog_2():
    return render_template("blog_2.html")

@app.route("/Jayanti")
def Jayanti_page():
    return render_template("Jayanti.html")

@app.route("/Kalechelvi")
def Kalechelvi_page():
    return render_template("Kalechelvi.html")

@app.route("/Rajeev_Agarwal")
def Rajeev_Agarwal_page():
    return render_template("Rajeev_Agarwal.html")

@app.route("/Ramakant")
def Ramakant_page():
    return render_template("Ramakant.html")

@app.route("/Ramesh_sarin")
def Ramesh_sarin_page():
    return render_template("Ramesh_sarin.html")

@app.route("/Sanjiv_Sharma")
def Sanjiv_Sharma_page():
    return render_template("Sanjiv_Sharma.html")

@app.route("/Jayanti_2")
def Jayanti_2():
    return render_template("Jayanti_2.html")

@app.route("/Kalechelvi_2")
def Kalechelvi_2():
    return render_template("Kalechelvi_2.html")

@app.route("/Rajeev_Agarwal_2")
def Rajeev_Agarwal_2():
    return render_template("Rajeev_Agarwal_2.html")

@app.route("/Ramakant_2")
def Ramakant_2():
    return render_template("Ramakant_2.html")

@app.route("/Ramesh_sarin_2")
def Ramesh_sarin_2():
    return render_template("Ramesh_sarin_2.html")

@app.route("/Sanjiv_Sharma_2")
def Sanjiv_Sharma_2():
    return render_template("Sanjiv_Sharma_2.html")

@app.route("/profile")
def profile():
    return render_template("profile.html")


@app.route("/home")
def home():
    return render_template("index_2.html")


@app.route("/doctors_2")
def doctors_2():
    return render_template("doctors_2.html")

@app.route("/about_2")
def about_2():
    return render_template("about_2.html")

# Route for the prediction model page (consultation page)
@app.route("/model")
def model_page():
    return render_template("model.html")

# Route for handling image submission and prediction
@app.route("/submit", methods=['POST'])
def get_output():
    if request.method == 'POST':
        img = request.files['my_image'] 
        img_path = "static/" + img.filename
        img.save(img_path)
        p = predict_label(img_path)
        return jsonify({"prediction": p, "img_path": img_path})
    

app.secret_key = "CodeSpecialist.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = "67477060356-f01olqjkf36csiqn8qs51md26h7t8tqr.apps.googleusercontent.com"
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
    redirect_uri="http://127.0.0.1:5000/callback"
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@app.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@app.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token,
        request=token_request,
        audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect("/protected_area")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@app.route("/")
def index():
    return render_template('index_2.html')


@app.route("/protected_area")
@login_is_required
def protected_area():
   return render_template('index_2.html')



if __name__ == '__main__':
    app.run(debug=True)
