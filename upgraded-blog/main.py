from flask import Flask, render_template, request
from datetime import date, timedelta
import requests
import smtplib
from dotenv import load_dotenv
import os


load_dotenv()

my_email = os.getenv("EMAIL")
to_email = os.getenv("TO_EMAIL")
password = os.getenv("EMAIL_PASSWORD")

app = Flask(__name__)

response =requests.get('https://api.npoint.io/bb22565080ae15a79a83')
blog_posts =response.json()

for post in blog_posts:
    post.setdefault('author', 'Dominik Bednář')
    post.setdefault('date', date.today().strftime("%Y-%m-%d"))

@app.route('/')
def get_all_posts():
    return render_template("index.html", posts=blog_posts)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            # Šifrování
            connection.starttls()
            # Login pod kterým odešlu mail
            connection.login(user=my_email, password=password)
            # Struktura mainlu
            connection.sendmail(
                from_addr=my_email,
                to_addrs=to_email,
                msg=f"Subject:Travel_blog\n\nName: {data['name']}\nEmail: {data['email']}\nPhone: {data['phone']}\nMessage: {data['message']}")
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)



@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in blog_posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)



if __name__ == "__main__":
    app.run(debug=True)