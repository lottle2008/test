import requests
import re
import html

def fetch_douban_top250():
    """
    抓取豆瓣电影 Top 250 的标题和引言。
    """
    url = "https://movie.douban.com/top250"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果请求失败，则抛出异常
        html_content = response.text

        # 匹配标题的正则表达式
        title_pattern = re.compile(r'<span class="title">(.*?)</span>')
        # 匹配引言的正则表达式，根据您的要求使用 class="quote"
        quote_pattern = re.compile(r'<p class="quote">.*?<span>(.*?)</span>.*?</p>', re.S)

        titles = title_pattern.findall(html_content)
        quotes = quote_pattern.findall(html_content)

        # 过滤掉非主标题（如“ / Other Name”）
        titles = [title for title in titles if '&nbsp' not in title]

        if not titles or not quotes:
            print("没有找到电影标题或引言。请检查网页结构或正则表达式是否已更新。")
            return

        # 清理和打印结果
        for i in range(min(len(titles), len(quotes))):
            title = html.unescape(titles[i].strip())
            quote = html.unescape(quotes[i].strip())
            print(f"电影: {title}")
            print(f"引言: {quote}")
            print("---")

    except requests.exceptions.RequestException as e:
        print(f"请求页面时出错: {e}")
    except Exception as e:
        print(f"处理数据时发生错误: {e}")

if __name__ == "__main__":
    fetch_douban_top250()