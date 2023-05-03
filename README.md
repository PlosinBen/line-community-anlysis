


## 訊息分析


### 上傳文字備份

#### Request

##### path
```
POST /analysis
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
POST /analysis/<hash>
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



