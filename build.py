import os
import shutil
import subprocess
import sys

print("🚀 بدء بناء تطبيق أندرويد...")

# تأكد من وجود index.html
if not os.path.exists("index.html"):
    print("❌ ملف index.html غير موجود!")
    sys.exit(1)

# تنظيف أي ملفات قديمة
if os.path.exists("platforms"):
    shutil.rmtree("platforms")

# تثبيت Cordova إذا لم يكن مثبتاً
print("📦 تثبيت Cordova...")
subprocess.run([sys.executable, "-m", "pip", "install", "cordova"], check=False)

# إنشاء مشروع Cordova
print("🏗️ إنشاء مشروع Cordova...")
subprocess.run(["npx", "cordova", "create", "app", "com.emad.accounting", "EmadAccounting"], check=True)

# الانتقال للمجلد
os.chdir("app")

# إضافة منصة أندرويد
print("🤖 إضافة منصة أندرويد...")
subprocess.run(["npx", "cordova", "platform", "add", "android"], check=True)

# نسخ الملفات
print("📄 نسخ الملفات...")
shutil.copy("../index.html", "www/index.html")

# بناء التطبيق
print("🔨 جاري بناء APK...")
try:
    subprocess.run(["npx", "cordova", "build", "android", "--release"], check=True)
    
    # البحث عن ملف APK
    for root, dirs, files in os.walk("."):
        for file in files:
            if file.endswith(".apk") and "release" in root:
                apk_path = os.path.join(root, file)
                shutil.copy(apk_path, "../emad-accounting.apk")
                print(f"✅ تم بناء التطبيق: {file}")
                print("📱 يمكنك تحميله الآن")
                break
except Exception as e:
    print(f"❌ خطأ في البناء: {e}")

# العودة للمجلد الرئيسي
os.chdir("..")
