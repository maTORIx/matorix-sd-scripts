# matorix-sd-scripts
https://github.com/kohya-ss/sd-scripts に入れ込む学習用のもろもろをいい感じに全部やってくれるUIです。
学習用画像のデータさえ用意すれば、タグ付け、正則化画像の生成、tomlファイルの記述、実行時のスクリプトの記述まで、学習に必要なことは基本的に全部やってくれます。
簡単にするために、様々なパラメータを省いているので、詳細なチューニングが必要な場合は、適宜tomlやスクリプトを改変することを推奨します。

## 使い方

1. kohyaさんのsd-scripts用に用意している仮想環境を利用。
2. READMEにしたがって、DeepDanbooruを入れる。(deepdanbooruコマンドにアクセスできる状態に)
3. config.pyのパスを変更。SD_SCRIPTS_PATHとDEEPDANBOORU_PROJECT_PATHさえ変更すれば動くと思います。
4. `python setup_train.py`
5. UIでパラメータを入力し、Runボタンを押す
6. 実行状態はコマンドラインに流れます。
7. 終了すると、UIが閉じます

"pip install onnxruntime"

おわり。
