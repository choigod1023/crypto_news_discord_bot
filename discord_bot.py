import discord
from discord.ext import commands, tasks
import asyncio
import os
import json
from dotenv import load_dotenv
from coinness_api import CoinnessAPI

# 환경 변수 로드
load_dotenv()

# 봇 설정
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# 설정
NEWS_FILE = 'last_news.json'  # 이전 뉴스를 저장할 파일
TARGET_TOPIC = 'coin_news'  # 뉴스를 보낼 채널의 주제

def save_news_to_file(news_list):
    """뉴스 리스트를 파일에 저장"""
    try:
        with open(NEWS_FILE, 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"뉴스 저장 중 에러: {e}")

def load_news_from_file():
    """파일에서 뉴스 리스트를 불러오기"""
    try:
        if os.path.exists(NEWS_FILE):
            with open(NEWS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"뉴스 불러오기 중 에러: {e}")
        return []

def find_new_news(current_news, previous_news):
    """새로운 뉴스를 찾아서 반환"""
    if not previous_news:
        return current_news
    
    previous_ids = {news.get('id') for news in previous_news}
    new_news = [news for news in current_news if news.get('id') not in previous_ids]
    return new_news

@bot.event
async def on_ready():
    print(f'{bot.user}이(가) 로그인했습니다!')
    print(f'Bot ID: {bot.user.id}')
    print(f'뉴스 알림 대상: 채널 주제가 "{TARGET_TOPIC}"인 모든 채널')
    print('------')
    
    # 뉴스 알림 대상 채널 찾기
    target_channels = find_target_channels()
    if target_channels:
        print(f'발견된 대상 채널: {len(target_channels)}개')
        for channel in target_channels:
            print(f'  - #{channel.name} (서버: {channel.guild.name})')
    else:
        print(f'⚠️  채널 주제가 "{TARGET_TOPIC}"인 채널을 찾을 수 없습니다.')
        print('📝 채널 주제를 "coin_news"로 설정해주세요.')
    
    print('------')
    
    # 자동 뉴스 체크 시작
    if not check_news.is_running():
        check_news.start()

def find_target_channels():
    """채널 주제가 TARGET_TOPIC인 모든 채널을 찾아서 반환"""
    target_channels = []
    for guild in bot.guilds:
        for channel in guild.text_channels:
            if channel.topic and TARGET_TOPIC.lower() in channel.topic.lower():
                target_channels.append(channel)
    return target_channels

@tasks.loop(seconds=10)  # 10초마다 체크
async def check_news():
    """새로운 뉴스를 주기적으로 체크합니다."""
    
    try:
        # 현재 뉴스 가져오기
        async with CoinnessAPI() as api:
            current_news = await api.get_breaking_news(limit=10)
            
            if not current_news:
                return
            
            # 이전 뉴스 불러오기
            previous_news = load_news_from_file()
            
            # 새로운 뉴스 찾기
            new_news = find_new_news(current_news, previous_news)
            
            # 새로운 뉴스가 있으면 알림
            if new_news:
                # 대상 채널들 찾기
                target_channels = find_target_channels()
                
                if not target_channels:
                    return
                
                # 각 대상 채널에 뉴스 전송
                for channel in target_channels:
                    if channel.permissions_for(channel.guild.me).send_messages:
                        try:
                            for news in new_news:
                                # 중요 뉴스인지에 따라 색상과 제목 결정
                                is_important = news.get('isImportant', False)
                                color = 0xff0000 if is_important else 0x0099ff
                                title_prefix = "🚨 새로운 중요 뉴스!" if is_important else "📰 새로운 뉴스!"
                                
                                embed = discord.Embed(
                                    title=title_prefix,
                                    description=f"**{news.get('title', '제목 없음')}**",
                                    color=color
                                )
                                
                                content = news.get('content', '')
                                if len(content) > 800:
                                    content = content[:800] + "..."
                                
                                embed.add_field(
                                    name="📄 내용",
                                    value=content,
                                    inline=False
                                )
                                
                                # 발행 시간 추가
                                publish_time = news.get('publishAt', '')
                                if publish_time:
                                    try:
                                        from datetime import datetime
                                        dt = datetime.fromisoformat(publish_time.replace('Z', '+00:00'))
                                        formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                                        embed.add_field(
                                            name="⏰ 발행 시간",
                                            value=formatted_time,
                                            inline=True
                                        )
                                    except:
                                        pass
                                
                                embed.add_field(
                                    name="📊 시장 반응",
                                    value=f"👍 {news.get('bullCount', 0)} 👎 {news.get('bearCount', 0)}",
                                    inline=True
                                )
                                
                                # 썸네일 이미지 추가
                                thumbnail = news.get('thumbnailImage')
                                if thumbnail:
                                    embed.set_thumbnail(url=thumbnail)
                                
                                link = news.get('link')
                                if link:
                                    embed.add_field(
                                        name="🔗 링크",
                                        value=link,
                                        inline=False
                                    )
                                
                                # 뉴스 전송 (중요 뉴스는 @everyone 멘션)
                                if is_important:
                                    message = await channel.send("@everyone", embed=embed)
                                    try:
                                        await message.pin()
                                        print(f"중요 뉴스 핀 고정: {news.get('title', '제목 없음')} → #{channel.name}")
                                    except Exception as pin_error:
                                        print(f"핀 고정 실패: {pin_error}")
                                else:
                                    message = await channel.send(embed=embed)
                                
                                await asyncio.sleep(0.5)  # 스팸 방지
                                
                                print(f"새로운 뉴스 전송: {news.get('title', '제목 없음')} → #{channel.name} (서버: {channel.guild.name})")
                        
                        except discord.Forbidden:
                            print(f"채널 #{channel.name}에 메시지 전송 권한이 없습니다.")
                        except Exception as e:
                            print(f"채널 #{channel.name}에서 알림 전송 실패: {e}")
                    else:
                        print(f"채널 #{channel.name}에 메시지 전송 권한이 없습니다.")
            
            # 현재 뉴스를 파일에 저장 (다음 체크에서 비교용)
            save_news_to_file(current_news)
    
    except Exception as e:
        print(f"뉴스 체크 중 에러 발생: {e}")

@check_news.before_loop
async def before_check_news():
    await bot.wait_until_ready()

if __name__ == "__main__":
    # 디스코드 봇 토큰 확인
    token = os.getenv('DISCORD_BOT_TOKEN')
    if not token:
        print("❌ DISCORD_BOT_TOKEN이 환경 변수에 설정되지 않았습니다!")
        print("📝 .env 파일을 생성하고 DISCORD_BOT_TOKEN=your_token_here를 추가하세요.")
        exit(1)
    
    try:
        bot.run(token)
    except discord.LoginFailure:
        print("❌ 디스코드 봇 토큰이 유효하지 않습니다!")
    except Exception as e:
        print(f"❌ 봇 실행 중 에러 발생: {e}")