# Báo cáo cá nhân — Nguyễn Văn Hiếu-2A202603746

## 1. Thông tin thành viên

- Họ tên: Nguyễn Văn Hiếu
- MSSV: 2A202603746
- Email: 26ai.hieunv3@vinuni.edu.vn

## 2. Phần việc phụ trách

- Step 4b: viết unit test offline cho các tool của research agent.
- Viết bộ regression test cho tool mới `hackernews`.

## 3. Đóng góp cụ thể

- Thay toàn bộ 17 stub `pytest.skip(...)` trong `starter_v0/tests/test_tools_todo.py` bằng test thực tế.
- Viết test cho các tool có sẵn: `clarify`, `format`, `send`, `lookup`, `fetch`, `timeline`, `social_search` và `policy`.
- Viết 3 test cho tool mới `hackernews`: happy path, input `story_type` ngoài enum và nhánh timeout/network failure.
- Dùng `fake_http` và `monkeypatch` để test chạy offline, không gọi API thật và không dùng API key thật.
- Regression test đã phát hiện hai lỗi trong Hacker News: input `story_type` sai vẫn gọi API; timeout bị raise thay vì trả error dict. Người phụ trách tool đã sửa và test xác nhận lại trên `main`.

## 4. Bằng chứng

- File: `starter_v0/tests/test_tools_todo.py`
- Nhánh: `VanHieu/step4b-tool-tests`
- Commit: `82a3175 test: complete tool unit test challenge`
- Lệnh kiểm tra:

  ```powershell
  .venv\Scripts\python.exe -m pytest -v tests/test_tools_todo.py
  ```

- Kết quả ban đầu khi phát hiện lỗi Hacker News: `15 passed, 2 failed, 0 skipped` trong file Step 4b; toàn suite: `82 passed, 2 failed, 0 skipped`.
- Kết quả xác nhận sau bản sửa trên `main` (commit `01c232a`): `17 passed` trong file Step 4b; toàn suite: `84 passed, 0 failed, 0 skipped`.

## 5. Tự đánh giá

- Hoàn thành phần viết test Step 4b, gồm challenge thay toàn bộ stub và ba test bắt buộc cho tool mới.
- Phần việc đã giúp phát hiện lỗi code của tool mà eval routing không phát hiện được; regression test xác nhận bản sửa đạt `0 failed, 0 skipped`.
