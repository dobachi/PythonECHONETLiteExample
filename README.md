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
値の意味はソースコードのコメント参照。

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