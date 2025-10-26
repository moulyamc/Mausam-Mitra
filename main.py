from flask import Flask, render_template,redirect,request,url_for,jsonify
from app1 import main as get_weather_data  
import datetime
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///locations.db'  # Use SQLite for simplicity
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create a Location model
class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(100), nullable=False)
    country = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Location {self.city}, {self.state}, {self.country}>'


now = datetime.datetime.now()
current_time = now.strftime("%I:%M %p")  # Format: HH:MM AM/PM
print(current_time)



current_day = datetime.datetime.now().strftime("%A")  

print(current_day)

current_date = datetime.datetime.now().strftime("%d/%m")


@app.route('/search', methods=['POST'])
def search():
    search_query = request.form.get('search_query').lower()
    
    # Redirect to /today for Bengaluru
    if search_query == "bengaluru":
        return redirect(url_for('today'))
    
    # Redirect to external links for other cities
    elif search_query == "delhi":
        return redirect("https://www.msn.com/en-gb/weather/forecast/in-New-Delhi,Delhi?loc=eyJsIjoiTmV3IERlbGhpIiwiciI6IkRlbGhpIiwicjIiOiJOZXcgRGVsaGkiLCJjIjoiSW5kaWEiLCJpIjoiSU4iLCJ0IjoxMDIsImciOiJlbi1nYiIsIngiOiI3Ny4yMTg4IiwieSI6IjI4LjYzMjQifQ%3D%3D&ocid=ansmsnweather&weadegreetype=C")
    elif search_query == "ahmedabad":
        return redirect("https://www.msn.com/en-gb/weather/forecast/in-Ahmedabad,Gujarat?loc=eyJsIjoiQWhtZWRhYmFkIiwiciI6Ikd1amFyYXQiLCJjIjoiSW5kaWEiLCJpIjoiSU4iLCJ0IjoxMDIsImciOiJlbi1nYiIsIngiOiI3Mi41OTE4IiwieSI6IjIzLjAxNDUifQ%3D%3D&ocid=ansmsnweather&weadegreetype=C")
    elif search_query == "kerala":
        return redirect("https://www.msn.com/en-gb/weather/forecast/in-Thrissur,Kerala?loc=eyJhIjoiS2VyYWxhIEFncmljdWx0dXJhbCBVbml2ZXJzaXR5IiwibCI6IlRocmlzc3VyIiwiciI6IktlcmFsYSIsImMiOiJJbmRpYSIsImkiOiJJTiIsInQiOjEwMiwiZyI6ImVuLWdiIiwieCI6Ijc2LjI4NjciLCJ5IjoiMTAuNTQ5In0%3D&ocid=ansmsnweather&weadegreetype=C")
    elif search_query == "gujrat":
        return redirect("https://www.msn.com/en-gb/weather/forecast/in-Chennai,Tamil-Nadu?loc=eyJsIjoiQ2hlbm5haSIsInIiOiJUYW1pbCBOYWR1IiwiYyI6IkluZGlhIiwiaSI6IklOIiwidCI6MTAyLCJnIjoiZW4tZ2IiLCJ4IjoiODAuMjAxOSIsInkiOiIxMy4wNzIxIn0%3D&ocid=ansmsnweather&weadegreetype=C")
    elif search_query == "chennai":
        return redirect("https://www.msn.com/en-gb/weather/forecast/in-Gujr%C4%81t,Punjab?loc=eyJsIjoiR3VqcsSBdCIsInIiOiJQdW5qYWIiLCJjIjoiUGFraXN0YW4iLCJpIjoiUEsiLCJ0IjoxMDIsImciOiJlbi1nYiIsIngiOiI3NC4wNjcyIiwieSI6IjMyLjU4MzMifQ%3D%3D&ocid=ansmsnweather&weadegreetype=C")
    # You can add more conditions for other cities or states here
    elif search_query == "kashmir":
        return redirect("https://www.msn.com/en-gb/weather/forecast/in-Kashmir-Residency,India?loc=eyJsIjoiS2FzaG1pciBSZXNpZGVuY3kiLCJjIjoiSW5kaWEiLCJpIjoiSU4iLCJ0IjoxMDEsImciOiJlbi1nYiIsIngiOiI3Ny41ODA0IiwieSI6IjE0LjY3MTIifQ%3D%3D&ocid=ansmsnweather&weadegreetype=C")
    elif  search_query == "pune":
        return redirect("https://www.msn.com/en-gb/weather/forecast/in-Pune,Maharashtra?loc=eyJsIjoiUHVuZSIsInIiOiJNYWhhcmFzaHRyYSIsInIyIjoiUHVuZSIsImMiOiJJbmRpYSIsImkiOiJJTiIsInQiOjEwMiwiZyI6ImVuLWdiIiwieCI6IjczLjg3NDMiLCJ5IjoiMTguNTI4OSJ9&ocid=ansmsnweather&weadegreetype=C")

    else:
        return "No matching city or state found", 404



