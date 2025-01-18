# 使用官方 Python 镜像作为基础镜像
FROM python:3.12

# 将当前目录下的文件复制到容器的 /app 目录中
COPY . /app

# 设置工作目录
WORKDIR /app

# 安装 Python 依赖
RUN pip install -r requirements.txt

EXPOSE 8000

# 定义启动命令
CMD ["uvicorn", "main:app", "--reload", "--port", "8000"]

 
