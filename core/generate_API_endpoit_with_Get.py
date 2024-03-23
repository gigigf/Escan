import re, os
from core import generate_output_filename_with_time, command_line_parser


# from .. import Escan_1.0

def process_file(filename):
    lines = read_file_content(filename)  # 读取文件内容
    get_parameters = extract_get_parameters(lines)  # 提取 GET 参数
    query_parameters = extract_query_parameters(lines)
    exposed_params = extract_exposed_params(lines)
    output_filename = generate_output_filename_with_time.get_output_filename_with_time(filename)  # 生成输出文件名
    print('\n')
    print('生成的对应时间文件名', output_filename)
    save_output_file(output_filename, get_parameters)  # 生成实际文件并保存
    ##迭代保存
    output_file_path = save_output_file(output_filename, get_parameters)
    print('逻辑提炼完成_文件位置:', output_file_path)
    print('\n')
    if not 1:
        generate_ParamHarvest_file(output_filename, output_file_path)


def save_output_file(output_filename, content):
    # 拼接文件路径
    output_file_path = os.path.join(os.path.dirname(__file__), '..', 'dict', output_filename)
    # 写入文件内容
    with open(output_file_path, 'w') as f:
        for item in content:
            f.write(f"{item}\n")
        return output_file_path


def generate_ParamHarvest_file(output_filenames, output_file_path):
    file_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__), '..', 'dict', 'get_endpoint_with_30w.txt'))  # 有效处理路径问题
    ParamHarvest_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'dict/ParamHarvest'))
    os.makedirs(ParamHarvest_dir, exist_ok=True)
    file_name_with_extension = os.path.basename(output_filenames)
    filename_without_extension = os.path.splitext(file_name_with_extension)[0]
    print(22)
    print(filename_without_extension)
    new_filename = f"New_add_{filename_without_extension}_get_with_parameters.txt"
    with open(f"{ParamHarvest_dir}/{new_filename}", 'w') as new_file:
        with open(file_path, 'r') as f:
            get_endpoint_content = f.read()
            new_file.write(get_endpoint_content)
            new_file.write('\n')
        with open(output_file_path, 'r') as f:
            output_content = f.read()
            new_file.write(output_content)


def read_file_content(filename):
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'File', filename))
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        with open(filename, 'r') as file:
            lines = file.readlines()
    return lines


def extract_get_parameters(lines):
    def clean_line(line):
        return line.rstrip('/')

    results_with_get = []
    for line in lines:
        line = clean_line(line)
        match = re.search(r'get\w+\b', line)
        if match:
            results_with_get.append(match.group())
    print('#####################封装函数提取##############################.Get_Funcation() 提取:##################################################################')
    print(list(set(results_with_get)))
    return results_with_get


def extract_query_parameters(lines):
    def clean_line(line):
        return line.rstrip('/')

    results_with_query = []
    results_with_query_line = []
    #print(len(lines))
    for line in lines:
        line = clean_line(line)
        match = re.search(r'query\w+\b', line)
        math1 = re.search(r'(.*?)query', line)
        if math1:
            matched_string = math1.group(1)
          #  math_1 = re.sub(r'query.*?$', '', matched_string)
            results_with_query_line.append(matched_string)
        if match:
            results_with_query.append(match.group())
        ##输出数据清洗
    print("\n")
    print(
        '#####################封装函数提取##...######################.####.Query_Funcation() 提取:#########################...########################')
    print(list(set(results_with_query)))
    print(
        '################## #封装函数API路径提取######################.####.Query_API路径提取:######################...#############################...######################')
    print(list(set(results_with_query_line)))
    return results_with_query


def extract_exposed_params(lines):
    def clean_line(line):
        return line.rstrip('/')
    #print(len(lines))
    result_with_params = []
    result_with_params_dir = []
    for line in lines:
        line = clean_line(line)
        #print(line)
        match = re.search(r'\?(.*?)$', line)
        match1 = re.search(r'(.*?)\?', line)
        if match:
            result_with_params.append(match.group())
        if match1:
            matched_string = match1.group(1)
            result_with_params_dir.append(matched_string)
    print("\n\n")
    print(
        '#####################暴露的参数值提取##...######################.####.暴露的参数值提取:#########################...#############################...######################')
    print(list(set(result_with_params)))
    print(
        '#####################暴露的参数值路径提取##...######################.暴露的参数值路径提取:#########################...#############################...######################')
    print(result_with_params_dir)
    return result_with_params