@app.route('/add', methods=['POST'])
def add_location():
    city = request.form.get('city')
    state = request.form.get('state')
    country = request.form.get('country')

    # Create a new Location instance
    new_location = Location(city=city, state=state, country=country)
    
    # Add to the session and commit
    db.session.add(new_location)
    db.session.commit()

    # Redirect to the home page
    return redirect('/home')


user_location = {"city": "", "state": ""}

@app.route('/')
def front_page():
    return render_template('front.html')

@app.route('/submit-location', methods=['POST'])
def submit_location():
    data = request.json
    user_location["city"] = data["city"]
    user_location["state"] = data["state"]
    return jsonify({"message": "Location received"}), 200

@app.route('/accuracy')
def accuracy():
    return render_template('accuracy.html')

@app.route('/home')
def index():
    city_name = 'Bengaluru'
    state_code = 'Karnataka'
    country_code = 'India'

   
    weather_info = get_weather_data(city_name, state_code, country_code)
    
    
    print("Weather Info:", weather_info)

    
    if weather_info is None:
        return "Failed to retrieve weather data", 500
    
    # Assign the weather details to variables if weather_info is valid
    banglore_main = weather_info.main
    bangalore_temp = weather_info.temp
    bangalore_temp_min = weather_info.temp_min
    bangalore_temp_max = weather_info.temp_max
    bangalore_humidity = weather_info.humidity
    bangalore_pressure = weather_info.pressure
    bangalore_visibility = weather_info.visibility
    bangalore_wind_speed = weather_info.speed
    bangalore_wind_deg = weather_info.deg
    bangalore_timezone = weather_info.timezone
    bangalore_description = weather_info.description
    banglore_icon = weather_info.icon

    # Pass the variables to the template
    return render_template('home.html',
                           bangalore_temp=bangalore_temp,
                           bangalore_temp_min=bangalore_temp_min,
                           bangalore_temp_max=bangalore_temp_max,
                           bangalore_humidity=bangalore_humidity,
                           bangalore_pressure=bangalore_pressure,
                           bangalore_visibility=bangalore_visibility,
                           bangalore_wind_speed=bangalore_wind_speed,
                           bangalore_wind_deg=bangalore_wind_deg,
                           bangalore_timezone=bangalore_timezone,
                           bangalore_description=bangalore_description,banglore_main = banglore_main,banglore_icon = banglore_icon,current_date = current_date,location=user_location)

# Other routes
@app.route('/today')
def today():
    city_name = 'Bengaluru'
    state_code = 'Karnataka'
    country_code = 'India'

    # Fetch weather data for Bengaluru
    weather_info = get_weather_data(city_name, state_code, country_code)
    
    # Debugging step: Print the weather_info object
    print("Weather Info:", weather_info)

    # If weather_info is None or invalid, return an error message
    if weather_info is None:
        return "Failed to retrieve weather data", 500
    
    # Assign the weather details to variables if weather_info is valid
    bangalore_temp = weather_info.temp
    bangalore_temp_min = weather_info.temp_min
    bangalore_temp_max = weather_info.temp_max
    bangalore_humidity = weather_info.humidity
    bangalore_pressure = weather_info.pressure
    bangalore_visibility = weather_info.visibility
    bangalore_wind_speed = weather_info.speed
    bangalore_wind_deg = weather_info.deg
    bangalore_timezone = weather_info.timezone
    bangalore_description = weather_info.description
    banglore_main = weather_info.main
    banglore_icon = weather_info.icon
    
    return render_template('today.html',bangalore_temp = bangalore_temp,bangalore_temp_min=bangalore_temp_min,bangalore_temp_max=bangalore_temp_max,bangalore_description = bangalore_description, bangalore_wind_speed = bangalore_wind_speed,bangalore_wind_deg = bangalore_wind_deg,current_time = current_time,
                           current_day = current_day,banglore_main = banglore_main,banglore_icon = banglore_icon,current_date = current_date)

