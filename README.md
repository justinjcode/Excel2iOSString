


<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->

<a name="readme-top"></a>

<!--

*** Thanks for checking out the Best-README-Template. If you have a suggestion

*** that would make this better, please fork the repo and create a pull request

*** or simply open an issue with the tag "enhancement".

*** Don't forget to give the project a star!

*** Thanks again! Now go create something AMAZING! :D

-->

<!-- PROJECT SHIELDS -->

<!--

*** I'm using markdown "reference style" links for readability.

*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).

*** See the bottom of this document for the declaration of the reference variables

*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.

*** https://www.markdownguide.org/basic-syntax/#reference-style-links

-->

  

<h1 align="center">Excel2iOSString</h1>

<br />

<p>
python3 script for converting excel into iOS/Android localization files  

<p>
python3脚本，用于将excel转成iOS/安卓本地化文件

<br />

  

<!-- ABOUT THE PROJECT -->

## About The Project

This project is modified based on CatchZeng's project Localizable.strings2Excel.
Since CatchZeng's project uses python2 and only supports the xls format (this format is outdated), it is not suitable for me to use, so I made some changes, including some logic of generating files, and the referenced libraries are different.
~~In addition, this project currently only supports the conversion of excel to iOS files, and other types of conversion are not currently used, so they are not added.~~
Both iOS and Android are supported now.

本项目是基于CatchZeng的项目Localizable.strings2Excel修改的。
由于CatchZeng的项目是用python2，并且只支持xls格式（该格式已经过时了），我用起来不合适，于是做了些改动，包括一些生成文件的逻辑，以及引用的库都有所不同。
另外本项目目前~~仅支持将excel转成iOS文件，其它类型的转换目前没用到所以没加。~~ 已支持iOS和安卓
  

<!-- GETTING STARTED -->

## Getting Started
<p>
Make sure you have python3 installed on your Mac before using
<p>
使用之前，请确保您的Mac上安装了python3

### Prerequisites
<p>
Installed python dependency library
<p>
安装的python依赖库

* openpyxl

```sh

pip3 install openpyxl

```

  

### Usage

1. <p>Terminal cd to the project
	<p>在终端进入到项目的目录

```sh
//replace with your own directory
//替换成你自己的目录

cd /Users/xxx/Documents/Excel2iOSString
```

2. <p>run
	<p>执行脚本
<p>excel to iOS
	
```sh

python3 Xls2Strings.py -f input -t output

```

<p>excel to Android
	
```sh

python3 Xls2Xml.py -f input -t output

```

### Excel format
<p>
Generally, an iOS project requires a Localizable.strings file and an InfoPlist.strings file. They correspond to a sheet in excel, and the title of the sheet is the file name.
The first column is the key of the entry, and each subsequent column represents a language.
<p>
一般来说，一个iOS工程需要一个Localizable.strings文件，以及一个InfoPlist.strings文件。它们在excel对应一个sheet，sheet的标题就是文件名。
第一列是词条的key，后面每一列表示一种语言。
<br />

[![Excel format][table-screenshot]](https://example.com)

<p>
results:
<p>
生成结果：
<br />

  [![Results][results-screenshot]](https://example.com)

<!-- LICENSE -->

## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<!-- CONTACT -->

## Contact

justin 
justinjcode@163.com

  

Project Link: [https://github.com/justinjcode/Excel2iOSString](https://github.com/justinjcode/Excel2iOSString)

<!-- MARKDOWN LINKS & IMAGES -->

<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->

[table-screenshot]: screenshots/table.png
[results-screenshot]: screenshots/results.png
