# PythonECHONETLiteExample

主に [MoekadenRoom] を用いた動作確認用のコントローラ側のサンプルスクリプト。

[MoekadenRoom]: https://github.com/SonyCSL/MoekadenRoom


## 前提

* コントローラのIPアドレス
  * 10.0.4.72
* MoekadenのIPアドレス
  * 10.0.4.73

## Light

電気のOn、Off。

```shell
$ ./bin/light_on.sh 10.0.4.73
$ ./bin/light_off.sh 10.0.4.73
```

予め受信者を立てておくと、一応戻り値を受け取れる。

```shell
$ ./bin/receive.sh
```

以下のようなメッセージ（戻り値）が出力される。

```
1081000002900105ff0171018000
```

## Air Conditiner

エアコンの状態確認

```shell
$ ./bin/aircon_info_send.sh 10.0.4.73
```

予め受信者を立てておくと以下のような結果が得られる。

```shell
$ ./bin/aircon_info_receive.sh
```

以下のようメッセージ（戻り値）が出力される。

```
# original
(b'\x10\x81\x00\x01\x010\x01\x05\xff\x01r\x02\x80\x011\xb3\x01\x14', ('10.0.4.73', 3610))
# parsed
[['0x10', '0x81'], ['0x0', '0x1'], ['0x1', '0x30', '0x1'], ['0x5', '0xff', '0x1'], ['0x72'], ['0x2'], ['0x80'], ['0x1'], ['0x31'], ['0xb3'], ['0x1'], ['0x14']]
```

以下、戻り値の簡単な解説。
[第２部 ECHONET Lite 通信ミドルウェア仕様] 、[APPENDIX ECHONET機器オブジェクト詳細規定] あたりを参照したもの。

[第２部 ECHONET Lite 通信ミドルウェア仕様]: https://echonet.jp/wp/wp-content/uploads/pdf/General/Standard/ECHONET_lite_V1_13_jp/ECHONET-Lite_Ver.1.13_02.pdf
[APPENDIX ECHONET機器オブジェクト詳細規定]: https://echonet.jp/wp/wp-content/uploads/pdf/General/Standard/Release/Release_N_jp/Appendix_Release_N.pdf

```
['0x10', '0x81']
```

ECHONET Liteであることを宣言する値。ミドルウェア仕様書のp.20あたり参照。

- EHD1: ECHONET Liteヘッダ
- EHD2: 電文形式（今回は、規定電文）

```
['0x0', '0x1']
```

- TID: やりとりを補助するためのID。送信時に指定されたものが入っている。

```
['0x1', '0x30', '0x1']
```

SEOJ: 送信元ECHONET Liteオブジェクトを示す。
詳細のp.110あたりを参照。

- クラスグループコード: 空調関連機器クラスグループ
- クラスコード: 家庭用エアコン
- インスタンスコード： 一般

```
['0x5', '0xff', '0x1']
```
DEOJ: 送信先ECHONET Liteオブジェクトを示す。
詳細のp.537あたりを参照。

- クラスグループコード: 管理・操作関連機器クラスグループ
- クラスコード: コントローラ
- インスタンスコード: 一般

```
['0x72']
```

ESV: ECHONET Liteサービス。
仕様書のp.23あたりを参照。

プロパティ値読み出し要求への返事。

```
['0x2']
```

OPC: 処理プロパティカウンタ。今回は、2件のプロパティ取得への返信なので、返信も2件。

```
['0x80'], ['0x1'], ['0x31']
```

- EPC: プロパティ名。今回は動作状態。
- PDC: バイト数。今回は1バイト。
- EDT: プロパティ値。今回はOFF。

詳細のp.112あたりを参照。

```
['0xb3'], ['0x1'], ['0x14']
```

$ EPC: プロパティ名。今回は温度設定値。
- PDC: バイト数。今回は1バイト。
- EDT: プロパティ値。今回は0x14つまり、20。

詳細のp.112あたりを参照。

## エアコンの設定

## インスタンス検索

インスタンスの検索

```shell
$ ./bin/search.sh 10.0.4.73
```

予め受信者を立てておくと以下のような結果が得られる。

```shell
$ ./bin/search_receive.sh
```

## 備考：マルチキャスト

MoekadenのIPアドレスの代わりに、 `224.0.23.0` のマルチキャストアドレスに送ることもできる。
ただ、Moekadenを利用するときは、マルチキャストが利用できないかもしれない。
実機（ダイキン製）では動いた。