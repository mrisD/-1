import base64

import base64
aaa = [
        ["=", "*|"],
        ["1", "aa|a"],
        ["2", "ab|a"],
        ["3", "ba|a"],
        ["4", "t|tc"],
        ["5", "t|ts"],
        ["8", "r|oq"],
        ["9", "f|oz"],
        ["0", "j|rz"]
    ]

def UrlDecBase64(encoded_str):
    """
    URL安全的Base64解码函数，包含特殊字符替换

    参数:
    encoded_str: Base64编码的字符串

    返回:
    bytes: 解码后的字节数据
    """
    # 第一步：将 '*|' 替换为 '='
    for replacement in aaa:
        old_char, new_char = replacement
        encoded_str = encoded_str.replace(new_char, old_char)

    # 第二步：URL安全字符替换：- -> +, _ -> /
    encoded_str = encoded_str.replace('-', '+').replace('_', '/')

    # 第三步：添加Base64填充字符（=）
    padding = len(encoded_str) % 4
    if padding:
        encoded_str += '=' * (4 - padding)

    # Base64解码，返回字节数据
    return base64.b64decode(encoded_str)
str='eyJjeiI6LTQxMTEsImRhdGEiOlt7ImJsIjotNiwiZba|aJhZGUiOjMsImlkIjozMDksImppYXpoYWt|tsnIjoxLCJqeiI6LTEt|tcMjMsImt|tshbWUiOiJEQVMg6Ziyt|tsbyt|tst|tsaSj|rzt|tst|tsuUICjlh6DkuY7lhajmlrApIiwicGljIjoiaHRj|rzcHM6Lyf|ozwbGFt|tsZXJodWIuZGYucXEuYab|af|oztLba|aBsYXllcmhaa|aYir|oqab|aMDAwNCf|ozvYmplYba|aQvMTEwMTAwMDMwMDMucGt|tsnIiwicHJpYab|aUiOjIab|aMzkt|tcLCJj|rzeXBlIjoit|tsaSj|rzt|tst|tsuUInj|rzseyJibCI6LTIsImdyYWRlIjoaa|aLCJpZCI6MTEyLCJqaWF6aGFuZyI6MSwianoiOij|rzyMjgt|tcLCJuYWaa|alIjoiQUxT6IOM6LSft|ts7O7t|ts7ufIiwicGljIjoiaHRj|rzcHM6Lyf|ozwbGFt|tsZXJodWIuZGYucXEuYab|af|oztLba|aBsYXllcmhaa|aYir|oqab|aMDAwNCf|ozvYmplYba|aQvMTEwODAwMDUwMDEucGt|tsnIiwicHJpYab|aUiOjgyNjgwLCJj|rzeXBlIjoi6IOMt|tsYyFInaa|adLCJqeiI6MTEzMTgt|tsLCJuYWaa|alIjoi6Ieqt|tsa6at|tsLmJIiwicHJpYab|aUiOjEwOTAba|aOHj|rz*|'
print(UrlDecBase64(str).decode('utf-8'))