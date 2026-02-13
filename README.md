# 텔레그램 소망의 말씀 봇

매일 자동으로 소망의 말씀을 텔레그램으로 전송하는 봇입니다.

## 설정 방법

### 1. 텔레그램 봇 생성
1. 텔레그램에서 @BotFather 검색
2. `/newbot` 명령어 입력
3. 봇 이름과 username 설정
4. 받은 **Bot Token** 저장

### 2. Chat ID 확인
1. 생성한 봇에게 아무 메시지 전송
2. `https://api.telegram.org/bot{YOUR_BOT_TOKEN}/getUpdates` 접속
3. `"chat":{"id":` 뒤의 숫자가 Chat ID

### 3. GitHub Secrets 설정
1. GitHub 저장소 > Settings > Secrets and variables > Actions
2. New repository secret 클릭
3. 두 개의 Secret 추가:
   - Name: `BOT_TOKEN`, Value: 봇 토큰
   - Name: `CHAT_ID`, Value: Chat ID

### 4. 실행 시간 변경 (선택사항)
`.github/workflows/daily-verse.yml` 파일에서 cron 시간 수정:
```yaml
- cron: '0 22 * * *'  # UTC 22:00 = 한국시간 오전 7시
