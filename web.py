import socket
import sys
import threading
import framework

#创建一个类
class WebHttpServer(object):
    def __init__(self,port):
        # 创建socket
        self.tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # 当socket关闭以后，立马释放端口，方便下次调用
        self.tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        # 绑定端口号
        self.tcp_server_socket.bind(("", port))
        # 设置监听最大连接数
        self.tcp_server_socket.listen(128)

    @staticmethod
    def tcp_socket_http(new_cliend):
        recv_data = new_cliend.recv(4096)

        if len(recv_data) == 0:
            new_cliend.close()
            return
        # 数据解码
        recv_content = recv_data.decode("utf-8")
        print(recv_content)
        # 字符串按照空格进行分割
        request_list = recv_content.split(" ", maxsplit=2)
        print(request_list)
        request_path = request_list[1]
        print(request_path)

        if request_path == "/":
            request_path = "/index.html"

        if request_path.endswith(".html"):
            print("动态资源请求")
            # 动态资源请求找框架进行处理，需要把请求参数给框架。
            # 把准备好的参数，用字典的方式给框架env{}
            env = {
                "request_path":request_path
                # 如果需要传入额外的参数，在字典里面增加即可
            }

            status,headers, response_data=framework.handle_request(env)

            print(status,headers,response_data)
            # 响应头
            response_header = ""
            # 遍历响应头，有可能有多个响应头
            for header in headers:
                # response_header += "%s: %s\r\n" % header("Server","HDX")
                response_header += "%s: %s\r\n" % header
            # 响应行
            response_line = "HTTP/1.1 %s\r\n" % status
            # # 响应体
            response_body = response_data

            # 把数据封装成HTTP数据格式
            # response = (response_line +
            #             response_header +
            #             "\r\n").encode("utf-8")+response_body
            response = (response_line +
                        response_header +
                        "\r\n"+
                        response_body).encode("utf-8")

            new_cliend.send(response)


        else:
            try:
                # if os.path.exists("static" + request_path):
                with open("static" + request_path, 'rb') as file:
                    file_data = file.read()  # with打开文件读取完成后，自动关闭文件
            except Exception as e:
                print(e)
                with open("static/error.html", 'rb') as file:
                    file_data = file.read()  # with打开文件读取完成后，自动关闭文件
                # 响应行
                response_line = "HTTP/1.1 400 Not Found\r\n"
                # 响应头
                response_header = "Server:HDX/1.0\r\n"
                # 响应体
                response_body = file_data
                # 把数据封装成HTTP数据格式
                response = (response_line +
                            response_header +
                            "\r\n").encode("utf-8") + response_body

                new_cliend.send(response)

                new_cliend.close()

            else:
                # 响应头
                response_header = "Server:HDX/1.0\r\n"
                # 响应行
                response_line = "HTTP/1.1 200 OK\r\n"
                # 响应体
                response_body = file_data

                # 把数据封装成HTTP数据格式
                response = (response_line +
                            response_header +
                            "\r\n").encode("utf-8") + response_body

                new_cliend.send(response)


            finally:
                new_cliend.close()

    #启动类的方法
    def start(self):
        while True:
            # 等待客户端连接
            new_cliend, ip_port = self.tcp_server_socket.accept()
            print('客户端端口：', ip_port)
            # 创建多任务线程，实现多客户端并发连接
            socket_thread = threading.Thread(target=self.tcp_socket_http, args=(new_cliend,))
            # 主线程关闭，子线程自动消亡 主线程守护
            socket_thread.daemon = True
            # 运行线程
            socket_thread.start()

def main():
    # params=sys.argv
    # if len(params) != 2:
    #     print("Please input:python XXX.py 8000")
    #     return
    #
    # print("web params:",params)
    #
    # web_port=params[1]
    #
    # if not web_port.isdigit:
    #     print("Please input:python XXX.py 8000")
    #     return
    #
    # port=int(web_port)
    #
    # print("WebHttpServer start!")
    #
    # "".isdigit()
    # # 创建WEBHTTP服务器
    # web_http=WebHttpServer(port)
    prot=8000
    web_http = WebHttpServer(prot)
    #启动服务器
    web_http.start()


if __name__ == '__main__':
    main()




