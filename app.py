
import os
import gradio as gr
from langchain_openai import ChatOpenAI

# 1. AI 설정하기 (하이퍼파라미터 설정)
llm = ChatOpenAI(
    base_url="https://mlapi.run/e55afb4c-afa7-4b64-b80f-937f9000573e/v1",
    api_key=os.getenv("OPENAI_API_KEY"),
    model="helpy-pro",
    max_tokens=800,
    temperature=0.8,
    presence_penalty=0.0
)

# 2. 시스템 프롬프트 설정하기
role = """너는 친절하게 수학을 알려주는 AI야.
초등학생이 알아듣기 쉽게 대답하고
수학과 관련된 재미있는 비밀을 3~5문장으로 알려줘."""

# ------------------------------------------------------
# 챗봇에서 보내기 버튼을 클릭하면 실행될 동작을 정의해요.
def function(message, history):

    # 역할을 memory에 저장해요.
    memory = role + "\n"

    # 이전 대화 내용을 하나씩 가져와요.
    for user, ai in history:
        memory += "사용자: " + user + "\n"
        memory += "AI: " + ai + "\n"

    # 새로운 질문을 추가해요.
    memory += "사용자: " + message + "\n"

    # AI에게 전체 대화 내용을 전달해요.
    response = llm.invoke(memory)

    # AI의 답변을 반환해요.
    return response.content

# -------------------------------------------------------
# 3. 챗봇 객체를 생성해요.
demo = gr.ChatInterface(
    fn=function,
    title="수학의 비밀을 알려주는 AI봇",
    description="원하는 수학 궁금증을 질문해볼래?"
)

# 4. 챗봇 실행하기
demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)
