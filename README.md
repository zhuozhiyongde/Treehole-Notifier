# Treehole Notifier

Inspired by my INSANE ICS REFRESHER friend.

## Process

1. 运行 `TreeholeSpider.py` 以爬取树洞。
2. 检运行查结果和已有结果的差异。
3. 将更新结果存储到 JSON 文件中。
4. 通过 Github Actions 来定时执行上述流程
5. 结果有更新时（此时自动触发了 git push），通过 Github Mobile 发送通知。

## Usage

### 配置 JSON 文件

请参考 `*_example.json` 文件对对应的 `json` 文件进行配置，以下对参数做说明：

**watch_list.json**

```js
// watch_list_example.json
{
    "watch_list": [ // 监测树洞列表
        {
            "tid": 1948761, // 监测树洞的id
            "nick": "advanced_math", // 监测树洞的自定义昵称，可选
            "last_update": 0 // 记录该树洞所有回复中的最新时间戳
        }
    ]
}
```



**watch_keywords.json**

```js
// watch_keywords_sample.json
{
    "watch_keywords": [ // 监测关键词列表
        { // 每个对象即为一个监测
            "keyword": "ICS", // 监测关键词
            "ignore_pattern": false, // 是否使用正则表达式过滤输出结果，可选
            "last_hole": 4642133 // 记录的该关键词最后更新的树洞
        }
    ]
}
```

说明：我内置实现了对于关键词的重新过滤，即对关键词搜搜结果进行了又一次的查找以解决并集问题。



### 配置账号、密码

