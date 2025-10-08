# --- Chức năng 6: Chat với Gemini AI ---
st.markdown("---")
st.subheader("💬 Chat với Gemini AI")

# Khởi tạo session state cho lịch sử chat nếu chưa có
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Hiển thị lịch sử chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Ô nhập liệu cho người dùng
user_prompt = st.chat_input("Nhập câu hỏi bất kỳ để hỏi Gemini...")

if user_prompt:
    st.chat_message("user").markdown(user_prompt)
    st.session_state.chat_history.append({"role": "user", "content": user_prompt})
    
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        ai_reply = "❌ Không tìm thấy Khóa API. Hãy cấu hình 'GEMINI_API_KEY' trong Streamlit Secrets."
    else:
        try:
            client = genai.Client(api_key=api_key)
            model = "gemini-2.5-flash"
            
            # Gọi Gemini
            response = client.models.generate_content(
                model=model,
                contents=user_prompt
            )
            ai_reply = response.text

        except APIError as e:
            ai_reply = f"Lỗi khi gọi Gemini API: {e}"
        except Exception as e:
            ai_reply = f"Đã xảy ra lỗi: {e}"
    
    # Hiển thị và lưu trả lời
    st.chat_message("assistant").markdown(ai_reply)
    st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})
