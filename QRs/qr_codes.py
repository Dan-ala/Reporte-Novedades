import qrcode
#Generate the QR code
img = qrcode.make("http://192.168.42.59:8000/puesto_trabajo/pt/1")

#Save the imng as an image file like (.jpg)
img.save('PT3.jpg')