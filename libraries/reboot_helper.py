import psutil
import sys
import os


def close_port(port):
    """
    关闭指定端口的进程
    """
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port:
            try:
                proc = psutil.Process(conn.pid)
                print(f"正在终止占用端口 {port} 的进程: PID {proc.pid}")
                proc.terminate()
                proc.wait(timeout=3)
                print(f"进程 {proc.pid} 已成功终止")
                return True
            except psutil.NoSuchProcess:
                print(f"进程已不存在，端口 {port} 可用")
                return True
            except Exception as e:
                print(f"关闭端口 {port} 时出错: {e}")
                return False
    print(f"未找到占用端口 {port} 的进程")
    return True

def main():
    if len(sys.argv) < 2:
        print("用法: python reboot_helper.py <脚本路径> [附加参数...]")
        sys.exit(1)

    
    script_path = sys.argv[1]
    extra_args = sys.argv[2:]
    port = int(sys.argv[2])  # 固定端口号

    # 关闭指定端口
    if not close_port(port):
        print(f"端口 {port} 无法释放，重启失败")
        sys.exit(1)

    # 重启目标程序
    python = sys.executable

    os.execl(python, python, script_path, *extra_args)

if __name__ == "__main__":
    main()
