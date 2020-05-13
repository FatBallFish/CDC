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
    "code": "200", 
    "data": {
        "rcmdItemList": [
            {
                "type": 1,
                "id": "6816515512", 
                "categoryItem": {
                    "id": "6816515512", 
                    "listPicUrl": "https://guosai-1251848017.cos.ap-shanghai.myqcloud.com/item/6816515512/portrait/6816515512.item", 
                    "simpleDesc": null, 
                    "simpleDescClose": false, 
                    "name": "夏季纯棉短T男", 
                    "retailPrice": 159.00, 
                    "activityPrice": 129.00}
            }, 
            {
                "type": 1, 
                "id": "6816515512", 
                "categoryItem": {
                    "id": "6816515512", 
                    "listPicUrl": "https://guosai-1251848017.cos.ap-shanghai.myqcloud.com/item/6816515512/portrait/6816515512.item", 
                    "simpleDesc": null, 
                    "simpleDescClose": false, 
                    "name": "夏季纯棉短T男", 
                    "retailPrice": 159.00, 
                    "activityPrice": 129.00}
            }, 
            {
                "type": 1, 
                "id": "6816515512",
                "categoryItem": {
                    "id": "6816515512",
                    "listPicUrl": "https://guosai-1251848017.cos.ap-shanghai.myqcloud.com/item/6816515512/portrait/6816515512.item", 
                    "simpleDesc": null, 
                    "simpleDescClose": false, 
                    "name": "夏季纯棉短T男", 
                    "retailPrice": 159.00, 
                    "activityPrice": 129.00}
            }, 
            {
                "type": 1, 
                "id": "6816515512", 
                "categoryItem": {
                    "id": "6816515512", 
                    "listPicUrl": "https://guosai-1251848017.cos.ap-shanghai.myqcloud.com/item/6816515512/portrait/6816515512.item", 
                    "simpleDesc": null, 
                    "simpleDescClose": false, 
                    "name": "夏季纯棉短T男", 
                    "retailPrice": 159.00, 
                    "activityPrice": 129.00}
            }, 
            {
                "type": 1,
                "id": "6816515512",
                "categoryItem": {
                    "id": "6816515512", 
                    "listPicUrl": "https://guosai-1251848017.cos.ap-shanghai.myqcloud.com/item/6816515512/portrait/6816515512.item",
                    "simpleDesc": null, 
                    "simpleDescClose": false, 
                    "name": "夏季纯棉短T男", 
                    "retailPrice": 159.00, 
                    "activityPrice": 129.00}
            }
        ]
    }
}
```

> **Notice**

+ 接口返回格式完全按照网易严选的主页商品列表的返回格式返回

> **Response Failed Example**

```python
{
    "code": 100, 
    "message": "Error item id", 
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
    "type":"recommend",
    "subtype":"index",
    "data":{
        "limit":10
    }
}
```

> **Data Param**

| Field | Type | Length | Null | Default |         **Description**          |
| :---: | :--: | :----: | :--: | :-----: | :------------------------------: |
| limit | int  |   10   |  √   |   all   | 商品返回数量，不传默认为返回全部 |

> **Response Success Example**

```python
{
    "code": "200", 
    "data": {
        "rcmdItemList": [
            {
                "type": 1,
                "id": "6816515512", 
                "categoryItem": {
                    "id": "6816515512", 
                    "listPicUrl": "https://guosai-1251848017.cos.ap-shanghai.myqcloud.com/item/6816515512/portrait/6816515512.item", 
                    "simpleDesc": null, 
                    "simpleDescClose": false, 
                    "name": "夏季纯棉短T男", 
                    "retailPrice": 159.00, 
                    "activityPrice": 129.00}
            }, 
            {
                "type": 1, 
                "id": "6816515512", 
                "categoryItem": {
                    "id": "6816515512", 
                    "listPicUrl": "https://guosai-1251848017.cos.ap-shanghai.myqcloud.com/item/6816515512/portrait/6816515512.item", 
                    "simpleDesc": null, 
                    "simpleDescClose": false, 
                    "name": "夏季纯棉短T男", 
                    "retailPrice": 159.00, 
                    "activityPrice": 129.00}
            }, 
            {
                "type": 1, 
                "id": "6816515512",
                "categoryItem": {
                    "id": "6816515512",
                    "listPicUrl": "https://guosai-1251848017.cos.ap-shanghai.myqcloud.com/item/6816515512/portrait/6816515512.item", 
                    "simpleDesc": null, 
                    "simpleDescClose": false, 
                    "name": "夏季纯棉短T男", 
                    "retailPrice": 159.00, 
                    "activityPrice": 129.00}
            }, 
            {
                "type": 1, 
                "id": "6816515512", 
                "categoryItem": {
                    "id": "6816515512", 
                    "listPicUrl": "https://guosai-1251848017.cos.ap-shanghai.myqcloud.com/item/6816515512/portrait/6816515512.item", 
                    "simpleDesc": null, 
                    "simpleDescClose": false, 
                    "name": "夏季纯棉短T男", 
                    "retailPrice": 159.00, 
                    "activityPrice": 129.00}
            }, 
            {
                "type": 1,
                "id": "6816515512",
                "categoryItem": {
                    "id": "6816515512", 
                    "listPicUrl": "https://guosai-1251848017.cos.ap-shanghai.myqcloud.com/item/6816515512/portrait/6816515512.item",
                    "simpleDesc": null, 
                    "simpleDescClose": false, 
                    "name": "夏季纯棉短T男", 
                    "retailPrice": 159.00, 
                    "activityPrice": 129.00}
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
    "code": 100, 
    "message": "Get Item Failed", 
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

# Community

**社区动态类**

## Community - publish

> **API Description**

`POST`

​	**发布动态接口**

​	此接口接收动态内容和`item_id`，返回动态`id`

> **URL**

`http://guosai.zustmanong.cn/api/v2/community/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"community",
    "subtype":"publish",
    "data":{
        "content": "疫情期间大家一定要注意安全！推荐这款口罩，保障你的出行健康", 
        "item_id": 3990811
    }
}
```

> **Data Param**

|  Field  |  Type  | Length | Null | Default | **Description** |
| :-----: | :----: | :----: | :--: | :-----: | :-------------: |
| content | string |        |      |         |    动态内容     |
| item_id | String |        |      |         |     商品id      |

> **Notice**

+ `content`前端怎么传过来就怎么传回去，因此可以选择存储纯文本或者html代码
+ `item_id`若不存在将返回`100`错误码

> **Response Success Example**

```python
{
    "id": -1, 
    "status": 0, 
    "message": "Successful", 
    "data": {"community_id":1}
}
```

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

| Status |    Message    |  Description  |
| :----: | :-----------: | :-----------: |
|  100   | Error item id | 错误的item id |

## Community - list

> **API Description**

`POST`

​	**发布动态接口**

​	此接口接收经纬度信息，返回按`创建时间降序排序`的社区动态列表

> **URL**

`http://guosai.zustmanong.cn/api/v2/community/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"community",
    "subtype":"list",
    "data":{
        "latitude": 30.2262500,
        "longitude": 120.0318500,
    }
}
```

> **Data Param**

|   Field   |  Type  | Length | Null | Default |                       **Description**                        |
| :-------: | :----: | :----: | :--: | :-----: | :----------------------------------------------------------: |
| latitude  | double |        |      |         |                             纬度                             |
| longitude | double |        |      |         |                             经度                             |
|   start   |  int   |        |  √   |    0    |            记录起始位置，默认为0。首记录从0开始。            |
|   limit   |  int   |        |  √   |   all   |                  返回记录条数，默认返回全部                  |
| distance  | double |        |  √   |   500   | 限制距离，仅返回与用户经纬度距离在distance内的社区动态。默认为500，单位米。 |

> **Response Success Example**

```python
{
    "id": -1, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        {
            "num": 3, 
            "list": [
                {
                    "community_id": 3, 
                    "user": {
                        "username": "wlc", 
                        "nickname": "ThinBallFish"
                    }, 
                    "content": "疫情期间大家一定要注意安全！推荐这款口罩，保障你的出行健康", 
                    "item": {
                        "id": "3990811", 
                        "name": "99%细菌过滤，儿童一次性医用口罩 10枚", 
                        "simpleDesc": null, 
                        "listPicUrl": "https://yanxuan-item.nosdn.127.net/aa436fa42dc09938c7f985c071503569.png", 
                        "retailPrice": 49.00, 
                        "activityPrice": 35.00
                    }, 
                    "add_time": 1589299920.0, 
                    "update_time": 1589299920.0
                }, 
                {
                    "community_id": 2, 
                    "user": {
                        "username": "wlc", 
                        "nickname": "ThinBallFish"
                    }, 
                    "content": "这款洗面奶非常不错！适合广大男同胞使用！", 
                    "item": {
                        "id": "7804238231", 
                        "name": "锐度洗面奶男士专用控油祛痘去黑头变美白除螨虫氨基酸洁面乳套装", 
                        "simpleDesc": "早控油，晚美白；分时洁面，科学有效！", 
                        "listPicUrl": "https://g-search1.alicdn.com/img/bao/uploaded/i4/imgextra/i3/34637306/O1CN01FVcCqQ23qCFfZZulY_!!0-saturn_solar.jpg_250x250.jpg_.webp", 
                        "retailPrice": 218.00, 
                        "activityPrice": 148.00
                    }, 
                    "add_time": 1589299320.0, 
                    "update_time": 1589299320.0
                }, 
                {
                    "community_id": 1, 
                    "user": {
                        "username": "wlc", 
                        "nickname": "ThinBallFish"}, 
                    "content": "夜深人静，一个人观赏月亮，心态平和", 
                    "item": null, 
                    "add_time": 1589298960.0, 
                    "update_time": 1589298960.0
                }
            ]
        }
    }
}
```

> **Json-item Param**

| param         | type   | describe     |
| ------------- | ------ | ------------ |
| id            | int    | 商品id       |
| name          | string | 商品名称     |
| simpleDesc    | string | 商品简述     |
| listPicUrl    | string | 商品图片url  |
| retailPrice   | double | 商品原始价格 |
| activityPrice | double | 商品活动价格 |

> **Notice**

+ 当用户发布动态时未指定item，则`item`将直接为`null`
+ 其他字段的记录不存在的时候，也将返回`null`,例如`simpleDesc`、`activityPrice`

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -1, 
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

null

## Community - update

> **API Description**

`POST`

​	**更新动态接口**

​	此接口接收动态`id`，动态内容和`item_id`，进行更新动态内容

> **URL**

`http://guosai.zustmanong.cn/api/v2/community/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"community",
    "subtype":"update",
    "data":{
        "community_id":1
        "content": "疫情期间大家一定要注意安全！推荐这款口罩，保障你的出行健康", 
        "item_id": 3990811
    }
}
```

> **Data Param**

|    Field     |  Type  | Length | Null | Default | **Description** |
| :----------: | :----: | :----: | :--: | :-----: | :-------------: |
| community_id |  int   |        |      |         |     动态id      |
|   content    | string |        |  √   |         |    动态内容     |
|   item_id    | String |        |  √   |         |     商品id      |

> **Notice**

+ `content`前端怎么传过来就怎么传回去，因此可以选择存储纯文本或者html代码
+ `community_id`若不存在将返回`100`错误码
+ `item_id`若不存在将返回`101`错误码

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
    "status": 100, 
    "message": "Error community id", 
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

| Status |      Message       |   Description    |
| :----: | :----------------: | :--------------: |
|  100   | Error community id | 错误的社区动态id |
|  101   |   Error item id    |  错误的item id   |

## Community - delete

> **API Description**

`POST`

​	**删除动态接口**

​	此接口接收动态`id`，进行删除社区动态

> **URL**

`http://guosai.zustmanong.cn/api/v2/community/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"community",
    "subtype":"delete",
    "data":{
        "community_id":1
    }
}
```

> **Data Param**

|    Field     | Type | Length | Null | Default | **Description** |
| :----------: | :--: | :----: | :--: | :-----: | :-------------: |
| community_id | int  |        |      |         |     动态id      |

> **Notice**

+ `community_id`若不存在将返回`100`错误码

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
    "status": 100, 
    "message": "Error community id", 
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

| Status |      Message       |   Description    |
| :----: | :----------------: | :--------------: |
|  100   | Error community id | 错误的社区动态id |

# Distance

**经纬网距离换算类**

## Distance - calc

> **API Description**

`POST`

​	**经纬网距离换算接口**

​	此接口接收两组经纬网信息，返回相距距离

> **URL**

`http://guosai.zustmanong.cn/api/v2/distance/

> **URL Param**

此接口无需任何url参数

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"distance",
    "subtype":"calc",
    "data":{
        "lat1": 30.2262500, 
        "lng1": 120.0318500,
        "lat2": 28.6756122,
        "lng2": 121.3628220,
    }
}
```

> **Data Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| lat1  | Double |        |      |         |      纬度1      |
| lng1  | Double |        |      |         |      经度1      |
| lat2  | Double |        |      |         |      纬度2      |
| lng2  | Double |        |      |         |      经度2      |

> **Response Success Example**

```python
{
    "id": -1, 
    "status": 0, 
    "message": "Successful", 
    "data": {"distance": 215498.4639470404}
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": 100, 
    "message": "Error location data", 
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

| Status |       Message       |  Description   |
| :----: | :-----------------: | :------------: |
|  100   | Error location data | 经纬网信息错误 |

# Msg

**站内信类**

后台地址：[易邻邦后台管理系统](https://guosai.zustmanong.cn/admin)

管理员账号：`guosai`

管理员密码：`guosai2020`

已获得所有权限

## Msg - has_new

> **API Description**

`POST`

此API用于获取用户的新消息条数，成功返回系统新站内信条数，新私聊条数和私聊条数详情

这里的系统消息，是指由`guosai`用户或者空用户发出的消息，并非是指`消息type`值为`system`的消息。

这里的私聊消息，是指由非系统`guosai`用户或者空用户发出的，且有指定单一的接收者的消息，并非是指`消息type`值为`private`的消息。

若想获取指定消息类型的消息，请使用[Msg - filter](#Msg - filter)API接口

> **URL**

`https://guosai.zustmanong.cn/api/v2/msg/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"has_new",
    "data":{}
}
```

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "sys": 4, 
        "private": 3, 
        "private_detail": {
            "13750687010": 2, 
            "13735866541": 1
        }
    }
}
```

> **Response Data Param**

|     Field      | Type |  **Description**   |
| :------------: | :--: | :----------------: |
|      sys       | int  |   系统新消息条数   |
|    private     | int  |  新私聊站内信条数  |
| private_detail | json | 私聊站内信条数详情 |

> **Notice**

+ `private_detail`中的格式为：`私聊对象`:`新消息条数`，无`num`字段统计，需自行判断

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -100, 
    "message": "Missing necessary args", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

**null**

## Msg - sys

> **API Description**

`POST`

此API用于获取发给用户的所有系统站内信，并自动**按发送时间降序排序**

这里的系统消息，是指由`hotel`用户或者空用户发出的消息，并非是指`消息type`值为`system`的消息。

若想获取指定消息类型的消息，请使用[Msg - filter](#Msg - filter)API接口

> **URL**

`https://guosai.zustmanong.cn/api/v2/msg/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"sys",
    "data":{
        "if_new":2
    }
}
```

> **Data Param**

| Field  | Type | Length | Null | Default |                       **Description**                        |
| :----: | :--: | :----: | :--: | :-----: | :----------------------------------------------------------: |
| if_new | int  |        |      |    √    | 消息过滤模式，可选值：`0`获取新消息;`1`获取已读消息;`2`获取全部消息。默认为`0` |

> **Notice**

+ 当`if_new`不为可选值范围时，将自动判定为获取新消息

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "num": 1, 
        "list": [
            {
                "msg_id": 1, 
                "type":"system",
                "subtype":"notice",
                "title": "这是一条测试通知", 
                "content": "嗯？我就测试一下", 
                "add_time": 1582964040.0, 
                "status": false,
                "extra":""
            }
        ]
    }
}
```

> **Response Data Param**

|  Field   |  Type   |  **Description**   |
| :------: | :-----: | :----------------: |
|  msg_id  |   int   |   此消息的消息id   |
|   type   | string  |  消息类型，自定义  |
| subtype  | string  | 消息子类型，自定义 |
|  title   | string  |      消息标题      |
| content  | string  |      消息内容      |
| add_time |  float  |  站内信发送时间戳  |
|  status  | boolean |    消息已读状态    |
|  extra   | string  |  额外信息，自定义  |

> **Notice**

+ 消息已读状态变更请用[Msg - sign](#Msg - sign)或者[Msg - sign_batch](#Msg - sign_batch)API
+ 不论是系统群发还是单独发送的站内信，全部规整到此api
+ **一般的系统通知我打算如此设置：`type`值为`system`,`subtype`值为`notice`。其他可自定义**

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -100, 
    "message": "Missing necessary args", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |        Message        |   Description    |
| :----: | :-------------------: | :--------------: |
|  100   | Get admin user failed | 获取系统用户失败 |

## Msg - private

> **API Description**

`POST`

此API用于获取用户发送出去或者发送给用户的所有私聊站内信，并自动**按发送时间降序排序**

这里的私聊消息，是指由非系统`hotel`用户或者空用户发出的，且有指定单一的接收者的消息，并非是指`消息type`值为`private`的消息。

若想获取指定消息类型的消息，请使用[Msg - filter](#Msg - filter)API接口

> **URL**

`https://guosai.zustmanong.cn/api/v2/msg/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"private",
    "data":{
        "if_new":2,
        "people": "13750687010", 
        "start": 0, 
        "limit": -1
    }
}
```

> **Data Param**

| Field  |  Type  | Length | Null | Default |                       **Description**                        |
| :----: | :----: | :----: | :--: | :-----: | :----------------------------------------------------------: |
| if_new |  int   |        |      |    √    | 消息过滤模式，可选值：`0`获取新消息;`1`获取已读消息;`2`获取全部消息。默认为`0` |
| people | string |        |      |    √    | 聊天对象用户名，当不传递或传递为空文本时，返回所有聊天对象的消息，默认为空文本 |
| start  |  int   |        |      |    √    | 记录起始位置，设定后将从`start`的位置开始获取记录，初始值为`0` |
| limit  |  int   |        |      |    √    | 记录返回条数，设定后将从`start`位置开始，返回limit条记录，若记录不足有多少返回多少。当`limit`设置为-1时，将返回从`start`开始的全部记录，默认为`-1` |

> **Notice**

+ 当`if_new`为`0`的时候，用户发送且对方未读的消息将不返回，因为这类消息对于用户自己来说是已读消息
+ 当`if_new`不为可选值范围时，将自动判定为获取新消息
+ `people`传递的值不存在时将返回`101`错误码
+ 当`start`不传递或传递的值数据类型有误时，当做`0`处理
+ 当`limit`不传递或传递的值数据类型有误或值为负数时，当做`-1`处理
+ **`limit`与`if_new`同时存在时，将先执行`limit`再执行`if_new`，因此在使用`limit`取出指定数量消息时，建议将`if_new`设置为2，否则会出现什么问题我也没考虑清楚**

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "records_num": 4, 
        "unit_num": 2, 
        "list": [
            {
                "people": "13750687010", 
                "num": 3, 
                "records": [
                    {
                        "source": 0, 
                        "type":"private",
                        "subtype":"default",
                        "msg_id": 2, 
                        "title": "你好", 
                        "content": "你好鸭", 
                        "add_time": 1582964040.0, 
                        "status": false,
                        "extra":""
                    }, 
                    {
                        "source": 0, 
                        "type":"private",
                        "subtype":"default",
                        "msg_id": 4, 
                        "title": "你好", 
                        "content": "你好鸭", 
                        "add_time": 1582984020.0, 
                        "status": false,
                        "extra":""
                    }, 
                    {
                        "source": 1, 
                        "msg_id": 5, 
                        "type":"private",
                        "subtype":"default",
                        "title": "回复", 
                        "content": "你也好呀！", 
                        "add_time": 1582985310.489896, 
                        "status": false,
                        "extra":""
                    }
                ]
            }, 
            {
                "people": "13735866541", 
                "num": 1, 
                "records": [
                    {
                        "source": 0, 
                        "msg_id": 3, 
                        "type":"private",
                        "subtype":"default",
                        "title": "你好", 
                        "content": "你好鸭", 
                        "add_time": 1582983960.0, 
                        "status": false,
                        "extra":""
                    }
                ]
            }
        ]
    }
}
```

> **Response Data Param**

> **list结构**

|  Field  |  Type  | **Description** |
| :-----: | :----: | :-------------: |
| people  | string |   私聊对象id    |
|   num   |  int   |    私聊条数     |
| records |  list  |    消息列表     |

> **records结构**

|  Field   |  Type   |                      **Description**                       |
| :------: | :-----: | :--------------------------------------------------------: |
|  source  |   int   | 消息类型，可选值：`0`:其他人发来的消息；`1`:用户发送的消息 |
|  msg_id  |   int   |                       此消息的消息id                       |
|   type   | string  |          消息类型，暂不可自定义，默认为`private`           |
| subtype  | string  |          消息子类型,暂不可自定义，默认为`default`          |
|  title   | string  |                          消息标题                          |
| content  | string  |                          消息内容                          |
| add_time |  float  |                      站内信发送时间戳                      |
|  status  | boolean |                     消息已读状态extra                      |
|  extra   | string  |            额外信息,暂不可自定义，默认为空文本             |

> **Notice**

+ 消息已读状态变更请用[Msg - sign](#Msg - sign)或者[Msg - sign_batch](#Msg - sign_batch)API
+ 在私聊中建议使用`content`字段传递聊天内容，保留`title`的原因是打算后期做成卡片式分享时用到。
+ 私聊消息之所以用消息列表式返回格式是为了前端更方便处理，同时也是借鉴了b站与其他论坛的格式
+ **私聊消息暂不使用`type`、`subtype`和`extra`的值**
+ **默认的私聊消息`type`值为`private`，`subtype`值为`default`，`extra`为空文本**

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -100, 
    "message": "Missing necessary args", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |        Message        |   Description    |
| :----: | :-------------------: | :--------------: |
|  100   | Get admin user failed | 获取系统用户失败 |
|  101   |   Get sender failed   |  获取发送者失败  |

## Msg - msg_list

> **API Description**

`POST`

此API用于获取用户的私聊过的聊天对象列表及最后一条消息，并自动**按最后一条消息发送时间降序排序**

这里的私聊消息，是指由非系统`hotel`用户或者空用户发出的，且有指定单一的接收者的消息，并非是指`消息type`值为`private`的消息。

若想获取指定消息类型的消息，请使用[Msg - filter](#Msg - filter)API接口

> **URL**

`https://guosai.zustmanong.cn/api/v2/msg/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"msg_list",
    "data":{}
}
```

> **Data Param**

**null**

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "num": 1, 
        "list": [
            {
                "username": "13858181317", 
                "nickname": "AmiKara", 
                "msg_id": 7, 
                "status": false, 
                "add_time": 1583053260.0, 
                "title": "这是一条测试通知", 
                "content": "嗯？我就测试一下", 
                "type": "private", 
                "subtype": "default", 
                "extra": ""
            }
        ]
    }
}
```

> **Response Data Param**

|  Field   |  Type   |  **Description**   |
| :------: | :-----: | :----------------: |
| username | string  |       用户名       |
| nickname | string  |      用户昵称      |
|  msg_id  |   int   |   此消息的消息id   |
|   type   | string  |  消息类型，自定义  |
| subtype  | string  | 消息子类型，自定义 |
|  title   | string  |      消息标题      |
| content  | string  |      消息内容      |
| add_time |  float  |  站内信发送时间戳  |
|  status  | boolean |    消息已读状态    |
|  extra   | string  |  额外信息，自定义  |

> **Notice**

+ `list`列表已按照最后回复时间降序排序，最后回复包括用户发送给聊天对象的时间
+ **修改了list内部数据结构，新增与聊天对象的最后一条消息信息**

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -100, 
    "message": "Missing necessary args", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |        Message        |   Description    |
| :----: | :-------------------: | :--------------: |
|  100   | Get admin user failed | 获取系统用户失败 |

## Msg - sign

> **API Description**

`POST`

此API用于标记**站内信**为已读状态，不论系统站内信还是私聊站内信。

> **URL**

`https://guosai.zustmanong.cn/api/v2/msg/?token=`


> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"sign",
    "data":{
        "msg_id":1
    }
}
```

> **Data Param**

| Field  | Type | Length | Null | Default | **Description** |
| :----: | :--: | :----: | :--: | :-----: | :-------------: |
| msg_id | int  |        |      |         |     消息id      |

> **Notice**

+ 当`msg_id`数据类型错误或不存在时，返回`100`状态码

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {}
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -100, 
    "message": "Missing necessary args", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |   Message    | Description  |
| :----: | :----------: | :----------: |
|  100   | Error msg_id | 错误的消息id |

## Msg - sign_batch

> **API Description**

`POST`

此API用于批量标记**站内信**为已读状态，不论系统站内信还是私聊站内信。

> **URL**

`https://guosai.zustmanong.cn/api/v2/msg/?token=`


> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"sign_batch",
    "data":{
        "sys":0,
        "private":1,
        "people":"13750687010"
    }
}
```

> **Data Param**

|  Field  |  Type  | Length | Null | Default |                       **Description**                        |
| :-----: | :----: | :----: | :--: | :-----: | :----------------------------------------------------------: |
|   sys   |  int   |        |      |    √    |  是否标记系统消息为已读：`0`为不标记，`1`为标记，默认为`0`   |
| private |  int   |        |      |    √    |  是否标记私聊消息为已读：`0`为不标记，`1`为标记，默认为`0`   |
| people  | string |        |      |    √    | 聊天对象id，仅在`private`设置时有效，设置后将仅标记与该聊天对象的未读消息为已读消息；不设置或设置为空文本表示标记所有未读私聊信息。 |

> **Notice**

+ 当`sys`数据类型错误或不存在时，默认使用`0`
+ 当`private`数据类型错误或不存在时，默认使用`0`
+ 当`people`数据类型错误或不存在时，默认使用空文本
+ 当同时标记系统消息与私聊消息时，若在标记系统消息过程中出现错误，将直接返回错误信息，不执行私聊消息的标记。
+ 私聊消息的标记仅针对于自身为接收者的未读信息，自己为发送者且对方未读的消息不会被标记

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {}
}
```

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -100, 
    "message": "Missing necessary args", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |        Message         |      Description       |
