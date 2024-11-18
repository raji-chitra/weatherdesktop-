import tkinter as tk
import requests
import time
from plyer import notification


def getWeather(event=None):
    city = textfield.get()
    api = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=965cace61cc5e11b3e5d973ccabe5b72"
    try:
        json_data = requests.get(api).json()

        if json_data.get("cod") != 200:
            raise ValueError(f"Error: {json_data.get('message', 'Invalid City')}")


        condition = json_data['weather'][0]['main']
        temp = int(json_data['main']['temp'] - 273.15)
        min_temp = int(json_data['main']['temp_min'] - 273.15)
        max_temp = int(json_data['main']['temp_max'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']
        sunrise = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunrise']))
        sunset = time.strftime("%I:%M:%S", time.gmtime(json_data['sys']['sunset']))


        final_info = condition + "\n" + str(temp) + "°C"
        final_data = (f"Max Temp: {max_temp}°C\nMin Temp: {min_temp}°C\n"
                      f"Pressure: {pressure} hPa\nHumidity: {humidity}%\n"
                      f"Wind Speed: {wind} m/s\nSunrise: {sunrise} UTC\nSunset: {sunset} UTC")

        label1.config(text=final_info)
        label2.config(text=final_data)


        notification_title = f"Weather in {city}"
        notification_message = (f"Condition: {condition}\n"
                                f"Temperature: {temp}°C\n"
                                f"Max Temp: {max_temp}°C\n"
                                f"Min Temp: {min_temp}°C\n"
                                f"Humidity: {humidity}%\n"
                                f"Wind Speed: {wind} m/s")


        notification.notify(
            title=notification_title,
            message=notification_message,
            timeout=10
        )

    except requests.exceptions.RequestException as req_err:
        label1.config(text="Network error: Unable to retrieve data")
        label2.config(text=str(req_err))
    except ValueError as val_err:
        label1.config(text="City not found or invalid")
        label2.config(text=str(val_err))
    except Exception as e:
        label1.config(text="Error retrieving weather data")
        label2.config(text=str(e))



root = tk.Tk()
root.geometry("600x500")
root.title("Weather App")


f = ("poppins", 15, "bold")
t = ("poppins", 35, "bold")


textfield = tk.Entry(root, font=t)
textfield.pack(pady=20)
textfield.focus()
textfield.bind('<Return>', getWeather)


label1 = tk.Label(root, font=t)
label1.pack()
label2 = tk.Label(root, font=f)
label2.pack()


root.mainloop()
