"""Eigenes Symbol für die Testversion (Stefan, 25.11.2026): das normale Symbol mit rotem Band „TEST“ unten.
Wird von tests/testversion.sh aufgerufen: python3 tests/test_icons.py <Ordner der Testversion>
Ändert dort apple-touch-icon.png, icon-192.png, icon-512.png."""
import os, sys
from PIL import Image, ImageDraw, ImageFont

HIER = os.path.dirname(os.path.abspath(__file__))
SCHRIFTEN = [os.path.join(HIER, '..', 'fonts', 'Stufenfibel-Bold.woff'),
             '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf']


def schrift(px):
    for f in SCHRIFTEN:
        try:
            return ImageFont.truetype(f, px)
        except Exception:
            pass
    return ImageFont.load_default()


def markieren(pfad):
    alt = Image.open(pfad).convert('RGBA'); w, h = alt.size
    band = int(h * 0.28)
    # Symbol verkleinert darüber, damit das Band nichts verdeckt
    im = Image.new('RGBA', (w, h), alt.getpixel((2, 2)))
    k = int(h * 0.78); klein = alt.resize((k, k), Image.LANCZOS)
    im.paste(klein, ((w - k) // 2, int(h * 0.0)), klein)
    d = ImageDraw.Draw(im)
    d.rectangle([0, h - band, w, h], fill=(201, 65, 74, 255))   # Rot der App (#c9414a)
    f = schrift(int(band * 0.72)); t = 'TEST'
    l, o, r, u = d.textbbox((0, 0), t, font=f)
    d.text(((w - (r - l)) / 2 - l, h - band + (band - (u - o)) / 2 - o), t, font=f, fill='white')
    im.save(pfad)


if __name__ == '__main__':
    ziel = sys.argv[1]
    for n in ['apple-touch-icon.png', 'icon-192.png', 'icon-512.png']:
        p = os.path.join(ziel, n)
        if os.path.exists(p):
            markieren(p)