| :----: | :--------------------: | :--------------------: |
|  100   | Get system user failed |    获取系统用户失败    |
|  101   |   Get sender Failed    | 获取私聊发送者对象失败 |

## Msg - filter

> **API Description**

`POST`

此API用于通过`msg_type`、`msg_subtype`和`if_new`值进行筛选**用户收到的所有站内信消息**，并自动**按发送时间降序排序**

通过此接口获取的私聊消息结构会非常混乱，不建议私聊消息使用此API

> **URL**

`https://guosai.zustmanong.cn/api/v2/msg/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"filter",
    "data":{
        "type": "system", 
        "subtype": "", 
        "if_new": 1
    }
}
```

> **Data Param**

|  Field  |  Type  | Length | Null | Default |                       **Description**                        |
| :-----: | :----: | :----: | :--: | :-----: | :----------------------------------------------------------: |
|  type   | string |        |      |         |                           消息类型                           |
| subtype | string |        |      |    √    |  消息子类型，不传递或者传递空文本表示筛选`type`下所有的消息  |
| if_new  |  int   |        |      |    √    | 消息过滤模式，可选值：`0`获取新消息;`1`获取已读消息;`2`获取全部消息。默认为`0` |

> **Notice**

+ `type`值不可为空，否则可能发生不可知错误（没测试过）
+ 当`if_new`数据类型错误或不存在时，默认使用`0`，自动判定为获取新消息
+ `type`与`subtype`、`if_new`三者为交集检索条件

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "num": 1, 
        "list": [
            {
                "msg_id": 1, 
                "type":"system",
                "subtype":"notice",
                "title": "这是一条测试通知", 
                "content": "嗯？我就测试一下", 
                "add_time": 1582964040.0, 
                "status": false,
                "extra":""
            }
        ]
    }
}
```

> **Response Data Param**

|  Field   |  Type   |          **Description**           |
| :------: | :-----: | :--------------------------------: |
|  msg_id  |   int   | 此消息的消息id，保留字段，暂无用处 |
|   type   | string  |              消息类型              |
| subtype  | string  |             消息子类型             |
|  title   | string  |              消息标题              |
| content  | string  |              消息内容              |
| add_time |  float  |          站内信发送时间戳          |
|  status  | boolean |            消息已读状态            |
|  extra   | string  |              额外信息              |

> **Notice**

+ 消息已读状态变更请用[Msg - sign](#Msg - sign)或者[Msg - sign_batch](#Msg - sign_batch)API
+ 不论是系统群发还是单独发送的站内信，全部规整到此api
+ 用此API获取的私聊消息返回结构非常混乱，不建议私聊消息使用此API

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -100, 
    "message": "Missing necessary args", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

**null**

## Msg - send

> **API Description**

`POST`

此API用于发送私聊站内信给指定用户

> **URL**

`https://guosai.zustmanong.cn/api/v2/msg/?token=`

