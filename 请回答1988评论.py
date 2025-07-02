import re
import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options as FirefoxOptions

# 设置请求的 URL
url = "https://movie.douban.com/subject/26302614/episode/1/"

# 配置 FirefoxOptions
firefox_options = FirefoxOptions()
firefox_options.add_argument("--headless")
firefox_options.add_argument("--disable-gpu")

# 设置 Selenium WebDriver
driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=firefox_options)

try:
    # 打开网页
    driver.get(url)

    # 等待评论区加载完成
    # 这里我们等待 class 为 'comment-item' 的第一个元素出现，最长等待20秒
    wait = WebDriverWait(driver, 20)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "comment-item")))

    # 获取页面源代码
    html_content = driver.page_source

    # --- 以下为之前优化的正则表达式解析部分 ---

    # 匹配每个评论的完整区块
    comment_blocks_pattern = re.compile(r'<div class="comment-item.*?" data-cid=".*?">(.*?)<div class="comment-ft">', re.S)
    comment_blocks = comment_blocks_pattern.findall(html_content)

    if comment_blocks:
        print(f"成功找到 {len(comment_blocks)} 个评论区块。正在提取详细信息...\n")
        
        username_pattern = re.compile(r'<span class="comment-info">.*?<a.*?>(.*?)</a>', re.S)
        comment_text_pattern = re.compile(r'<span class="short">(.*?)</span>', re.S)

        for block in comment_blocks:
            user_match = username_pattern.search(block)
            comment_match = comment_text_pattern.search(block)

            if user_match and comment_match:
                username = user_match.group(1).strip()
                comment_text = comment_match.group(1).strip()
                
                print(f"用户: {username}")
                print(f"评论: {comment_text}")
                print("-" * 40)

    else:
        print("没有找到任何评论区块。请检查网页结构或正则表达式是否已更新。")

finally:
    # 关闭浏览器
    driver.quit()