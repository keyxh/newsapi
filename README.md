# newsapi
python模仿2023年全国职业的移动应用开发赛项样式开发的开源的新闻api，以及安卓接入案例代码 
<P>
<br>**1.环境配置:** 
<p>(1).python环境
<br>pip install flask
<br>pip install gevent
<br>pip install pyjwt</p>
<p>(2).程序配置
<br>默认api接口地址为:127.0.0.1:39999
<br>默认文件接口地址为:127.0.0.1:5000
<br>可以通过编辑文件路径:libs/ServerUtils.py进行修改
</p>

<br>**2.api介绍:** 
<p>此app前后端完全开源，前端采用java android编写，后端使用python httpserver+flask框架处理http请求，代码量前后端合计约5k，较轻量。使用jwt进行动态授权token，需要获取用户，例如点赞、评论均需要传token获取用户大部分数据存入sqlite数据库，部分数据例如公告以文件方式存储，便于修改。
<br>1.详细api文档可以参考<a href="https://blog.csdn.net/m0_60277871/article/details/132381794?spm=1001.2014.3001.5501">点击我</a>
<br>2.api运行文档:运行server.bat，发现三个py文件都跑起来，说明运行成功
<br>3.基于flask实现的http请求在fileupdata.py这个文件，禁止访问的文件路径已经写死在代码里，往数组里加即可
</p>

<br>**3.接入案例介绍:**
<p>上传的源码提供了安卓java的接入的案例，几乎接入了所有api,提供了原生安卓的上传功能、类似抖音的短视频实现、列表和block的切换案例等等,demo的apk版本可以前往<a href="http://222.187.232.63:39999">http://222.187.232.63:39999</a>,下载体验。</p>










