from bs4 import BeautifulSoup
import requests
import pandas as pd

def get_melon_chart():
    url = 'https://www.melon.com/chart/index.htm'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')

    songs = soup.select('div.wrap_song_info')
    rankings = []
    titles = []
    genres = []

    for idx, song_info in enumerate(songs[:200], 1):  # 200개의 요소를 가져와 필터링
        title_element = song_info.select_one('div.ellipsis.rank01 a')
        genre_element = song_info.select_one('div.ellipsis.rank02 a')

        if title_element and genre_element and idx % 2 != 0:  # 짝수 인덱스만 사용
            title = title_element.get('title', '').replace(' - 페이지 이동', '').replace(' 재생', '').strip()
            genre = genre_element.text.replace(' - 페이지 이동', '').strip()

            rankings.append(idx // 2 + 1)  # 인덱스 보정
            titles.append(title)
            genres.append(genre)
            
            print(f"Rank: {idx // 2 + 1}, Title: {title}, Genre: {genre}")  # 확인을 위한 출력

        if not title_element or not genre_element:
            print(f"Missing data at index {idx}")

    return rankings, titles, genres

def save_to_csv(rankings, titles, genres):
    df = pd.DataFrame({
        "순위": rankings,
        "제목": titles,
        "장르": genres
    })
    df.to_csv("melon_chart.csv", index=False, encoding="utf-8-sig")
    print("데이터가 csv 파일로 저장되었습니다.")

if __name__ == "__main__":
    rankings, titles, genres = get_melon_chart()
    save_to_csv(rankings, titles, genres)
