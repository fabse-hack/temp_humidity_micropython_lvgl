import lvgl as lv
import lcd_bus
import ili9341
from machine import SPI, Pin
import machine
import network
import task_handler
from umqtt.simple import MQTTClient
import dht
import asyncio
import utime
import ntptime
import neopixel

spi_bus = SPI.Bus(
    host=1,
    mosi=11,
    miso=9,
    sck=7
)

display_bus = lcd_bus.SPIBus(
    spi_bus=spi_bus,
    dc=2,
    cs=15,
    freq=40000000,
)

display = ili9341.ILI9341(
    data_bus=display_bus,
    display_width=240,
    display_height=320,
    reset_pin=4,
    reset_state=ili9341.STATE_LOW,
    color_space=lv.COLOR_FORMAT.RGB565,
    rgb565_byte_swap=True
)

display.set_power(True)
display.init()
display.set_rotation(lv.DISPLAY_ROTATION._90)

scrn = lv.screen_active()
scrn.set_style_bg_color(lv.color_hex(0x000000), 0)

dispp = lv.display_get_default()
theme = lv.theme_default_init(dispp, lv.palette_main(lv.PALETTE.BLUE), lv.palette_main(lv.PALETTE.RED), True, lv.font_default())
dispp.set_theme(theme)

# ################################### temperature chart #####################
ui_TemperatureChart = lv.chart(scrn)
ui_TemperatureChart.set_width(184)
ui_TemperatureChart.set_height(63)
ui_TemperatureChart.set_x(60)
ui_TemperatureChart.set_y(-41)
ui_TemperatureChart.set_align(lv.ALIGN.CENTER)
ui_TemperatureChart.add_flag(lv.obj.FLAG.OVERFLOW_VISIBLE)
ui_TemperatureChart.set_type(lv.chart.TYPE.LINE)

ui_TemperatureChart_Xaxis = lv.scale(ui_TemperatureChart)
ui_TemperatureChart_Xaxis.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
ui_TemperatureChart_Xaxis.set_size(lv.pct(100), 50)
ui_TemperatureChart_Xaxis.set_align(lv.ALIGN.BOTTOM_MID)
ui_TemperatureChart_Xaxis.set_y(50 + ui_TemperatureChart.get_style_pad_bottom(lv.PART.MAIN) + ui_TemperatureChart.get_style_border_width(lv.PART.MAIN))

ui_TemperatureChart_Xaxis.set_total_tick_count(10)
ui_TemperatureChart_Xaxis.set_major_tick_every(2)
ui_TemperatureChart_Xaxis.set_style_line_width(0, lv.PART.MAIN)
ui_TemperatureChart_Xaxis.set_style_line_width(1, lv.PART.ITEMS)
ui_TemperatureChart_Xaxis.set_style_line_width(1, lv.PART.INDICATOR)
ui_TemperatureChart_Xaxis.set_style_length(8, lv.PART.INDICATOR)
ui_TemperatureChart_Xaxis.set_style_length(5, lv.PART.ITEMS)

ui_TemperatureChart_Yaxis1 = lv.scale(ui_TemperatureChart)
ui_TemperatureChart_Yaxis1.set_mode(lv.scale.MODE.VERTICAL_LEFT)
ui_TemperatureChart_Yaxis1.set_size(50, lv.pct(100))
ui_TemperatureChart_Yaxis1.set_align(lv.ALIGN.LEFT_MID)
ui_TemperatureChart_Yaxis1.set_x(-50 - ui_TemperatureChart.get_style_pad_left(lv.PART.MAIN) - ui_TemperatureChart.get_style_border_width(lv.PART.MAIN) + 2)

ui_TemperatureChart_Yaxis1.set_style_line_width(0, lv.PART.MAIN)
ui_TemperatureChart_Yaxis1.set_style_line_width(1, lv.PART.ITEMS)
ui_TemperatureChart_Yaxis1.set_style_line_width(1, lv.PART.INDICATOR)
ui_TemperatureChart_Yaxis1.set_style_length(10, lv.PART.INDICATOR)
ui_TemperatureChart_Yaxis1.set_style_length(5, lv.PART.ITEMS)

ui_TemperatureChart_series_1 = ui_TemperatureChart.add_series(lv.color_hex(0x0C00FF), lv.chart.AXIS.PRIMARY_Y)

