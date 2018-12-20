import os
import glob

path = 'split/'
wavs = glob.glob(path + '*.wav')

names = ['a', 'i', 'u', 'e', 'o']

for i in range(5):
    os.rename(wavs[i], path + names[i] + '.wav')
