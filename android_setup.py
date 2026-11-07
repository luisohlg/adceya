import sys,os,re,glob
from PIL import Image
root=sys.argv[1];icon=Image.open(sys.argv[2]).convert('RGBA')
BG=(228,235,238);BGHEX='#E4EBEE'
res=os.path.join(root,'app/src/main/res')
def w(path,txt):
    os.makedirs(os.path.dirname(path),exist_ok=True);open(path,'w').write(txt)
# iconos de lanzador
leg={'mdpi':48,'hdpi':72,'xhdpi':96,'xxhdpi':144,'xxxhdpi':192}
fg={'mdpi':108,'hdpi':162,'xhdpi':216,'xxhdpi':324,'xxxhdpi':432}
for d,sz in leg.items():
    out=os.path.join(res,'mipmap-'+d);os.makedirs(out,exist_ok=True)
    im=icon.resize((sz,sz),Image.LANCZOS);im.save(os.path.join(out,'ic_launcher.png'));im.save(os.path.join(out,'ic_launcher_round.png'))
    f=fg[d];cv=Image.new('RGBA',(f,f),(0,0,0,0));k=int(f*0.62);ic=icon.resize((k,k),Image.LANCZOS);cv.paste(ic,((f-k)//2,(f-k)//2),ic);cv.save(os.path.join(out,'ic_launcher_foreground.png'))
ad='<?xml version="1.0" encoding="utf-8"?>\n<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">\n  <background android:drawable="@color/ic_launcher_background"/>\n  <foreground android:drawable="@mipmap/ic_launcher_foreground"/>\n</adaptive-icon>\n'
w(os.path.join(res,'mipmap-anydpi-v26/ic_launcher.xml'),ad);w(os.path.join(res,'mipmap-anydpi-v26/ic_launcher_round.xml'),ad)
w(os.path.join(res,'values/ic_launcher_background.xml'),'<?xml version="1.0" encoding="utf-8"?>\n<resources>\n  <color name="ic_launcher_background">%s</color>\n</resources>\n'%BGHEX)
for f in glob.glob(os.path.join(res,'drawable-v24/ic_launcher_foreground.xml')):os.remove(f)
# pantalla de arranque
for f in glob.glob(os.path.join(res,'drawable*','splash.png')):
    W,H=Image.open(f).size;cv=Image.new('RGB',(W,H),BG);k=int(min(W,H)*0.42);ic=icon.resize((k,k),Image.LANCZOS);cv.paste(ic,((W-k)//2,(H-k)//2),ic);cv.save(f)
# version, nombre y orientación
g=os.path.join(root,'app/build.gradle');t=open(g).read()
t=re.sub(r'versionCode\s+\d+','versionCode 13',t);t=re.sub(r'versionName\s+"[^"]*"','versionName "1.0.4"',t);open(g,'w').write(t)
m=os.path.join(root,'app/src/main/AndroidManifest.xml');t=open(m).read()
if 'screenOrientation' not in t:t=t.replace('<activity','<activity\n            android:screenOrientation="portrait"',1)
open(m,'w').write(t)
print('listo')
