import json

def parse_csv_line(line):
    """手动解析包含引号的CSV行"""
    result = []
    current_field = ""
    in_quotes = False
    
    i = 0
    while i < len(line):
        char = line[i]
        
        if char == '"':
            if in_quotes and i + 1 < len(line) and line[i + 1] == '"':
                # 转义的引号
                current_field += '"'
                i += 1
            else:
                # 开始或结束引号
                in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            # 字段分隔符
            result.append(current_field.strip())
            current_field = ""
        else:
            current_field += char
        
        i += 1
    
    # 添加最后一个字段
    result.append(current_field.strip())
    return result

# 读取CSV文件
def read_csv_data(filename):
    data = {}
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    # 跳过头部
    for line in lines[1:]:
        line = line.strip()
        if line:
            fields = parse_csv_line(line)
            if len(fields) >= 8:
                prompt_id = int(fields[0])
                data[prompt_id] = {
                    'prompt': fields[2].strip('"'),
                    'color_score': float(fields[3]) if fields[3] else 0,
                    'spatial_score': float(fields[4]) if fields[4] else 0,
                    'count_score': float(fields[5]) if fields[5] else 0,
                    'relevance_score': float(fields[6]) if fields[6] else 0,
                    'overall_score': float(fields[7]) if fields[7] else 0
                }
    return data

# 读取数据
dola_data = read_csv_data('NewPrompts_DOLA_evaluation.csv')
normal_data = read_csv_data('NewPrompts_Normal_evaluation.csv')

# 创建合并数据，使用CSV中的prompt作为显示的prompt
merged_data = {}

for i in range(1, 101):  # 1到100
    # 从CSV获取prompt（两个CSV文件中的prompt应该是一样的）
    prompt_text = ""
    if i in dola_data:
        prompt_text = dola_data[i]['prompt']
    elif i in normal_data:
        prompt_text = normal_data[i]['prompt']
    
    merged_data[str(i)] = {
        'prompt': prompt_text,  # 使用CSV中的prompt
        'dola': dola_data.get(i, {
            'color_score': 0, 'spatial_score': 0, 'count_score': 0, 
            'relevance_score': 0, 'overall_score': 0
        }),
        'normal': normal_data.get(i, {
            'color_score': 0, 'spatial_score': 0, 'count_score': 0, 
            'relevance_score': 0, 'overall_score': 0
        })
    }

# 保存为JSON文件
with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(merged_data, f, ensure_ascii=False, indent=2)

print("数据处理完成，已生成data.json文件")
print(f"处理了 {len(merged_data)} 条记录")
print(f"DOLA数据: {len(dola_data)} 条")
print(f"Normal数据: {len(normal_data)} 条")
print("现在使用CSV中的prompt作为显示内容")