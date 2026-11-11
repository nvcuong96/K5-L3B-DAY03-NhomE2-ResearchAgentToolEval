# Team

## Thông tin nhóm

- Tên nhóm: Nhóm E2
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-NhomE2-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: `https://github.com/nvcuong96/K5-L3B-DAY03-NhomE2-ResearchAgentToolEval`, nhánh `main`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Nguyễn Văn Cường | 2A202603750 | nvcuong9696@gmail.com | nvcuong96 | Trưởng nhóm, CP3 (Tool mới `hackernews`), Phân tích lỗi |
|   2 | Đoàn Công Hải | 2A202603739 | haidoan2004426@gmail.com | rawser246 | Thành viên, CP4, CP5 (UI & Báo cáo), Tích hợp Telegram |
|   3 | Nguyễn Văn Hiếu | 2A202603746 | 26ai.hieunv3@vinuni.edu.vn | | Thành viên, Step 4b (Unit test suite & Regression tests) |
|   4 | Lê Nguyễn Anh Khôi | | lnakhoi5a@gmail.com | KN16 | Thành viên, CP1, CP2 (Tối ưu Prompt & Tools v0-v3) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/2A202603750_NguyenVanCuong.md`, `report/team/2A202603739_DoanCongHai.md`.

## NguyenVanCuong

### Phần việc phụ trách

- Trưởng nhóm, điều phối tiến độ chung của nhóm.
- Chịu trách nhiệm chính Checkpoint 3: Thiết kế, cài đặt, đăng ký và tích hợp tool mới `hackernews` (`starter_v0/tools/hackernews/`).
- Phân tích lỗi (Failure Analysis) và tổng hợp dữ liệu chạy baseline.

### Đóng góp cụ thể

- Hiện thực hàm `get_hn_stories` gọi public Hacker News Firebase API, giới hạn số bài trả về từ 1 đến 20 và chuẩn hóa dữ liệu thành tiêu đề, URL, nguồn, điểm số và số bình luận.
- Thêm URL dự phòng trỏ tới trang thảo luận Hacker News nếu bài viết không có URL riêng; kiểm tra loại bài viết hợp lệ (`top`, `new`, `best`) và trả lỗi theo cấu trúc chuẩn dùng chung khi API hoặc đầu vào gặp sự cố.
- Soạn thảo tài liệu `TOOL.md`, khai báo schema tham số trong `tools.yaml` và đăng ký tool trong `tools/__init__.py`.
- Viết 3 unit test cho tool `hackernews` bao phủ kết quả bình thường, loại bài viết không hợp lệ và lỗi mạng (dùng mock để không phụ thuộc API thật).

### Bằng chứng

- File: `starter_v0/tools/hackernews/tool.py`, `starter_v0/tools/hackernews/TOOL.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/tools/__init__.py`.
- Commit: `c12890d` (thêm tool và tích hợp); `01c232a` (hoàn thiện xử lý phản hồi và lỗi).
- Báo cáo cá nhân: `report/team/2A202603750_NguyenVanCuong.md`.

## DoanCongHai

### Phần việc phụ trách

- Chịu trách nhiệm chính Checkpoint 4 (Bộ test case đánh giá nhóm 10 case) và Checkpoint 5 (Xây dựng Web UI Streamlit, tích hợp Telegram bot gửi tin nhắn thật, thu thập live transcript).
- Viết 3 unit test cho tool mới `hackernews` trong `tests/test_tools_todo.py`.
- Viết báo cáo cá nhân và hoàn thiện báo cáo nhóm `group_report.md`.

### Đóng góp cụ thể

- Soạn thảo 10 test case trong `starter_v0/data/eval_group.json` (5 single-turn và 5 multi-turn) bao phủ các khía cạnh: routing tool mới, quy định nội bộ, ranh giới xác nhận Telegram.
- Chạy đánh giá bộ test case nhóm trên model Groq đạt 80% case accuracy và 90% routing accuracy (`runs/v4_B_group_groq_20261111T075843555174.json`).
- Viết 3 unit test cho `hackernews` kiểm thử happy path, bad input handling, và failure timeout, giúp `pytest` đạt 70 passed, 0 failed.
- Phát triển giao diện Streamlit `starter_v0/app.py`, cấu hình động model, API key và tích hợp gửi tin nhắn thật vào Telegram group `Hải and Lab3VinUni`.
- Thực hiện phiên live chat 5 lượt tạo bằng chứng transcript `v4_groq_20261111T065440457626.transcript.json`.

### Bằng chứng

- Commit `b99af04`: `feat: add 10 eval cases into eval_group.json`
- Code UI: `starter_v0/app.py`, `starter_v0/requirements.txt`
- Unit tests: `starter_v0/tests/test_tools_todo.py`
- Run file: `starter_v0/runs/v4_B_group_groq_20261111T075843555174.json`
- Transcript: `starter_v0/transcripts/v4_groq_20261111T065440457626.transcript.json`
- Báo cáo cá nhân: `report/team/DoanCongHai.md`

## NguyenVanHieu

### Phần việc phụ trách

- Step 4b: viết unit test offline cho các tool của research agent.
- Viết bộ regression test cho tool mới `hackernews`.

### Đóng góp cụ thể

- Thay toàn bộ 17 stub `pytest.skip(...)` trong `starter_v0/tests/test_tools_todo.py` bằng test thực tế.
- Viết test cho các tool có sẵn: `clarify`, `format`, `send`, `lookup`, `fetch`, `timeline`, `social_search` và `policy`.
- Viết regression test cho tool mới `hackernews`: happy path, input `story_type` ngoài enum và nhánh timeout/network failure.
- Dùng `fake_http` và `monkeypatch` để test chạy offline, không gọi API thật và không dùng API key thật.
- Regression test đã phát hiện hai lỗi trong Hacker News: input `story_type` sai vẫn gọi API; timeout bị raise thay vì trả error dict. Người phụ trách tool đã sửa và test xác nhận lại trên `main`.

### Bằng chứng

- File: `starter_v0/tests/test_tools_todo.py`
- Nhánh: `VanHieu/step4b-tool-tests`
- Commit: `82a3175 test: complete tool unit test challenge`
- Kết quả test: 87 passed (17 passed trong file Step 4b, 0 failed, 0 skipped)
- Báo cáo cá nhân: `report/team/2A202603746_NguyenVanHieu.md`
