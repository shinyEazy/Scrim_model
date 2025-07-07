import requests
import json
import os
from dotenv import load_dotenv
import time

load_dotenv()

url = "https://api.openai.com/v1/chat/completions"

system_prompt = """
Bạn là trợ lý tạo dữ liệu QA. Nhiệm vụ: Tạo 100 cặp Q&A từ thông tin người dùng cung cấp với các yêu cầu:
1. Câu hỏi phải đa dạng: hỏi sự kiện, định nghĩa, so sánh, nguyên nhân-kết quả
2. Câu trả lời ngắn gọn (1-2 câu), chính xác với nội dung gốc
3. Định dạng nghiêm ngặt: 
   "Q1: [Nội dung]"
   "A1: [Trả lời]"
   "Q2: ..."
   "A2: ..."
4. Chỉ sử dụng thông tin từ dữ liệu đầu vào
5. Tạo đủ 100 cặp Q&A
6. Các cặp phải độc lập với nhau
"""

content_with_weight = "Quyền lợi của sinh viên 1. Được hưởng đầy đủ chế độ, chính sách hiện hành của Đảng, Nhà nước cũng như các quy chế, quy định của Đại học Quốc gia Hà Nội và của đơn vị đào tạo. 2. Được phép thôi học vì lý do chủ quan của cá nhân, trong trường hợp này, sinh viên phải hoàn trả cho đơn vị đào tạo toàn bộ kinh phí đào tạo từ ngân sách nhà nước trong thời gian theo học. 3. Sinh viên được xin nghỉ học tạm thời và bảo lưu kết quả đã học trong các trường hợp sau đây: a) Được động viên vào lực lượng vũ trang; b) Được cơ quan có thẩm quyền điều động, đại diện quốc gia tham dự các kỳ thi, giải đấu quốc tế; c) Bị ốm, thai sản hoặc tai nạn phải điều trị thời gian dài có chứng nhận của cơ sở khám bệnh, chữa bệnh có thẩm quyền theo quy định của Bộ Y tế; d) Vì lý do cá nhân khác nhưng phải học tối thiểu 01 học kỳ và không thuộc các trường hợp bị xem xét buộc thôi học hoặc xem xét kỷ luật và phải đạt điểm trung bình chung tích lũy tổi thiểu 2,0. Thời gian nghỉ học tạm thời vì nhu cầu cá nhân được tính vào thời gian tối đa được phép học. 4. Ngoài những quyền lợi chung đối với sinh viên chương trình đào tạo chuẩn, sinh viên thuộc chương trình đào tạo tài năng, chất lượng cao còn được hưởng các quyền lợi sau: a) Được các nhà khoa học đầu ngành, các giáo sư, giảng viên có trình độ, kinh nghiệm và có uy tín trong nước, quốc tế trực tiếp giảng dạy, hướng dẫn nghiên cứu khoa học; b) Được ưu tiên cung cấp hoặc sử dụng các tài liệu học tập; được ưu tiên sử dụng các phương tiện, trang thiết bị kỹ thuật, thư viện và hệ thống internet phục vụ cho học tập và nghiên cứu khoa học; c) Được ưu tiên xét cấp học bổng khuyến khích phát triển và học bổng của các tổ chức, cá nhân trong, ngoài nước. Những sinh viên ở xa được ưu tiên bố trí chỗ ở trong ký túc xá; d) Được ưu tiên xét chọn đi học ở nước ngoài hoặc theo các chương trình hợp tác quốc tế của Đại học Quốc gia Hà Nội, của đơn vị đào tạo."


headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"
}

payload = {
  "model": "gpt-4.1-nano",
  "messages": [
    {
      "role": "system",
      "content": system_prompt
    },
    {
      "role": "user",
      "content": f"Đây là thông tin đầu vào:\n\n{content_with_weight}"
    }
  ],
  "temperature": 0.6
}

try:
    start_time = time.time()

    response = requests.post(url, headers=headers, data=json.dumps(payload))
    response.raise_for_status()

    end_time = time.time()
    total_time = end_time - start_time

    response_data = response.json()
    response_data['total_time'] = total_time

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(response_data, f, indent=4, ensure_ascii=False)
    print(f"✅ Response saved to data.json (total_time: {total_time:.2f} seconds)")
except requests.exceptions.RequestException as e:
    print(f"❌ Request failed: {e}")
