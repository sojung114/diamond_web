# 프로젝트 설명

- 클라우드 기반 실시간 허위 과대광고 지능형 분석 및 알람 서비스 
- 이 서비스를 통해 물품 판매자와 소비자에게 올바른 정보를 제공하는 것이 최종 목표이다. 즉, 소비자에게는 허위과대광고에 현혹되지 않고 똑똑한 소비를 할 수 있는 지표를 제공해주고, 광고를 만드는 판매자는 본인 광고의 허위과대광고 유무를 판별하여 판매하기 전 올바르게 정보를 개선하여 소비자와 판매자 사이의 긍정적인 순환을 만드는 것이 본 프로젝트의 목표이다. 추가로 판매자를 위해 허위과대광고의 원인이 되는 단어들의 영향을 보여줌으로써 광고를 보다 빠르게 제작할 수 있게 도와 줄 것이다.
- XAI모델(판별결과를 설명하는 모델)과 LSTM모델(결과 판별모델)을 사용하여 사용자에게 신뢰도 있는 판결결과를 제공한다.
- 프로젝트 개발 환경: requirements.txt 에 제공한다.


# 프로젝트 결과물

### 1. 광고 문장 입력 화면
  
 ![input_screen](https://user-images.githubusercontent.com/63996585/172108855-6774acc2-d786-4453-bf4b-9e789018619f.png)

### 2. 결과페이지 로딩화면

 ![loading_screen](https://user-images.githubusercontent.com/63996585/172108882-d88e4bb7-1d6b-44f5-9e2c-acef5fe9c175.png)

### 3. 결과 화면

- 허위과대광고 결과와 정확도를 제공한다.
- 허위과대광고일 위험도가 높은 문장은 빨간색으로 처리된다.
- 마우스오버 시 XAI결과를 제공한다.

![result_screen](https://user-images.githubusercontent.com/63996585/172108912-d5b60078-67f2-499d-95ac-639f9962163b.png)
