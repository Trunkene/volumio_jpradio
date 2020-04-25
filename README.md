volumio_jpradio
====

Japanese radio relay server for Volumio

## Description
Volumio2でラジオを聞く場合、[こちらの記事](https://monoworks.co.jp/post/2019-05-05-listen-to-radiko-on-volumio/)
の方法で可能ですが、いちいちLogitech Media Serverなるものに切り替えるので使い勝手が
いまひとつよくありません。
そんな折、[burroさんの投稿](#acknowledgments)を見つけ、Volumio2で動くように手を加えてみました。
基本、丸パクリです<(_ _)>

## Requirement
* volumio2

以下も必要ですが導入方法は後述の[Install](#install)で説明。
* python
* flask
* ffmpeg

## Usage
下記インストール後、raspberry-piを再起動し、Volumio2の「Playlist」>「Radiko」から選局。

## Install
※ あくまで、私のやった方法です。
Volumio2が普通に動作している状態で、sshでvolumioユーザーで入って作業。

FFMPEGのインストール
```bash
$ mkdir bin
$ cd bin
# https://github.com/bushev/rpi-ffmpeg からbinaryをダウンロードし/home/volumio/binに入れる
$ chmod 755 ffmpeg
```

python3、flaskの用意
```bash
$ sudo apt-get update
$ sudo apt-get -y install apt-utils apt-show-versions
$ sudo apt-get -y install vim
$ sudo apt-get -y install python3 python3-setuptools python3-venv python3-dev
$ sudo easy_install3 pip
$ mkdir radiko
$ python3 -m venv /home/volumio/radiko/venv
$ source /home/volumio/radiko/venv/bin/activate
$ pip3 install flask
```

プロジェクトのクローン
```bash
git clone https://github.com/Trunkene/volumio_jpradio .
```

動作確認
```bash
$ cd ~/bin
$ cmod 755 radiko
$ radiko
# Volumio2の「Playlist」>「Radiko」から選局
```

自動起動
```bash
$ sudo apt-get -y install supervisor
$ sudo vi /etc/supervisor/supervisord.conf

# 下記を変更
logfile=/var/log/supervisor/supervisord.log --> logfile=/var/log/supervisord.log
childlogdir=/var/log/supervisor --> childlogdir=/var/log/

$ sudo cp ~/supervisor/radiko.conf /etc/supervisor/conf.d/
```

## Acknowledgments
* [NanoPi NEOにインストールしたMPDでradikoを聞く](http://burro.hatenablog.com/entry/2019/02/16/175836)
* [Github for Streaming server for relaying "radiko" radio stream to Music Player Daemon (MPD)](https://github.com/burrocargado/RadioRelayServer)

## Author

[Trunkene](https://github.com/Trunkene)
