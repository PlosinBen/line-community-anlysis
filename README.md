


## 訊息分析


### 上傳文字備份

#### Request

##### path
```
POST /api/analysis
```

#### Response
```
{
    "hash": "1aab83a68814893ef1013ad74c2dfd2c"
}
```

### 取得文字基本分析結果

#### Request
```
POST /api/analysis/<hash>
```
#### Response
```
{
    "analysis": {
        "average_of_messages_by_spoken_user": 3093.4844720496894,
        "number_of_message": 1003540,
        "number_of_spoken_user": 322,
        "number_of_sys_message": 7438,
        "number_of_user_message": 996102,
        "ranking_of_user_message": [
            [
                "探吉教-淡藍羽翼的韭韭TMF",
                53527
            ],
            [
                "探吉教-資工探吉爸",
                47997
            ],
            [
                "探吉教-茉莉茉茉茉莉",
                33444
            ],
            [
                "探吉教-頭回去火鍋ㄉFong",
                28360
            ],
            [
                "探吉教-Jason.L",
                23415
            ]
        ],
        "ranking_of_user_sticker": [
            [
                "探吉教 - SQQQDer3cm橘子",
                2606
            ],
            [
                "探吉教-🥭可愛芒果❤️VT",
                1164
            ],
            [
                "探吉教-頭回去火鍋ㄉFong",
                911
            ],
            [
                "探吉教 Olivia",
                753
            ],
            [
                "探吉教-造天計畫龍",
                642
            ]
        ]
    }
}
```

### 風險評價計算

#### Request
```
GET /api/risk
```
#### query parameter
```
start_date: YYYY-MM-DD
end_date: YYYY-MM-DD
asset[]: 標的代號 ex: QQQ, SPY
period[]: 計算週期 ex:8, 10, 200

example
start_date=2015-01-01&end_date=2023-05-05&asset[]=QQQ&asset[]=SPY&asset[]=TLT&period[]=8&period[]=10&asset[]=SMH&asset[]=IWM
```

#### Response
```
{
    "10": {
        "IWM": 0.17202524916311449,
        "QQQ": 0.17214714355907348,
        "SMH": 0.16739940305795112,
        "SPY": 0.18231924506796843,
        "TLT": 0.30610895915189257
    },
    "8": {
        "IWM": 0.17177344217466417,
        "QQQ": 0.16771423201818084,
        "SMH": 0.1661925918592342,
        "SPY": 0.18143739346377075,
        "TLT": 0.31288234048415003
    }
}
```



