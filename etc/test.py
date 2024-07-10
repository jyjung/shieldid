import webbrowser
import os
import qrcode
from qrcode.image.pure import PyPNGImage

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
qr.add_data('Some data')
img = qr.make_image(image_factory=PyPNGImage)
image_path = 'image.png'
abs_path = os.path.abspath(image_path)
file_url = 'file://' + abs_path
newurl= "file://wsl.localhost/Ubuntu/home/jung/ztcapwork/shieldid/image.png"
img.save(image_path)
webbrowser.open(newurl)
#webbrowser.open('https://python.org')



#img_3 = qr.make_image(image_factory=StyledPilImage, embeded_image_path="image.png")

# img = qrcode.make('Some data here')
# img = img.convert("RGB")
# image_array = np.array(img)

# plt.imshow(img)
# plt.show()
