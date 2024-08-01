
import subprocess

def grade_python_code(file_path, expected_output):
    # 파이썬 파일 실행
    result = subprocess.run(["python", file_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    
    # 실행 결과 출력
    print("=== Execution Result ===")
    print(result.stdout)
    
    # 예상 출력과 비교
    if result.stdout.strip() == expected_output.strip():
        print("=== Grade: Passed ===")
    else:
        print("=== Grade: Failed ===")

# 채점할 파이썬 파일 경로와 기대하는 출력
file_path = "../codes/1.py"
expected_output = "10.5\n"+"10\n"+"abcd\n"+"1234\n"

# 채점 실행
print("grading...")
grade_python_code(file_path, expected_output)