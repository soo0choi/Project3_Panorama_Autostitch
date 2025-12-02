# **📚 CV_class_2025_2_Assignment_3**

2025-2 Computer Visoin Assigmnet 3, 파노라마 이미지를 생성하는 과제입니다. 아래 과정을 따라 과제를 진행해주세요:D

과제 관련 문의가 있다면 아래 조교 메일로 연락해주세요.

- 최수영: csy010921@naver.com

---

## 🧩 **Project 3: Panorama Stitching & Image Alignment**

이 프로젝트에서는

<aside>

**여러 장의 이미지를 정렬(alignment) → Homography를 이용해 변환(warping) → 부드럽게 합성(blending) → 파노라마 이미지 생성**

</aside>

하는 과정을 구현합니다.

### **주요 목표**

- Spherical Warping (구면 투영 변환)
- Feature Alignment (Homography 기반 정렬)
- RANSAC 기반 Inlier 추출
- Image Bounding Box 계산 및 Accumulator 크기 계산
- 단일 파노라마를 위한 이미지 영역 합성

이 프로젝트는 전체 파이프라인 중 핵심 수학적 단계를 직접 구현해 결과 이미지를 시각화하는 것을 목표로 합니다.

---

## 🪜 **단계별 진행**

아래 단계들을 test.py의 TODO를 따라 진행해주시면 됩니다.

1. **Spherical Warping (TODO 1):** 이미지를 구면으로 펼쳐 파노라마 형태에 맞게 변환
2. **Homography 계산 (TODO 2–3):** 두 이미지의 대응점을 이용해 이미지 사이의 변환 관계(H) 추정
3. **이미지 정렬 (TODO 4):** 계산한 Homography를 기반으로 두 이미지를 같은 좌표계에 맞게 정렬
4. **Inlier 추출 (TODO 5):** RANSAC 방식으로 정확한 대응점(inlier)만 추출
5. **Homography 재추정 (TODO 6–7):** 추출된 inlier들만 사용해 Homography를 더 정확하게 계산
6. **Bounding Box 계산 (TODO 8):** 변환된 이미지가 어느 좌표 범위에 위치하는지 최소·최대 x,y 범위 계산
7. **Panorama 크기 계산 (TODO 9):** 모든 이미지가 들어갈 파노라마의 폭·높이를 계산하고, 필요한 translation 값 결정

---

## 🚀 **실행 및 테스트 방법**

1. **`test.py` 파일의 TODO 1–9 구현**
    - `alignment.py`, `warp.py`, `blend.py`의 관련 클래스와 함수를 참고해 `test.py`의 **빈칸(_______)** 만 채우면 됩니다.
2. **GUI 프로그램 실행**
    - `test.py` 파일 구현 후 `python gui.py` 를 실행하면 **GUI 프로그램이 실행**됩니다.
    <img width="1468" height="841" alt="image-6" src="https://github.com/user-attachments/assets/447c5788-66a8-4f0f-9cd4-ec71b0b68fc5" />
    
3. **이미지 불러오기**
    - GUI 프로그램의 **Panorama** 탭의 ‘Load Directory’를 통해 파노라마 소스 이미지들을 불러옵니다.
    - 이때, 이미지 파일 경로는 `Project3_Panorama_Autostitch/resources/yosemite/panorama` 로 설정합니다.
    <img width="1467" height="788" alt="image-4" src="https://github.com/user-attachments/assets/d9ae3cf0-ccc7-4d2d-b7a0-dbe34ea0fb82" />
    
4. **파노라마 실험(제공 데이터셋)**
    - GUI에서 파라미터 값을 조정해 파노라마 이미지를 완성하고 화면을 캡처합니다.
        - 아래 예시와 같은 결과 화면이 나오면 성공입니다.
    - `Project3_Panorama_Autostitch/resources` 경로에 **test_result** 폴더를 생성한 뒤,
        
        완성된 **GUI 결과 화면 캡처**를 해당 폴더에 저장합니다.
        
        - 파일명 형식: `학번_test_1.jpg`
        - 예: `20211234_test_1.jpg`
    <img width="1470" height="841" alt="image-5" src="https://github.com/user-attachments/assets/4154a9b9-07ab-4c20-a110-4f586fc694c8" />
    
---

**5. 파노라마 실험(개인 데이터셋 사용)**

- GUI 프로그램을 활용하여 **본인이 직접 준비한 이미지들로 파노라마를 생성**합니다.
- 과제에서 제공된 데이터셋은 사용하지 않으며, **직접 촬영한 이미지** 또는 **인터넷에서 구한 파노라마용 이미지 세트**를 활용해 파노라마를 구성합니다.
  
**6. 파노라마 실험(개인 데이터셋 사용) 설명 pdf**
- 각자 만든 파노라마 결과에 대해 **설명 PDF**를 작성해 제출합니다.
- PDF 분량은 **2페이지 이내**로 하며, 아래 내용을 포함해야 합니다.
  - 사용한 **데이터셋 설명**
    - **테스트 과정 및 결과 분석**
      - 어떤 조건에서 파노라마가 잘 생성되었는지 / 잘 생성되지 않았는지
        - 그 이유에 대한 본인의 분석
      - **GUI 프로그램에서 생성한 파노라마 결과 이미지(필수 포함)**
- 파일명은 **test_result 폴더** 안에 `학번_test_2.pdf` 형식으로 저장합니다.
    - 예: `20211234_test_2.pdf`

---

## ⭐️ **과제 제출 총정리**

- 본 레포지토리를 자신의 컴퓨터로 **pull**한 뒤, `test.py`의 TODO 함수를 구현합니다.
- 구현 후, **test_result** 폴더 안에 아래 두 파일을 추가합니다.
    - 실습한 **제공 데이터셋 파노라마 결과(GUI 화면 캡처:** `학번_test_1.jpg`**)**
    - **개인 데이터셋 파노라마 설명 PDF(**`학번_test_2.pdf`**)**
- 모든 파일을 추가한 뒤 **push**하면 과제 제출이 완료됩니다.
