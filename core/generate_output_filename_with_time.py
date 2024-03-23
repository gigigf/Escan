import datetime, os


def get_output_filename_with_time(filename):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name_with_extension = os.path.basename(filename)
    filename_without_extension = os.path.splitext(file_name_with_extension)[0]
    output_file_with_time = f"{filename_without_extension}_get_parameters_{current_time}.txt"
    return output_file_with_time


def out_filename_with_time():
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    target_file = f"All_Line_Get_parameters_{current_time}.txt"
    return target_file
