# simple_ap

RSSフィードを定期チェックして更新情報をActivityPubでフォロワーに配信するAPIサーバです。APIサーバはflaskを使い、DB周りはdjangoを使ってます。Mastodonとの連携を想定しています。

## 要件
- Ubuntu
- nginx等Webサーバ
- SSL/TLS証明書
- python3.8
- sqlite3
- make

## 使い方

```
$ git clone git@github.com:wakin-/simple_ap.git
$ cd simple_ap
$ vi fixture/setup.json
```

初期データの準備。

adminパネルから追加することも可能です。

```json:fixture/setup.json
[
  {
    "model": "activitypub.account",
    "pk": 1,
    "fields": {
      "name": "<アカウントID 半角英数-_>",
      "display_name": "<表示名>",
      "feed_url": "<RSSフィードのURL>",
      "icon": "<アイコンのパス>"
    }
  }
]
```

```python:simple_ap/settings.py
DOMAIN = '<自分のサイトのドメイン eg: www.example.com>'
```

セットアップスクリプトの実行。

```
$ make dependencies
$ make setup
```

## サーバー起動

nginxでHTTPS化して公開する場合(letsencryptで秘密鍵入手済み前提)

```
$ make nginx_setup
$ make nginx_enable
```

uwsgiなしでHTTPサーバーを立てる場合

```
$ make run_standalone
```

いずれの場合もリモートフォローにはHTTPSが必須な点に注意してください

## サーバー常駐化

Systemdを使う場合

```
$ make systemd_setup
$ make systemd_enable # sudo required
```

Supervisor

```
$ make supervisor_setup
$ make supervisor_enable # sudo required
```

## 定期実行設定

現在のRSS情報を取得。

```
$ python manage.py rss
```

cronで定期的にRSSの更新を確認。新着があればPOST。

```
* * * * * cd /path/to/simple_ap ; env/bin/python manage.py rss
```

外部インスタンスの検索エリアから `https://~/<name>` でアカウントを検索し、リモートフォロー。

## その他コンソール操作

adminパネルからモデルの操作

```
$ make superuser
-> 作成するadminの情報を入力

$ make run_standalone_admin
```
表示されたURL(127.0.0.1:8000)にポートフォワードなどでアクセスしてログイン
Accountを追加する際、`Public Key`と`Private Key`が空欄に出来ないが、目はSAVE後に更新されるので何を入れても大丈夫