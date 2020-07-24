# selenium使用

## 基础

### requirements基本使用

`requirements`作用描述：

很多 `Python` 项目中经常会包含一个 `requirements.txt` 文件，里面内容是项目的依赖包及其对应版本号的信息列表，
即项目依赖关系清单，其作用是用来重新构建项目所需要的运行环境依赖，
比如你从 `GitHub` 上 `clone` 了一个 `Python` 项目，
通常你会先找到 `requirements.txt` 文件，然后运行命令 `pip install -r requirements.txt` 来安装该项目所依赖的包。
同样，你也可以在你的项目目录下运行命令 `pip freeze > requirements.txt` 来生成 `requirements.txt` 文件，以便他人重新安装项目所依赖的包。


文件生成：
```
pip freeze > requirements.txt
pip3 freeze > requirements.txt
```
包安装
```
pip install -r requirements.txt
pip3 install -r requirements.txt
```
### ChromeDriver路径

安装时的位置：
```
/usr/local/bin/chromedriver
```

### 查看chrome安装位置

打开`chrome`在地址栏输入`chrome://version/`即可看到相关信息：
```txt
Google Chrome	84.0.4147.89 (正式版本) （64 位）
修订版本	19abfe7bcba9318a0b2a6bc6634a67fc834aa592-refs/branch-heads/4147@{#852}
操作系统	macOS 版本10.15.4（版号19E287）
JavaScript	V8 8.4.371.19
Flash	32.0.0.403 /Users/yunxi/Library/Application Support/Google/Chrome/PepperFlash/32.0.0.403/PepperFlashPlayer.plugin
用户代理	Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36
命令行	/Applications/Google Chrome.app/Contents/MacOS/Google Chrome --flag-switches-begin --flag-switches-end --enable-audio-service-sandbox
可执行文件路径	/Applications/Google Chrome.app/Contents/MacOS/Google Chrome
个人资料路径	/Users/yunxi/Library/Application Support/Google/Chrome/Default
```

## selenium定位

1. driver.find_element_by_id('su')

   定位到元素的id一般id是唯一的，可以精确定位到元素

2. driver.find_element_by_name()

   通过元素的name来定位元素

3. driver.find_element_by_class_name()

  通过元素的class属性来定位

4. driver.find_element_by_link_text()

  通过链接的文本来定位元素

5.driver.find_element_by_partial_link_text()

  通过链接的部分文本来定位元素

6. driver.find_element_by_tag_name()

  通过标签名来定位元素，比如链接的标签<a></a>

7. driver.find_element_by_xpath

  通过xpath来定位元素，比较万能的定位方式

8. driver.find_element_by_css_selector()

 通过css选择器来定位元素

可以将定位到的元素赋值给一个变量，然后对元素做一些操作