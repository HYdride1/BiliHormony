import json
import os.path
import requests
from time import sleep
from lxml import etree
import pprint
import requests  # 导入requests库以发送HTTP请求
import json  # 导入json库以处理JSON数据
import pandas as pd  # 导入pandas库以创建和操作数据表格

# 定义B站热门视频API的URL
url = 'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all'

# 定义请求头，模拟浏览器访问
headers = {
    'Referer': 'https://www.bilibili.com/v/popular/rank/all/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0'
}

# 发送GET请求到B站API并获取响应
response = requests.get(url, headers=headers)
# 解析响应内容为JSON格式
data = json.loads(response.text)

# 从响应数据中提取视频列表
video_list = data['data']['list']

# 初始化空列表以存储视频信息
rank_list = []  # 排行
title_list = []  # 视频标题
play_cnt_list = []  # 播放数
danmu_cnt_list = []  # 弹幕数
coin_cnt_list = []  # 投币数
like_cnt_list = []  # 点赞数
share_cnt_list = []  # 分享数
favorite_cnt_list = []  # 收藏数
author_list = []  # 作者
video_url = []  # 视频地址
pic_url = []
# 遍历视频列表并提取每部视频的信息
for idx, video in enumerate(video_list):
    rank_list.append(idx + 1)  # 添加视频排行
    title_list.append(video['title'])  # 添加视频标题
    play_cnt_list.append(video['stat']['view'])  # 添加播放数
    danmu_cnt_list.append(video['stat']['danmaku'])  # 添加弹幕数
    coin_cnt_list.append(video['stat']['coin'])  # 添加投币数
    like_cnt_list.append(video['stat']['like'])  # 添加点赞数
    share_cnt_list.append(video['stat']['share'])  # 添加分享数
    favorite_cnt_list.append(video['stat']['favorite'])  # 添加收藏数
    author_list.append(video['owner']['name'])  # 添加作者名称
    video_url.append(f'https://www.bilibili.com/video/{video["bvid"]}')  # 添加视频地址
    pic_url.append(video['pic'])

# 使用pandas创建DataFrame，准备存储所有提取的数据
df = pd.DataFrame({
    '排行': rank_list,
    '视频标题': title_list,
    '视频地址': video_url,
    '作者': author_list,
    '播放数': play_cnt_list,
    '弹幕数': danmu_cnt_list,
    '硬币数': coin_cnt_list,
    '点赞数': like_cnt_list,
    '分享数': share_cnt_list,
    '收藏数': favorite_cnt_list,
    '封面地址': pic_url
})

# 将DataFrame保存为CSV文件，不包含索引，使用utf_8_sig编码
df.to_csv('B站TOP100.csv', index=False, encoding="utf_8_sig")

url = video_url[0]
response = requests.get(url)
cookie = "buvid3=5C5D0069-031F-2213-8E11-3B17C971719F69389infoc; b_nut=1688698369; _uuid=7F76CBFD-ADE2-44103-424C-D73D5E9ACC2869255infoc; header_theme_version=CLOSE; CURRENT_FNVAL=4048; buvid4=780B8373-C6A6-6800-F372-7CF18F799AE570981-023070710-7YWVed7pFp%2FuoShCfdfYnQ%3D%3D; DedeUserID=175444232; DedeUserID__ckMd5=b4a676bf5d8afe1c; rpdid=|(k|)mum~~uJ0J'uY))~|uklm; LIVE_BUVID=AUTO5916888971292528; SESSDATA=6b25c9b2%2C1705192174%2Cba23f%2A71bQR5hFBMOt8AXYHjziKE4HOwWw6Ei8wrCIByshPnLAkTd2jwLJy4WYgVkViOyIUPNssSUQAAIAA; bili_jct=e29211bb7e88730fc2bc6691218d247e; sid=858nix09; FEED_LIVE_VERSION=V8; buvid_fp_plain=undefined; hit-new-style-dyn=1; hit-dyn-v2=1; i-wanna-go-back=-1; b_ut=5; fingerprint=b2371c9349b15d5ad60e75cd01f7dc55; buvid_fp=5b9a1047d9ef9ba48290adcd4ba39e58; share_source_origin=copy_web; bsource=share_source_copylink_web; bili_ticket=eyJhbGciOiJIUzI1NiIsImtpZCI6InMwMyIsInR5cCI6IkpXVCJ9.eyJleHAiOjE2OTY0NzMzNjcsImlhdCI6MTY5NjIxNDEwNywicGx0IjotMX0.D2ixQib5vaXOyxTBLWhIR8KzpbGQloGjxzXDgnOum3E; bili_ticket_expires=1696473307; CURRENT_QUALITY=80; b_lsid=4F245FCD_18AFACA514A; home_feed_column=5; browser_resolution=1552-827; bp_video_offset_175444232=848638555060174904; PVID=1"

head = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",

    # Referer: 防盗链。用于告诉服务器我是从哪个链接跳转来的。
    'Referer': 'https://www.bilibili.com/',
    'Cookie': cookie
}
sleep(2)
page_text = response.text

with open('./bilibili.html', 'w', encoding='utf-8') as fp:
    fp.write(page_text)

# print(page_text)
# 获取标题和播放信息
tree = etree.HTML(page_text)
title = tree.xpath('//*[@id="viewbox_report"]/h1/text()')[0]
play_info = tree.xpath('/html/head/script[4]')[0].text  # 通过tree.xpath得到script对象，然后通过text属性得到其内容
play_info = play_info[20:]  # 去掉前面的window.__playinfo__=这几个字符
print(play_info)

# 将数据转为json格式，方便获取其中的部分数据
play_info_json = json.loads(play_info)
# print(play_info_json)
pprint.pprint(play_info_json)  # 格式化输出

# 获取音频、视频url
# B站的音频和视频链接是分开的，所以要分别获取，然后通过一定的方法进行合并。
video_url = play_info_json['data']['dash']['video'][0]['baseUrl']  # 得到视频链接
audio_url = play_info_json['data']['dash']['audio'][0]['baseUrl']  # 得到音频链接

# 获取音频、视频数据
video_content = requests.get(url=video_url, headers=head).content  # content表示二进制数据
audio_content = requests.get(url=audio_url, headers=head).content

if not os.path.exists('./B站视频'):
    os.mkdir('./B站视频')

with open('./B站视频/' + title + '.mp4', 'wb') as fp:
    fp.write(video_content)

with open('./B站视频/' + title + '.mp3', 'wb') as fp:
    fp.write(audio_content)

print("提取到的title", title)
