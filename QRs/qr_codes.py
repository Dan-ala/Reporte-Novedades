import qrcode
#Generate the QR code
img = qrcode.make("http://192.168.148.59:8000/puesto_trabajo/pt/2")

#Save the imng as an image file like (.jpg)
img.save('168.1.8.jpg')