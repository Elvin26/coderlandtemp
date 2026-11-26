import os
import gradio as gr
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://mlapi.run/e55afb4c-afa7-4b64-b80f-937f9000573e/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
    model="helpy-pro",
    max_tokens=800,
    temperature=0.8,
    presence_penalty=0.0
)

role = """
너는 친절하게 수학을 알려주는 AI야.
초등학생이 알아듣기 쉽게 대답하고,
수학과 관련된 재미있는 비밀을 3~5문장으로 알려줘.
"""

def function(message, history):
    conversation = role + "\n\n"

    # 이전 대화 기록 불러오기
    for item in history or []:

        # Gradio의 메시지 형식 처리
        if isinstance(item, dict):
            speaker = item.get("role")
            content = item.get("content")

            if content is None:
                continue

            if speaker == "user":
                conversation += f"사용자: {content}\n"
            elif speaker == "assistant":
                conversation += f"AI: {content}\n"

        # Gradio의 튜플 형식 처리
        elif isinstance(item, (list, tuple)) and len(item) == 2:
            user, ai = item

            if user is not None:
                conversation += f"사용자: {user}\n"

            if ai is not None:
                conversation += f"AI: {ai}\n"

    # 현재 입력한 질문 추가
    conversation += f"사용자: {message}\n"
    conversation += "AI: "

    # AI 답변 생성
    response = llm.invoke(conversation)

    # 답변 문자열만 반환 (대화 기록은 Gradio가 관리)
    return str(response.content)


```python
demo = gr.ChatInterface(
    fn=function,
    title="🔍 수학 탐험대!",
    description="""
    🧭 수학 탐험을 시작해 볼까요?

    어려운 수학도 걱정하지 마세요!
    초등학생 눈높이에 맞춰 쉽고 재미있게 설명해 줄게요.

    ✨ 수학 속에 숨겨진 신기한 비밀도 함께 찾아봐요!
    """,
    examples=[
        "분수는 왜 배우는 거야?",
        "피타고라스 정리가 뭐야?",
        "0은 누가 처음 만들었어?",
        "곱셈을 쉽게 하는 방법을 알려줘!"
    ],
    submit_btn="질문하기 🚀",
    fill_height=True,
    fill_width=False
)
```

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)