ui_TemperatureChart.set_style_outline_pad(max(50, 50, 50), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_TemperatureChart.set_style_outline_width(-1, lv.PART.MAIN | lv.STATE.DEFAULT)

ui_TemperatureChart.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

# ################################### temperature chart END ###################
# ################################### humidity chart ##########################

ui_HumidityChart = lv.chart(scrn)
ui_HumidityChart.set_width(184)
ui_HumidityChart.set_height(63)
ui_HumidityChart.set_x(60)
ui_HumidityChart.set_y(60)
ui_HumidityChart.set_align(lv.ALIGN.CENTER)
ui_HumidityChart.add_flag(lv.obj.FLAG.OVERFLOW_VISIBLE)
ui_HumidityChart.set_type(lv.chart.TYPE.LINE)

ui_HumidityChart_Xaxis = lv.scale(ui_HumidityChart)
ui_HumidityChart_Xaxis.set_mode(lv.scale.MODE.HORIZONTAL_BOTTOM)
ui_HumidityChart_Xaxis.set_size(lv.pct(100), 50)
ui_HumidityChart_Xaxis.set_align(lv.ALIGN.BOTTOM_MID)
ui_HumidityChart_Xaxis.set_y(50 + ui_HumidityChart.get_style_pad_bottom(lv.PART.MAIN) + ui_HumidityChart.get_style_border_width(lv.PART.MAIN))
ui_HumidityChart_Xaxis.set_total_tick_count(10)
ui_HumidityChart_Xaxis.set_major_tick_every(2)
ui_HumidityChart_Xaxis.set_style_line_width(0, lv.PART.MAIN)
ui_HumidityChart_Xaxis.set_style_line_width(1, lv.PART.ITEMS)
ui_HumidityChart_Xaxis.set_style_line_width(1, lv.PART.INDICATOR)
ui_HumidityChart_Xaxis.set_style_length(10, lv.PART.INDICATOR)
ui_HumidityChart_Xaxis.set_style_length(5, lv.PART.ITEMS)

ui_HumidityChart_Yaxis1 = lv.scale(ui_HumidityChart)
ui_HumidityChart_Yaxis1.set_mode(lv.scale.MODE.VERTICAL_LEFT)
ui_HumidityChart_Yaxis1.set_size(50, lv.pct(100))
ui_HumidityChart_Yaxis1.set_align(lv.ALIGN.LEFT_MID)

ui_HumidityChart_Yaxis1.set_x(-50 - ui_HumidityChart.get_style_pad_left(lv.PART.MAIN) - ui_HumidityChart.get_style_border_width(lv.PART.MAIN) + 2)

ui_HumidityChart_Yaxis1.set_style_line_width(0, lv.PART.MAIN)
ui_HumidityChart_Yaxis1.set_style_line_width(1, lv.PART.ITEMS)
ui_HumidityChart_Yaxis1.set_style_line_width(1, lv.PART.INDICATOR)
ui_HumidityChart_Yaxis1.set_style_length(10, lv.PART.INDICATOR)
ui_HumidityChart_Yaxis1.set_style_length(5, lv.PART.ITEMS)

ui_HumidityChart_series_1 = ui_HumidityChart.add_series(lv.color_hex(0xFF0000), lv.chart.AXIS.PRIMARY_Y)

ui_HumidityChart.set_style_outline_pad(max(50, 50, 50), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_HumidityChart.set_style_outline_width(-1, lv.PART.MAIN | lv.STATE.DEFAULT)

ui_HumidityChart.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)

# ################################### humidity chart END ######################

ui_Temperature = lv.label(scrn)
ui_Temperature.set_text("Temperature")
ui_Temperature.set_width(lv.SIZE_CONTENT)
ui_Temperature.set_height(lv.SIZE_CONTENT) 
ui_Temperature.set_x(-99)
ui_Temperature.set_y(2)
ui_Temperature.set_align(lv.ALIGN.CENTER)
ui_Temperature.set_style_text_color(lv.color_hex(0x0C00FF), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_Temperature.set_style_text_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT)

ui_Temp_data = lv.label(scrn)
ui_Temp_data.set_width(lv.SIZE_CONTENT)
ui_Temp_data.set_height(lv.SIZE_CONTENT)
ui_Temp_data.set_x(-102)
ui_Temp_data.set_y(-38)
ui_Temp_data.set_align(lv.ALIGN.CENTER)
ui_Temp_data.set_style_text_color(lv.color_hex(0x0C00FF), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_Temp_data.set_style_text_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT)
ui_Temp_data.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN | lv.STATE.DEFAULT)

