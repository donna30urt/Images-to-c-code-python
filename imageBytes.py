import os

folder_path = 'C:/Users/Admin/Desktop/captchas' # Path to folder containing images / subfolders of images
subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]
image_data = {}

for subfolder in subfolders:
    subfolder_path = os.path.join(folder_path, subfolder)
    images = os.listdir(subfolder_path)
    byte_arrays = []
    for image in images:
        image_path = os.path.join(subfolder_path, image)
        with open(image_path, "rb") as file:
            byte_array = file.read()
            byte_arrays.append(byte_array)
    image_data[subfolder] = byte_arrays

cpp_source_code = ""

for subfolder, byte_arrays in image_data.items():
    vector_name = subfolder.lower()
    byte_array_name = f"{vector_name}_data"
    size_array_name = f"{vector_name}_size"
    
    cpp_source_code += f"std::vector<std::vector<unsigned char>> {vector_name} = {{\n"
    
    for byte_array in byte_arrays:
        cpp_source_code += "    {"
        for i in range(len(byte_array)):
            if i % 8 == 0:
                cpp_source_code += "\n        "
            cpp_source_code += f"{byte_array[i]}, "
        cpp_source_code = cpp_source_code.rstrip(", ")
        cpp_source_code += "},\n"
    
    cpp_source_code += f"}};\n"
    cpp_source_code += f"std::vector<unsigned int> {size_array_name} = {{\n"
    
    for byte_array in byte_arrays:
        cpp_source_code += f"    {len(byte_array)},\n"
    
    cpp_source_code += f"}};\n\n"

cpp_header_code = ""
cpp_header_code += "#ifndef IMAGEDATA_H\n"
cpp_header_code += "#define IMAGEDATA_H\n\n"

for subfolder in subfolders:
    vector_name = subfolder.lower()
    size_array_name = f"{vector_name}_size"
    cpp_header_code += f"extern std::vector<std::vector<unsigned char>> {vector_name};\n"
    cpp_header_code += f"extern std::vector<unsigned int> {size_array_name};\n\n"

cpp_header_code += "#endif // IMAGEDATA_H\n"

cpp_source_file_path = "imageData.cpp"
with open(cpp_source_file_path, "w") as file:
    file.write(cpp_source_code)

cpp_header_file_path = "imageData.h"
with open(cpp_header_file_path, "w") as file:
    file.write(cpp_header_code)
    