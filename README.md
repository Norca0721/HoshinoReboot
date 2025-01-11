## Hoshino Reboot
基于 [HoshinoBotv2](https://github.com/Ice9Coffee/HoshinoBot) 的用于快速重启bot的插件

### 注意事项
```
该项目在 windows 环境下编写与运行
linux 环境请翻到查看最底下的项目
```

### 使用前置
```bash
pip install -r requirements.txt
```

### 环境需求
```
python 3.9+
```

### 使用说明
```
在 hoshino/config/__bot__.py 中添加本项目文件名
在群里或私信向 bot 发送 [开启 HoshinoReboot] 启用插件

开启 HoshinoReboot      ：启用插件
/sudo reboot            ：重启bot
/sudo check             ：查看bot存活情况

重启成功之后会在群聊中发送 [bot名 启动成功]
```

### Linux 相关
- **请前往此仓库 -> [Git-Manage](https://github.com/KBVsent/Git-Manage)**

| Nickname         | Contribution      |
| ---------------- | ----------------- |
| [HoshinoReboot](https://github.com/Norca0721/HoshinoReboot) | 提供的重启相关功能 |