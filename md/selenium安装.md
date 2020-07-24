# selenium安装

[selenium下载](https://www.selenium.dev/)

搭建 `Selenium` 库 加`ChromeDriver` 爬虫环境。

## 安装elenium

```
# pip3安装
pip3 install selenium

# 查看selenium安装的版本
pip3 list selenium
```
我已经安装过`appium`，是已经安装了`selenium`的，所有安装时提示：
```
pip3 install selenium
Requirement already satisfied: selenium in /usr/local/lib/python3.7/site-packages (3.141.0)
Requirement already satisfied: urllib3 in /usr/local/lib/python3.7/site-packages (from selenium) (1.22)
```

## 安装ChromeDriver

1. 查看`chrome`的版本：

`chrome`打开时点击左上角`Chrome`,再点击`关于 Chrome`,即可查看到版本`版本 83.0.4103.116（正式版本） （64 位）`。

2. 下载

[官网](http://chromedriver.chromium.org/)下载与`chrome`对应的版本。
也可以选择从[淘宝镜像](http://npm.taobao.org/mirrors/chromedriver/)下载对应的安装包。

下载完成后将安装包加入到环境变量。`mac`系统将`chromedriver`移至`/usr/bin`目录下即可
```
sudo mv ~/Downloads/chromedriver /usr/bin
```

3. 验证

终端输入：
```
chromedriver
```
测试调用`chrome`：
```
ipython
Python 3.7.0 (default, Aug 22 2018, 15:22:33)
Type 'copyright', 'credits' or 'license' for more information
IPython 6.5.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: from selenium import webdriver

In [2]: browser = webdriver.Chrome()

In [3]:
```
如果能调用chrome浏览器，即表示安装成功

## 遇见的问题

### 无法将`chromedriver`移动到环境变量

执行`sudo mv ~/Downloads/chromedriver /usr/bin`时，提示：
```
sudo mv ~/Downloads/chromedriver /usr/bin
mv: rename /Users/yunxi/Downloads/chromedriver to /usr/bin/chromedriver: Operation not permitted
```
原因是因为系统有一个 `System Integrity Protection (SIP)` 系统完整性保护，如果此功能不关闭，是无法移动到 `/usr/bin` 目录下的。

检查当前SIP的开启状况，输入如下命令：
```
csrutil status
```
返回命令为：System Integrity Protection status: enabled.，则SIP为开启状态
返回命令为：System Integrity Protection status: disabled.，则SIP为关闭状态

解决办法是：

1. 电脑关机，然后在开机时按住 `command + R` 键，直到出现苹果 `logo` 和进度条时松开，进入OS X恢复模式。
2. 进入恢复模式后打开【实用工具】——【终端】
3. 在终端输入命令`csrutil disable`，然后关闭终端。（如果要重新开启，同样的方法输入`csrutil enable`）
4. 重启电脑即可。