# CDC-Python

国赛Python端接口文档 - China Computer Design Competition Python interface document

[TOC]

# Common Request Json Format

```python
{
  "id":1234,
  "type":"xxx",
  "subtype":"xxxx",
  "data":{
      "key":"value"
  }
}
```

# Common Response Json Format

```python
{
  "id":1234,
  "status":0,
  "message":"successful",
  "data":{
      "key":"value"
  }
}
```

# Param Description

|  Field  |  Type  |                         Description                          |   Caller   |             Example              |
| :-----: | :----: | :----------------------------------------------------------: | :--------: | :------------------------------: |
|   id    |  int   |      事件处理id，整型，请求端发送，接收端返回时原样返回      | 请求、返回 |           "id":123456            |
| status  |  int   | 返回请求处理状态，请求时status填写0。默认返回0时为请求处理成功，若失败返回错误码 |    返回    |            "status":0            |
| message | string | 状态简略信息，若成功调用则返回"successful"，失败返回错误信息 |    返回    |      "message":"successful"      |
|  type   | string |                           请求类型                           |    请求    |          "type":"user"           |
| subtype | string |                          请求子类型                          |    请求    |        "subtype":"login"         |
|  data   |  json  |                   包含附加或返回的请求数据                   | 请求、返回 | "data":{"token":"xxxxxxxxxxxxx"} |

# Recommend

**商品推荐类**

## Recommend-Item

> **API Description**

`POST`

​	**类似商品推荐接口**

​	此API采用基于用户行为的协同过滤算法，通过对用户的行为习惯进行权重换算，并与其他用户群体进行对比，定位归属此用户所在群体，并以该群体为出发点，向此用户推荐商品

​	此API的应用场景如下：

+ 每个商品下方的“猜你喜欢”、“购买了此商品的人还看了...”、“看了又看”之类的模块（类似商品/群体爱好推荐）

> **URL**

`http://guosai.zustmanong.cn/api/v2/recommend/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "status":0,
    "type":"recommend",
    "subtype":"item",
    "data":{
        "item_id":"3412843468",
    }
}
```

> **Data Param**

|  Field  |  Type  | Length | Null | Default | **Description** |
| :-----: | :----: | :----: | :--: | :-----: | :-------------: |
| item_id | string |   10   |      |         |     商品id      |

> **Response Success Example**

```python
{
    "id": -1, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "num": 2, 
        "list": [
            {
                "id": "6816515512", 
                "store_id": "8996951955lxy", 
                "item_name": "夏季纯棉短T男", 
                "item_des": "{\"num\":3,\"list\":[\"http://127.0.0.1:8088/api/picture/getItemDetails?item_id=6816515512&index=1\",\"http://127.0.0.1:8088/api/picture/getItemDetails?item_id=6816515512&index=2\",\"http://127.0.0.1:8088/api/picture/getItemDetails?item_id=6816515512&index=3\"]}", 
                "item_portrait": "https://guosai-1251848017.cos.ap-shanghai.myqcloud.com/item/6816515512/portrait/6816515512.item",
                "item_type": "服装", 
                "item_geohash": null, 
                "item_status": 1, 
                "item_stock": 5,
                "original_price": "159", 
                "discount_price": "129", 
                "create_time": 1588231344.0, 
                "last_modified_time": 1588419373.0
            }, 
            {
                "id": "3990811", 
                "store_id": "8264815679admin", 
                "item_name": "99%细菌过滤，儿童一次性医用口罩 10枚", 
                "item_des": "", 
                "item_portrait": "https://yanxuan-item.nosdn.127.net/aa436fa42dc09938c7f985c071503569.png", 
                "item_type": "医用品", 
                "item_geohash": "", 
                "item_status": 1, 
                "item_stock": 100, 
                "original_price": "49", 
                "discount_price": "35", 
                "create_time": 1588387560.0, 
                "last_modified_time": 1588609110.0
            }
        ]
    }
}
```

> **Notice**

+ 所有文本型字段若判断是否为空时请同时判断null和空文本两种情况
+ 具体的商品信息字段介绍请看Java端的API接口

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": 100, 
    "message": "Error item id", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |          Message          |       Description        |
| :----: | :-----------------------: | :----------------------: |
|  100   |       Error item id       |      错误的item id       |
|  101   | Get recommend data failed | 获取推荐信息的商品id失败 |

## Recommend-Index

> **API Description**

`POST`

​	**主页商品推荐接口**

​	此API采用基于商品标签的协同过滤算法，通过用户行为对商品的标签进行权重换算，并与用户自身标签进行匹配，筛选出推荐商品

​	此API的应用场景如下：

+ app主页等非商品详情页（主页推荐）

> **URL**

`http://guosai.zustmanong.cn/api/v2/recommend/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "status":0,
    "type":"recommend",
    "subtype":"index",
    "data":{"limit":10}
}
```

> **Data Param**

| Field | Type | Length | Null | Default |         **Description**          |
| :---: | :--: | :----: | :--: | :-----: | :------------------------------: |
| limit | int  |   10   |  √   |   all   | 商品返回数量，不传默认为返回全部 |

> **Response Success Example**

