import qrcode
#Generate the QR code
img = qrcode.make("http://190.9.217.44:8000/puesto_trabajo/pt/1")

#Save the imng as an image file like (.jpg)
img.save('test_PT1.jpg')