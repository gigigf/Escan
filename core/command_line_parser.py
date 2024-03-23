import os
from core import Escan_logo, generate_API_endpoit_with_Get, generate_ParamHarvest_file


def parser_command_line(args):
    if args.file:
        print(1)
        filename = args.file
        print('逻辑提炼文件名:',filename)
        generate_API_endpoit_with_Get.process_file(filename)
    if args.folders_path:
        folder_path = args.folders_path
        print(2)
        print('逻辑提炼文件目录:', args.folders_path)
        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            print('逐步提炼文件目录文件，当前处理:', file_path)
            generate_API_endpoit_with_Get.process_file(file_path)
        #print(file_list)
    if args.collected:
            collected = args.collected
            print(3)
            generate_ParamHarvest_file.generate_Parmharvest_file(collected)
