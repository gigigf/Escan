import datetime , os
from core import generate_output_filename_with_time


def generate_Parmharvest_file(folder_path):
   # print(1)
    all_lines = set()
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            with open(file_path, "r") as file:
                all_lines.update(file.readlines())
    generate_file = generate_output_filename_with_time.out_filename_with_time()
    with open(generate_file, "w") as target:
        for line in all_lines:
            target.write(line)
    project_folder = os.getcwd()
    target_file_path = os.path.join(project_folder, generate_file)
    print('All_Line_Get_parmaterters文件生成已生成到', target_file_path)