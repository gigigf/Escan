"""def Escan_logo():
    logo = r'''
        #####                             
        #                                 
        #                ###          ###        ###           #   ##            +-------------------------------+
        #####      #             #       #             #        ##       #        +  Version: 1.0                            +
        #                 ###      #                ####        #         #        +  Author: Echo Vx:xzxxzx552   +
        #                        #    #       #    #       #        #         #        +--------------------------------
        #####        ###          ###        ####        #         #
'''
    return logo
"""


def logo():
    logo = r'''
 #####                             
 #                                 
 #       ###    ###    ###   # ##         +---------------------------+
 ####   #      #   #      #  ##  #        + Version: 1.0              +
 #       ###   #       ####  #   #        + Author: Echo Vx:xzxxzx552 +
 #          #  #   #  #   #  #   #        +---------------------------+
 #####  ####    ###    ####  #   #'''
    return logo


print(logo())

def Operation():
    print('''
    用法:
            逻辑提炼文件名:                   python3 Escan_1.0.py -f D:\\python_helpers\\File\\Folder_1\2.txt
            或者OR (提供完整路径):            python3 Escan_1.0.py -f D:/python_helpers/File/Folder_1/2.txt
            批量提炼文件目录:                 python3 Escan_1.0.py -folders_path D:/python_helpers/File/Folder_1/
            或者OR (提供完整路径)：           python3 Escan_1.0.py -folders_path D:\python_helpers\\File\\Folder_1\

            整合的文件目录:                   python3 Escan_1.0.py -collected  D:/python_helpers/dict


    用法介绍:
            Escan是一款分析API功能端点、收集功能端点的混淆测试工具，在金融测试、运营商测试，常常面对大量index.js文件混淆，
            通过分析路由的封装函数、暴露的参数值来达到发现一些边缘未授权业务的目的。
            是一款为了发现边缘业务而收集的工具，熟练掌握Escan的测试思路能发现一些多参数校验，非auth模块鉴权的业务；能发现因参数混淆，
            无从下手参数e，到获取到e值的分析工具。
            Escan使用文档_实际测试案例  -> https://github.com/gigigf/Escan

            ''')