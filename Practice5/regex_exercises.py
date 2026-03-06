import re


text1 = "a ab abb abbb bba"
pattern1 = r"ab*"
result1 = re.findall(pattern1, text1)
print("1.", result1)


text2 = "a ab abb abbb abbbb"
pattern2 = r"ab{2,3}"
result2 = re.findall(pattern2, text2)
print("2.", result2)


text3 = "my_variable test_case some_value"
pattern3 = r"[a-z]+_[a-z]+"
result3 = re.findall(pattern3, text3)
print("3.", result3)


text4 = "Hello World Python Regex"
pattern4 = r"[A-Z][a-z]+"
result4 = re.findall(pattern4, text4)
print("4.", result4)


text5 = "acb a123b ab aXYZb"
pattern5 = r"a.*b"
result5 = re.findall(pattern5, text5)
print("5.", result5)


text6 = "Hello, world. Python is fun"
result6 = re.sub(r"[ ,\.]", ":", text6)
print("6.", result6)


def snake_to_camel(s):
    return re.sub(r'_([a-z])', lambda m: m.group(1).upper(), s)

text7 = "my_variable_name"
print("7.", snake_to_camel(text7))


text8 = "HelloWorldPython"
result8 = re.split(r"(?=[A-Z])", text8)
print("8.", result8)


text9 = "HelloWorldPython"
result9 = re.sub(r"([A-Z])", r" \1", text9).strip()
print("9.", result9)


def camel_to_snake(s):
    s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', s)
    return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

text10 = "myVariableName"
print("10.", camel_to_snake(text10))


text11 = "I have 2 apples and 15 bananas and 300 grapes"
pattern11=r"\d+"
finding_number=re.findall(pattern11, text11)
print("11. ", finding_number)