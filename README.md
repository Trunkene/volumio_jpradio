volumio_jpradio
====

Japanese radio relay server for Volumio

## Description

## Requirement
* volumio2
* python
* flask
* ffmpeg

## Usage

## Install
※ あくまで、私のやった方法です。

FFMPEGのインストール

```bash
$ mkdir bin
$ cd bin
https://github.com/bushev/rpi-ffmpeg からbinaryをダウンロードし/home/volumio/binに入れる
$chmod 755 ffmpeg
```

python3、flaskの用意

```bash
$ sudo apt-get update
$ sudo apt-get -y install apt-utils apt-show-versions
$ sudo apt-get -y install vim
$ sudo apt-get -y install python3 python3-setuptools python3-venv python3-dev
$ sudo easy_install3 pip
$ mkdir radiko
$ python3 -m venv /home/volumio/radiko
$ source /home/volumio/radiko/venv/bin/activate
$ pip3 install flask
```

## Author

[Trunkene](https://github.com/Trunkene)
