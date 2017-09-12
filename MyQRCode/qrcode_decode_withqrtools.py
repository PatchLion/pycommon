import qrtools
from qrtools.qrtools import QR

def deQCimages(path):
    image = QR()
    res = image.decode(path)
    if res:
        return image.data


if __name__ == '__main__':
    path = "dhqme_qrcode_withicon.png"
    print(deQCimages(path))