from datetime import datetime, timedelta

@app.route('/hourly')
def hourly():
    city_name = 'Bengaluru'
    state_code = 'Karnataka'
    country_code = 'India'

    # Fetch weather data for Bengaluru
    weather_info = get_weather_data(city_name, state_code, country_code)
    
    # If weather_info is None or invalid, return an error message
    if weather_info is None:
        return "Failed to retrieve weather data", 500
    
    # Assign the weather details to variables if weather_info is valid
    bangalore_temp = weather_info.temp
    bangalore_temp_min = weather_info.temp_min
    bangalore_temp_max = weather_info.temp_max
    bangalore_humidity = weather_info.humidity
    bangalore_pressure = weather_info.pressure
    bangalore_visibility = weather_info.visibility
    bangalore_wind_speed = weather_info.speed
    bangalore_wind_deg = weather_info.deg
    bangalore_description = weather_info.description
    bangalore_main = weather_info.main
    banglore_icon = weather_info.icon

    # Get current time
    current_time = datetime.now()
    formatted_current_time = current_time.strftime("%I:%M %p")  # Format: HH:MM AM/PM

    # Generate times for the next 8 blocks and format them with AM/PM
    formatted_times = [(current_time + timedelta(hours=i)).strftime("%I:%M %p") for i in range(8)]
    
    return render_template('hourly.html',
                           bangalore_temp=bangalore_temp,
                           bangalore_temp_min=bangalore_temp_min,
                           bangalore_temp_max=bangalore_temp_max,
                           bangalore_description=bangalore_description,
                           bangalore_wind_speed=bangalore_wind_speed,
                           bangalore_wind_deg=bangalore_wind_deg,
                           bangalore_humidity=bangalore_humidity,
                           bangalore_pressure=bangalore_pressure,
                           bangalore_visibility=bangalore_visibility,
                           bangalore_main=bangalore_main,
                           current_time = current_time,banglore_icon = banglore_icon,current_date = current_date,formatted_times =formatted_times)
