import qrcode

class qRCode:
    image = None

    def __init__(self, data):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
            )
            qr.add_data(data)
            qr.make(fit=True)

            self.image = qr.make_image()

        def getImage(self):
            return self.image
        

