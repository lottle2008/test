from bs4 import BeautifulSoup
import requests

# 设置请求的 URL
url = "https://movie.douban.com/top250"

# 定义请求头，模拟浏览器
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# 发送 GET 请求，获取页面内容
response = requests.get(url, headers=headers)

# 检查请求是否成功
if response.status_code == 200:
    html_content = response.text  # 获取网页 HTML 内容
    
    # 使用 BeautifulSoup 解析 HTML 内容
    soup = BeautifulSoup(html_content, 'lxml')
    
    # 查找所有的电影条目
    movies = soup.find_all('div', class_='item')
    
    # 遍历每个电影条目，提取相关信息
    for movie in movies:
        # 提取电影标题
        title = movie.find('span', class_='title').text
        
        # 提取评分
        rating = movie.find('span', class_='rating_num').text
        
        # 提取导演和主演信息
        director = movie.find('p').text.strip().split('\n')[0].strip()
        
        # 提取简短评论，如果有的话
        quote = movie.find('span', class_='inq')
        if quote:
            quote = quote.text
        else:
            quote = "暂无简评"
        
        # 输出电影信息
        print(f"电影: {title}")
        print(f"评分: {rating}")
        print(f"导演: {director}")
        print(f"简评: {quote}")
        print("-" * 40)

else:
    print(f"请求失败，状态码: {response.status_code}")
