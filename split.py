# 参考
# 【Python/pydub】mp3、wavファイルの分割（無音部分で区切る）
# https://algorithm.joho.info/programming/python/pydub-split-on-silence/

from pydub import AudioSegment
from pydub.silence import split_on_silence

# wavファイルのデータ取得
sound = AudioSegment.from_file('target_aiueo.wav', format='wav')

# wavデータの分割（無音部分で区切る）
chunks = split_on_silence(sound, min_silence_len=100, silence_thresh=-40, keep_silence=10)

# 分割したデータ毎にファイルに出力
for i, chunk in enumerate(chunks):
    chunk.export('split/' + str(i) +'.wav', format='wav')
