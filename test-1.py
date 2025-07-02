import requests
import re
import html

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

    # 正则表达式匹配电影标题
    title_pattern = re.compile(r'<span class="title">([^<]+)</span>')
    all_titles = title_pattern.findall(html_content)
    titles = [html.unescape(title) for title in all_titles if not title.startswith('&nbsp;')]


    # 正则表达式匹配电影评分
    rating_pattern = re.compile(r'<span class="rating_num" property="v:average">([\d.]+)</span>')
    ratings = rating_pattern.findall(html_content)

    # 正则表达式匹配导演信息
    director_pattern = re.compile(r'导演: (.*?)&nbsp;')
    directors = director_pattern.findall(html_content)

    # 正则表达式匹配电影的简短描述（可能存在，不一定有）
    # quote_pattern = re.compile(r'<span class="inq">([^<]+)</span>')
    # quotes = quote_pattern.findall(html_content)

    # 确定可迭代的最小长度，避免超出索引范围
    min_length = min(len(titles), len(ratings), len(directors))

    # 打印提取的信息
    for i in range(min_length):
        print(f"电影: {titles[i]}")
        print(f"评分: {ratings[i]}")
        print(f"导演: {directors[i].strip()}")
        # if i < len(quotes):
        #     print(f"简评: {quotes[i]}")
        # else:
        #     print("简评: 暂无")
        print("-" * 40)

else:
    print(f"请求失败，状态码: {response.status_code}")
