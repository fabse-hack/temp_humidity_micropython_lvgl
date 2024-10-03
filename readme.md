# Temperature and Humidity with MicroPython and LVGL
  
**Content:**  
- [Temperature and Humidity with MicroPython and LVGL](#temperature-and-humidity-with-micropython-and-lvgl)
- [Hardware](#hardware)
- [Project Description](#project-description)
- [Code](#code)
- [CAD Case](#cad-case)
- [To Do](#to-do)

# Hardware
- ILI9341 Display
- Lolin ESP32-S2 Mini
- DHT11 Sensor
- Neopixel LED (P9823)

![image](ili9341+esp32_s2_mini.jpg)

# Project Description  
In this project, I'll explain how I built a temperature and humidity display using MicroPython and LVGL.

- **Building the Firmware:**  
  I checked out lvgl-micropython from [lvgl-micropython](https://github.com/lvgl/lv_micropython) and built the binary file for the ESP32-S2 Mini with the ILI9341 display. I'm not sharing the exact make command because the code is still under development and there are ongoing changes.

- **Wiring the ESP32-S2 Mini to the ILI9341 and DHT11:**  
  Proper connections were made between the ESP32-S2 Mini and the ILI9341 display, as well as the DHT11 sensor. You can refer to the `main.py` for the pin definitions.

- **Using Squareline Studio:**  
  I downloaded [Squareline Studio](https://squareline.io/). Although it's not recommended by the lvgl_micropython developers due to compatibility issues with the generated code, I used it and customized the code to fit the lvgl_micropython bindings from kdschlosser.

- **Additional Features:**  
  - **German Time:** The `German_time` class handles synchronization with an NTP server, including summer and winter time adjustments, though I'm not yet 100% satisfied with the solution.
  - **MQTT:** The project includes MQTT functionality. If you use Home Assistant, you can send the temperature and humidity measurements via MQTT to your MySQL database.
  - **WiFi Connection:** The code attempts to connect to your defined SSID and password. If unsuccessful, it opens an access point.
  - **Error Exceptions:** I've implemented "try/except" blocks in several places to handle errors, timeouts, or OS errors, and log error messages in the MicroPython REPL.
  - **Automatic Y-Axis Range Adjustments:** The Y-axis range in both diagrams adjusts automatically.
  - **Automatic X-Axis Range:** The X-axis range in both diagrams updates automatically (one step per hour).

# Code
The project uses asyncio for asynchronous programming. It includes:

- An LVGL-based UI
- A `German_time` class
- An MQTT class
- An asyncio `data_to_lvgl_every_hour` function
- An asyncio `data_to_lvgl_every_second` function
- `asyncio.gather` for running multiple coroutines concurrently
- Global variables
- Neopixel LED for status indication
- Exception handling for information logging

# CAD Case

UNDER CONSTRUCTION!  
  
I provide CAD files in the following formats: `.par`, `.asm`, and `.stl`.

For 3D printing, I have included built-in support structures. You can slice it without additional support. The support structures are in the `.asm` (assembly) file.

![image](cad_case.jpg)

Here are the direct download links:
- [Link1](#)
- [Link2](#)
- [Link3](#)
- [Link4](#)

# To Do
- provide CAD Files & Photos
- add printables project site
- add blog entry to fabse-hack
- posting repo to kdschlossers lvgl_binding
- Code is runnable but not yet finished (99%)
- Create a YouTube video tutorial (unhappily, I didn't record the building process of this project)
