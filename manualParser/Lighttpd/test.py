def remove_leading_spaces(text):
    # 将文本分割成行
    lines = text.splitlines()

    # 去除每行开头的空格
    cleaned_lines = [line.lstrip() for line in lines]

    # 重新组合成一个字符串
    cleaned_text = '\n'.join(cleaned_lines)

    return cleaned_text


# 测试示例
with open()

cleaned_text = remove_leading_spaces(text)
print(cleaned_text)
