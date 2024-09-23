# Run the project

## Installing scrapy

## Seeting up programs for getting usable proxies. Set up according instructions here:

https://github.com/jhao104/proxy_pool/tree/release-2.4.0

## Start the project

Go to alibaba folder, run

```
pip install -r requirements.txt
```

Go to alibaba folder, run

```
scrapy crawl manufacture_group_1
```

## How it works

All manufactures are divided into 3 groups and are expected to run as 3 spiders at the same time. All categories are data_group_1, data_group_2, data_group_3. In each category, we name the manufacture categories as the directory name, and csv file inside stores all manufactures in that categories with names and link, the program will read all the names and links when scraping.

Switching UA and proxy functions are rewritten in middware.py in the same directory level of spider directory.

## Important

Currently, manufacture_group_1 is under developing, while manufacture_group_2, manufacture_group_3 are still in old version. Once manufacture_group_1 is ready, copy and paste it and just changed corresponding spider name and directory at the class definition and they'll work.

The problem now is switching UA and proxy seemingly doesn't work.

## Commonly used command

### Virtual Environment

python3 -m venv myenv
source myenv/bin/activate

### Example manufacture

## Main page URL

https://textileframe.en.alibaba.com/factory.html?wx_navbar_transparent=true&productId=60708538690

## Getting pictures - Product list URL

https://textileframe.en.alibaba.com/productlist.html

## Getting main text data - Manufacture profile URL

https://www.alibaba.com/factory/index.html?spm=a2700.product_home_l0.home-tab.manufacturers

## Getting all manufactures - Manufacture example category URL (Power Transmission)

https://www.alibaba.com/factory/Power-Transmission_p201723202?spm=a2700.factory_home.category_nav.category_popup

## Captcha:

https://xmksyl.en.alibaba.com//factory.html/_____tmd_____/punish?x5secdata=xcn95togwpYx5ObT5jF5xyrUf5SRxZnULTdH7AqEyb%2fQxfqpEWRXoFThgB%2fZ95wyg2%2fbfV%2flIeeVh0fXgXLXu%2fypTSVcLn9vJnTTtvkP%2b04FJP8JkFITpAxFJUIEqdWyXZ5ojuSHF0wd2KuiMqj8PaIlOGAO6AtmWJUfWkEX72rtEJZZkhSsda7YxBqls7%2fltn8r%2fEw9yM2zlKuMQ7FpGtTw%3d%3d__bx__xmksyl.en.alibaba.com%2ffactory.html&x5step=1

## Redis common commands

brew services start redis

brew services info redis

brew services stop redis

## An Error like this, then, pkill chromedriver

selenium.common.exceptions.WebDriverException: Message: Service /Users/liuqiming/.wdm/drivers/chromedriver/mac64/128.0.6613.137/chromedriver-mac-arm64/chromedriver unexpectedly exited. Status code was: -9

## Useful Blogs

UA-switching
https://blog.csdn.net/SoraAkalin/article/details/104469189

Proxy-switching program setup
https://blog.csdn.net/weixin_41586246/article/details/126856234?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-1-126856234-blog-135285921.235%5Ev43%5Epc_blog_bottom_relevance_base1&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-1-126856234-blog-135285921.235%5Ev43%5Epc_blog_bottom_relevance_base1&utm_relevant_index=2
