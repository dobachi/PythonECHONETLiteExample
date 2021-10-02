#!/usr/bin/env python

# https://yomon.hatenablog.com/entry/2020/09/sharp_aircon_echonet_lite を
# 参考に試してみる例

import socket
import sys

def create_command():
    # ---------------------------------------------------
    # 3.2.1 ECHONET Lite ヘッダ(EHD)
    # ---------------------------------------------------
    # 3.2.1.1 ECHONET Lite ヘッダ 1(EHD1)
    EHD1 = "10"  # ECHONET Lite規格
    
    # 3.2.1.2 ECHONET Lite ヘッダ 2(EHD2)
    EHD2 = "81"  # 形式１（規定電文形式）
    
    # 3.2.2 Transaction ID(TID)
    TID = "0001"  # IDなのでこの検証ではどの値でもOK
    
    # フレームのヘッダ－を構成
    EHD = EHD1 + EHD2 + TID
    
    # ---------------------------------------------------
    # 3.2.1 ECHONET Lite データ(EDATA)
    # ---------------------------------------------------
    # 3.2.4 ECHONETオブジェクト
    # EOJ = ECHONET Lite オブジェクト
    
    # SEOJ = 送信元ECHONET Lite オブジェクト
    SEOJ_CLS_GROUP = "05"     # 管理・操作関連クラスグループ
    SEOJ_CLS_CODE = "ff"      # コントローラー
    SEOJ_CLS_INSTANCE = "01"  # インスタンス番号
    SEOJ = SEOJ_CLS_GROUP + SEOJ_CLS_CODE + SEOJ_CLS_INSTANCE
    
    # DEOJ = 送信先ECHONET Lite オブジェクト
    DEOJ_CLS_GROUP = "01"     # 空調関連機器クラスグループ
    DEOJ_CLS_CODE = "30"      # 家庭用エアコンクラス
    DEOJ_CLS_INSTANCE = "01"  # All Instanses
    DEOJ = DEOJ_CLS_GROUP + DEOJ_CLS_CODE + DEOJ_CLS_INSTANCE
    
    
    # 3.2.5 ECHONET Lite サービス(ESV)
    ESV = "60"  # プロパティ値書き込み要求 (Set)
    
    ###############
    # APPENDIX ECHONET機器オブジェクト詳細規定
    # - 空調関連機器クラスグループ
    #  - 家庭用エアコンクラス規定
    # を確認
    
    # 3.2.6 処理プロパティカウンタ
    OPC = "01"  # 1件
    
    
    # プロパティ（今回は電源の操作なので1件だけ）
    EPC1 = "80"    # 動作状態
    PDC1 = "01"    # Setなので1Byte指定
    EDT1 = "31"    # Offつまり0x31を指定
    PROP1 = EPC1 + PDC1 + EDT1
    
    # フレームのデータ部分であるEDATAを構成
    EDATA = SEOJ + DEOJ + ESV + OPC + PROP1
    
    echonet_command = EHD + EDATA

    return echonet_command


def send(host, echonet_command):
    echonet_port = 3610
    #aircon_ip = "192.168.1.10"  # 224.0.23.0のアドレスを使うとマルチキャストもできます
    
    # 要求送信用ソケットでコマンド送信
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    send_sock.sendto(bytes.fromhex(echonet_command), (host, echonet_port))
    send_sock.close()

if __name__ == '__main__':
    args = sys.argv
    echonet_command = create_command()
    send(args[1], echonet_command);