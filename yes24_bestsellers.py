import aiohttp # type: ignore
import asyncio
from bs4 import BeautifulSoup # type: ignore
import pandas as pd
import aiofiles # type: ignore

async def fetch(session, url, retries=5):
    for attempt in range(retries):
        try:
            async with session.get(url) as response:
                response_text = await response.text()
                return response_text
        except aiohttp.ClientError as e:
            print(f'Error fetching {url}: {e}. Retrying {attempt + 1}/{retries}...')
            await asyncio.sleep(1)
    raise aiohttp.ClientError(f'Failed to fetch {url} after {retries} retries.')

async def get_book_details(session, book_id):
    detail_url = f'http://www.yes24.com/Product/Goods/{book_id}'
    try:
        html = await fetch(session, detail_url)
        soup = BeautifulSoup(html, 'html.parser')
        title_tag = soup.find('h2', class_='gd_name')
        title = title_tag.text.strip() if title_tag else "No Title"
        
        # Get book class information
        class_tag = soup.find('span', class_='yes_b')
        book_class = class_tag.text.strip() if class_tag else "No Class"

        return title, book_id, book_class
    except Exception as e:
        print(f'Error fetching details for book {book_id}: {e}')
    return "No Title", book_id, "No Class"

async def get_yes24_bestsellers(max_rank=400):
    base_url = 'http://www.yes24.com/24/category/bestseller'
    books = []
    current_rank = 1
    page = 1

    async with aiohttp.ClientSession() as session:
        while current_rank <= max_rank:
            url = f'{base_url}?PageNumber={page}'
            html = await fetch(session, url)
            soup = BeautifulSoup(html, 'html.parser')

            book_list = soup.select('ul#yesBestList > li')
            tasks = []
            for book in book_list:
                if current_rank > max_rank:
                    break

                book_id = book.get('data-goods-no')
                tasks.append((current_rank, book_id))
                current_rank += 1

            detail_tasks = [get_book_details(session, book_id) for rank, book_id in tasks]
            detail_results = await asyncio.gather(*detail_tasks)

            for (rank, book_id), (title, book_id, book_class) in zip(tasks, detail_results):
                books.append({
                    'Rank': rank,
                    'Title': title,
                    'GoodsNo': book_id,
                    'Class': book_class
                })
                print(f'Rank: {rank}, Title: {title}, GoodsNo: {book_id}, Class: {book_class}')

            page += 1
            await asyncio.sleep(1)  # 페이지 요청 사이에 지연 시간 추가

    return books

async def main():
    bestseller_books = await get_yes24_bestsellers(max_rank=400)
    df = pd.DataFrame(bestseller_books)
    async with aiofiles.open('yes24_bestsellers.csv', mode='w', encoding='utf-8') as f:
        await f.write(df.to_csv(index=False, encoding='utf-8'))

if __name__ == '__main__':
    asyncio.run(main())
