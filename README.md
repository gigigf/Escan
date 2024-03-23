# Escan
Escan 一款分析API功能端点、收集功能端点的混淆测试工具
郑重声明：文中所涉及的技术、思路和工具仅供以安全为目的的学习交流使用，任何人不得将其用于非法用途以及盈利等目的，否则后果自行承担。



##### 0x01.介绍

    Escan是一款分析API功能端点、收集功能端点的混淆测试工具，在金融测试、运营商测试，常常面对大量index.js文件混淆，
    通过分析路由的封装函数、暴露的参数值来达到发现一些边缘未授权业务的目的。
    是一款为了发现边缘业务而收集的工具，熟练掌握Escan的测试思路能发现一些多参数校验，非auth模块鉴权的业务；能发现因参数混淆，
    无从下手参数e，到获取到e值的分析工具。

![Snipaste_2024-03-23_21-57-00](https://github.com/gigigf/Escan/assets/62227278/88b7579b-0c12-4152-a7b2-ceb322550fd4)
![Snipaste_2024-03-23_20-41-03](https://github.com/gigigf/Escan/assets/62227278/de7adca3-7edd-4895-b95e-32f114a8d40c)



##### 0x02.实例

###### 业务环境

很多时候，业务涉及运营商系统、金融系统，常常面对大量index.js文件混淆的情况，同时系统有一套很完善的鉴权机制，因此，常常实难入手。

![Snipaste_2024-03-23_21-00-53](https://github.com/gigigf/Escan/assets/62227278/856c2588-0a32-4485-909a-6d0c31037ad7)


```
$.ajaxSettings.beforeSend=function(t,e){var n=sessionStorage.getItem("token"),n=n?`bearer ${n}
```

一套特别好的逻辑鉴权判断，任何ajax请求通过getItem取值token，鉴权字段在后续调用。

但这是所有站点里，唯一的开发环境，因此不愿放掉这块好骨头

![Snipaste_2024-03-23_21-05-41](https://github.com/gigigf/Escan/assets/62227278/c5ecd987-2906-4fe0-b84f-068cf5eac4a3)


大部分业务取值通过sessionStrage函数调用，因此测试路线是寻找边缘业务，业务调用不走sessionStrage函数

利用yitaiqifilter 来hook到一些js的API地址

![Snipaste_2024-03-23_21-10-04](https://github.com/gigigf/Escan/assets/62227278/2f69a262-5c2e-47e6-ae9b-2cdf6016ed92)


正常来说，到这里是很明显的缺参数值。

###### 处理混淆e值

来观察前端是如何封装getChatUrl函数的?

![Snipaste_2024-03-23_21-14-48](https://github.com/gigigf/Escan/assets/62227278/65539075-d75e-494a-892a-36949343d7f5)


```
,_getChatUrlAjax:function(e){return this.$axios.get(this.BASE_URL+"/XXX/complaintsupervision/v1/chat/getChatUrl",{params:e})}
```

传递的是参数e, 做了混淆，那么如何来获取e的值呢?

我这里测试发现，封装函数:getChatUrlAjax、_closeMeetingAjax都在

/complaintsupervision/v1/chat/ 路径下。说明他们都是同套组件业务，

可以通过_closeMeetingAjax暴露的参数值取批量喷洒同路径的封装函数

###### Escan提取暴露参数值

这里通过Escan提取相关暴露参数值

![Snipaste_2024-03-23_21-21-55](https://github.com/gigigf/Escan/assets/62227278/b20ae0ae-b7e4-42b7-841f-b2feef346030)


['?fileId=', '?governDesignAttachmentId=', '?userId=', '?status=', '?cutId=', '?riskStreamId=', '?mobile=', '?cityCode=', '?meetingId=', '?orgName=', '?', '?file=', '?queryKey=']

![Snipaste_2024-03-23_21-23-44](https://github.com/gigigf/Escan/assets/62227278/9b228e74-a26b-466e-9c33-fb5d99c6570f)


批量喷洒，成功拿到混淆e参数的值

同时，根据这点，相比大家都已经明白了，在混淆的情况下，同路径下的封装函数可以批量喷洒。

通过yitaiqifilter，发现一处和业务无直接关联的端点，不能查询但没鉴权很鸡肋

![Snipaste_2024-03-23_21-27-32](https://github.com/gigigf/Escan/assets/62227278/40f1f9f5-5951-4da7-a3e1-34f1031feb4b)


观察到/XX/commoncomponent/query/存放了系统label选取相关信息的一些组件接口信息

###### Escan提取API功能端点

通过Escan提取系统包含query的端点

![Snipaste_2024-03-23_21-31-03](https://github.com/gigigf/Escan/assets/62227278/25957f51-3b65-4c9d-82a5-04e02525c44f)




喷洒出一处queryCityByProvinceForRedisKey(e)

![Snipaste_2024-03-23_21-33-16](https://github.com/gigigf/Escan/assets/62227278/4141d75e-8e38-4c88-950a-9dd387204a65)


所以Escan的核心功能就是根据业务设计的。

通过封装函数->定级到API路径下提炼->端点喷洒

通过封装函数->暴露的参数值->参数值喷洒

###### Escan整合结果

由于开发的时候是同套思路开发站点，因此，批量测试存储的API端点后续测试同端口、开发环境会很具有针对性，有效更高。

通过Escan整合批量测试结果

![Snipaste_2024-03-23_20-51-50](https://github.com/gigigf/Escan/assets/62227278/50adbe5f-a907-4216-a740-c37636e83326)




##### 0x03.效果展示

###### 封装函数的提取、暴露的参数值提取

![Snipaste_2024-03-23_20-43-39](https://github.com/gigigf/Escan/assets/62227278/db9e6cad-2c6e-4a22-b6a9-93dfe878731b)


每次批量逻辑提取都会在dict目录生成对应提取GET端点的时间线文件

![Snipaste_2024-03-23_20-44-41](https://github.com/gigigf/Escan/assets/62227278/a4c24929-4326-45e8-a23d-5cbb60db415a)


###### 整合dict目录全部Get_parmaters


![Snipaste_2024-03-23_20-51-50](https://github.com/gigigf/Escan/assets/62227278/28bc0342-72be-4356-b3bc-0861ca419be5)

![Snipaste_2024-03-23_20-52-16](https://github.com/gigigf/Escan/assets/62227278/f85b47bd-34a9-453b-b431-bf96d6fd8d61)


###### Escan环境配置；

复制yitaiqifilter_API文档到File目录下，运行指定文件或目录即可

![Snipaste_2024-03-23_21-42-18](https://github.com/gigigf/Escan/assets/62227278/c3e6f185-1ca0-4aa5-9382-7af4435d998e)


