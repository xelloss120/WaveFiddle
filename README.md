# WaveFiddle
自分の声を好きな声に変換したかったけどダメだったやつ  

## これなに？
任意の声の母音をフーリエ変換を使って、別の声に変換しようとしたPythonコードです。  
実行結果のサンプルとして「棒読みちゃん」を「琴葉葵」に変換した際の音声ファイルと波形画像を含みます。  

## 背景
動画配信で地声を晒すのを避け、「ゆかりねっと」を使っていますが、誤認識やタイムラグが悩みです。ボイチェンも使っていますが、地声の影響を受けますし、音割れがあったり、僅かとは言え利用シーンによっては遅延が致命的だったりします。だったら「自分の声が好きな声になればいいじゃない」と誰もが思うことでしょう。  

## 概要
世の音声認識やボイチェンは万人が使えるようにしているから大変なんだ！というのが起点です。自分の声と目標の声が決まっているなら、簡単な計算だけで実現できたりしないのか？用途を制限し、利用者が分かって使えば「ケプストラム」だの「マルコフ」だの「機械学習」は不要なのでは？いっそフーリエ変換だけでそこそこやれないか？を試してみました。(そこそこ具合に味が出たら良いなぁと願いを込めつつ……)  

## 方法
自分の声と目標の声のフーリエ結果の差？を係数にして、自分の声に掛けたら目標の声になるんじゃないの？という頭の足りない方法です。認識は単純比較(差の最小を選択)です。頭が足りないのでかっこいい式は書けないので、詳細はコードを読んでください。  

## 結果
だめでした。  

## 図
■あいうえお認識  
![あいうえお認識](https://github.com/xelloss120/WaveFiddle/blob/master/dif.png "あいうえお認識")  
図1 : 縦軸が差、横軸が時間？です。この例は「あいうえお」と発話してるので、まぁ……？みたいな感じです。  

■「あ」の変換  
![「あ」の変換](https://github.com/xelloss120/WaveFiddle/blob/master/fig/0000.png "「あ」の変換")  
図2 : 図1の横軸0に該当する変換例です。青が変換前、橙が変換後  

■誤認識  
![誤認識](https://github.com/xelloss120/WaveFiddle/blob/master/fig/0003.png "誤認識")  
図3 : 図1の横軸3に該当する誤認識例です。  

■無音部分  
![無音部分](https://github.com/xelloss120/WaveFiddle/blob/master/fig/0004.png "無音部分")  
図4 : 図1の横軸4に該当する例です。ここはほぼ無音と思われます。  

## 動かし方
1.「あいうえお」と発話した音声をsplit.pyで分離します。※1  
2.rename.pyで名前変更します。※2  
3.分離した音声を対象と目標で分けて保存します。※3  
4.最後にfiddle.pyで引数設定して実行  

※1.元々分けて収録した場合は当然不要です。  
※2.手作業しても良いですし、自前や慣れたツールでもいいです。  
※3.自分の声は3回くらい平均すると良さげ？  
※4.各工程で色々数値調整が必要です。がんばって！（無責任  
※5.必要なモジュールは頑張って入れてね！（無責任  

## 免責
ご利用は自己責任で！！  

## ぼやき
閾値調整したりすればもう少しマシに……、処理は大した事ないのでGPU処理して遅延解決したり……、夢はあったんですけどねぇ……。  
最強のバイオボイチェン(両声類)も練習したりしましたが、やっぱり大変です。  

## 参考
http://chi.usamimi.info/Program/Application/BouyomiChan/  
https://www.ah-soft.com/voiceroid/kotonoha/  
http://www.okayulu.moe/  
https://www.slideshare.net/akinoriito549/ss-23821600  
https://github.com/Hiroshiba/become-yukarin  
https://algorithm.joho.info/programming/python/numpy-fast-fourier-transform/  
https://algorithm.joho.info/programming/python/pydub-split-on-silence/  
