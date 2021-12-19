# movie-cutter

特定のフォーマットでタイムスタンプを指定すると動画を切り出します

## install

```bash
poetry install
```

## how to use

タイムスタンプで切り出したい時間を指定したテキストファイルを用意します

```
00:00:00 00:00:10 チャプター名1
00:00:36 00:00:39 チャプター名2
```

適当なオプションを指定して実行します

```
poetry run python main.py --chapter-file sample_chapter.txt --movie sample.mp4
```

動画ファイルと同じディレクトリにファイルが出力されます

```
sample.txt youtube 動画チャプター形式でのタイムスタンプ
チャプター名1.mp4 テキストファイルで指定したファイル名
チャプター名2.mp4 テキストファイルで指定したファイル名
```
