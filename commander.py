import requests
import subprocess
import sys

def ask_ai(user_input):
    """إرسال السؤال إلى النموذج الذكي"""
    full_prompt = f"أنت مساعد تقني خبير. أجب بدقة واختصار: {user_input}"
    try:
        response = requests.post('http://localhost:11434/api/generate', 
                                 json={'model': 'llama3.2:1b', 'prompt': full_prompt, 'stream': False},
                                 timeout=60)
        return response.json().get('response', 'لا يوجد رد من الذكاء الاصطناعي.')
    except Exception as e:
        return f"خطأ في الاتصال بالخادم: {e}"

def run_command(command):
    """تنفيذ أوامر النظام"""
    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
        return result.decode('utf-8')
    except subprocess.CalledProcessError as e:
        return f"خطأ في التنفيذ: {e.output.decode('utf-8')}"
    except Exception as e:
        return f"حدث خطأ غير متوقع: {e}"

def main():
    print("--- المساعد الشخصي جاهز للعمل ---")
    print("اكتب 'نفذ [أمر]' لتنفيذ أوامر النظام.")
    print("اكتب أي شيء آخر للدردشة مع الذكاء الاصطناعي.")
    
    while True:
        try:
            user_input = input("\nأنت: ")
            if not user_input.strip(): continue
            if user_input.lower() in ['خروج', 'exit', 'quit']: break
            
            if user_input.startswith("نفذ"):
                cmd = user_input.replace("نفذ", "").strip()
                print(f"جاري التنفيذ: {cmd}...")
                print(run_command(cmd))
            else:
                print("جاري المعالجة...")
                print("المساعد:", ask_ai(user_input))
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()

