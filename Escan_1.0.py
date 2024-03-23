from core import Escan_logo, generate_API_endpoit_with_Get, command_line_parser
import argparse


def parse_arguments():
    parser = argparse.ArgumentParser(description="Escan: 一款收集功能端点的混淆测试工具", usage="python3 Escan_1.0.py")
    parser.add_argument("-f", "--file", type=str, help="读取的文件名完整地址")
    parser.add_argument("-folders_path", type=str, help="批量的文件目录完整地址")
    parser.add_argument("-collected", type=str, help="整合的文件目录")
    args = parser.parse_args()
    return args


def main():
    Escan_logo.logo()
    Escan_logo.Operation()
    args = parse_arguments()
    command_line_parser.parser_command_line(args)
    #filename = args.file
    #filenames = args.folders_path
    #print(filenames)
    # print(filename)
   # generate_API_endpoit_with_Get.process_file(filename)


if __name__ == '__main__':
    main()