@app.route('/daily')
def daily():
    city_name = 'Bengaluru'
    state_code = 'Karnataka'
    country_code = 'India'

    # Fetch weather data for Bengaluru (current weather data)
    weather_info = get_weather_data(city_name, state_code, country_code)

    if weather_info is None:
        return "Failed to retrieve weather data", 500
    
    bangalore_temp = weather_info.temp
    bangalore_temp_min = weather_info.temp_min
    bangalore_temp_max = weather_info.temp_max
    bangalore_humidity = weather_info.humidity
    bangalore_pressure = weather_info.pressure
    bangalore_visibility = weather_info.visibility
    bangalore_wind_speed = weather_info.speed
    bangalore_wind_deg = weather_info.deg
    bangalore_timezone = weather_info.timezone
    bangalore_description = weather_info.description
    banglore_main = weather_info.main
    banglore_icon = weather_info.icon

    current_weather = {
        'temp': weather_info.temp,
        'temp_min': weather_info.temp_min,
        'temp_max': weather_info.temp_max,
        'humidity': weather_info.humidity,
        'pressure': weather_info.pressure,
        'visibility': weather_info.visibility,
        'wind_speed': weather_info.speed,
        'wind_deg': weather_info.deg,
        'description': weather_info.description,
        'icon': weather_info.icon  # Use this in the template
    }

    # Get day names and dates for the next 7 days (including today)
    today = datetime.now()
    day_names = [(today + timedelta(days=i)).strftime('%A') for i in range(7)]
    dates = [(today + timedelta(days=i)).strftime('%d/%m') for i in range(7)]

    # Create slight variations for future weather data (for the next 6 days)
    future_weather = []
    for i in range(1, 7):
        future_weather.append({
            'temp_max': current_weather['temp_max'] + i * 0.5,
            'temp_min': current_weather['temp_min'] + i * 0.3,
            'humidity': current_weather['humidity'] + i * 1,
            'wind_speed': current_weather['wind_speed'] + i * 0.2,
            'icon': current_weather['icon'],
            'description': current_weather['description']
        })

    # Render the template with current and future weather data
    return render_template('daily.html',
                           day_names=day_names,
                           dates=dates,
                           current_weather=current_weather,
                           future_weather=future_weather,bangalore_temp = bangalore_temp,bangalore_temp_min=bangalore_temp_min,bangalore_temp_max=bangalore_temp_max,bangalore_description = bangalore_description, bangalore_wind_speed = bangalore_wind_speed,bangalore_wind_deg = bangalore_wind_deg,current_time = current_time,
                           current_day = current_day,bangalore_humidity = bangalore_humidity, bangalore_pressure = bangalore_pressure,bangalore_visibility = bangalore_visibility,banglore_main = banglore_main,banglore_icon = banglore_icon,current_date = current_date)


@app.route('/radar')
def radar():
    city_name = 'Bengaluru'
    state_code = 'Karnataka'
    country_code = 'India'

    # Fetch weather data for Bengaluru
    weather_info = get_weather_data(city_name, state_code, country_code)
    
    # Debugging step: Print the weather_info object
    print("Weather Info:", weather_info)

    # If weather_info is None or invalid, return an error message
    if weather_info is None:
        return "Failed to retrieve weather data", 500
    
    # Assign the weather details to variables if weather_info is valid
    bangalore_temp = weather_info.temp
    bangalore_temp_min = weather_info.temp_min
    bangalore_temp_max = weather_info.temp_max
    bangalore_humidity = weather_info.humidity
    bangalore_pressure = weather_info.pressure
    bangalore_visibility = weather_info.visibility
    bangalore_wind_speed = weather_info.speed
    bangalore_wind_deg = weather_info.deg
    bangalore_timezone = weather_info.timezone
    bangalore_description = weather_info.description
    banglore_main = weather_info.main
    banglore_icon = weather_info.icon
    
    return render_template('radar.html',bangalore_temp = bangalore_temp,bangalore_temp_min=bangalore_temp_min,bangalore_temp_max=bangalore_temp_max,bangalore_description = bangalore_description, bangalore_wind_speed = bangalore_wind_speed,bangalore_wind_deg = bangalore_wind_deg,current_time = current_time,
                           current_day = current_day,bangalore_humidity = bangalore_humidity, bangalore_pressure = bangalore_pressure,bangalore_visibility = bangalore_visibility,banglore_main = banglore_main,banglore_icon = banglore_icon,current_date = current_date)

@app.route('/minute')
def minute():
    city_name = 'Bengaluru'
    state_code = 'Karnataka'
    country_code = 'India'

    # Fetch weather data for Bengaluru
    weather_info = get_weather_data(city_name, state_code, country_code)
    
    # Debugging step: Print the weather_info object
    print("Weather Info:", weather_info)

    # If weather_info is None or invalid, return an error message
    if weather_info is None:
        return "Failed to retrieve weather data", 500
    
    # Assign the weather details to variables if weather_info is valid
    bangalore_temp = weather_info.temp
    bangalore_temp_min = weather_info.temp_min
    bangalore_temp_max = weather_info.temp_max
    bangalore_humidity = weather_info.humidity
    bangalore_pressure = weather_info.pressure
    bangalore_visibility = weather_info.visibility
    bangalore_wind_speed = weather_info.speed
    bangalore_wind_deg = weather_info.deg
    bangalore_timezone = weather_info.timezone
    bangalore_description = weather_info.description
    banglore_main = weather_info.main
    banglore_icon = weather_info.icon
    
    return render_template('minute.html',bangalore_temp = bangalore_temp,bangalore_temp_min=bangalore_temp_min,bangalore_temp_max=bangalore_temp_max,bangalore_description = bangalore_description, bangalore_wind_speed = bangalore_wind_speed,bangalore_wind_deg = bangalore_wind_deg,current_time = current_time,
                           current_day = current_day,bangalore_humidity = bangalore_humidity, bangalore_pressure = bangalore_pressure,bangalore_visibility = bangalore_visibility,banglore_main = banglore_main,banglore_icon = banglore_icon,current_date = current_date,bangalore_timezone = bangalore_timezone)

