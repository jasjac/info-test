# web框架，专门负责处理动态参数
import  time

def index():
    # 响应状态
    status = "200 OK";
    # 响应头
    response_header = [("Server", "PWS2.0")]

    # 1. 打开模板文件，读取数据
    with open("template/index.html", "r") as file:
        file_data = file.read()

    # 处理后的数据, 从数据库查询
    data = time.ctime()
    # 2. 替换模板文件中的模板遍历
    result = file_data.replace("{%content%}", data)

    return status, response_header, result

# def index():
#     # 状态status
#     status="200 OK\r\n"
#     #header 报头
#     header=[("Server","HDX")]
#     #response_boby 报文 以获得当前事件为例
#     # data = time.ctime()
#
#     # 1. 打开模板文件，读取数据
#     # with open("template/index.html", encoding='urf-8') as file:
#     # with open("template/index.html", "r") as file:
#     with open("template/index.html", encoding="utf-8") as file:
#         file_data = file.read()
#
#     # 处理后的数据, 从数据库查询
#     data = time.ctime()
#
#     # datas=data.decode()
#     # 2. 替换模板文件中的模板遍历
#     # files_datas=file_data.decode("utf-8")
#     result = file_data.replace("{%content%}", data)
#
#
#
#     return status,header,result

def not_found():
    # 状态status
    status="400 NOT Found\r\n"
    #header 报头
    header=[("Server","HDX2.0")]
    #response_boby 报文 以获得当前事件为例
    response_boby = "NOT Found"

    return status,header,response_boby


# 处理动态资源请求
def handle_request(env):
    request_path=env["request_path"]
    print("框架获取的动态资源路径：",request_path)

    if request_path == "/index.html":
        result=index()
        return result
    else:
        result=not_found()
        return result


