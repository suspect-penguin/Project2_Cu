from flask import Flask, render_template, request
import requests
import os
from dotenv import load_dotenv

# Инициализация приложения и загрузка переменных окружения
app = Flask(__name__)
load_dotenv()
API_KEY = os.getenv("ACCUWEATHER_TOKEN")


def get_weather(city):
    location_url = f"http://dataservice.accuweather.com/locations/v1/cities/search"
    params = {"apikey": API_KEY, "q": city, "language": "ru-ru"}
    location_response = requests.get(location_url, params=params).json()

    if location_response:
        location_key = location_response[0]['Key']
        weather_url = f"http://dataservice.accuweather.com/currentconditions/v1/{location_key}"
        weather_params = {"apikey": API_KEY, "language": "ru-ru", "details": "true"}
        weather_response = requests.get(weather_url, params=weather_params).json()

        if weather_response:
            return {
                "city": city,
                "temperature": weather_response[0]['Temperature']['Metric']['Value'],
                "humidity": weather_response[0]['RelativeHumidity'],
                "wind_speed": round(weather_response[0]['Wind']['Speed']['Metric']['Value'] / 3.6, 2),
                "precipitation": weather_response[0]['HasPrecipitation'],
                "description": weather_response[0]['WeatherText']
            }
    return None


def check_bad_weather(weather, temp, humidity, wind):
    conditions = {}

    # Температура
    actual_temp = weather['temperature']
    if temp:
        preferred_temp = float(temp)
        if preferred_temp - 4 <= actual_temp <= preferred_temp + 4:
            conditions['temperature'] = 'Температура соответствует вашим предпочтениям'
        else:
            conditions['temperature'] = 'Температура плохая(не соответствует предпочтениям)'
    elif 0 <= actual_temp <= 34:
        conditions['temperature'] = 'Температура в пределах допустимых значений'
    else:
        conditions['temperature'] = 'Температура плохая'

    # Влажность
    actual_humidity = weather['humidity']
    if humidity:
        preferred_humidity = float(humidity)
        if preferred_humidity - 10 <= actual_humidity <= preferred_humidity + 10:
            conditions['humidity'] = 'Влажность соответствует вашим предпочтениям'
        else:
            conditions['humidity'] = 'Влажность плохая(не соответствует предпочтениям)'
    elif 60 <= actual_humidity <= 80:
        conditions['humidity'] = 'Влажность комфортная'
    else:
        conditions['humidity'] = 'Влажность плохая'

    # Скорость ветра
    actual_wind = weather['wind_speed']
    if wind:
        preferred_wind_speed = float(wind)
        if actual_wind <= preferred_wind_speed:
            conditions['wind_speed'] = 'Скорость ветра в пределах предпочтений'
        else:
            conditions['wind_speed'] = 'Скорость ветра плохая(не соответствует предпочтению)'
    elif actual_wind <= 15:
        conditions['wind_speed'] = 'Скорость ветра комфортная'
    else:
        conditions['wind_speed'] = 'Скорость плохая'

    return conditions


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/check_weather', methods=['POST'])
def check_weather():
    start_city = request.form['start_city']
    end_city = request.form['end_city']

    temp_pref = request.form.get('temperature')
    humidity_pref = request.form.get('humidity')
    wind_pref = request.form.get('wind_speed')

    # Получение данных о погоде
    start_weather = get_weather(start_city)
    end_weather = get_weather(end_city)

    if not start_weather or not end_weather:
        return render_template('error.html', error_message="Не удалось получить данные о погоде. Проверьте ввод.")

    try:
        start_conditions = check_bad_weather(start_weather, temp_pref, humidity_pref, wind_pref)
        end_conditions = check_bad_weather(end_weather, temp_pref, humidity_pref, wind_pref)
    except Exception as e:
        return render_template('error.html', error_message=f"Ошибка обработки данных: {e}")

    return render_template(
        'res.html',
        start_weather=start_weather,
        end_weather=end_weather,
        start_conditions=start_conditions,
        end_conditions=end_conditions
    )


if __name__ == '__main__':
    app.run(debug=True)
