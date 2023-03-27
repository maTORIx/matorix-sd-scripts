# matorix-sd-scripts
https://github.com/kohya-ss/sd-scripts における前処理を行うためのスクリプトです。

- 画像のタグ付け(`waifu diffusion 1.4 tagger`)
- 正則化画像生成(透明 or 任意のモデルを用いた画像生成)
- tomlファイル出力
- 学習用コマンドの出力
- 学習用実行ファイル(`.bat` and `.sh`)

上記の処理を一括で行います。

これにより、出力されたbatファイルを実行するだけでLoRAの学習を行うことができます。

## Easy Install
https://raw.githubusercontent.com/maTORIx/matorix-sd-scripts/master/install.bat

URLを開いて、右クリックのメニューから「名前をつけて保存」を選択してください。

つぎに、このファイルを`sd-scripts`のディレクトリ直下に移動してください。

最後に、`install.bat`を実行します。

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

おわり。