> **URL Param**

| Field |  Type  | Length | Null | Default | **Description** |
| :---: | :----: | :----: | :--: | :-----: | :-------------: |
| token | string |   32   |      |         |    用户凭证     |

> **Request Json Text Example**

```python
{
    "id":1234,
    "type":"msg",
    "subtype":"send",
    "data":{
        "receiver": "13750687010", 
        "title": "回复", 
        "content": "你也好呀！"
    }
}
```

> **Data Param**

|  Field   |  Type  | Length | Null | Default |    **Description**     |
| :------: | :----: | :----: | :--: | :-----: | :--------------------: |
| receiver | string |   11   |      |         |      接收者用户名      |
|  title   | string |  100   |      |         | 消息标题，建议为空文本 |
| content  | string |        |      |         |        消息内容        |

> **Notice**

+ 在私聊中建议使用`content`字段传递聊天内容，`title`字段一般情况建议为空文本。
+ 保留`title`的原因是打算后期做成卡片式分享时用到。
+ **在私聊消息中，暂不支持自定义`type`、`subtype`和`extra`字段**
+ **默认的私聊消息`type`值为`private`，`subtype`值为`default`，`extra`为空文本**

> **Response Success Example**

```python
{
    "id": 0, 
    "status": 0, 
    "message": "Successful", 
    "data": {
        "msg_id": 5
    }
}
```

