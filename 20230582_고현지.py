#!/usr/bin/env python
# coding: utf-8

# # 과제: 다양한 정렬 알고리즘을 이용한 성적 관리 프로그램 
# - 학생 성적 레코드(이름, 나이, 점수)를 랜덤으로 30개 생성하여, 다양한 정렬 알고리즘을 사용하여 특정 필드 기준으로 레코드를 정렬하는 프로그램을 작성하세요. 
# - 프로그램은 사용자 인터페이스를 제공하며, 메뉴를 통해 정렬 기준 선택, 정렬 후 결과 출력 및 프로그램 종료 기능을 포함한다.

# ### 1. import

# In[10]:


import random
import string
import json


# ### 2. sort function

# In[11]:


# 1. 선택 정렬
def selection_sort(A, by):
    n = len(A)
    for i in range(n-1):
        least = i
        for j in range(i+1, n):
            if A[j][by] < A[least][by]:
                least = j
        A[i], A[least] = A[least], A[i]
    return A

# 2. 삽입 정렬
def insertion_sort(A, by):
    n  = len(A)
    for i in range(1, n):
        key = A[i] # 딕셔너리 전체를 key로 설정
        key_value = A[i][by] # 비교 기준 값
        
        # 삽입할 위치 찾기
        j = i - 1
        while j >= 0 and A[j][by] > key_value:
            A[j+1] = A[j]
            j -= 1
        # key 삽입
        A[j+1] = key
    return A

# 3. 퀵 정렬
def quick_sort(A, left, right, by):
    if left < right:
        q = partition(A, left, right, by)
        quick_sort(A, left, q-1, by)
        quick_sort(A, q+1, right, by)
    return A

def partition(A, left, right, by):
    low = left + 1
    high = right 
    pivot = A[left][by]
    
    while low <= high:
        # 1. 피벗보다 큰 요소를 찾기 위해 low 위치에서 오른쪽으로 이동
        while low <= right and A[low][by] <= pivot:
            low += 1
            
        # 2. 피벗보다 작은 요소를 찾기 위해 high 위치에서 왼쪽으로 이동
        while high >= left and A[high][by] > pivot:
            high -= 1
            
        # 요소 교환
        if low < high:
            A[low], A[high] = A[high], A[low]
    
    # 피벗 위치 교환
    A[left], A[high] = A[high], A[left]
    
    # pivot의 인덱스 반환
    return high

# 4. 기수 정렬
class ArrayQueue:
    def __init__(self, capacity = 10):
        self.capacity = capacity
        self.array = [None] * capacity
        self.front = 0
        self.rear = 0

    def is_empty(self):
        return self.front == self.rear

    def is_full(self):
        return self.front == (self.rear + 1) % self.capacity

    def enqueue(self,item):
        if not self.is_full():
            self.rear = (self.rear + 1) % self.capacity
            self.array[self.rear] = item
        else:
            print("Queue is full. Cannot enqueue.")

    def dequeue(self):
        if not self.is_empty():
            self.front = (self.front + 1) % self.capacity
            item = self.array[self.front]
            self.array[self.front] = None # 삭제된 자리 초기화
            return item
        else:
          print("Queue is empty. Cannot dequeue.")
          return None

