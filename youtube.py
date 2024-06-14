import requests
import pandas as pd

API_KEY = 'APIkey' 
TRENDING_URL = 'https://www.googleapis.com/youtube/v3/videos'

params = {
    'part': 'snippet,statistics',
    'chart': 'mostPopular',
    'regionCode': 'KR', 
    'maxResults': 40, 
    'key': API_KEY
}

response = requests.get(TRENDING_URL, params=params)
data = response.json()

titles = []
channel_names = []
view_counts = []

for item in data['items']:
    titles.append(item['snippet']['title'])
    channel_names.append(item['snippet']['channelTitle'])
    view_counts.append(item['statistics']['viewCount'])

df = pd.DataFrame({
    '제목': titles,
    '채널명': channel_names,
    '조회수': view_counts
})
df.index += 1 
df.index.name = '순위'
df.to_csv('youtube_trending_titles.csv', encoding='utf-8-sig')
print("데이터가 csv 파일로 저장되었습니다.")
