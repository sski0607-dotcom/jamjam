import streamlit as st
import random
import re

st.set_page_config(page_title="생활 속의 인공지능 마스터", layout="centered")

# --- [174문제 데이터 베이스] ---
# 잼님, 이 아래 따옴표 사이에 제가 밑에 따로 드리는 174문제를 전부 붙여넣으세요!
QUIZ_DATA = """
Q1: 인공지능의 정의는 무엇인가요?
- 인공적으로 만들어낸 지능
- 자연적인 지능
- 모든 지능의 통합
- 인간의 지능과 동일한 지능
Answer: 인공적으로 만들어낸 지능

Q2: 약한 인공지능을 다른 용어로 무엇이라고 부르나요?
- 협의의 인공지능
- 범용 인공지능
- 초 인공지능
- 기계 학습
Answer: 협의의 인공지능

Q3: 강한 인공지능의 약자는 무엇인가요?
- AGI
- ANI
- ASI
- ML
Answer: AGI

Q4: 초인공지능의 정의는 무엇인가요?
- 인간의 능력을 넘는 지능
- 인간과 유사한 지능
- 인간보다 낮은 지능
- 특정 작업에 특화된 지능
Answer: 인간의 능력을 넘는 지능

Q5: 전통적인 프로그래밍 방법에 비교해서 기계 학습의 가장 큰 특징은 무엇인가요?
- 입력과 출력의 역할이 바뀐다
- 사전 정의된 규칙에 따른다
- 모든 데이터를 처리할 수 있다
- 정확한 결과를 보장한다
Answer: 입력과 출력의 역할이 바뀐다

Q6: 비지도학습의 대표적인 알고리즘은 무엇인가요?
- 클러스터링
- 회귀분석
- 분류
- 강화학습
Answer: 클러스터링

Q7: 강화 학습의 주요 특징은 무엇인가요?
- 보상 시스템을 통한 학습
- 라벨이 있는 데이터 사용
- 정확한 결과를 보장하는 학습
- 모든 데이터를 처리하는 학습
Answer: 보상 시스템을 통한 학습

Q8: 인공지능의 발전 단계에서 현재 우리는 어떤 단계에 있나요?
- 약한 인공지능 시대
- 강한 인공지능 시대
- 초인공지능 시대
- 기계학습 시대
Answer: 약한 인공지능 시대

Q9: 결정 경계선을 추가함으로써 해결할 수 있는 문제의 예시는 무엇인가요?
- 익스클루시브 OR 문제
- XOR 문제
- 선형 분류 문제
- 단순 회귀 문제
Answer: 익스클루시브 OR 문제 & XOR 문제

Q10: 옵티마이저와 손실 함수를 설정하는 모델 학습 구성 요소는?
- 옵티마이저(optimizer)
- 손실 함수(loss)
- 데이터 레이블
- 학습률
Answer: 옵티마이저(optimizer) & 손실 함수(loss)

Q11: 티처블 머신을 통해 훈련시킬 수 있는 자료 유형은?
- 이미지
- 사운드
- 포즈
- 텍스트 파일
Answer: 이미지 & 사운드 & 포즈

Q12: 프로젝트 저장 방법 두 가지는?
- 구글 드라이브
- 로컬 파일 저장
- 클라우드 자동 저장
- USB 저장
Answer: 구글 드라이브 & 로컬 파일 저장

Q13: 인공지능이 데이터를 통해 스스로 학습하는 기술은?
- 머신러닝
- 딥러닝
- 알고리즘
- 빅데이터
Answer: 머신러닝

Q14: 주피터 노트북에서 코드 셀을 실행하는 방법은 무엇인가요?
- Shift + Enter
- Ctrl + Enter
- Alt + Enter
- Tab + Enter
Answer: Shift + Enter & Ctrl + Enter
"""

# --- [로직 시작] ---
if 'quiz_bank' not in st.session_state:
    matches = re.findall(r"(Q\d+:.*?Answer:.*?(?=\nQ\d+:|$))", QUIZ_DATA, re.DOTALL | re.IGNORECASE)
    bank = []
    for block in matches:
        try:
            parts = re.split(r'Answer\s*:', block, flags=re.IGNORECASE)
            ans = [a.strip() for a in parts[1].strip().split('&')]
            content = re.split(r'\s*-\s*', parts[0])
            q_text = re.sub(r'^Q\d+:\s*', '', content[0]).strip()
            opts = [opt.strip() for opt in content[1:] if opt.strip()]
            if q_text and opts: bank.append({"q": q_text, "o": opts, "a": ans})
        except: continue
    st.session_state.quiz_bank = bank
    if bank: st.session_state.current_quiz = random.choice(bank)

st.title("📘 생활 속의 인공지능 퀴즈")
st.caption("등굣길에도, 학교에서도 열공하세요! 📖")

if st.session_state.quiz_bank and st.session_state.current_quiz:
    st.write(f"📊 총 문제 수: **{len(st.session_state.quiz_bank)}개**")
    q = st.session_state.current_quiz
    
    with st.container(border=True):
        st.subheader(f"Q. {q['q']}")
        user_selections = []
        for opt in q['o']:
            if st.checkbox(opt, key=f"opt_{opt}_{random.random()}"):
                user_selections.append(opt)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ 정답 확인", use_container_width=True):
                if not user_selections:
                    st.warning("답을 골라주세요!")
                else:
                    if set(user_selections) == set(q['a']):
                        st.balloons()
                        st.success("정답입니다!")
                    else:
                        st.error(f"오답! 정답: {' & '.join(q['a'])}")
        with col2:
            if st.button("➡️ 다음 문제", use_container_width=True):
                st.session_state.current_quiz = random.choice(st.session_state.quiz_bank)
                st.rerun()