import qrcode


class qrCode:
    image = None

    def __init__(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=20,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)

        self.image = qr.make_image()
        print(self.image)
        self.image.save('images/QR.png')

    def getImage(self):
        return 'images/QR.png'
