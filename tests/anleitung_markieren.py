import json, glob, os, re
from PIL import Image, ImageDraw, ImageFont
from common import URL, launch  # noqa: E402 (Adresse, Browser, Ausgabeordner)
S=1.5; D='anleitung/'; O=D+'final/'
os.makedirs(O, exist_ok=True)
HL=json.load(open(D+'hl.json'))
OR=(232,137,12)
F=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 26)
def box(dr, bb, pad=7):
    x0,y0=(bb['x']-pad)*S,(bb['y']-pad)*S; x1,y1=(bb['x']+bb['width']+pad)*S,(bb['y']+bb['height']+pad)*S
    dr.rounded_rectangle([x0,y0,x1,y1], radius=16, outline=OR, width=6)
for f in sorted(glob.glob(D+'[01]*.png')):
    n=os.path.basename(f)[:-4]
    im=Image.open(f).convert('RGB'); dr=ImageDraw.Draw(im)
    if n in HL: box(dr, HL[n])
    im=im.resize((1400, int(im.height*1400/im.width)), Image.LANCZOS)
    im.save(O+n+'.png', optimize=True)
# Mit --uebernehmen landen die fertigen Bilder in docs/bilder (nur die, die die Anleitung verwendet)
import sys, shutil
from common import ROOT
if '--uebernehmen' in sys.argv:
    used = set(re.findall(r'bilder/([0-9a-z_]+\.png)', open(ROOT/'docs'/'anleitung.md').read()))
    for f in sorted(used):
        if os.path.exists(O + f): shutil.copy(O + f, ROOT/'docs'/'bilder'/f); print('übernommen:', f)
