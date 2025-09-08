import re
from titlecase import titlecase

# bib自动格式化: 自动将title字段大写, pages字段采用双横线


# 需要清理的字段
# 此类别外的bib将不做处理, 只保留格式化之后的内容
# 类别内的bib将按顺序保留这些字段, 其他字段删除
clean_fields = {
    'article': ['title', 'author', 'journal', 'volume', 'pages', 'year'],
    'inproceedings': ['title', 'author', 'booktitle', 'pages', 'year'],
}


def valid_bib_entry(bib):
    left = 0
    for ch in bib:
        if ch == '{':
            left += 1
        elif ch == '}':
            left -= 1
            if left < 0:
                return False
    return left == 0


def process_bib(bib):
    result = {}
    bib = re.sub(r'\s+', ' ', bib.strip())
    key_re = re.search(r'@(\w+)\s*\{\s*([^,\s]+)\s*', bib)
    if key_re:
        result['type'] = key_re.group(1).lower()
        result['alias'] = key_re.group(2).strip()
    else:
        return None
    idx = key_re.end(2)
    while idx < len(bib):
        key, value, st = "", "", 0
        while idx < len(bib) and (bib[idx] == ' ' or bib[idx] == '\n' or bib[idx] == ','):
            idx += 1
        while idx < len(bib) and bib[idx] != ' ' and bib[idx] != '\n' and bib[idx] != '=':
            key += bib[idx]
            idx += 1
        while idx < len(bib) and (bib[idx] == ' ' or bib[idx] == '\n' or bib[idx] == '='):
            idx += 1
        st += 1
        idx += 1
        while idx < len(bib) and st > 0:
            if bib[idx] == '{':
                st += 1
                idx += 1
                continue
            if bib[idx] == '}':
                st -= 1
                idx += 1
                continue
            value += bib[idx]
            idx += 1
        if len(value) > 0:
            result[key] = value
    result['type'] = result['type'].lower()
    result['title'] = '{' + titlecase(result['title']) + '}'
    ret = '@' + result['type'] + '{' + result['alias'] + ',\n'

    if result['pages'] and result['pages'].find('--') == -1:
        result['pages'] = result['pages'].replace('-', '--')

    if result['type'] in clean_fields:
        ret += '\n'.join(['  ' + k + ' = {' + result[k] + '},' for k in clean_fields[result['type']] if k in result])
    else:
        ret += '\n'.join(sorted(['  ' + k + ' = {' + result[k] + '},' for k in result]))
    ret += '\n}'
    return ret


input_file = 'raw.bib'
output_file = 'res.bib'

if __name__ == "__main__":
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            bibFile = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 '{input_file}'")
        exit(-1)
    except UnicodeDecodeError:
        print(f"错误：无法读取文件 '{input_file}'")
        exit(-1)
    bibs = re.sub(r'\n+', '\n', bibFile.replace('\r', '')).split('@')
    entries = []
    for item in bibs:
        if len(entries) == 0 or valid_bib_entry(entries[-1]):
            entries.append('@' + item)
        else:
            entries[-1] += '@' + item
    res = '\n\n'.join(filter(None, map(process_bib, entries)))
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(res)
        print(f"处理完成！结果已保存到: {output_file}")
    except Exception as e:
        print(f"错误：无法写入文件 '{output_file}': {e}")
