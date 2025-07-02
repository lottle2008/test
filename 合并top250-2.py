import requests
import re
import html
from typing import List, Dict, Optional

def fetch_douban_top250(url: str = "https://movie.douban.com/top250") -> Optional[List[Dict]]:
    """
    抓取豆瓣电影Top250的标题、评分、导演和引言信息
    
    Args:
        url: 豆瓣电影Top250的URL，默认为第一页
    
    Returns:
        包含电影信息的列表，每个元素是一个字典；若失败返回None
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # 发送HTTP请求并检查状态码
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text
        
        # 修正的正则表达式模式
        title_pattern = re.compile(r'<span class="title">([^<]+)</span>')
        rating_pattern = re.compile(r'<span class="rating_num" property="v:average">([\d.]+)</span>')
        director_pattern = re.compile(r'导演: (.*?)&nbsp;')
        # quote_pattern = re.compile(r'<span class="quote">([^<]+)</span>')
        # quote_pattern = re.compile(r'<p class=\"quote\">.*?<span class=\"inq\">([^<]+)</span>.*?</p>', re.S)
        quote_pattern = re.compile(r'<p\s+class="quote">\s*<span>(.*?)</span>\s*</p>', re.S)
        # 提取并处理数据
        all_titles = title_pattern.findall(html_content)
        ratings = rating_pattern.findall(html_content)
        directors = director_pattern.findall(html_content)
        quotes = quote_pattern.findall(html_content)
        
        # 过滤副标题，保留中文名
        titles = [html.unescape(title) for title in all_titles if not title.startswith('&nbsp;')]
        
        # 数据完整性检查
        if not titles or len(titles) < 10:
            raise ValueError("未能提取到足够的电影标题，可能页面结构已变化")
        
        # 构建电影信息列表
        movies = []
        for i in range(len(titles)):
            movie = {
                'title': titles[i].strip(),
                'rating': ratings[i] if i < len(ratings) else 'N/A',
                'director': directors[i].strip() if i < len(directors) else 'N/A',
                'quote': quotes[i] if i < len(quotes) else '暂无引言'
            }
            movies.append(movie)
        
        return movies
    
    except requests.exceptions.RequestException as e:
        print(f"网络请求异常: {e}")
    except (ValueError, IndexError) as e:
        print(f"数据解析异常: {e}")
    except Exception as e:
        print(f"未知异常: {e}")
    
    return None

def print_movies(movies: List[Dict]) -> None:
    """格式化打印电影信息"""
    for movie in movies:
        print(f"电影: {movie['title']}")
        print(f"评分: {movie['rating']}")
        print(f"导演: {movie['director']}")
        print(f"引言: {movie['quote']}")
        print("-" * 40)

def main() -> None:
    """主函数，支持分页抓取"""
    base_url = "https://movie.douban.com/top250?start={}"
    all_movies = []
    
    # 抓取前3页（共75部电影）
    for start in range(0, 75, 25):
        url = base_url.format(start)
        print(f"正在抓取: {url}")
        movies = fetch_douban_top250(url)
        
        if movies:
            all_movies.extend(movies)
            print(f"成功获取 {len(movies)} 部电影信息")
        else:
            print(f"第 {start//25 + 1} 页抓取失败，跳过")
    
    # 打印所有电影信息
    if all_movies:
        print(f"\n共获取 {len(all_movies)} 部电影信息")
        print_movies(all_movies)
    else:
        print("未能获取任何电影信息")

if __name__ == "__main__":
    main()