import json
import os.path

import requests
from time import sleep
from lxml import etree
import pprint
import csv
import json
import requests
import json
import pprint
import re
import os
import subprocess
import sys

"""获取url响应体"""


def csv_to_json(csv_file, json_file):
    # 打开 CSV 文件并读取数据
    with open(csv_file, mode='r', encoding='utf-8') as infile:
        # 使用 csv.DictReader 自动将 CSV 的每一行解析为字典
        reader = csv.DictReader(infile)

        # 将 CSV 数据转存到列表中
        data = []
        for row in reader:
            data.append(row)

    # 将数据写入 JSON 文件
    with open(json_file, mode='w', encoding='utf-8') as outfile:
        json.dump(data, outfile, indent=4, ensure_ascii=False)


def extract_info(json_file, key):
    # 打开 JSON 文件并读取数据
    with open(json_file, mode='r', encoding='utf-8') as infile:
        data = json.load(infile)

    # 提取信息：根据键值提取数据
    extracted_data = []
    for item in data:
        if key in item:
            extracted_data.append(item[key])

    return extracted_data


# 使用示例


def getResponse(url):
    # 设置请求头
    headers = {

        'referer': 'https://www.bilibili.com/',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36'
    }
    # 发起get请求
    response = requests.get(url=url, headers=headers)
    return response


"""解析响应体"""


def parseResponse(url):
    # 获取url响应体
    response = getResponse(url)
    # 用正则表达式取出返回的视频数据
    html_data = re.findall('<script>window.__playinfo__=(.*?)</script>', response.text)[0]
    # 解析成json数据
    jsonData = json.loads(html_data)
    # 获取视频标题
    videoTitle = re.findall('<title data-vue-meta="true">(.*?)</title>', response.text)[0]
    # 获取音频
    audioUrl = jsonData['data']['dash']['audio'][0]['baseUrl']
    # 获取视频
    videoUrl = jsonData['data']['dash']['video'][0]['baseUrl']
    # 封装视频信息
    videoInfo = {

        'videoTitle': videoTitle,
        'audioUrl': audioUrl,
        'videoUrl': videoUrl,
    }
    print( videoInfo)
    return videoInfo


"""保存视频和音频"""


def saveMedia(fileName, content, mediaType):
    # 创建目录（如果不存在）
    os.makedirs('D:\\bilibili', exist_ok=True)
    # 写入文件
    with open(f'D:\\bilibili\\{fileName}.{mediaType}', mode='wb') as f:
        f.write(content)
    print(f"保存{mediaType}成功！")


def AvMerge(Mp3Name, Mp4Name, savePath):
    print("开始合并音频和视频.........")
    print(f"音频文件: {Mp3Name}")
    print(f"视频文件: {Mp4Name}")
    print(f"合并后文件保存路径: {savePath}")

    # 使用subprocess来调用ffmpeg，并重定向输出
    with open(os.devnull, 'w') as devnull:
        result = subprocess.run(
            ['ffmpeg', '-i', Mp4Name, '-i', Mp3Name, '-c:v', 'copy', '-c:a', 'aac', '-strict', 'experimental',
             savePath],
            stdout=devnull,
            stderr=devnull
        )

    print("合并成功！")
    os.remove(Mp3Name)
    os.remove(Mp4Name)


def main():
    csv_file = 'B站TOP100.csv'
    json_file = 'myjson'

    # 将 CSV 转换为 JSON
    csv_to_json(csv_file, json_file)

    # 提取 JSON 文件中的信息，例如提取所有 'name' 字段
    names = extract_info(json_file, '视频地址')
    print(names)  # 输出: ['John', 'Jane', 'Bob']
    for url in names:
        videoInfo = parseResponse(url)
        # 获取视频标题
        #fileName = videoInfo['videoTitle']
        # 下载并保存音频
        #audioContent = getResponse(videoInfo['audioUrl']).content
        #saveMedia(fileName, audioContent, 'mp3')
        # 下载并保存视频
       # videoContent = getResponse(videoInfo['videoUrl']).content
        #saveMedia(fileName, videoContent, 'mp4')

        #Mp3Name = f'D:\\bilibili\\{fileName}.mp3'
        #Mp4Name = f'D:\\bilibili\\{fileName}.mp4'
        #savePath = f'D:\\bilibili\\merge_{fileName}.mp4'
        #AvMerge(Mp3Name, Mp4Name, savePath)


if __name__ == '__main__':
    main()
