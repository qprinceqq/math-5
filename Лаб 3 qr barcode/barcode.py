import barcode
from barcode.writer import ImageWriter

# Customize barcode settings
options = {
    'text': 'Custom Text',
    'font_size': 10,
    'module_height': 15,
    'quiet_zone': 1
}

# Generate and save barcode with custom settings
ean = barcode.get('ean13', '123456789102', writer=ImageWriter())
ean.save('ean13_barcode_png', options={'format': 'PNG'})
