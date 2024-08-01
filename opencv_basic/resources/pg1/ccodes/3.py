import subprocess
import os

def run_test2(base_dir):
    test2_path = os.path.join(base_dir, "../codes/3.py")
    result = subprocess.run(["python", test2_path], capture_output=True, text=True)
    return result.stdout

def parse_output(output):
    # 여기서 적절한 파싱을 수행하고 원하는 값 추출
    parsed_value = output.strip()  # 예시로 단순히 문자열을 제거
    return parsed_value

base_dir = "ccode"
output = run_test2(base_dir)
parsed_value = parse_output(output)
print("Parsed value:", parsed_value)
