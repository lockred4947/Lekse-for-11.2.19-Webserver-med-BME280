import usocket as socket
import time
from machine import Pin, I2C
import BME280
i2c = I2C(scl=Pin(22),sda=Pin(21), freq=10000)
bme = BME280.BME280(i2c=i2c)

# Denne funksjonen returnerer html koden 
def index(temp,hum):
    header = 'HTTP/1.0 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'
    html = """

<html>
    <head>
    <style>
    body {
      background-image: url("https://makerspaceskien.org/wp-content/uploads/2018/09/cropped-LRM_EXPORT_81668194679729_20180918_141756269_11111111.jpg");
  background-color: #cccccc; }
  </style>
   """
   #Denne sier at den skal hente en bakgrunn far nettsiden som er limt inn.
    html += """ 
    <meta http-equiv="refresh" content="3;
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.6/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.2.1/js/bootstrap.min.js"></script>
    </head>
    """
    #Her Henter jeg inn filene for at grafene skal se slik ut med animasjoner osv
    html += """
    <body>
        <h1>BME280 Sensor</h1>
    </body>
    <div class="container">
    <div class="progress" style="height:20px">
      <div class="progress-bar progress-bar-striped progress-bar-animated" style="width:70%;height20px">"""+str(temp)+"""</div>
          <div class="container">
    <div class="progress" style="height:20px">
      <div class="progress-bar progress-bar-striped progress-bar-animated" style="width:70%;height20px">"""+str(hum)+"""</div>
          <div class="container">
    <div class="progress" style="height:20px">
      <div class="progress-bar progress-bar-striped progress-bar-animated" style="width:70%;height20px">"""+str(psu)+"""</div>
    </div>
    """
    #Her er kodene for grafene som sier at det skal ha striper, animasjon, bredde og høyde som som jeg vil og føker ser fint ut.
    html +="""
</html>

"""
    return header + html

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    Temp = bme.temperature
    hum = bme.humidity
    psu = bme.pressure
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    print('Content = %s' % str(request))
    response = index(Temp, hum)
    conn.send(response)
    conn.close()