郑重声明：文中所涉及的技术、思路和工具仅供以安全为目的的学习交流使用，任何人不得将其用于非法用途以及盈利等目的，否则后果自行承担。



##### 0x01.介绍

    Escan是一款分析API功能端点、收集功能端点的混淆测试工具，在金融测试、运营商测试，常常面对大量index.js文件混淆，
    通过分析路由的封装函数、暴露的参数值来达到发现一些边缘未授权业务的目的。
    是一款为了发现边缘业务而收集的工具，熟练掌握Escan的测试思路能发现一些多参数校验，非auth模块鉴权的业务；能发现因参数混淆，
    无从下手参数e，到获取到e值的分析工具。
![Snipaste_2024-03-23_21-57-00](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_21-57-00.png)

![Snipaste_2024-03-23_20-41-03](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_20-41-03.png)

##### 0x02.实例

###### 业务环境

很多时候，业务涉及运营商系统、金融系统，常常面对大量index.js文件混淆的情况，同时系统有一套很完善的鉴权机制，因此，常常实难入手。

![Snipaste_2024-03-23_21-00-53](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_21-00-53.png)

```
$.ajaxSettings.beforeSend=function(t,e){var n=sessionStorage.getItem("token"),n=n?`bearer ${n}
```

一套特别好的逻辑鉴权判断，任何ajax请求通过getItem取值token，鉴权字段在后续调用。

但这是所有站点里，唯一的开发环境，因此不愿放掉这块好骨头

![Snipaste_2024-03-23_21-05-41](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_21-05-41.png)

大部分业务取值通过sessionStrage函数调用，因此测试路线是寻找边缘业务，业务调用不走sessionStrage函数

利用yitaiqifilter 来hook到一些js的API地址

![Snipaste_2024-03-23_21-10-04](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_21-10-04.png)

正常来说，到这里是很明显的缺参数值。

###### 处理混淆e值

来观察前端是如何封装getChatUrl函数的?

![Snipaste_2024-03-23_21-14-48](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_21-14-48.png)

```
,_getChatUrlAjax:function(e){return this.$axios.get(this.BASE_URL+"/XXX/complaintsupervision/v1/chat/getChatUrl",{params:e})}
```

传递的是参数e, 做了混淆，那么如何来获取e的值呢?

我这里测试发现，封装函数:getChatUrlAjax、_closeMeetingAjax都在

/complaintsupervision/v1/chat/ 路径下。说明他们都是同套组件业务，

可以通过_closeMeetingAjax暴露的参数值取批量喷洒同路径的封装函数

###### Escan提取暴露参数值

这里通过Escan提取相关暴露参数值

![Snipaste_2024-03-23_21-21-55](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_21-21-55.png)

['?fileId=', '?governDesignAttachmentId=', '?userId=', '?status=', '?cutId=', '?riskStreamId=', '?mobile=', '?cityCode=', '?meetingId=', '?orgName=', '?', '?file=', '?queryKey=']

![Snipaste_2024-03-23_21-23-44](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_21-23-44.png)

批量喷洒，成功拿到混淆e参数的值

同时，根据这点，相比大家都已经明白了，在混淆的情况下，同路径下的封装函数可以批量喷洒。

通过yitaiqifilter，发现一处和业务无直接关联的端点，不能查询但没鉴权很鸡肋

![Snipaste_2024-03-23_21-27-32](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_21-27-32.png)

观察到/XX/commoncomponent/query/存放了系统label选取相关信息的一些组件接口信息

###### Escan提取API功能端点

通过Escan提取系统包含query的端点

![Snipaste_2024-03-23_21-31-03](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_21-31-03.png)



喷洒出一处queryCityByProvinceForRedisKey(e)

![Snipaste_2024-03-23_21-33-16](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_21-33-16.png)

所以Escan的核心功能就是根据业务设计的。

通过封装函数->定级到API路径下提炼->端点喷洒

通过封装函数->暴露的参数值->参数值喷洒

###### Escan整合结果

由于开发的时候是同套思路开发站点，因此，批量测试存储的API端点后续测试同端口、开发环境会很具有针对性，有效更高。

通过Escan整合批量测试结果

![Snipaste_2024-03-23_20-51-50](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_20-51-50-1711201059830.png)



##### 0x03.效果展示

###### 封装函数的提取、暴露的参数值提取

![Snipaste_2024-03-23_20-43-39](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_20-43-39.png)

每次批量逻辑提取都会在dict目录生成对应提取GET端点的时间线文件

![Snipaste_2024-03-23_20-44-41](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_20-44-41.png)

###### 整合dict目录全部Get_parmaters

![Snipaste_2024-03-23_20-51-50](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_20-51-50.png)

![Snipaste_2024-03-23_20-52-16](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_20-52-16.png)

###### Escan环境配置；

复制yitaiqifilter_API文档到File目录下，运行指定文件或目录即可

![Snipaste_2024-03-23_21-42-18](D:/MD%E5%9B%BE%E5%83%8F%E6%9D%90%E6%96%99/Snipaste_2024-03-23_21-42-18.png)

