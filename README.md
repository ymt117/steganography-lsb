# steganography-lsb
Steganography: Hide image inside image

LSBを使ったステガノグラフィです．
カバー画像の各ピクセルのRGB値の下位4ビットをシークレット画像の上位4ビットに置き換えます．

pngとjpgファイルに対応してます．

カバー画像よりシークレット画像のサイズが大きい場合はシークレット画像をリサイズして隠します．

## 使い方

#### 画像を隠す

```
> python lsb.py -c cover_image.png -s secret_image.png
```

#### 画像を復元する

```
> python lsb.py -d output.png
```

#### オプション

`-l n`で置き換えるビット数をnビットに変更できます．

```
カバー画像の下位2ビットをシークレット画像の上位2ビットに置き換える
> python lsb.py -c cover_image.png -s secret_image.png -l 2
```

![img](https://raw.githubusercontent.com/ymt117/steganography-lsb/master/lsb_sample.png)
