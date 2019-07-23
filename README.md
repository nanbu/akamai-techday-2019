# akamai-techday-2019
Akamai Tech Day 2019のLightning Talkセッションで紹介した、Akamai Reporting APIを使った「ダッシュボードツールによるトラフィックデータの可視化」のためのサンプルPythonスクリプトです。

## 使い方
    python client.py <設定ファイル> <ポート番号>

### 引数
- 設定ファイル: EdgeRCのパス、EdgeRCで使用する認証情報(Credential)のセクション名、対象CPコードをYAML記法で記載した設定ファイル
- ポート番号: クライアントを起動するポート

### 使用例
    python client.py data-1.yml 8010

## Tech Day実行環境の構築手順

Linuxサーバーを用意

### インストールするもの
- python3.7.3 (この記事作成時点での最新)
- prometheus 2.10.0 / 2019-05-25
- grafana 6.2.2
- Akamai EdgeGrid
- Prometheus client

### 参考にした記事
- pyenv / python3のインストールはこちらを参照
  https://qiita.com/tisk_jdb/items/01bd6ef9209acc3a275f

- python3.7系のインストールについてはこちらも参照
  https://qiita.com/hitochan777/items/941d4422c53978b275f8

- Akamai EdgeGridのインストール方法
  https://github.com/akamai/AkamaiOPEN-edgegrid-python

- Prometheusのインストールはここを参考にした
  https://qiita.com/holy_road_ss/items/eb0030fd17a2030eb5f0

- Prometheus client (python)
  https://github.com/prometheus/client_python

- Grafanaのインストールはこれらを参考にした
  https://grafana.com/docs/installation/rpm/#install-via-yum-repository
  https://grafana.com/grafana/download
  http://blog.serverworks.co.jp/tech/2016/03/11/play-with-grafana-1/

- Grafana初期設定
  http://blog.serverworks.co.jp/tech/2016/03/11/play-with-grafana-1/


## 各種設定
### Python 3.7インストール
    sudo yum update
    sudo yum install git -y
    git clone https://github.com/yyuu/pyenv.git ~/.pyenv
    echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.bash_profile
    echo 'export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.bash_profile
    echo 'eval "$(pyenv init -)"' >> ~/.bash_profile
    source ~/.bash_profile
    sudo yum install gcc zlib-devel bzip2 bzip2-devel readline readline-devel sqlite sqlite-devel openssl openssl-devel -y
    sudo yum install libffi-devel -y     (*python 3.7系に必要)
    pyenv install 3.7.3
    pyenv global 3.7.3
    pyenv rehash
### Pythonライブラリ各種インストール
    pip install edgegrid-python
    pip install prometheus_client
    pip install pyyaml

### Prometheusインストール
    sudo wget https://github.com/prometheus/prometheus/releases/download/v2.10.0/prometheus-2.10.0.linux-amd64.tar.gz
    sudo tar -zxf prometheus-2.10.0.linux-amd64.tar.gz

### Grafanaインストール
    sudo yum install https://dl.grafana.com/oss/release/grafana-6.2.2-1.x86_64.rpm 

## 各種設定
### Prometheus設定
- prometheus.ymlを編集し、「scrape_configs:」以下にPrometheusクライアントの名前とポート名を追加

      - job_name: cpcode1
        static_configs:
        - targets:
          - localhost:8010
      - job_name: cpcode2
        static_configs:
        - targets:
          - localhost:8020
      - job_name: cpcode3
        static_configs:
        - targets:
          - localhost:8030

### Grafana設定
- Prometheusをデータソースとしてクエリを書き、ダッシュボードを作成
