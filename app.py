from flask import Flask, render_template, request
import requests

app = Flask(__name__)

API_KEY = '0aa9e4c62edc0525abd44d283f00d4e0'

@app.route('/', methods=['GET','POST'])
def index():
    weather_data = None
    if request.method == 'POST':
        city = request.form.get('city')
        if city:
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            response = requests.get(url)
            weather_data = response.json()
        else:
                weather_data = {"error": "City not found!"}
    return render_template('index.html', weather_data=weather_data)


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000,debug=True)