```python
{
  "id": -1,
  "status": 0,
  "message": "Successful",
  "data": {
    "num": 5,
    "list": [
      {
        "id": "8604229547",
        "store_id": "8996951955lxy",
        "item_name": "NASA联名款夏季短T男",
        "item_des": null,
        "item_portrait": null,
        "item_type": "服装",
        "item_geohash": null,
        "item_status": 0,
        "item_stock": 10,
        "original_price": "99",
        "discount_price": "79",
        "create_time": 1588228011.0,
        "last_modified_time": 1588228011.0
      },
      {
        "id": "3412843468",
        "store_id": "8996951955lxy",
        "item_name": "漱口水",
        "item_des": "",
        "item_portrait": "",
        "item_type": "个人用品",
        "item_geohash": "",
        "item_status": 1,
        "item_stock": 12,
        "original_price": "99",
        "discount_price": "59",
        "create_time": 1588227960.0,
        "last_modified_time": 1588242240.0
      },
      {
        "id": "3990118",
        "store_id": "8264815679admin",
        "item_name": "【浙江专供】一次性日常防护口罩",
        "item_des": "",
        "item_portrait": "https://yanxuan-item.nosdn.127.net/093cc020e9b5e1bd6736f7bc72bf9227.png",
        "item_type": "医用品",
        "item_geohash": "",
        "item_status": 1,
        "item_stock": 100,
        "original_price": "16",
        "discount_price": null,
        "create_time": 1588387560.0,
        "last_modified_time": 1588609182.0
      },
      {
        "id": "3990811",
        "store_id": "8264815679admin",
        "item_name": "99%细菌过滤，儿童一次性医用口罩 10枚",
        "item_des": "",
        "item_portrait": "https://yanxuan-item.nosdn.127.net/aa436fa42dc09938c7f985c071503569.png",
        "item_type": "医用品",
        "item_geohash": "",
        "item_status": 1,
        "item_stock": 100,
        "original_price": "49",
        "discount_price": "35",
        "create_time": 1588387560.0,
        "last_modified_time": 1588609110.0
      },
      {
        "id": "6816515512",
        "store_id": "8996951955lxy",
        "item_name": "夏季纯棉短T男",
        "item_des": "{\"num\":3,\"list\":[\"http://127.0.0.1:8088/api/picture/getItemDetails?item_id=6816515512&index=1\",\"http://127.0.0.1:8088/api/picture/getItemDetails?item_id=6816515512&index=2\",\"http://127.0.0.1:8088/api/picture/getItemDetails?item_id=6816515512&index=3\"]}",
        "item_portrait": "https://guosai-1251848017.cos.ap-shanghai.myqcloud.com/item/6816515512/portrait/6816515512.item",
        "item_type": "服装",
        "item_geohash": null,
        "item_status": 1,
        "item_stock": 5,
        "original_price": "159",
        "discount_price": "129",
        "create_time": 1588231344.0,
        "last_modified_time": 1588419373.0
      }
    ]
  }
}
```

> **Notice**

+ 所有文本型字段若判断是否为空时请同时判断null和空文本两种情况
+ 具体的商品信息字段介绍请看Java端的API接口

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": 100, 
    "message": "Get Item Failed", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |     Message     |   Description    |
| :----: | :-------------: | :--------------: |
|  100   | Get Item Failed | 获取商品信息失败 |

# Tags

关键词提取类

## Tag-Text

> **API Description**

`POST`

​	**文本关键字提取接口**

​	此API采用jieba分词+Tfidf词频矩阵算法，获得一句话中的关键词列表

​	此API的应用场景如下：

+ 新增商品时自动添加关键词组

> **URL**

`http://guosai.zustmanong.cn/api/v2/tags/`

> **Request Json Text Example**

```python
{
    "id":1234,
    "status":0,
    "type":"tags",
    "subtype":"text",
    "data":{"text_list":["2020网红新款夏季清凉女装", "99%细菌过滤，儿童一次性医用口罩 10枚"]}
}
```

> **Data Param**

|   Field   |  Type  | Length | Null | Default | **Description** |
| :-------: | :----: | :----: | :--: | :-----: | :-------------: |
| text_list |  list  |        |  √   |         |  商品名称列表   |
|   text    | string |        |  √   |         |    商品名称     |

> **Notice**

+ `text`与`text_list`都未传入时，返回`-3`状态码
+ `text`与`text_list`都传入时，使用`text_list`，忽略`text`
+ 当只传了`text`，将自动等价于长度为1的`text_list`:`[text]`

> **Response Success Example**

```python
{
  "id": -1,
  "status": 0,
  "message": "Successful",
  "data": {
    "num": 2,
    "list": [
      ["2020","夏季","女装","新款","清凉","网红"],
      ["10","99","一次性","儿童","医用","口罩","细菌","过滤"]
    ]
  }
}
```

> **Notice**

+ `list`里的元素与请求时的顺序一致
+ 不管请求中传入的是`text`还是`text_list`，结果都将返回成list形式。
+ 即当元素只有一个时，list的结构为`[["key1","key2","key3"]]`

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -1, 
    "message": "Error JSON key", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -3     |
| -2     |
| -1     |

> **Local Status**

**null**

## Tag-item

> **API Description**

`POST`

​	**商品名称关键字提取接口，传入`item_list`将自动提取商品关键字并更新记录**

​	**此API仅Java端使用，前端请勿使用此接口，因为这个接口没有做权限验证**

​	此API采用jieba分词+Tfidf词频矩阵算法，获得一句话中的关键词列表

​	此API的应用场景如下：

+ 新增商品时自动添加关键词组

> **URL**

`http://guosai.zustmanong.cn/api/v2/tags/`

> **Request Json Text Example**

```python
{
    "id":1234,
    "status":0,
    "type":"tags",
    "subtype":"item",
    "data":{"item_list":[3454002, 3987066]}
}
```

> **Data Param**

|   Field   | Type | Length | Null | Default | **Description** |
| :-------: | :--: | :----: | :--: | :-----: | :-------------: |
| item_list | list |        |  √   |         |   商品id列表    |

> **Response Success Example**

```python
{
    "id": -1, 
    "status": 0, 
    "message": "Successful", 
    "data": {}
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -1, 
    "message": "Error JSON key", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |    Message    |  Description  |
| :----: | :-----------: | :-----------: |
|  100   | Error item id | 错误的item id |