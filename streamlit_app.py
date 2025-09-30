import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

# ✅ NanumGothic 폰트 불러오기
font_path = "fonts/NanumGothic-Regular.ttf"
nanum_font = fm.FontProperties(fname=font_path)

plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지

st.title("📊 Dyscalculia 설문 데이터 분석")

# 📌 파일 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("파일 업로드 성공 ✅")

    # 📌 변수명과 질문 연결
    questions = {
        "SchoolRegion": "1. 교육지원청",
        "SchoolLevel": "2. 근무하시는 학교급",
        "Sex": "3. 성별",
        "Age": "4. 연령대",
        "EduLevel": "5. 최종 학력",
        "Career": "6. 교직 경력",
        "CareerSupport": "7. 학습지원 담당교원 근무 경력",
        "AwareDyscal": "8. 난산증 용어를 알고 계십니까?",
        "Other_Dyscal": "9. 난산증 학생 중 다른 어려움 비율",
        # 10번은 따로 처리
        "Exp_Dyscal": "11. 진단된 난산증 학생 경험 수",
        "Pos_Dyscal": "12. 최근 3년간 의심된 학생 수",
        "Edu_Dyscal": "13. 난산증 관련 연수 경험",
        "Sup_Dyscal": "14. 난산증 학생 지원 가능 여부",
        "Asses_Dyscal": "15. 난산증 진단 절차 인지 여부",
        "SchSup_Dyscal": "16. 학교 내 공식 지원 제도 여부",
        "SchSup_Dyscal2": "17. 외부 기관 연계 제도 여부"
    }

    # 📌 10번: 복수응답 데이터
    causes_data = {
        "난독증, ADHD 등의 다른 학습 관련 장애": 270,
        "적절한 학습 기회의 부족": 257,
        "뇌와 신경의 발달적·신경학적 원인": 241,
        "지능 발달 지연": 216,
        "학생의 동기 및 노력 부족": 119,
        "기타의견": 7
    }

    # 📌 특정 문항 정렬 순서 지정
    category_orders = {
        "Age": ["20대", "30대", "40대", "50대", "60대 이상"],
        "EduLevel": ["대학 졸업", "석사 재학·수료", "석사 졸업", "박사 재학·수료", "박사 졸업"],
        "Career": [
            "5년 미만",
            "5년 이상 10년 미만",
            "10년 이상 15년 미만",
            "16년 이상 20년 미만",
            "20년 이상"
        ],
        "Other_Dyscal": ["20% 미만", "20% 이상 40% 미만", "40% 이상 60% 미만", "60% 이상 80% 미만", "80% 이상"],
        "Exp_Dyscal": ["없음", "1~5명", "6~10명", "11~20명", "21명 이상"],
        "Pos_Dyscal": ["없음", "1~5명", "6~10명", "11~20명", "21명 이상"]
    }

    # 📌 y축 눈금 간격 1로 표시할 문항
    scale_1_ticks = ["AwareDyscal", "Sup_Dyscal", "Asses_Dyscal"]

    # 📌 루프 돌며 그래프 & 표 생성
    for col, q in questions.items():
        # 9번 뒤에 새로운 10번 문항 삽입
        if col == "Other_Dyscal":
            n_resp = len(df[col].dropna())
            with st.expander(f"9. 난산증 학생 중 다른 어려움 비율 (응답자 수: {n_resp})"):
                order = category_orders.get(col, None)
                if order:
                    counts = df[col].value_counts().reindex(order, fill_value=0).reset_index()
                else:
                    counts = df[col].value_counts().reset_index()
                counts.columns = ["응답", "빈도"]
                counts["비율(%)"] = (counts["빈도"] / counts["빈도"].sum() * 100).round(1)

                fig, ax = plt.subplots()
                counts.set_index("응답")["빈도"].plot(kind="bar", ax=ax)
                ax.set_ylabel("응답 수", fontproperties=nanum_font)
                ax.set_xlabel("응답", fontproperties=nanum_font)
                for label in ax.get_xticklabels():
                    label.set_fontproperties(nanum_font)
                for label in ax.get_yticklabels():
                    label.set_fontproperties(nanum_font)
                st.pyplot(fig)
                st.dataframe(counts)

            # 🔹 새 문항 (10번: 복수응답, 응답자 기준 457명)
            total_respondents = 457
            with st.expander(f"10. 생각하는 난산증의 주된 원인(복수응답) (응답자 수: {total_respondents})"):
                causes_df = pd.DataFrame(list(causes_data.items()), columns=["원인", "응답 수"])
                causes_df["비율(%)"] = (causes_df["응답 수"] / total_respondents * 100).round(1)

                fig, ax = plt.subplots()
                causes_df.set_index("원인")["응답 수"].plot(kind="barh", ax=ax, color="skyblue")
                ax.set_xlabel("응답 수", fontproperties=nanum_font)
                ax.set_ylabel("원인", fontproperties=nanum_font)
                for label in ax.get_xticklabels():
                    label.set_fontproperties(nanum_font)
                for label in ax.get_yticklabels():
                    label.set_fontproperties(nanum_font)
                st.pyplot(fig)
                st.dataframe(causes_df)

        else:
            n_resp = len(df[col].dropna())
            with st.expander(f"{q} (응답자 수: {n_resp})"):
                if pd.api.types.is_numeric_dtype(df[col]):
                    # 📊 히스토그램
                    fig, ax = plt.subplots()
                    df[col].plot(kind="hist", bins=10, ax=ax, rwidth=0.8)
                    ax.set_xlabel(col, fontproperties=nanum_font)
                    ax.set_ylabel("빈도", fontproperties=nanum_font)
                    for label in ax.get_xticklabels():
                        label.set_fontproperties(nanum_font)
                    for label in ax.get_yticklabels():
                        label.set_fontproperties(nanum_font)

                    # ✅ 특정 문항은 y축 눈금 간격 1로
                    if col in scale_1_ticks:
                        ax.set_yticks(range(0, int(df[col].max())+2, 1))

                    st.pyplot(fig)

                    # 📌 평균/표준편차
                    if col in ["AwareDyscal", "Sup_Dyscal", "Asses_Dyscal"]:
                        mean_val = df[col].mean()
                        std_val = df[col].std()
                        st.write(f"**평균:** {mean_val:.2f}, **표준편차:** {std_val:.2f}")

                    # 📌 분포표
                    counts = df[col].value_counts().reset_index()
                    counts.columns = ["값", "빈도"]
                    counts["비율(%)"] = (counts["빈도"] / counts["빈도"].sum() * 100).round(1)
                    st.dataframe(counts)

                else:
                    # 📊 범주형 데이터 (순서 지정 적용)
                    order = category_orders.get(col, None)
                    if order:
                        counts = df[col].value_counts().reindex(order, fill_value=0).reset_index()
                    else:
                        counts = df[col].value_counts().reset_index()
                    counts.columns = ["응답", "빈도"]
                    counts["비율(%)"] = (counts["빈도"] / counts["빈도"].sum() * 100).round(1)

                    fig, ax = plt.subplots()
                    counts.set_index("응답")["빈도"].plot(kind="bar", ax=ax)
                    ax.set_ylabel("응답 수", fontproperties=nanum_font)
                    ax.set_xlabel("응답", fontproperties=nanum_font)
                    for label in ax.get_xticklabels():
                        label.set_fontproperties(nanum_font)
                    for label in ax.get_yticklabels():
                        label.set_fontproperties(nanum_font)
                    st.pyplot(fig)
                    st.dataframe(counts)

else:
    st.info("⬆️ CSV 파일을 업로드하면 분석 결과가 표시됩니다.")
