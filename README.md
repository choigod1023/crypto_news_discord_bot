# 코인니스 디스코드 뉴스 봇

코인니스 API를 사용하여 암호화폐 뉴스를 실시간으로 가져와 디스코드에 전송하는 간단한 봇입니다.

## 🚀 기능

- 📰 10초마다 새로운 뉴스 자동 감지
- 🔥 중요 뉴스와 일반 뉴스 구분
- 📊 시장 반응 (상승/하락 투표) 표시
- 🎨 디스코드 임베드 형식으로 깔끔한 메시지
- 💾 파일 비교 방식으로 중복 방지

## 📋 요구사항

- Python 3.8 이상
- 디스코드 봇 토큰
- 인터넷 연결

## 🛠️ 설치 방법

### 1. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 환경 변수 설정

`.env.example` 파일을 `.env`로 복사하고 설정하세요:

```bash
copy .env.example .env
```

`.env` 파일을 열고 다음 내용을 입력:

```
DISCORD_BOT_TOKEN=your_discord_bot_token_here
COINNESS_API_URL=https://api.coinness.com/feed/v1/breaking-news
```

> **참고**: `COINNESS_API_URL`은 선택사항입니다. 설정하지 않으면 기본 URL을 사용합니다.

## 🤖 디스코드 봇 생성 방법

1. [디스코드 개발자 포털](https://discord.com/developers/applications)에 접속
2. "New Application" 클릭
3. 봇 이름 입력 후 "Create" 클릭
4. 좌측 메뉴에서 "Bot" 클릭
5. "Add Bot" 클릭
6. "Token" 섹션에서 "Copy" 클릭하여 토큰 복사
7. `.env` 파일에 토큰 붙여넣기

## 🎯 뉴스 알림 채널 설정 방법

1. 뉴스 알림을 받고 싶은 채널을 선택
2. 채널 설정 (톱니바퀴 아이콘) 클릭
3. "개요" 탭에서 채널 주제에 `coin_news` 입력
4. 저장

## 🚀 봇 실행

```bash
python discord_bot.py
```

봇이 성공적으로 실행되면 다음과 같은 메시지가 표시됩니다:

```
코인니스 뉴스 봇#1234이(가) 로그인했습니다!
Bot ID: 123456789012345678
뉴스 알림 대상: 채널 주제가 "coin_news"인 모든 채널
------
발견된 대상 채널: 2개
  - #crypto-news (서버: My Server)
  - #coin-updates (서버: Trading Guild)
------
```

## 🔄 자동 기능

- **자동 뉴스 체크**: 10초마다 새로운 뉴스를 체크
- **실시간 알림**: 새로운 뉴스가 있으면 자동으로 알림 전송
- **중복 방지**: 파일 비교 방식으로 이미 전송한 뉴스 제외
- **중요 뉴스**: 중요 뉴스는 빨간색으로 표시하고 @everyone 멘션 + 핀 고정
- **다중 채널 지원**: 채널 주제가 "coin_news"인 모든 채널에 자동 전송

## 📁 파일 구조

```
crypto_news_bot/
├── discord_bot.py      # 메인 봇 파일
├── coinness_api.py     # 코인니스 API 클라이언트
├── requirements.txt    # 필요한 패키지 목록
├── .env.example       # 환경 변수 예시
├── .env               # 환경 변수 (직접 생성)
├── last_news.json     # 이전 뉴스 저장 파일 (자동 생성)
└── README.md          # 이 파일
```

## ⚠️ 주의사항

- 디스코드 봇 토큰은 절대 공개하지 마세요
- `.env` 파일은 `.gitignore`에 추가하는 것을 권장합니다
- 봇이 메시지를 보낼 수 있는 권한이 있는지 확인하세요

## 🐛 문제 해결

### 봇이 응답하지 않는 경우

1. 봇 토큰이 올바른지 확인
2. 봇이 서버에 초대되었는지 확인
3. 봇에게 메시지 읽기/보내기 권한이 있는지 확인
4. 채널 주제가 "coin_news"로 설정되어 있는지 확인

### API 오류가 발생하는 경우

1. 인터넷 연결 상태 확인
2. 코인니스 API 서버 상태 확인
3. 잠시 후 다시 시도

## 📊 API 정보

- **데이터 출처**: [코인니스](https://coinness.com)
- **API 엔드포인트**: `https://api.coinness.com/feed/v1/breaking-news`
- **언어**: 한국어 (ko)
- **업데이트 주기**: 10초마다 체크

## 🤝 기여하기

버그 리포트나 기능 제안은 언제든 환영합니다!

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.
