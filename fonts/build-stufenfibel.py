from fontTools.ttLib import TTFont
from fontTools import subset
import base64, os
NEW = 'Stufenfibel'
chars = set(range(0x20, 0x7F)) | set(range(0xA0, 0x100)) | {0x20AC, 0x2212, 0x2013, 0x2014, 0x201E, 0x201C, 0x201A, 0x2018, 0x2019, 0x201D, 0x2026, 0x00B7, 0x00D7, 0x00F7, 0x2192, 0x2190, 0x2022, 0x2032, 0x2033, 0x1E9E, 0x2009, 0x202F, 0x2011}
out = {}
for style, fn in [('Regular', 'Andika-Regular.ttf'), ('Bold', 'Andika-Bold.ttf')]:
    f = TTFont(fn)
    # 1) l mit Bogen als Standard
    for t in f['cmap'].tables:
        if t.isUnicode() and ord('l') in t.cmap: t.cmap[ord('l')] = 'l.TailL'
    # 2) Namen ohne reservierten Namen (OFL)
    for r in f['name'].names:
        try: s = r.toUnicode()
        except Exception: continue
        if r.nameID in (1, 3, 4, 6, 16, 17, 21, 22):
            r.string = s.replace('Andika', NEW).replace('SIL', 'SW')
    opts = subset.Options()
    opts.layout_features = ['kern', 'mark', 'mkmk', 'ccmp', 'locl']
    opts.name_IDs = ['*']; opts.name_languages = ['*']; opts.notdef_outline = True
    opts.flavor = 'woff'; opts.with_zopfli = False
    opts.drop_tables += ['DSIG']
    sub = subset.Subsetter(opts); sub.populate(unicodes=sorted(chars)); sub.subset(f)
    f.flavor = 'woff'; p = f'{NEW}-{style}.woff'; f.save(p)
    print(p, os.path.getsize(p), f['name'].getDebugName(4))