> **Response Data Param**

| Field  | Type |          **Description**           |
| :----: | :--: | :--------------------------------: |
| msg_id | int  | 此消息的消息id，保留字段，暂无用处 |

> **Notice**

+ 用户不存在返回`100`错误;消息正文创建失败返回`101`错误

> **Response Failed Example**

```python
{
    "id": 1234, 
    "status": -100, 
    "message": "Missing necessary args", 
    "data": {}
}
```

> **Used Global Status**

Please refer to [Global Status Table](#Global Status Table)

| Status |
| ------ |
| -101   |
| -100   |
| -3     |
| -2     |
| -1     |

> **Local Status**

| Status |          Message          |   Description    |
| :----: | :-----------------------: | :--------------: |
|  100   |      Error receiver       |   错误的接收者   |
|  101   | Create MessageText Failed | 创建消息内容失败 |

# Global Status Table

**所有的全局status值皆小于0**

**大于 0 的status值皆为请求局部status值**

| Status |              Message               |             Description             | Method    |
| :----: | :--------------------------------: | :---------------------------------: | --------- |
|   0    |             successful             |            函数处理正确             | POST、GET |
|   -1   |           Error JSON key           |         json文本必需key缺失         | POST      |
|   -2   |          Error JSON value          |          json文本value错误          | POST      |
|   -3   |           Error data key           |      data中有非预料中的key字段      | POST      |
|   -4   |             Error Hash             |          Hash校验文本错误           | POST      |
|  -100  |       Missing necessary args       |  api地址中缺少token或其他必需参数   | POST、GET |
|  -101  |            Error token             |             token不正确             | POST、GET |
|  -102  |  Get userid failed for the token   |       使用token获取userid失败       | POST、GET |
|  -103  |      No permission to operate      |            用户无权操作             | POST      |
|  -104  |       Error device_id token        |         错误的设备id token          | POST      |
|  -200  |    Failure to operate database     | 数据库操作失败，检查SQL语句是否正确 | POST、GET |
|  -201  | Necessary key-value can't be empty |        关键键值对值不可为空         | POST      |
|  -202  |  Missing necessary data key-value  |          缺少关键的键值对           | POST      |
|  -203  |       Arg's value type error       |         键值对数据类型错误          | POST      |
|  -204  |         Arg's value error          |           键值对数据错误            | POST      |
|  -404  |           Unknown Error            |           未知的Redis错误           | POST      |
|  -500  |          COS upload Error          |           COS储存上传失败           | POST      |
|  -600  |         Local upload Error         |            本地上传失败             | POST      |

