# ripgrep-gui



一个用python开发的ripgrep图形化界面工具，用于快速运行和管理 `ripgrep`命令。用户可以方便地在文件系统中选择文件或目录，并通过自定义搜索条件执行 `ripgrep` 搜索命令，支持实时显示搜索结果。非常适合搜索几十G的大型txt，csv，sql等文本文件。

![1.png](https://github.com/di-ao/ripgrep-gui/blob/main/img/1.png)

## 功能

- 灵活的文件/目录路径选择
- 自定义搜索条件
- 实时输出搜索内容

## 使用方法

> **python**：本工具使用python 3.9开发，需要安装python环境。
>
> **Ripgrep**：本工具依赖rg，确保已在系统中安装并能够正常运行。https://github.com/BurntSushi/ripgrep

### 配置config.ini文件

把path的路径更改为你存放Ripgrep的**绝对路径**。

```
[rgpath]
path = G:\rg.exe
```

### 条件搜索

关于rg命令可以查看官方手册这里不过多赘述，搜索查询的目录/文件和命令在**查询输出框**内有显示。

- **条件1**：rg最常用的两个搜索参数-e和-w。输入框输入命令点击搜索即可。

  ```
  -e 1303 -e 1344 -w 1231
  1303 1344 -w 1231
  ```

  ![2.png](https://github.com/di-ao/ripgrep-gui/blob/main/img/2.png)

- **条件1+条件2**：将条件1查询到的内容丢给条件2，根据条件2的关键字再筛选一遍最后输出内容，本质上是利用管道符 “|”，条件不够可继续往条件2添加管道符+关键字即可。

  ```
  命令长这样子，案例可见图1
  rg.exe 1234 test.txt | rg.exe 4444 | rg.exe 232
  ```

- **编码**：内置两个常用的gbk和utf8，空白表示不使用，不合适的可以自行修改。
- **可选参数**：列出了一些常用的，如果没有你要使用的参数可自行在搜索条件上添加。