def radix_sort(A, by):
    BUCKETS = 10
    DIGITS = 3  # 정렬할 숫자의 자릿수 (예: 3자리까지)

    # 계수 정렬을 위한 함수 정의
    def counting_sort_for_radix(A, by, factor):
        n = len(A)
        output = [None] * n
        count = [0] * BUCKETS

        # 각 요소의 자릿수 값을 기준으로 빈도 계산
        for i in range(n):
            digit = (A[i][by] // factor) % BUCKETS
            count[digit] += 1

        # 누적합 계산
        for i in range(1, BUCKETS):
            count[i] += count[i - 1]

        # 배열 요소를 출력 배열에 배치
        for i in range(n - 1, -1, -1):
            digit = (A[i][by] // factor) % BUCKETS
            output[count[digit] - 1] = A[i]
            count[digit] -= 1

        # 결과를 원본 배열 A로 복사
        for i in range(n):
            A[i] = output[i]

    # 기수 정렬 수행
    factor = 1
    for d in range(DIGITS):
        counting_sort_for_radix(A, by, factor)
        factor *= BUCKETS
    return A
        


# ###  3. 학생 성적 관리 시스템 class

# In[12]:


class StudentManagementSystem:
    # 학생 정보 생성
    def generateStudents(self, n):
        list = []
        for i in range(n):
            dict = {}
            # 1. 이름
            name = ""
            name+= random.choice(string.ascii_uppercase)
            name+= random.choice(string.ascii_uppercase)

            # 2. 나이
            age = random.randint(18, 22)

            # 3. 성적
            score = random.randint(0, 100)

            # 4. 리스트에 딕셔너리 형태로 학생 정보를 추가한다. 
            dict['이름'] = name
            dict['나이'] = age
            dict['성적'] = score
            list.append(dict)
        return list # 최종 리스트를 반환한다.

    # 학생 정보를 파일에 저장
    def save_to_json_file(self, filename, students):
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(students, file, ensure_ascii=False, indent=4)

    # 리스트 출력 
    def show(self, A, message=''):
        print(message)
        for i in range(len(A)):
            print(A[i])
    
    # main
    def main(self):
        # 30명의 무작위 학생 정보를 생성하고, 파일에 저장한다.
        students = self.generateStudents(30) 
        self.save_to_json_file("students.json", students)
        print("학생 정보가 'students.json'에 저장되었습니다.")
        
        # 생성된 학생 정보 출력
        self.show(students, '생성된 학생 정보:')
        
        exit_flag = False # 반복문 탈출 플래그
        
        while True:
            # 정렬된 리스트를 저장하는 변수 (정렬이 한 번 끝날 때마다 초기화된다.)
            sorted_list = []
            
            # 메뉴
            print("\n메뉴:")
            print("1. 이름을 기준으로 정렬")
            print("2. 나이를 기준으로 정렬")
            print("3. 성적을 기준으로 정렬")
            print("4. 프로그램 종료")
            
            while True: # 1. 정렬 기준 선택 
                choice = input("정렬 기준을 선택하세요 (1, 2, 3, 4): ")
                if (choice == '1'): 
                    by = '이름'
                    break
                elif (choice == '2'): 
                    by = '나이'
                    break
                elif (choice == '3'): 
                    by = '성적'
                    break
                elif (choice == '4'): 
                    print("프로그램을 종료합니다.")
                    exit_flag = True
                    break;
                else:
                    print("1, 2, 3, 4 중에서 선택하세요.")
                
            if exit_flag: 
                break
                
            while True: # 2. 정렬 알고리즘 선택 
                algo = input("정렬 알고리즘을 선택하세요 (선택, 삽입, 퀵, 기수)(성적만 기수 정렬 가능): ")
                if (algo == '선택'): 
                    sorted_list = selection_sort(students, by)
                elif (algo == '삽입'):
                    sorted_list = insertion_sort(students, by)
                elif (algo == '퀵'):
                    sorted_list = quick_sort(students, 0, len(students)-1, by)
                elif (algo == '기수'):
                    if (choice == '3'):
                        sorted_list = radix_sort(students, by)
                    else:
                        print('성적을 기준으로 정렬할 때만 가능합니다.')
                        continue
                elif (algo == '-1'): # -1 : 뒤로 가기 (기준 선택 메뉴로 돌아간다.)
                    break
                else:
                    print("올바르지 않은 선택입니다.")
                    continue
                    
                # 정렬된 결과 출력
                if sorted_list:
                    self.show(sorted_list, '정렬된 학생 정보:')
                    break
        


# ### 4. 프로그램 실행

# In[13]:


def main():
    spmsys = StudentManagementSystem()
    spmsys.main()
    
if __name__ == '__main__':
    main()
    


# In[ ]:




