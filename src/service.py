from dto import ChatResponse, ChatRequest
import requests
from fastapi.responses import StreamingResponse
import json
from clean_text import clean_and_format, clean_text, format_text, smart_format_text
import re

API_KEY = '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'
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-chat"

system_promt = (
    "Bạn là 'Trợ lý triết học' chuyên về Chủ nghĩa duy vật lịch sử (Chương 3: Hình thái kinh tế-xã hội — "
    "biện chứng giữa cơ sở hạ tầng và kiến trúc thượng tầng). "
    "QUY TẮC: 1) Nếu câu hỏi có thể trả lời bằng 'Có' hoặc 'Không' -> trả lời **chính xác một từ duy nhất** 'Có' hoặc 'Không' (không dấu chấm, không giải thích). "
    "2) Nếu câu hỏi yêu cầu giải thích -> trả lời ngắn gọn 1-3 câu, chỉ tập trung Chương 3. "
    "3) Nếu không liên quan -> trả 'Tôi chỉ chuyên về Chương 3.' "
    "4) Nếu không chắc -> trả 'Không chắc.'"
    "5) Ví dụ câu hỏi: 'Bạn có biết về Chủ nghĩa duy vật lịch sử không?' -> 'Có', chỉ một từ duy nhất, không giải thích. Nếu người dùng cần giải thích, họ sẽ hỏi tiếp."
    "6) không trả lời lan man ngoài chủ đề."
    "7) REMEMBER TẬP TRUNG VÀO Ý CHÍNH VÀ KHÔNG TRẢ LỜI LAN MAN. Ví dụ: 'Có mấy hình thái kinh tế-xã hội?' -> 'Có 5 hình thái kinh tế-xã hội.' (Chỉ một câu, không giải thích thêm)."
    "8) Nếu người dùng hỏi về các chương khác ngoài Chương 3 -> trả lời 'Tôi chỉ chuyên về Chương 3.'"
    "9) Mỗi câu trả lời của bạn chỉ gồm một đoạn văn ngắn gọn, tập trung vào ý chính, không lan man ngoài chủ đề."
)

def chat_service(request: ChatRequest):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Bạn là một trợ lý triết học chuyên về Chủ nghĩa duy vật lịch sử."},
            {"role": "user", "content": request.message},
        ],
        "temperature": 0.7,
        "max_tokens": 500,
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    data = response.json()
    raw_answer = data["choices"][0]["message"]["content"]
    formatted_answer = clean_and_format(raw_answer)
    return {"answer": formatted_answer}


def chat_service_streaming(request: ChatRequest):
    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": system_promt},
            {"role": "user", "content": request.message},
        ],
        "temperature": 0.7,
        "max_tokens": 500,
        "stream": True
    }
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    def event_stream():
        buffer = ""
        with requests.post(API_URL, headers=headers, json=payload, stream=True) as r:
            for line in r.iter_lines():
                if line:
                    decoded = line.decode("utf-8")
                    if decoded.startswith("data: "):
                        data = decoded[len("data: "):]
                        if data.strip() == "[DONE]":
                            if buffer.strip():
                                yield smart_format_text(buffer)
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk["choices"][0]["delta"].get("content", "")
                            if delta:
                                buffer += delta
                                if re.search(r"\d+\.|\-|\. ", buffer):
                                    yield smart_format_text(buffer)
                                    buffer = ""
                        except Exception:
                            continue

    return StreamingResponse(event_stream(), media_type="text/event-stream")