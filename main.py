import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# GitHub Secrets에서 환경변수 가져오기
BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')
VERSES_URL = "https://charged-particle.blogspot.com/2026/01/blog-post_15.html"
PROGRESS_FILE = "verse_progress.json"

def get_all_verses(url):
    """블로그에서 모든 말씀 추출"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        verses = []
        
        # Blogspot 본문 추출
        post_body = (
            soup.find('div', class_='post-body') or 
            soup.find('div', class_='entry-content') or
            soup.find('article')
        )
        
        if post_body:
            text_lines = post_body.get_text().strip().split('\n')
            for line in text_lines:
                line = line.strip()
                if line and len(line) > 10:
                    verses.append(line)
        
        if not verses:
            paragraphs = soup.find_all('p')
            for p in paragraphs:
                text = p.get_text().strip()
                if text and len(text) > 10:
                    verses.append(text)
        
        print(f"✅ 총 {len(verses)}개의 말씀을 추출했습니다.")
        return verses
        
    except Exception as e:
        print(f"❌ 말씀 추출 실패: {e}")
        return []

def load_progress():
    """현재 진행 상황 불러오기"""
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {"current_index": 0}

def save_progress(index):
    """진행 상황 저장"""
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump({"current_index": index}, f, ensure_ascii=False, indent=2)

def send_telegram_message(text):
    """텔레그램 메시지 전송"""
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    
    try:
        response = requests.post(url, data=data, timeout=10)
        return response.json()
    except Exception as e:
        print(f"❌ 텔레그램 전송 실패: {e}")
        return {"ok": False, "error": str(e)}

def send_daily_verse():
    """매일 말씀 전송"""
    print(f"\n{'='*50}")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - 말씀 전송 시작")
    
    verses = get_all_verses(VERSES_URL)
    
    if not verses:
        print("❌ 말씀을 가져올 수 없습니다.")
        return False
    
    progress = load_progress()
    current_index = progress["current_index"]
    
    if current_index >= len(verses):
        current_index = 0
    
    verse = verses[current_index]
    
    message = f"""📖 <b>오늘의 소망의 말씀</b>

{verse}

<i>({current_index + 1}/{len(verses)})</i>"""
    
    result = send_telegram_message(message)
    
    if result.get("ok"):
        print(f"✅ 전송 완료: [{current_index + 1}/{len(verses)}]")
        print(f"📝 내용: {verse[:50]}...")
        
        next_index = (current_index + 1) % len(verses)
        save_progress(next_index)
        
        if next_index == 0:
            print("🔄 모든 말씀을 완료했습니다. 다음번에 처음부터 다시 시작합니다.")
        
        return True
    else:
        print(f"❌ 전송 실패: {result}")
        return False

if __name__ == "__main__":
    print("🚀 텔레그램 소망의 말씀 봇 시작")
    success = send_daily_verse()
    print(f"{'='*50}\n")
    
    if not success:
        exit(1)
