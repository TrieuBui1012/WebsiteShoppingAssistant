import os
import requests
import streamlit as st

CHATBOT_URL = os.getenv("CHATBOT_URL", "http://localhost:8082/market-rag-agent")

with st.sidebar:
    st.header("Giới thiệu")
    st.markdown(
        """
        Chatbot này giao tiếp với một
        [LangChain](https://python.langchain.com/docs/get_started/introduction)
        agent được thiết kế để trả lời các câu hỏi về sản phẩm, danh mục,
        người bán, thương hiệu và các thông tin liên quan khác trong hệ thống
        thị trường giả lập. Agent sử dụng phương pháp tạo nội dung tăng cường truy xuất (RAG)
        trên cả dữ liệu có cấu trúc và phi cấu trúc đã được tạo tổng hợp.
        """
    )

    st.header("Câu hỏi Ví dụ")
    st.markdown("- Cho tôi tổng quan thông tin về sản phẩm: chuột có dây logitech b100 - hàng chính hãng")
    st.markdown("- Cho tôi một số sản phâm kết nối không dây đáng tin cậy")
    st.markdown("- Tôi cần một chiếc laptop nhẹ để dễ dàng mang theo khi đi du lịch, bạn giới thiệu sản phẩm nào?")
    st.markdown("- Đưa cho tôi một số thiết bị chuột và bàn phím phù hợp với dân văn phòng")
    st.markdown("- Cho tôi tổng quan thông tin về sản phẩm Tai Nghe Chụp Tai Sony MDR-ZX110AP")
    st.markdown("- Thông tin dịch vụ khách hàng là gì?")

st.title("Chatbot Hệ Thống Thị Trường")
st.info(
    """Hãy hỏi tôi về sản phẩm, danh mục, người bán, thương hiệu và các thông tin liên quan khác trong hệ thống thị trường!"""
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if "output" in message.keys():
            st.markdown(message["output"])

        if "explanation" in message.keys():
            with st.status("Cách tạo nội dung này", state="complete"):
                st.info(message["explanation"])

if prompt := st.chat_input("Bạn muốn biết gì?"):
    st.chat_message("user").markdown(prompt)

    st.session_state.messages.append({"role": "user", "output": prompt})

    data = {"text": prompt}

    with st.spinner("Đang tìm kiếm câu trả lời..."):
        response = requests.post(CHATBOT_URL, json=data)

        if response.status_code == 200:
            output_text = response.json()["output"]
            explanation = response.json()["intermediate_steps"]

        else:
            output_text = """Đã xảy ra lỗi khi xử lý tin nhắn của bạn.
            Điều này thường có nghĩa là chatbot không thể tạo truy vấn để
            trả lời câu hỏi của bạn. Vui lòng thử lại hoặc thay đổi cách diễn đạt câu hỏi."""
            explanation = output_text

    st.chat_message("assistant").markdown(output_text)
    st.status("Cách tạo nội dung này?", state="complete").info(explanation)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "output": output_text,
            "explanation": explanation,
        }
    )
