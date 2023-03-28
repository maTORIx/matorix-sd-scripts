# matorix-sd-scripts
https://github.com/kohya-ss/sd-scripts における前処理を行うためのスクリプトです。

- 画像のタグ付け(`waifu diffusion 1.4 tagger`)
- 正則化画像生成(透明 or 任意のモデルを用いた画像生成)
- tomlファイル出力
- 学習用コマンドの出力
- 学習用実行ファイル(`.bat` and `.sh`)

上記の処理を一括で行います。

これにより、出力されたbatファイルを実行するだけでLoRAの学習を行うことができます。

*生成したファイルは、`matorix-sd-scripts/outputs`以下に保存されます。*

## Easy Install
https://raw.githubusercontent.com/maTORIx/matorix-sd-scripts/master/install.bat

URLを開いて、右クリックのメニューから「名前をつけて保存」を選択してください。

つぎに、このファイルを`sd-scripts`のディレクトリ直下に移動してください。

最後に、`install.bat`を実行します。(この際、setup.batが実行されるため、WaifuDiffusion 1.4 Taggerモデルのダウンロード等で時間がかかる場合があります。)

これでインストールは完了です。

`start.bat`から起動できます。



## Install
```
$ ../path/to/sd-scripts/venv/Scripts/activate
$ git clone https://github.com/matorix/matorix-sd-scripts
$ cd matorix-sd-scripts
$ pip install onnxruntime
$ ./setup.bat
$ ./start.bat
```

## Help

お気軽にissueにて、ご連絡をお願いします。

## 利用しているソースコード
- https://github.com/kohya-ss/sd-scripts
- https://huggingface.co/SmilingWolf/wd-v1-4-swinv2-tagger-v2
- https://github.com/SmilingWolf/SW-CV-ModelZoo


## License
MIT License

なお、セットアップスクリプト等でダウンロードされるファイルは、それぞれのライセンスに従います。
