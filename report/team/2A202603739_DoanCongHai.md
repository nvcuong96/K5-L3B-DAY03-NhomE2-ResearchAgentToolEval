# Báo cáo cá nhân — Đoàn Công Hải

## 1. Thông tin thành viên

- **Họ tên:** Đoàn Công Hải
- **MSSV:** 2A202603739
- **Email:** 26ai.haidc@vinuni.edu.vn
- **Nhóm:** Nhóm E2 — Lớp L3B
- **Vai trò:** Thành viên (CP4, CP5, UI & Báo cáo)

## 2. Phần việc phụ trách

- **CP4 (Bộ Eval của nhóm):** Thiết kế bộ dữ liệu đánh giá 10 test case chuyên biệt (`starter_v0/data/eval_group.json`), thực thi đánh giá phiên bản `v4` với tool mới `hackernews`.
- **CP3 (Unit tests tool mới):** Phát triển bộ 3 unit test cho tool `hackernews` trong `starter_v0/tests/test_tools_todo.py`, xử lý các trường hợp ngoại lệ, ép kiểu an toàn và timeout.
- **CP5 (Giao diện người dùng UI & Live Chat):** Xây dựng ứng dụng Streamlit `starter_v0/app.py`, cấu hình provider động, tích hợp xác thực API key và tích hợp gửi tin nhắn thật qua bot Telegram (`@lab3_research_bot`).
- **Báo cáo nhóm & cá nhân:** Phối hợp tổng hợp kết quả, ghi nhận bằng chứng transcript thực tế và hoàn thiện báo cáo nhóm `group_report.md` cùng báo cáo cá nhân.

## 3. Đóng góp cụ thể

1. **Thiết kế 10 Test Cases trong `eval_group.json`:**
   - 5 Single-turn cases: Kiểm tra routing chính xác vào tool mới `hackernews` (`G01`, `G02`), tìm kiếm bài báo khoa học trên arXiv (`G03`), tra cứu quy định bảo mật nội bộ `policy` (`G04`), và ranh giới an toàn không tự ý gửi tin ra ngoài khi chưa xác nhận (`G05`).
   - 5 Multi-turn cases: Chuyển đổi ngữ cảnh sang xem tin tức Hacker News (`G06`), xử lý thiếu URL rồi bổ sung ở lượt sau (`G07`), thay đổi tác giả và số lượng tweet cần lấy (`G08`), định dạng bản tin và gửi Telegram sau khi có xác nhận rõ ràng (`G09`), và đọc trích xuất nội dung bài báo arXiv theo ID (`G10`).
   - Thực thi lệnh đánh giá: `python run_eval.py --provider groq --model openai/gpt-oss-20b --version v4 --suite group --eval-cases data/eval_group.json`, đạt độ chính xác routing 90% (8/10 case passed).

2. **Viết Unit Test cho Tool mới (`tests/test_tools_todo.py`):**
   - Viết 3 test case theo chuẩn RUBRIC:
     - `test_my_new_tool_happy_path`: Kiểm thử luồng hoạt động chuẩn, mock API Hacker News lấy tin top, kiểm tra cấu trúc dữ liệu trả về và tóm tắt điểm số/bình luận.
     - `test_my_new_tool_bad_input_from_model`: Kiểm tra khả năng chịu lỗi khi model truyền tham số sai kiểu (`limit="not_a_number"`) hoặc giá trị ngoài enum (`story_type="invalid_type_xyz"`), đảm bảo tool tự động fallback an toàn mà không bị crash.
     - `test_my_new_tool_failure_returns_error_dict`: Giả lập lỗi mạng `TimeoutError`, đảm bảo tool bắt exception và trả về dictionary lỗi chuẩn `{tool, error, message}` thay vì làm gián đoạn chương trình.
   - Kết quả: `pytest` đạt 70 passed, 0 failed.

3. **Phát triển Web UI Streamlit (`starter_v0/app.py`):**
   - Tạo giao diện chat trực quan với Streamlit.
   - Thêm sidebar cấu hình Provider linh hoạt (`groq`, `openrouter`, `openai`, `gemini`, `ollama`), tự động điền model tương ứng.
   - Bổ sung ô nhập API Key và cấu hình Telegram Bot (`TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`) trực tiếp trên giao diện.
   - Hiển thị chi tiết từng tool call trong giao diện chat dưới dạng dropdown expander.
   - Tự động xuất transcript theo chuẩn quy định vào thư mục `starter_v0/transcripts/`.

4. **Tích hợp gửi tin nhắn thật lên Telegram:**
   - Cấu hình bot `@lab3_research_bot` và kết nối thành công với nhóm Telegram `Hải and Lab3VinUni` (`-1004487409127`).
   - Bổ sung cơ chế tự động fallback trong `tools/send/tool.py`: Khi Telegram từ chối định dạng Markdown do ký tự đặc biệt, hệ thống tự động gửi lại dưới dạng plain text, bảo đảm tin nhắn luôn được gửi thành công đến người dùng.

## 4. Bằng chứng

- **Commits / Code:**
  - Commit `b99af04`: `feat: add 10 eval cases into eval_group.json`
  - Các tệp xây dựng & đóng góp chính:
    - `starter_v0/data/eval_group.json`
    - `starter_v0/tests/test_tools_todo.py`
    - `starter_v0/tools/hackernews/tool.py`
    - `starter_v0/tools/send/tool.py`
    - `starter_v0/app.py`
    - `starter_v0/requirements.txt`
    - `report/team/group_report.md`
- **File kết quả đánh giá (Run JSON):**
  - `starter_v0/runs/v4_B_group_groq_20261111T075843555174.json`
- **File Transcript thực tế (Live Chat):**
  - `starter_v0/transcripts/v4_groq_20261111T065440457626.transcript.json` (chứng minh đủ 5 lượt hội thoại: câu hỏi thường, hỏi lại khi thiếu thông tin, và xác nhận trước khi gửi Telegram).
- **Công cụ AI & Cách tự kiểm tra:**
  - Sử dụng AI hỗ trợ phân tích cấu trúc schema của Hacker News API và debug Telegram Markdown parsing error.
  - Tự kiểm tra độc lập bằng cách chạy `pytest starter_v0/tests/` (xanh 100%), chạy `run_eval.py` trên model Groq thật, và kiểm tra tin nhắn hiển thị thực tế trên ứng dụng Telegram.

## 5. Tự đánh giá

- **Mức độ hoàn thành công việc:** 100% các mục tiêu cam kết theo CHECKPOINTS (CP3, CP4, CP5).
- **Điểm nổi bật:**
  - Hoàn thiện trọn vẹn cả ứng dụng UI và tích hợp Telegram gửi tin nhắn thực tế.
  - Bộ 10 test case đa dạng, phản ánh sát thực tế tương tác đa lượt và bảo vệ ranh giới an toàn của Agent.
- **Điểm cần cải thiện:** Cần nghiên cứu thêm kỹ thuật few-shot prompt để tăng tỷ lệ pass ở các case đa lượt có chuyển đổi ngữ cảnh phức tạp.
