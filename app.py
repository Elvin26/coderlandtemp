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


demo = gr.ChatInterface(
    fn=function,
    title="수학의 비밀을 알려주는 AI봇",
    description="원하는 수학 궁금증을 질문해볼래?"
)

demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)
