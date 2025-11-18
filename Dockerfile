FROM python:3.9-slim

# 使用国内源
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    sed -i 's/security.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y socat

# 使用国内pip源
RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple \
    pycryptodome sympy

RUN useradd -m ctf
WORKDIR /home/ctf

COPY ./src/server.py /home/ctf/server.py
COPY ./service/docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

USER ctf

ENTRYPOINT ["/bin/sh","/docker-entrypoint.sh"]
