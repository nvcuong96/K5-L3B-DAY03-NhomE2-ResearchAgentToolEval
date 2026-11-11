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
|   3 | Nguyễn Văn Hiếu | 2A202603746 | 26ai.hieunv3@vinuni.edu.vn | lunaHieu | Thành viên, Step 4b (Unit test suite & Regression tests) |
|   4 | Lê Nguyễn Anh Khôi | 2A202603755 | lnakhoi5a@gmail.com | KN16 | Thành viên, CP1, CP2 (Tối ưu Prompt & Tools v0-v3), Groq Provider |

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

### Bằng chứng

- File: `starter_v0/tools/hackernews/tool.py`, `starter_v0/tools/hackernews/TOOL.md`, `starter_v0/artifacts/tools.yaml`, `starter_v0/tools/__init__.py`.
- Commit: `c12890d` (thêm tool và tích hợp); `01c232a` (hoàn thiện xử lý phản hồi và lỗi).
- Báo cáo cá nhân: `report/team/2A202603750_NguyenVanCuong.md`.

## DoanCongHai

### Phần việc phụ trách

- Chịu trách nhiệm chính Checkpoint 4 (Bộ test case đánh giá nhóm 10 case) và Checkpoint 5 (Xây dựng Web UI Streamlit, tích hợp Telegram bot gửi tin nhắn thật, thu thập live transcript).
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
- Viết 3 unit test cho tool `hackernews` bao phủ kết quả bình thường, loại bài viết không hợp lệ và lỗi mạng (dùng mock để không phụ thuộc API thật).

### Bằng chứng

- File: `starter_v0/tests/test_tools_todo.py`
- Nhánh: `VanHieu/step4b-tool-tests`
- Commit: `82a3175 test: complete tool unit test challenge`
- Kết quả test: 87 passed (17 passed trong file Step 4b, 0 failed, 0 skipped)
- Báo cáo cá nhân: `report/team/2A202603746_NguyenVanHieu.md`

## LeNguyenAnhKhoi

### Phần việc phụ trách

- Chịu trách nhiệm chính Checkpoint 1 & Checkpoint 2 (CP1, CP2): Thiết lập baseline v0, thực thi chu trình lặp cải tiến Hypothesis – Fix – Measure từ v1 đến v3; chuẩn hóa `system_prompt.md` và `tools.yaml`.
- Phát triển và tích hợp module Groq Provider (`groq_provider.py`) hỗ trợ cơ chế Tool Calling / Function Calling.
- Ghi nhận và kiểm toán toàn bộ chu trình thực nghiệm vào `version_log.csv`.

### Đóng góp cụ thể

- Lập trình adapter kết nối Groq API thông qua OpenAI-compatible client (`starter_v0/providers/groq_provider.py`), xử lý chuyển đổi format function calling schema và quản lý ngoại lệ; bổ sung tùy chọn `groq` đồng bộ vào `starter_v0/providers/__init__.py`, `starter_v0/scripts/preflight_provider.py` và `starter_v0/run_eval.py`.
- Khảo sát Baseline v0: Chạy benchmark phát hiện lỗi gốc Provider Error HTTP 400 tại Case R13 (`Tool choice is required`), xung đột ranh giới tại Case R12 và thiếu ánh xạ handle tại Case R01.
- Vòng lặp v1: Bổ sung cấu trúc schema tường minh và quy tắc Multi-Tool calling trong `artifacts/system_prompt.md`, khắc phục triệt để lỗi HTTP 400 tại Case R13.
- Vòng lặp v2: Xử lý hiện tượng suy giảm năng lực (Regression tại Case R01) bằng cách nhúng trực tiếp tri thức ánh xạ (`Sam Altman -> sama`) vào mô tả của tool `timeline` trong `artifacts/tools.yaml` thay vì nhồi nhét vào prompt.
- Vòng lặp v3: Tái cấu trúc `artifacts/system_prompt.md`, thiết lập nguyên tắc phân cấp cưỡng chế với Confirmation Boundary là ưu tiên cao nhất (Highest Priority), giải quyết triệt để xung đột ranh giới xác nhận Telegram `yes_no` tại Case R12.
- Kiểm toán và ghi chép trung thực toàn bộ diễn tiến thực nghiệm v0–v3 vào `version_log.csv` theo chuẩn quy trình Hypothesis – Fix – Measure.

### Bằng chứng

- File:
  - `starter_v0/providers/groq_provider.py`
  - `starter_v0/providers/__init__.py`
  - `starter_v0/scripts/preflight_provider.py`
  - `starter_v0/run_eval.py`
  - `artifacts/system_prompt.md`
  - `artifacts/tools.yaml`
  - `version_log.csv`
- Báo cáo cá nhân: `report/team/2A202603755_LeNguyenAnhKhoi.md`
