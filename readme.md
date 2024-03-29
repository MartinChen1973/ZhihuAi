# 项目说明
1. 此项目以《知乎Ai大模型课程》讲授内容为骨架，包括课上内容及扩展内的练习代码。
2. 为适应本地运行、避免版权问题、紧跟框架更新，多数练习都与课程原练习内容有所不同。
3. 在此基础上，本项目会不断扩充全新案例的演示，预计2024年第一季度的更新频率为每周3~5个练习内容（以单个文件计算）。

# 练习命名与素材存放
1. 所有练习均以Cnnnnnnn_练习领域_练习名称_增强内容.py命名。
2. 若一个练习文件中用到另外一个文件，请在此练习文件头中查看 from ... import ...
   比如：from SemanticKernel.NativeFunctions.CommandVerifier import NormalCommandVerifier, NativeCommandVerifier 表明从./SemanticKernel/NativeFunctions/CommandVerifier.py中，引用了两个类：NormalCommandVerifier, NativeCommandVerifier

# 常见问题
以下问题按英文错误字母顺序排序。
## UnicodeDecodeError: 'gbk' codec can't decode byte 0xaa in position 82: illegal multibyte sequence
发生：此问题发生在对本地中文文件读取的过程中，如Semantic Kernel的kernel.import_semantic_skill_from_directory方法。

原因：一般文件的中文编码缺省为utf-8，而系统却使用gbk进行解码。注意当使用Python3.X时，缺省的编解码都是使用utf-8的，因此无需在代码中指定encoding方法。

解决：在windows环境中发生此问题，需要在本地设置环境PYTHONUTF8=1

方法1：在PowerShell中运行$env:PYTHONUTF8=1，重启电脑。

方法2：在windows10+右下角的搜索框搜索“环境变量”或“environment”，找到后在个人或系统中，添加环境变量PYTHONUTF8，取值为1。