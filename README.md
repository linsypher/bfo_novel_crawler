# 一般网站文本抓取

适用于防爬策略不强的站点。

- 环境：
>	* Python: 2.7
>	* Python lib:  
		Scrapy 1.7.3  
		``` 
		~/venv/bin/pip install Scrapy
		```

- 启动：
>	* scrapy crawl spider  
	``` 
	~/venv/bin/scrapy crawl xybook --nolog
	```

- 调试：
>	* ~/venv/bin/scrapy shell url  
	``` 
	~/venv/bin/scrapy shell 'https://www.9awx.com/xuanhuanxiaoshuo/'
	```

- 目录结构
> 
	```
	▾ bfo_novel_crawler/	// 主目录
		▾ spiders/			// 爬虫目录
			__init__.py
			jawx.py			// www.9awx.com 站点爬虫
			qb5.py
			shuhai.py
			xxsy.py
			xybook.py			// www.xingyueboke.com 站点爬虫
		__init__.py
		items.py				// 抓取数据结构
		middlewares.py		// 中间件，预处理页面数据
		pipelines.py			// 管道，页面数据后处理
		settings.py			// 配置文件，调控爬虫、管道、中间件等相关组件
	```

- 其他
> 	* 抓取流程中的数据流向  
		- spider.start_urls -> 中间件（若配置） -> spider.parse -> 管道（若配置）  
>	* 页面解析： 
		- 参考[语法](https://www.w3school.com.cn/xpath/xpath_syntax.asp)  
>	* scrapy用法：
		- 参考[语法](http://www.scrapyd.cn/doc/144.html)  


		注意：
		1. 一般防爬策略不严格的站点，中间件不需要开启；
		2. 可通过调试命令，检测爬虫逻辑，验证是否抓取到数据；
		3. 针对强制登录、页面手动触发等防爬策略，需要通过中间件借助虚拟浏览器插件(selenium)来模拟登陆、点击按钮等操作；
		4. 其他防爬策略需要具体问题具体解决。


