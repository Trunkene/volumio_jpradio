volumio_jpradio
====
Japanese radio relay server for Volumio

## Description
Volumio2でRadikoを聞く場合、[こちらの記事](https://monoworks.co.jp/post/2019-05-05-listen-to-radiko-on-volumio/)
の方法で可能ですが、いちいちLogitech Media Serverなるものに切り替えるので使い勝手が
いまひとつよくありません。
そんな折、[burroさんの投稿](#acknowledgments)を見つけ、Volumio2で動くように手を加えてみました。
基本、丸パクリです<(_ _)>

+ 2021/01/10 番組名をプレーヤー側で表示できるようにしました。
+ 2021/02.23 TimeFree Downloaderを追加

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

crontabを日本時間にするためTimezoneを変更
```
$ sudo dpkg-reconfigure tzdata
# Asia→Tokyoを選択
```

FFMPEGのインストール
```bash
$ mkdir bin
$ cd bin
# https://www.johnvansickle.com/ffmpeg からダウンロードし /home/volumio/bin に入れる
# armhf - Raspberry-pi 3以降, armel - Raspberry-pi 2以前
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
$ git clone https://github.com/Trunkene/volumio_jpradio .
```
※ ↑ここ失敗しますね。面倒ですが、以下のような感じでやってみてください。
```bash
$ git clone https://github.com/Trunkene/volumio_jpradio ./aaa
$ cd aaa
$ cp -r -f -v ./* ~/
$ cd ../
$ rm -r -f ./aaa
```

番組情報の自動更新
```bash
$ cd ~/bin
$ chmod 755 pgupdate.sh
sudo apt-get -y install cron
crontab -e

#下記を登録 (3:01,9:01,15:01に更新: UTCで指定)
01 3,9,15 * * * /home/volumio/bin/pgupdate.sh > /dev/null 2>&1
```

動作確認
```bash
$ cd ~/bin
$ chmod 755 radiko
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

## TimeFree Downloader
7日前までの番組をDLするコマンドです。cronに設定すると予約録音のように使えます。

ffmpegを日本語のメタをパラメーターにつけて呼び出すためロケールを設定
```
$ sudo locale-gen ja_JP.UTF-8
$ sudo dpkg-reconfigure locales
# ja_JP.UTF-8 UTF-8 をgenerateしdefaultに設定
```

Usage
```
$ dlradiko.sh <STATION_ID> <START_DATETIME> <OUTFILE>
# STATION_ID: 放送局ID
# START_DATETIME: YYYYMMDDhhmm
```

メタデータを下記で設定します。Volumioのアルバムやジャンルからアクセスできます。
```
アルバム: Radikoタイムフリー
ジャンル: Broadcast
```

crontabの設定
```
$ crontab -e

# 以下設定例
PATH=/home/volumio/bin:/usr/local/bin:/usr/bin:/bin
10 15 * * sat /home/volumio/bin/dlradiko.sh FMT "`date +\%Y\%m\%d`1400" "/mnt/USB/xxxxx/radikotf/FTM_SAT1400.m4a" > /dev/null > 2>&1
00 17 * * sat /home/volumio/bin/dlradiko.sh FMT "`date +\%Y\%m\%d`1600" "/mnt/USB/xxxxx/radikotf/FMT_SAT1600.m4a" > /dev/null > 2>&1
00 18 * * sun /home/volumio/bin/dlradiko.sh FMT "`date +\%Y\%m\%d`1700" "/mnt/USB/xxxxx/radikotf/FMT_SUN1700.m4a" > /dev/null > 2>&1
```

## Acknowledgments
* [NanoPi NEOにインストールしたMPDでradikoを聞く](http://burro.hatenablog.com/entry/2019/02/16/175836)
* [Github for Streaming server for relaying "radiko" radio stream to Music Player Daemon (MPD)](https://github.com/burrocargado/RadioRelayServer)

## Author

[Trunkene](https://github.com/Trunkene)
