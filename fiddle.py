import os
import glob
import copy
import numpy as np
import matplotlib.pyplot as plt
import wave
from scipy import fromstring, int16

# 音声ファイル読込
def read_wav(path):
    wav = wave.open(path, 'r')
    channel = wav.getnchannels()
    width = wav.getsampwidth()
    rate = wav.getframerate()
    frame = wav.getnframes()
    frames = wav.readframes(frame)
    wav.close()
    wav = fromstring(frames, dtype=int16)
    print('ch:' + str(channel) + ' width:' + str(width) + ' rate:' + str(rate) + ' len:' + str(len(wav)))
    return wav

# 音声ファイル保存
def save_wav(path, wav):
    ww = wave.open(path, 'w')
    ww.setnchannels(1)
    ww.setsampwidth(2)
    ww.setframerate(44100)
    ww.writeframes(wav.astype(np.int16))
    ww.close()

# 周波数特性取得(フーリエの絶対値)
def get_fft_abs(data):
    fft = np.fft.fft(data)
    fft_abs = np.abs(fft)
    return fft_abs

# 変調
def change_wav(data, coef):
    fft = np.fft.fft(data)
    change = fft * coef
    if False:
        length = int(len(change) / 2)
        change[length :] = change[length - 1 : : -1]
    ifft = np.fft.ifft(change)
    return ifft

# 変調する標本と対象の周波数特性と波形のグラフ出力
def show_wav_fft(i, index, label, size, fft, coef, in_wav, out_wav):
    name = str(label[index])
    step = int(size / 100)
    coef = coef.reshape(size)

    plt.figure(figsize=(10,5))

    # 周波数特性(100sample-最大値正規化)
    plt.subplot(121)
    plt.title('No.' + str(i) + ' wave - ' + name)
    plt.plot(fft[::step] / fft[::step].max(), alpha=0.5)
    plt.plot(coef[::step] / coef[::step].max(), alpha=0.5)
    
    # 波形
    plt.subplot(122)
    plt.title('No.' + str(i) + ' fft - ' + name)
    plt.plot(in_wav, alpha=0.5)
    plt.plot(out_wav, alpha=0.5)
    
    plt.savefig('fig/' + '{:04d}'.format(i) + '.png')

# 母音ごとに平均を取得
def average_vowel(path, name, count, offset, size):
    vowel = np.zeros(size)
    for i in range(count):
        wav = read_wav(path + str(i) + '/' + name + '.wav')
        vowel += get_fft_abs(wav[offset:offset + size])
    return vowel / count

# 主な関数
def fiddle(in_path, sample_path, count, offset, size, target_path, out_path):
    # 母音ラベル(ファイル名)
    vowels = np.array(['a', 'i', 'u', 'e', 'o'])
    vowel_n = len(vowels)

    # 対象と標本の母音から係数取得
    sample = np.zeros((vowel_n, size))
    coef = np.zeros((vowel_n, size))
    for i in range(vowel_n):
        sample[i] = average_vowel(sample_path, vowels[i], count, offset, size)
        target = read_wav(target_path + '/' + vowels[i] + '.wav')
        coef[i] = get_fft_abs(target[offset:offset + size]) / sample[i]

    # 変調対象の音声ファイルを読込
    wav = read_wav(in_path)
    length = int(len(wav) / size)

    dif = np.zeros((vowel_n, length))

    # 母音を判別しつつ対応した係数で変調
    for i in range(length):
        start = int(size * i)
        end = int(size * (i + 1))
        win = copy.deepcopy(wav[start:end])
        win_fft_abs = get_fft_abs(win)
        for v in range(vowel_n):
            dif[v, i] = sum(abs(sample[v] - win_fft_abs))
        index = np.where(dif[:, i] == dif[:, i].min())
        change = change_wav(win, coef[index].reshape(size))
        wav[start:end] = (change * (max(win) / max(change))).astype(np.int)
        show_wav_fft(i, index, vowels, size, win_fft_abs, coef[index], win, wav[start:end])

    save_wav(out_path, wav)

    # 判別に用いた差の折れ線グラフ出力
    plt.figure()
    for i in range(vowel_n):
        plt.plot(dif[i], label=vowels[i])
    plt.legend()
    plt.savefig('dif.png')

if __name__ == '__main__':
    # args
    in_path = 'sample_aiueo.wav'
    sample_path = 'sample'
    count = 1
    offset = 3000
    size = int(44100 / 10)
    target_path = 'target'
    out_path = 'output_aiueo.wav'

    # 捕捉説明
    # 入力音声ファイルのサンプリングレートは44100前提
    # 対象とは変換したい先の声(声優さんの声とか)
    # 標本とは変換したい元の声(自分の声とか)
    # countは標本の平均を取る回数(3回くらいやると良さげ)
    # offsetは有効とする対象と標本の先頭ズラし(先頭がほぼ無音だったりするので)
    # sizeは有効とする対象と標本の長さ(末尾がほぼ無音だったりするので)
    # 分離した母音のファイルの中央部分が安定するのでそこを狙って引数を設定

    # 主な関数(固定フォルダへのグラフ出力等含むため注意)
    fiddle(in_path, sample_path, count, offset, size, target_path, out_path)
