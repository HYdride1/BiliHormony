import requests
from bs4 import BeautifulSoup
import re

# 获取视频页面源代码
url = 'https://www.bilibili.com/video/BV1ey411q7UE/?spm_id_from=333.337.search-card.all.click&vd_source=fc7e92b8ea5cfa8d6b60f51d83a80bf9'
response = requests.get(url)
html = response.text

# 解析页面源代码
soup = BeautifulSoup(html, 'html.parser')

# 找到视频标签或脚本标签中的视频URL
video_url = None
for script in soup.find_all('script'):
    if 'video' in script.text:
        # 假设视频URL在script标签的内容中，通过正则表达式提取
        match = re.search(r'"videoUrl":"(http[^"]+)"', script.text)
        if match:
            video_url = match.group(1)
            break

# 输出视频URL
if video_url:
    print('Video URL:', video_url)
else:
    print('Video URL not found')

