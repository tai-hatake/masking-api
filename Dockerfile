FROM alpine:3.7
RUN apk update && \
   apk add --no-cache git python3 python3-dev tar \
   # numpy、scipy、scikit-learn、pandas
   zlib-dev g++ musl linux-headers gcc g++ make gfortran openblas-dev swig \
   # mecab-ipadic-neologd
   openssl sudo bash curl file \
   # timezone
   tzdata && \
   cp /usr/share/zoneinfo/Asia/Tokyo /etc/localtime && \
   apk del tzdata && \
   rm -rf /var/cache/apk/*

WORKDIR /usr/src/mecab/
RUN mkdir -p /temp/mecab_src/ && \
    git clone https://github.com/taku910/mecab.git  /temp/mecab_src/ && \
    mv -f /temp/mecab_src/mecab/* /usr/src/mecab/ && \
    ./configure  --with-charset=utf8 && \
    make && \
    make install && \
    rm -rf  /temp/mecab_src/  && \
    rm -rf  /usr/src/mecab/

RUN git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git \
      /usr/src/mecab-ipadic-neologd && \
    /usr/src/mecab-ipadic-neologd/bin/install-mecab-ipadic-neologd -n -y

ARG project_dir=/app/
ADD requirements.txt $project_dir
ADD app.py $project_dir

WORKDIR $project_dir

RUN pip3 install --upgrade pip
RUN pip install -r requirements.txt

ENV FLASK_APP /app/app.py
CMD flask run -h 0.0.0.0 -p $PORT
