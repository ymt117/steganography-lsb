from PIL import Image
import sys

import argparse

ap = argparse.ArgumentParser()
ap.add_argument('-c', help='path to cover image file')
ap.add_argument('-s', help='path to secret image file')
ap.add_argument('-d', help='path to decode image file')
ap.add_argument('-l', help='LSB length')
args = ap.parse_args()

def secret_image_resize(img_cov, img_sec):
    resize_flag = False
    w_cov, h_cov = img_cov.size
    w_sec, h_sec = img_sec.size
    print("w "+str(w_sec)+" h "+str(h_sec))

    if w_cov < w_sec: # 横幅が大きいとき
        re_h = (h_sec * w_cov) / w_sec
        img_sec = img_sec.resize((int(w_cov), int(re_h)))
        w_sec, h_sec = img_sec.size
        resize_flag = True

    if h_cov < h_sec: # 縦幅が大きいとき
        re_w = (h_cov * w_sec) / h_sec
        img_sec = img_sec.resize((int(re_w), int(h_cov)))
        resize_flag = True

    if resize_flag is True:
        print('resized secret image')

    w_sec, h_sec = img_sec.size
    print("w "+str(w_sec)+" h "+str(h_sec))
    return img_sec

def encode(cover_file, secret_file):
    # 画像を読み込む
    with Image.open(cover_file) as img_cov:
        with Image.open(secret_file) as img_sec:
            # cover fileよりsecret fileのピクセルサイズが大きい場合，secret fileをリサイズする
            img_sec = secret_image_resize(img_cov, img_sec)

            w_cov, h_cov = img_cov.size
            w_sec, h_sec = img_sec.size
            
            size = (w_cov, h_cov)
            img_out = Image.new('RGB', size)

            for h in range(0, h_cov):
                for w in range(0, w_cov):
                    if (h >= h_sec or w >= w_sec): # secret fileで穴埋めしない処理
                        pixel_cov = list(img_cov.getpixel((w, h)))
                        for i in range(0, 3):
                            pixel_cov[i] = (pixel_cov[i] >> args.l) << args.l
                        img_out.putpixel((w, h), tuple(pixel_cov))
                    else: # secret fileで穴埋めする処理
                        pixel_cov = list(img_cov.getpixel((w, h)))
                        pixel_sec = list(img_sec.getpixel((w, h)))
                        for i in range(0, 3):
                            # R,G,Bの各ピクセルにおいて，下位ビット[8-args.l]個をsecret fileの上位ビット[8-args.l]個と置き換える
                            pixel_cov[i] = ((pixel_cov[i] >> (args.l)) << (args.l)) | (pixel_sec[i] >> (8-args.l))
                        img_out.putpixel((w, h), tuple(pixel_cov))

            img_out.save('output.png', 'PNG')

def ret_shift_bits():
    if   8 == args.l:
        return 0b00000000
    elif 7 == args.l:
        return 0b00000001
    elif 6 == args.l:
        return 0b00000011
    elif 5 == args.l:
        return 0b00000111
    elif 4 == args.l:
        return 0b00001111
    elif 3 == args.l:
        return 0b00011111
    elif 2 == args.l:
        return 0b00111111
    elif 1 == args.l:
        return 0b01111111
    else:
        return 0b11111111

def decode(filename):
    # 画像を読み込む
    with Image.open(filename) as img:
        width, height = img.size
        size = (width, height)
        img_out = Image.new('RGB', size)
        shift_bits = ret_shift_bits()

        for h in range(0, height):
            for w in range(0, width):
                pixel = list(img.getpixel((w, h)))
                for i in range(0, 3):
                    # 下位ビットの画像を抽出する
                    # R,G,Bの各ピクセルにおいて，下位ビットを取り出し，左に[args.l]ビットシフトする
                    pixel[i] = (pixel[i] & shift_bits) << args.l
                img_out.putpixel((w, h), tuple(pixel))

    img_out.save('decoded_img.png')



'''
Main program
'''
if args.l is None:
    args.l = 4
else:
    args.l = int(args.l)

if args.c is not None and args.s is not None:
    encode(args.c, args.s)
elif args.d is not None:
    decode(args.d)
else:
    print("Error!")
