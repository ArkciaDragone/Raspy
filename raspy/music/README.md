# Music Lab - alpha v0.1.9

欢迎测试Alpha版Music Lab！

开始的方式很简单：点击运行startMidi.py即可，不过您需要事先安装statistics、numpy、mido、pprint四个package。

程序会首先要求您输入midi文件的路径，详细输入方法请参考程序指示。建议您把需要添加的midi文件直接放在桌面，这样您只需输入“-/Users/*your-name*/Desktop/*your-file*.mid”即可。请注意，需要在路径前面添加“-”，不然Minecraft会因为路径最前面是“/”而认定其为游戏内部指令，从而影响程序进程。

midi文件处理成功之后，需要您输入您（或者别人）的游戏昵称，以便红石系统添加到对应玩家的身旁。

程序目前暂不支持：
 - 声部数过多的midi文件（建议midi的每个时刻不要超过15个音符）
 - 玩家速度控制

欢迎您在本界面进行漏洞反馈，我们会尽力修复它们！