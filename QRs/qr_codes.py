import qrcode
#Generate the QR code
img = qrcode.make("http://192.168.120.192:8000/puesto_trabajo/pt/1")

#Save the imng as an image file like (.jpg)
img.save('PT1.jpg')