@app.route('/monthly')
def monthly():
    city_name = 'Bengaluru'
    state_code = 'Karnataka'
    country_code = 'India'

    # Fetch weather data for Bengaluru
    weather_info = get_weather_data(city_name, state_code, country_code)
    
    # Debugging step: Print the weather_info object
    print("Weather Info:", weather_info)

    # If weather_info is None or invalid, return an error message
    if weather_info is None:
        return "Failed to retrieve weather data", 500
    
    # Assign the weather details to variables if weather_info is valid
    bangalore_temp = weather_info.temp
    bangalore_temp_min = weather_info.temp_min
    bangalore_temp_max = weather_info.temp_max
    bangalore_humidity = weather_info.humidity
    bangalore_pressure = weather_info.pressure
    bangalore_visibility = weather_info.visibility
    bangalore_wind_speed = weather_info.speed
    bangalore_wind_deg = weather_info.deg
    bangalore_timezone = weather_info.timezone
    bangalore_description = weather_info.description
    banglore_main = weather_info.main
    banglore_icon = weather_info.icon
    
    return render_template('monthly.html',bangalore_temp = bangalore_temp,bangalore_temp_min=bangalore_temp_min,bangalore_temp_max=bangalore_temp_max,bangalore_description = bangalore_description, bangalore_wind_speed = bangalore_wind_speed,bangalore_wind_deg = bangalore_wind_deg,current_time = current_time,
                           current_day = current_day,bangalore_humidity = bangalore_humidity, bangalore_pressure = bangalore_pressure,bangalore_visibility = bangalore_visibility,banglore_main = banglore_main,banglore_icon = banglore_icon,current_date = current_date)

@app.route('/air')
def air():
    city_name = 'Bengaluru'
    state_code = 'Karnataka'
    country_code = 'India'

    # Fetch weather data for Bengaluru
    weather_info = get_weather_data(city_name, state_code, country_code)
    
    # Debugging step: Print the weather_info object
    print("Weather Info:", weather_info)

    # If weather_info is None or invalid, return an error message
    if weather_info is None:
        return "Failed to retrieve weather data", 500
    
    # Assign the weather details to variables if weather_info is valid
    bangalore_temp = weather_info.temp
    bangalore_temp_min = weather_info.temp_min
    bangalore_temp_max = weather_info.temp_max
    bangalore_humidity = weather_info.humidity
    bangalore_pressure = weather_info.pressure
    bangalore_visibility = weather_info.visibility
    bangalore_wind_speed = weather_info.speed
    bangalore_wind_deg = weather_info.deg
    bangalore_timezone = weather_info.timezone
    bangalore_description = weather_info.description
    banglore_main = weather_info.main
    banglore_icon = weather_info.icon
    return render_template('air.html',bangalore_temp = bangalore_temp,bangalore_temp_min=bangalore_temp_min,bangalore_temp_max=bangalore_temp_max,bangalore_description = bangalore_description, bangalore_wind_speed = bangalore_wind_speed,bangalore_wind_deg = bangalore_wind_deg,current_time = current_time,
                           current_day = current_day,bangalore_humidity = bangalore_humidity, bangalore_pressure = bangalore_pressure,bangalore_visibility = bangalore_visibility,banglore_main = banglore_main,banglore_icon = banglore_icon,current_date = current_date)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/bus')
def business():
    return render_template('business.html')

if __name__ == '__main__':
    app.run(debug=True)
