import os
# gradio와 langchain_openai 기능을 이 코드에 불러왔어요.
import gradio as gr
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://mlapi.run/e55afb4c-afa7-4b64-b80f-937f9000573e/v1",
    api_key=os.getenv("OPENAI_API_KEY"), 
    model="helpy-pro",
    # 1. 하이퍼파라미터 설정하기
    max_tokens=800,
    temperature=0.8,
    presence_penalty=0.0
  
)

# 2. 시스템 프롬프트 설정하기
role = "너는 친절하게 수학을 알려주는AI야, 초등학생이 알아듣기 쉽게 대답하고 수학과 관련된 재미있는 비밀을 3~5문장으로 알려줘."

# ------------------------------------------------------
# 챗봇에서 보내기 버튼을 클릭하면 실행될 동작을 정의해요.

def function(message, history, memory):

    # 이전 역할과 학생 정보를 가져와요.
    conversation = memory

    # 이전 대화 기록을 하나씩 확인해요.
    for item in history or []:

        # 대화가 질문과 답변으로 구성되어 있는지 확인해요.
        if isinstance(item, (list, tuple)) and len(item) == 2:

            user, ai = item

            if user and ai:
                conversation += "사용자: " + user + "\n"
                conversation += "AI: " + ai + "\n"

    # 새롭게 입력한 질문을 추가해요.
    conversation += "사용자: " + message + "\n"

    # AI에게 전체 대화 내용을 전달해요.
    response = llm.invoke(conversation)

    # 기존 대화 기록을 복사해요.
    new_history = list(history or [])

    # 새로운 질문과 답변을 추가해요.
    new_history.append((message, response.content))

    # 전체 대화 기록을 반환해요.
    return new_history

# -------------------------------------------------------
# 챗봇 객체를 생성해요.
demo = gr.ChatInterface(
    fn=function,
    # 3. title, theme 등 속성 설정하기
    title="수학의 비밀을 알려주는 AI봇",
    description="원하는 수학 궁금증을 질문해볼래?"
)

# 챗봇 객체를 실행해요.
demo.launch(
    server_name="0.0.0.0",
    server_port=int(os.environ.get("PORT", 10000))
)