ui_Humidity = lv.label(scrn)
ui_Humidity.set_text("Humidity")
ui_Humidity.set_width(lv.SIZE_CONTENT)
ui_Humidity.set_height(lv.SIZE_CONTENT)
ui_Humidity.set_x(-104)
ui_Humidity.set_y(39)
ui_Humidity.set_align(lv.ALIGN.CENTER)
ui_Humidity.set_style_text_color(lv.color_hex(0xFF0000), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_Humidity.set_style_text_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT)

ui_Humidity_data = lv.label(scrn)
ui_Humidity_data.set_width(lv.SIZE_CONTENT)
ui_Humidity_data.set_height(lv.SIZE_CONTENT)
ui_Humidity_data.set_x(-104)
ui_Humidity_data.set_y(74)
ui_Humidity_data.set_align(lv.ALIGN.CENTER)
ui_Humidity_data.set_style_text_color(lv.color_hex(0xFF0000), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_Humidity_data.set_style_text_opa(255, lv.PART.MAIN| lv.STATE.DEFAULT)
ui_Humidity_data.set_style_text_font(lv.font_montserrat_16, lv.PART.MAIN | lv.STATE.DEFAULT)

ui_Time = lv.label(scrn)
ui_Time.set_width(lv.SIZE_CONTENT)
ui_Time.set_height(lv.SIZE_CONTENT)
ui_Time.set_x(-76)
ui_Time.set_y(-108)
ui_Time.set_align(lv.ALIGN.CENTER)

ui_Wifi = lv.label(scrn)
ui_Wifi.set_text("WiFi:")
ui_Wifi.set_width(lv.SIZE_CONTENT)
ui_Wifi.set_height(lv.SIZE_CONTENT)
ui_Wifi.set_x(-121)
ui_Wifi.set_y(-91)
ui_Wifi.set_align(lv.ALIGN.CENTER)

ui_connected = lv.label(scrn)
ui_connected.set_width(lv.SIZE_CONTENT)
ui_connected.set_height(lv.SIZE_CONTENT)
ui_connected.set_x(-60)
ui_connected.set_y(-91)
ui_connected.set_align(lv.ALIGN.CENTER)

ui_MQTT = lv.label(scrn)
ui_MQTT.set_text("MQTT:")
ui_MQTT.set_width(lv.SIZE_CONTENT)
ui_MQTT.set_height(lv.SIZE_CONTENT)
ui_MQTT.set_x(29)
ui_MQTT.set_y(-107)
ui_MQTT.set_align(lv.ALIGN.CENTER)

ui_enabled = lv.label(scrn)
ui_enabled.set_width(lv.SIZE_CONTENT)
ui_enabled.set_height(lv.SIZE_CONTENT)
ui_enabled.set_x(104)
ui_enabled.set_y(-107)
ui_enabled.set_align(lv.ALIGN.CENTER)

ui_IP_ = lv.label(scrn)
ui_IP_.set_text("IP:")
ui_IP_.set_width(lv.SIZE_CONTENT)
ui_IP_.set_height(lv.SIZE_CONTENT)
ui_IP_.set_x(14)
ui_IP_.set_y(-91)
ui_IP_.set_align(lv.ALIGN.CENTER)

ui_ip_data = lv.label(scrn)
ui_ip_data.set_width(lv.SIZE_CONTENT)
ui_ip_data.set_height(lv.SIZE_CONTENT)
ui_ip_data.set_x(88)
ui_ip_data.set_y(-91)
ui_ip_data.set_align(lv.ALIGN.CENTER)

ui_punkt1 = lv.obj(scrn)
ui_punkt1.set_width(10)
ui_punkt1.set_height(10)
ui_punkt1.set_x(-1)
ui_punkt1.set_y(-107)
ui_punkt1.set_align(lv.ALIGN.CENTER)

ui_punkt2 = lv.obj(scrn)
ui_punkt2.set_width(10)
ui_punkt2.set_height(10)
ui_punkt2.set_x(-1)
ui_punkt2.set_y(-91)
ui_punkt2.set_align(lv.ALIGN.CENTER)

ui_punkt3 = lv.obj(scrn)
ui_punkt3.set_width(10)
ui_punkt3.set_height(10)
ui_punkt3.set_x(-150)
ui_punkt3.set_y(-107)
ui_punkt3.set_align(lv.ALIGN.CENTER)

ui_punkt4 = lv.obj(scrn)
ui_punkt4.set_width(10)
ui_punkt4.set_height(10)
ui_punkt4.set_x(-150)
ui_punkt4.set_y(-91)
ui_punkt4.set_align(lv.ALIGN.CENTER)

ui_frame_status = lv.obj(scrn)
ui_frame_status.set_width(318)
ui_frame_status.set_height(39)
ui_frame_status.set_x(0)
ui_frame_status.set_y(-100)
ui_frame_status.set_align(lv.ALIGN.CENTER)
ui_frame_status.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_frame_status.set_style_bg_opa(5, lv.PART.MAIN| lv.STATE.DEFAULT)

ui_frame_temp = lv.obj(scrn)
ui_frame_temp.set_width(318)
ui_frame_temp.set_height(100)
ui_frame_temp.set_x(0)
ui_frame_temp.set_y(-28)
ui_frame_temp.set_align(lv.ALIGN.CENTER)
ui_frame_temp.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_frame_temp.set_style_bg_opa(5, lv.PART.MAIN| lv.STATE.DEFAULT)

ui_frame_humidity = lv.obj(scrn)
ui_frame_humidity.set_width(318)
ui_frame_humidity.set_height(95)
ui_frame_humidity.set_x(0)
ui_frame_humidity.set_y(71)
ui_frame_humidity.set_align(lv.ALIGN.CENTER)
ui_frame_humidity.set_style_bg_color(lv.color_hex(0xFFFFFF), lv.PART.MAIN | lv.STATE.DEFAULT)
ui_frame_humidity.set_style_bg_opa(5, lv.PART.MAIN| lv.STATE.DEFAULT)


class WiFiManager:
    def __init__(self, wifi_ssid, wifi_password, ap_ssid, ap_password):
        self.wifi_ssid = wifi_ssid
        self.wifi_password = wifi_password
        self.ap_ssid = ap_ssid
        self.ap_password = ap_password
        self.ssid = None
        self.ip_address = None
        self.status = None

    def connect_to_wifi(self):
        try:
            wlan = network.WLAN(network.STA_IF)
            wlan.active(True)

            if not wlan.isconnected():
                print("Wifi - testing connection")
                wlan.connect(self.wifi_ssid, self.wifi_password)
                while not wlan.isconnected():
                    pass
            print("Wifi - connected with:", self.wifi_ssid)
            self.ssid = self.wifi_ssid
            self.ip_address = wlan.ifconfig()[0]
            print("Wifi - IP-Adresse:", self.ip_address)
            self.status = "connected"
        except Exception as e:
            print(f"Wifi connection failed with msg: {e}")

    def create_access_point(self):
        try:
            ap = network.WLAN(network.AP_IF)
            ap.active(True)
            ap.config(essid=self.ap_ssid, password=self.ap_password)
            print("Wifi - access point created:")
            print("Wifi - SSID:", self.ap_ssid)
            print("Wifi - Passwort:", self.ap_password)
            print("Wifi - IP-Adresse:", ap.ifconfig()[0])
            self.ssid = self.ap_ssid
            self.ip_address = ap.ifconfig()[0]
            self.status = "access point"
        except Exception as e:
            print(f"Wifi Access Point failed to open - msg: {e}")

    def configure_wifi(self):
        try:
            self.connect_to_wifi()
        except Exception as e:
            print(f"Wifi cannot connect - create access point - msg: {e})")
            self.create_access_point()

        return self.ssid, self.ip_address, self.status


class German_time:
    def __init__(self):
        self.sekunden_liste = [0]
        self.stelle_zeit_ein()
        self.aktualisiere_zeit()

    def stelle_zeit_ein(self):
        try:
            print("NTP syncronize time over..")
            ntptime.host = "de.pool.ntp.org"
            ntptime.settime()
            print("NTP time synchronized")
        except Exception as e:
            print(f"NTP Time Server Error with msg: {e})")


    def aktualisiere_zeit(self):
        zeit_utc = utime.localtime()

        offset = 1  # Normalzeit (MEZ)
        if self.is_summertime(zeit_utc):
            offset += 1

        self.jahr, self.monat, self.tag, self.stunde, self.minute, self.sekunde, _, _ = zeit_utc
        self.stunde = (self.stunde + offset) % 24

    def is_summertime(self, zeit):
        monat, tag = zeit[1], zeit[2]

        if monat > 3 and monat < 10:
            return True
        elif monat == 3:
            return tag >= 8
        elif monat == 10:
            return tag < 25
        return False

    def update_sekunden_liste(self):
        self.sekunden_liste.append(self.sekunde)
        if len(self.sekunden_liste) > 8:
            self.sekunden_liste.pop(0)
        return self.sekunden_liste

    def __str__(self):
        return self.zeige_zeit()

    def zeige_zeit(self):
        return f"{self.tag:02d}.{self.monat:02d}.{self.jahr} {self.stunde:02d}:{self.minute:02d}:{self.sekunde:02d}"

    async def tick(self):
        while True:
            self.aktualisiere_zeit()
            zeit = self.zeige_zeit()
            ui_Time.set_text(zeit)
            lv.task_handler()
            await asyncio.sleep(1)


async def update_temperature_list(temp_list, humidity_list):
    d.measure()
    temperature = int(d.temperature())
    humidity = int(d.humidity())
    temperature_int = temperature
    humidity_int = humidity

    temp_list.append(temperature_int)
    if len(temp_list) > 10:
        temp_list.pop(0)

    humidity_list.append(humidity_int)
    if len(humidity_list) > 10:
        humidity_list.pop(0)


class MQTTSensorPublisher:
    def __init__(self, broker_address, port, topic, username, password, sensor_callback):
        self.broker_address = broker_address
        self.port = port
        self.topic = topic
        self.username = username
        self.password = password
        self.client = MQTTClient("MQTT SensorPublisher", self.broker_address, self.port, self.username, self.password)
        self.client.set_callback(self.on_message)
        self.sensor_callback = sensor_callback()

    def on_message(self, topic, msg):
        print("MQTT recieved data:", topic, msg)

    async def connect(self):
        try:
            self.client.connect()
            self.client.set_last_will(self.topic, "MQTT disconnected")
            self.client.set_callback(self.on_message)
            print("MQTT connect successful")
        except Exception as e:
            print(f"MQTT connect failed with msg: {e}")

    async def publish_sensor_data(self):
        try:
            sensor_data = await self.sensor_callback()
            self.client.publish(self.topic, sensor_data)
            print("MQTT publish_sensor_data send:", sensor_data)
        except Exception as e:
            print(f"MQTT publish_sensor_data with msg: {e}")

    async def run(self):
        await self.connect()
        while True:
            await self.publish_sensor_data()
            # await asyncio.sleep(10)
            # self.client.disconnect()


async def data_to_lvgl_every_hours():

    get_seconds = German_time()
    while True:
        get_seconds.aktualisiere_zeit()
        await update_temperature_list(temperature_list, humidity_list)
        print("......temperature list:", temperature_list)
        print("......humidity list:", humidity_list)

        # ################# temp chart #########################
        range_down_temp = min(temperature_list) - 1
        range_up_temp = max(temperature_list) + 1
        ui_TemperatureChart.set_ext_y_array(ui_TemperatureChart_series_1, temperature_list)

        ui_TemperatureChart_Yaxis1.set_range(range_down_temp, range_up_temp)

        range_span_temp = range_up_temp - range_down_temp
        desired_major_ticks_temp = 3
        major_tick_every_temp = max(1, range_span_temp // (desired_major_ticks_temp - 1))
        total_tick_count_temp = (desired_major_ticks_temp - 1) * major_tick_every_temp + 1

        ui_TemperatureChart_Yaxis1.set_total_tick_count(total_tick_count_temp)
        ui_TemperatureChart_Yaxis1.set_major_tick_every(major_tick_every_temp)

        ui_TemperatureChart.set_range(lv.chart.AXIS.PRIMARY_Y, range_down_temp, range_up_temp)
        ui_TemperatureChart.set_range(lv.chart.AXIS.SECONDARY_Y, range_down_temp, range_up_temp)

        # ################# temp chart END #####################

        # ################# humidtiy chart #####################
        range_down_humi = min(humidity_list) - 1
        range_up_humi = max(humidity_list) + 1
        ui_HumidityChart.set_ext_y_array(ui_HumidityChart_series_1, humidity_list)

        ui_HumidityChart_Yaxis1.set_range(range_down_humi, range_up_humi)

        range_span_humi = range_up_humi - range_down_humi
        desired_major_ticks_humi = 3
        major_tick_every_humi = max(1, range_span_humi // (desired_major_ticks_humi - 1))
        total_tick_count_humi = (desired_major_ticks_humi - 1) * major_tick_every_humi + 1

        ui_HumidityChart_Yaxis1.set_total_tick_count(total_tick_count_humi)
        ui_HumidityChart_Yaxis1.set_major_tick_every(major_tick_every_humi)

        ui_HumidityChart.set_range(lv.chart.AXIS.PRIMARY_Y, range_down_humi, range_up_humi)
        ui_HumidityChart.set_range(lv.chart.AXIS.SECONDARY_Y, range_down_humi, range_up_humi)

        # ################# humidtiy chart END #################

        sekunden_liste = get_seconds.update_sekunden_liste()

        sekunden_min = sekunden_liste[0]
        sekunden_max = sekunden_liste[-1]

        ui_HumidityChart_Xaxis.set_range(sekunden_min, sekunden_max)
        ui_TemperatureChart_Xaxis.set_range(sekunden_min, sekunden_max)

        ui_ip_data.set_text(ip_address)
        ui_connected.set_text(status)
        ui_enabled.set_text("enabled")
        temperature = int(d.temperature())
        ui_Temp_data.set_text(f"{temperature} °C")
        humidity = int(d.humidity())
        ui_Humidity_data.set_text(f"{humidity} %")

        led.fill((0, 0, 50))
        led.write()

        await asyncio.sleep(3)

        led.fill((0, 50, 0))
        led.write()

        await asyncio.sleep(3)


async def sensor_callback():
    while True:
        await asyncio.sleep(3)
        return "23.5"


async def data_to_lvgl_every_second():

    while True:
        ui_punkt1.set_style_bg_color(lv.color_make(255, 0, 0), lv.PART.MAIN | lv.STATE.DEFAULT)
        ui_punkt2.set_style_bg_color(lv.color_make(0, 0, 255), lv.PART.MAIN | lv.STATE.DEFAULT)
        ui_punkt3.set_style_bg_color(lv.color_make(0, 0, 255), lv.PART.MAIN | lv.STATE.DEFAULT)
        ui_punkt4.set_style_bg_color(lv.color_make(255, 0, 0), lv.PART.MAIN | lv.STATE.DEFAULT)
        lv.task_handler()
        await asyncio.sleep(1)
        ui_punkt1.set_style_bg_color(lv.color_make(0, 0, 255), lv.PART.MAIN | lv.STATE.DEFAULT)
        ui_punkt2.set_style_bg_color(lv.color_make(255, 0, 0), lv.PART.MAIN | lv.STATE.DEFAULT)
        ui_punkt3.set_style_bg_color(lv.color_make(255, 0, 0), lv.PART.MAIN | lv.STATE.DEFAULT)
        ui_punkt4.set_style_bg_color(lv.color_make(0, 0, 255), lv.PART.MAIN | lv.STATE.DEFAULT)
        lv.task_handler()
        await asyncio.sleep(1)


async def main():
    task1 = asyncio.create_task(data_to_lvgl_every_hours())
    task2 = asyncio.create_task(data_to_lvgl_every_second())
    uhr = German_time()
    task3 = asyncio.create_task(uhr.tick())
    task4 = asyncio.create_task(mqtt_publisher.run())
    await asyncio.gather(task1, task2, task3)


if __name__ == "__main__":
    try:
        led = neopixel.NeoPixel(Pin(36), 1)
        led.fill((50, 50, 50))
        led.write()

        th = task_handler.TaskHandler()

        d = dht.DHT11(machine.Pin(40))

        d.measure()
        temp_init = d.temperature()
        humidity_init = d.humidity()
        print("initial temperature: {:.2f} °C".format(temp_init))
        print("initial humidity: {:.2f} %".format(humidity_init))

        wifi_manager = WiFiManager('idontknow', 'dumdidum', 'temp_humidity', '12345678')
        ssid, ip_address, status = wifi_manager.configure_wifi()
        print(f'SSID: {ssid}, IP: {ip_address}, Status: {status}')
        led.fill((60, 0, 0))
        led.write()

        uhr = German_time()
        print(uhr)

        mqtt_publisher = MQTTSensorPublisher(
                                            broker_address="192.168.178.103",
                                            port=1883,
                                            topic="humi_temp",
                                            username="homeassistant",
                                            password="dumdidum",
                                            sensor_callback=sensor_callback()
                                            )

        mqtt_publisher.connect()

        temperature_list = [25] * 10
        humidity_list = [14] * 10

        asyncio.run(main())

    except Exception as e:
        print(f"Booting Error with msg: {e}")
