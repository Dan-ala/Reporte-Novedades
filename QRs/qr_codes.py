import qrcode
#Generate the QR code
img = qrcode.make("http://192.168.1.8:8000/puesto_trabajo/pt/4")

#Save the imng as an image file like (.jpg)
img.save('PT4.jpg')