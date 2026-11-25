import re, shutil, sys, os
base = sys.argv[1]          # cartella S4MeAssistant di partenza
for name in "DG":
    dst = f"var_{name}"
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(base, dst)
    man = f"{dst}/app/src/main/AndroidManifest.xml"
    svc = f"{dst}/app/src/main/java/com/s4me/assistant/AssistantService.java"
    s = open(man).read()
    s = s.replace('    <uses-permission android:name="android.permission.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS" />\n', '')
    if name == "E":
        s = s.replace('    <uses-permission android:name="android.permission.WAKE_LOCK" />\n', '')
        s = s.replace('    <uses-permission android:name="android.permission.ACCESS_WIFI_STATE" />\n', '')
    if name == "G":
        s = s.replace('FOREGROUND_SERVICE_DATA_SYNC','FOREGROUND_SERVICE_SPECIAL_USE')
        s = s.replace('android:foregroundServiceType="dataSync">\n        </service>','android:foregroundServiceType="specialUse">\n            <property android:name="android.app.PROPERTY_SPECIAL_USE_FGS_SUBTYPE" android:value="Server locale per risolvere le challenge Cloudflare per Kodi" />\n        </service>')
    open(man, "w").write(s)
    c = open(svc).read()
    if name == "E":
        c = re.sub(r'PowerManager pm = .*?wifi\.acquire\(\);', '', c, flags=re.S)
        c = c.replace('if (wake != null && wake.isHeld()) wake.release();', '').replace('if (wifi != null && wifi.isHeld()) wifi.release();', '')
    if name == "F":
        c = c.replace('http = new HttpServer(this, PORT);\n                http.start();', 'http = null; if (PORT < 0) throw new IOException("x");')
    open(svc, "w").write(c)
