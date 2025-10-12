import aiohttp
import asyncio
import json
import os
from typing import List, Dict, Optional
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

class CoinnessAPI:
    def __init__(self):
        self.base_url = os.getenv('COINNESS_API_URL')
        self.session = None
    
    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
    
    async def get_breaking_news(self, language_code: str = "ko", limit: int = 10) -> Optional[List[Dict]]:
        """
        코인니스 API에서 브레이킹 뉴스를 가져옵니다.
        
        Args:
            language_code: 언어 코드 (기본값: "ko")
            limit: 가져올 뉴스 개수 (기본값: 10)
            
        Returns:
            뉴스 리스트 또는 None (에러 시)
        """
        try:
            params = {
                "languageCode": language_code,
                "limit": limit
            }
            
            async with self.session.get(self.base_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                else:
                    print(f"API 요청 실패: {response.status}")
                    return None
                    
        except Exception as e:
            print(f"뉴스 가져오기 중 에러 발생: {e}")
            return None
    
    def format_news_for_discord(self, news_list: List[Dict]) -> List[str]:
        """
        뉴스를 디스코드 메시지 형식으로 포맷팅합니다.
        
        Args:
            news_list: 뉴스 리스트
            
        Returns:
            포맷팅된 메시지 리스트
        """
        messages = []
        
        for news in news_list:
            # 기본 정보 추출
            title = news.get('title', '제목 없음')
            content = news.get('content', '내용 없음')
            publish_time = news.get('publishAt', '')
            bull_count = news.get('bullCount', 0)
            bear_count = news.get('bearCount', 0)
            is_important = news.get('isImportant', False)
            link = news.get('link', '')
            
            # 시간 포맷팅 (한국 시간)
            if publish_time:
                try:
                    from datetime import datetime
                    dt = datetime.fromisoformat(publish_time.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    formatted_time = publish_time
            else:
                formatted_time = "시간 정보 없음"
            
            # 중요 뉴스 표시
            importance_marker = "🔥 **중요** " if is_important else ""
            
            # 내용 길이 제한 (디스코드 메시지 길이 제한 고려)
            if len(content) > 500:
                content = content[:500] + "..."
            
            # 디스코드 메시지 포맷팅
            message = f"""
{importance_marker}**{title}**

📄 **내용:**
{content}

📊 **시장 반응:** 👍 {bull_count} 👎 {bear_count}
⏰ **발행 시간:** {formatted_time}
"""
            
            # 링크가 있으면 추가
            if link:
                message += f"🔗 **링크:** {link}"
            
            # 메시지 길이 확인 (디스코드 제한: 2000자)
            if len(message) > 1900:
                message = message[:1900] + "\n...(내용이 잘림)"
            
            messages.append(message)
        
        return messages
