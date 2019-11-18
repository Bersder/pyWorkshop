## 网易云接口
三个定值参数
- 010001
- 00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7
- 0CoJUm6Qyw8W8jud

**所有`csrf_token`都是非必需参数,置空字符串/舍弃即可**
### 登录接口
`ncm_login`
```javascript
api = 'https://music.163.com/weapi/login/cellphone?csrf_token=';
raw = {
    password: "md5(pwd)", //md5(pwd)
    phone: "13823468874",
    rememberLogin: true
}
```

### 歌词获取（包括翻译）
`get_lyric`
```javascript
api = 'https://music.163.com/weapi/song/lyric?csrf_token=';
raw = {
	id:'song id',//歌曲id
	lv:-1,
	tv:-1,
	csrf_token:''
}
```

### 歌曲详情获取
`get_song_detail`
```javascript
api = 'https://music.163.com/weapi/v3/song/detail';
raw = {
    c:[{id:111}],//{id:id}的集合
    ids:[111]//对应id的集合
}
```

### 歌曲源获取
`get_song_url`
```javascript
api = 'https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token=';
raw = {
    ids:'id list',//歌曲id列表
    level:'standard',//or higher、exhigh
    encodeType:'acc',//or mp3
    csrf_token:''
}
```

### 歌曲评论获取
`get_song_comment`
```javascript
api = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{song_id}?csrf_token=';
raw = {
    rid:'R_SO_4_{song_id}',//非必需
    offset:0,//偏移值 (page-1)*20
    total:true,//第一页是"true",其余页数是"false"
    limit:20,//评论数
    csrf_token:''
}
```

### 歌单详情获取
`waiting`
```javascript
api = 'https://music.163.com/weapi/v3/playlist/detail?csrf_token=';
raw = {
    csrf_token: "",
    id: "playlist_id",//歌单id
    limit: "1000",
    n: "1000",
    offset: "0",
    total: true
}
```

### 歌单评论获取
`waiting`
```javascript
api = 'https://music.163.com/weapi/v1/resource/comments/A_PL_0_3020182385?csrf_token=';
raw = {
    //同歌曲评论
    csrf_token: "",
    limit: "",
    offset: "",
    rid: "A_PL_0_{playlist_id}",
    total: ""
}
```

### 用户个人歌单/收藏歌单信息
`waiting`
```javascript
api = 'https://music.163.com/weapi/user/playlist?csrf_token=';
raw = {
    uid:'user id',
    wordwrap:7,
    offset:0,// (page-1)*limit - 1
    total:true,// 第一页是"true",其余页数是"false"
    limit:36,
    csrf_token:''
}
```

### 用户听歌排行
`get_user_listen_rank`
```javascript
api = 'https://music.163.com/weapi/v1/play/record?csrf_token=';
raw = {
    uid:'user id',
    type:1,//1是一周内，0是所有时间
    limit:1000,
    offset:0,
    total:true,
    csrf_token:''
}
```

### 搜索推荐
`waiting`
```javascript
api = 'https://music.163.com/weapi/search/suggest/web?csrf_token=';
raw = {
    csrf_token: "",
    limit: "8",
    s: "新",//搜索关键词
}
```

### 搜索
`waiting`
```javascript
api = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token=';
raw = {
    csrf_token: "",
    hlposttag: "</span>",
    hlpretag: "<span class=\"s-fc7\">",
    limit: "30",
    offset: "0", // (pn-1) * limit
    s: "天空花之都", //搜索关键词
    total: "true", //第一页true,其他false
    type: "1" //1 歌曲,100 歌手,10 专辑,1014 视频,1006 歌词,1000 歌单,1009 主播电台,1002 用户
}
```