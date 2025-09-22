import re

def clean_text(text: str) -> str:
    if not text:
        return ""
    
    text = re.sub(r"<\|.*?\|>", "", text)
    text = re.sub(r"</?s>", "", text)
    text = re.sub(r"\*+", "", text)
    text = text.replace("▁", " ")
    text = text.replace("\\n", "\n")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def format_text(text: str) -> str:
    if not text:
        return ""
    
    text = re.sub(r"\s*(\d+)\.\s*", r"\n\1. ", text)
    text = re.sub(r"\.\s+", ".\n", text)
    text = re.sub(r"\n+", "\n", text)
    return text.strip()


def clean_and_format(text: str) -> str:
    """Kết hợp clean và format"""
    cleaned = clean_text(text)
    formatted = format_text(cleaned)
    return formatted

def smart_format_text(text: str) -> str:
    """
    Format text tự động xuống dòng sau mỗi ý:
    - Sử dụng dấu chấm, dấu '-', số mục, hoặc các câu ngắn.
    - Giữ khoảng trắng hợp lý.
    """
    if not text:
        return ""
    
    # clean cơ bản
    text = clean_text(text)

    # xuống dòng trước số mục
    text = re.sub(r"(\d+)\.\s", r"\n\1. ", text)
    # xuống dòng sau dấu gạch ngang
    text = re.sub(r"\s-\s", r"\n- ", text)
    
    # xuống dòng sau câu dài (>60 ký tự) hoặc sau dấu chấm
    sentences = re.split(r'(?<=[.])\s+', text)
    formatted = ""
    for s in sentences:
        s = s.strip()
        if not s:
            continue
        # nếu s quá dài, cắt ra thành nhiều dòng (~60 ký tự)
        while len(s) > 60:
            # tìm khoảng trắng gần 60 ký tự để xuống dòng
            idx = s.rfind(" ", 0, 60)
            if idx == -1:
                idx = 60
            formatted += s[:idx].strip() + "\n"
            s = s[idx:].strip()
        formatted += s + "\n"
    
    return formatted.strip()
