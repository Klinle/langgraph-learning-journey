FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 安装系统依赖（如 git、curl，便于调试或下载资源）
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 设置 Python 环境变量
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# 默认挂起容器，保持其后台运行
CMD ["tail", "-f", "/dev/null"]
