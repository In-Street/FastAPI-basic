from urllib.parse import quote,unquote

"""
	请求路径参数汉字编码
"""
str_a  = '/song/1/周杰伦'
quote_str = quote(str_a)
print(quote_str)

print(unquote(quote_str))

