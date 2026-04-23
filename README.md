# SNSアプリ（Django）

## 概要
Djangoを用いて作成したシンプルなSNSアプリです。 ユーザー同士の投稿・いいね・フォローといった基本的なSNS機能を実装しています。

## デモ
https://django-snsapp.onrender.com

## 主な機能

* ユーザー登録 / ログイン / ログアウト（django-allauth）
* 投稿の作成 / 一覧表示 / 詳細表示 / 編集 / 削除
* いいね機能（Ajaxによる非同期通信）
* フォロー機能
* フォローしているユーザーの投稿一覧表示
  
## 使用技術

* Python
* Django
* SQLite
* Bootstrap
* JavaScript（fetch API / Ajax）
アプリ構成

```
snsproject/
├── config/
├── snsapp/
├── templates/
├── static/
└── manage.py

```

## 工夫した点
1. Ajaxによるいいね機能
ページ遷移なしでいいねの追加・解除ができるように実装しました。 フロント側ではfetch APIを使用し、バックエンドはJsonResponseで状態を返しています。
2. フォロー機能
ユーザー同士の関係を管理するため、Connectionモデルを作成し、 ManyToManyFieldでフォロー関係を管理しています。
3. 権限制御

* LoginRequiredMixin によるログイン制限
* UserPassesTestMixin による投稿者のみ編集・削除可能
ER図（簡易）

* User
* Post（ユーザーに紐づく）
* Connection（フォロー関係）
## 今後の改善点

* コメント機能の追加
* フォロー機能のAjax化
* UI/UXの改善
* 画像投稿機能の追加
* ページネーションの実装

## 起動方法

```bash
git clone <リポジトリURL>
cd snsproject
python manage.py migrate
python manage.py runserver

```

ブラウザで以下にアクセス http://127.0.0.1:8000/
備考
学習目的で作成したアプリですが、 実用性を意識して機能を拡張しています。
