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

`sd-scripts`の親フォルダの中に、`matorix-sd-scripts`が追加されています。

`matorix-sd-scripts/start.bat`から起動できます。

学習を開始するときは、`matorix-sd-scripts/outputs`以下に作成されたディレクトリから`train.bat`を起動してください。

詳細は[wiki](https://github.com/maTORIx/matorix-sd-scripts/wiki/matorix%E2%80%90sd%E2%80%90scripts) に記載しています。

## Install
```
$ ../path/to/sd-scripts/venv/Scripts/activate
$ git clone https://github.com/matorix/matorix-sd-scripts
$ cd matorix-sd-scripts
$ pip install onnxruntime
$ ./setup.bat
$ ./start.bat
```

SDXLで使用する場合は、sd_scriptsのディレクトリ以下で、下記のコマンドを実行してください。
```
git fetch origin
git checkout sdxl
```
なお、sd_scripts側で完全にSDXL対応が済んだ場合、この手順は不要になります。これは、暫定的な処置です。

## Update
`setup.bat`を実行してください。

## Help

お気軽にissueにて、ご連絡をお願いします。

## 利用しているソースコード
- https://github.com/kohya-ss/sd-scripts
- https://huggingface.co/SmilingWolf/wd-v1-4-swinv2-tagger-v2
- https://github.com/SmilingWolf/SW-CV-ModelZoo

## 環境によって異なる推奨設定
### torch 2.xを使用している場合
sdpaをONにしてください。

### xformersを使用している場合
torch 2.xと併用できるか確認していません。torch 1.xを使用している場合はONにすると学習速度が向上します。

## Learning Rateの設定方法
config.json内部でoptimizerごとに設定することが可能です。(デフォルト値はsd_scriptsの推奨設定を参考にしています。)
training_types.optimizer以下にある各optimizer設定項目のなかで、"--learning_rate"という項目があります。ここに、学習率を設定してください。

## Networkの追加方法
config.json内部のtraining_types.networksに、追加したいネットワークの設定を追記してください。

## その他、学習に関する情報
wikiを参照してください。色々追記していく予定です。
[wiki](https://github.com/maTORIx/matorix-sd-scripts/wiki)

## License
MIT License

なお、セットアップスクリプト等でダウンロードされるファイルは、それぞれのライセンスに従います。
