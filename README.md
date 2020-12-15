# quizScatterer
## 概要
日本語のクイズ問題の配置を最適化する（ジャンルで分散させる）ツールです。

## セットアップ

```shell
# リポジトリコピー
git clone https://github.com/miyax0227/quizScattererDoc2Vec
# 必要なライブラリのインストール
cd quizScattererDoc2Vec
sudo pip3 install -r requirements.txt
# 学習済みモデルのダウンロード（白ヤギコーポレーション様）
sudo chmod 755 getGensimModel.sh
./getGensimModel.sh
```

## コマンド

```shell
python3 -m quizScattererDoc2Vec INPUT_FILE (> OUTPUT_FILE)
```

例：
```shell
python3 -m quizScattererDoc2Vec sample.txt > result.txt
```

## 作者
Miyax ([@mi_yax](https://twitter.com/mi_yax))