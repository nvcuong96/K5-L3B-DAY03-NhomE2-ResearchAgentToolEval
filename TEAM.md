# Team

## Thông tin nhóm

- Tên nhóm: Nhóm E2
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-NhomE2-ResearchAgentToolEval`
- URL repo, nhánh nộp, commit chốt: `https://github.com/nvcuong96/K5-L3B-DAY03-NhomE2-ResearchAgentToolEval`, nhánh `main` / `DoanCongHai`

## Thành viên

| STT | Họ tên | MSSV | Email | GitHub | Vai trò |
| --: | ------ | ---- | ----- | ------ | ------- |
|   1 | Đoàn Công Hải | *(Điền MSSV)* | haidoan2426@gmail.com | haidoan2426 | Trưởng nhóm, CP4, CP5 (UI & Báo cáo), Unit tests |
|   2 | Nguyễn Văn Cường | 2A202603750 | nvcuong9696@gmail.com | nvcuong96 | Thành viên, CP3 (Tool mới `hackernews`), Phân tích lỗi |
|   3 | Lê Nguyễn Anh Khôi | | lnakhoi5a@gmail.com | KN16 | Thành viên, CP1, CP2 (Tối ưu Prompt & Tools v0-v3) |

## Cá nhân

Mỗi thành viên đồng thời tạo một báo cáo riêng trong `report/` theo dạng:

```text
report/team/MSSV_HoTen.md
```

Ví dụ: `report/team/DoanCongHai.md`.

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
