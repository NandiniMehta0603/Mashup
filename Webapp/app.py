from flask import Flask, render_template, request, send_file
import os
import zipfile
import sys
from mashup import mash
import requests
import base64
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        singer_name = request.form.get("singer_name")
        number_of_videos = int(request.form.get("number_of_videos"))
        duration_of_each_video = int(request.form.get("duration_of_each_video"))
        email = request.form.get("email")

        mash(singer_name,number_of_videos,duration_of_each_video)
        # Generate a dummy zip file
        with zipfile.ZipFile("videos.zip", "w") as zip:
            zip.write("out.mp3")

        # Send the zip file as an attachment to the entered email
        send_email(singer_name, email, "videos.zip")

        return "Zip file sent successfully!"

    return render_template("index.html")


def send_email(singer_name, receiver_email, file):
    subject = "Mashup file of "+ singer_name
    body = "PFA mashup file of "+ singer_name
    message = MIMEMultipart()
    password = "uypswxasbjjdvwad"
    message["From"] = "nandini.python6@gmail.com"
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    with open(file, "rb") as attachment:
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
    "Content-Disposition",
    f"attachment; filename= {file}",
    )

    message.attach(part)
    text = message.as_string()
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login("nandini.python6@gmail.com", password)
        server.sendmail("nandini.python6@gmail.com", receiver_email, text)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)