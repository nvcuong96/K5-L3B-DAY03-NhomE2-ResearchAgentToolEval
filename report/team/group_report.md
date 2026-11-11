# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm:
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v3:

## 2. Mục tiêu và cách tiếp cận — PHẦN A: Giới thiệu agent

### A1. Agent này làm được gì

Research Agent của nhóm E2 giúp người dùng **tìm kiếm và tổng hợp thông tin từ nhiều nguồn** (web, Twitter/X, Hacker News, arXiv, URL cụ thể) rồi định dạng thành digest và gửi lên Telegram khi được xác nhận.

**Cách chạy UI:**

```bash
# Từ trong thư mục starter_v0/
streamlit run app.py
```

Dependency đã thêm vào `starter_v0/requirements.txt`: `streamlit>=1.30.0`

**Link dùng thử (deploy):**

> Chạy local: http://localhost:8501
>
> URL public (Cloudflare Tunnel): _(chạy `cloudflared tunnel --url http://localhost:8501` để lấy URL)_

### A2. Tool agent có

| Tên tool | Làm được gì | Tool mới nhóm thêm? |
|---|---|---|
| clarify | Hỏi lại người dùng khi thiếu thông tin hoặc xin xác nhận trước khi gửi | không |
| timeline | Lấy tweet gần nhất từ trang cá nhân của một tài khoản Twitter/X | không |
| social_search | Tìm bài thảo luận trên Twitter/X theo từ khóa | không |
| lookup | Tra cứu tin tức và bài báo trên web qua Tavily | không |
| fetch | Đọc nội dung một URL cụ thể do người dùng cung cấp | không |
| format | Định dạng danh sách tin tức thành digest (brief/sections/bullets/thread) | không |
| send | Gửi nội dung lên Telegram sau khi người dùng xác nhận | không |
| policy | Tra cứu chính sách nội bộ về trích dẫn, an toàn dữ liệu, đạo đức AI | không |
| papers | Tìm bài báo khoa học trên arXiv theo từ khóa | không |
| paper_text | Tải và trích xuất nội dung văn bản từ bài báo arXiv | không |
| hackernews | Lấy danh sách bài nổi bật trên Hacker News (top/new/best) | **có** |

### A3. Câu hỏi mẫu để thử

1. `Lấy cho tôi 3 tin tức nổi bật nhất trên Hacker News hôm nay.`
2. `Tìm kiếm các tweet mới nhất về chủ đề "AI agent" và tổng hợp thành bản tin ngắn.`
3. `Đọc URL này và tóm tắt nội dung: https://example.com/article`
4. `Tìm các bài báo arXiv mới nhất về "multimodal LLM" và liệt kê 5 bài quan trọng nhất.`
5. `Hãy tìm 5 bài báo về "LLM agent" trên arXiv rồi đăng lên Telegram.`

## 3. Giải pháp

> Tóm tắt các thay đổi chính trong `starter_v0/artifacts/system_prompt.md` và `starter_v0/artifacts/tools.yaml`, và tool mới nhóm viết (tên, làm gì, khi nào agent nên gọi).

-

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline |  |  |  |  |
| v1 |  |  |  |  |  |
| v2 |  |  |  |  |  |
| v3 |  |  |  |  |  |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
|  |  |  |  |  |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn).

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
|  |  |  |  |

### B4. Live Chat Evidence

Lấy từ `starter_v0/transcripts/v4_groq_20261111T065440457626.transcript.json`.

| Turn | User Request | Tool Calls | Version Evidence | Outcome |
|---|---|---|---|---|
| 1 | Lấy cho tôi 3 tin tức nổi bật nhất trên HackerNews hôm nay. | `hackernews` | v4 (`v4_groq_20261111T065440457626.transcript.json`) | Gọi đúng tool mới `hackernews`, lấy chính xác 3 tin hot kèm điểm số và link |
| 2 | Tìm cho tôi các bài báo khoa học mới nhất về chủ đề Tool Calling LLM Agents trên arXiv. | `papers`, `format` | v4 (`v4_groq_20261111T065440457626.transcript.json`) | Gọi `papers` tìm trên arXiv và `format` digest chuẩn |
| 3 | Tóm tắt giúp tôi nội dung tài liệu này. | `clarify` | v4 (`v4_groq_20261111T065440457626.transcript.json`) | Phát hiện thiếu link tài liệu, chủ động hỏi lại người dùng thay vì ảo giác |
| 4 | Gửi bản tin tổng hợp này lên kênh Telegram giúp tôi. | `clarify` | v4 (`v4_groq_20261111T065440457626.transcript.json`) | Tuân thủ boundary an toàn: KHÔNG gửi ngay mà hỏi xác nhận yes/no |
| 5 | Có, tôi đồng ý gửi. | `send` | v4 (`v4_groq_20261111T065440457626.transcript.json`) | Sau khi người dùng xác nhận, agent gọi `send` tool chuẩn xác |

### B5a. Required Evidence — Tool mới, unit test, UI

| Item | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Tool mới (`tools/<tên>/`) |  |  |  |
| Unit test tool mới (≥ 3 test/tool) | `pytest` output (0 failed) |  |  |
| UI (lệnh chạy + link dùng thử) |  |  |  |

Tool unit tests: số test đã viết, và một ví dụ lỗi mà unit test bắt được nhưng eval không bắt được.

### B5. Bonus Evidence

Chỉ điền nếu nhóm làm bonus (ghi riêng, tối đa 10 điểm). Tool có sẵn (`send`, `policy`, `papers`, `paper_text`) không tự được bonus.

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| Small Local Model | xem B7 |  |  |
| Hơn 3 tool mới (≥ 4) |  |  |  |
| `send` gửi thật lên Telegram sau xác nhận | transcript |  |  |
| Test challenge (0 skipped / regression test) | `pytest` output |  |  |

Test challenge: số bug tìm được trong tool có sẵn (nếu có), cách sửa, và test regression tương ứng.

### B7. Small Local Model Challenge (bonus)

Chỉ điền nếu nhóm làm bonus này.

| Version | Model (provider) | Prompt/Tools | case_accuracy | tool_routing | argument | multiturn | Run File |
|---|---|---|---|---|---|---|---|
| v3 | (cloud) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v3-<model> | (ollama) | v3 |  |  |  |  |  |
| v4-local |  |  |  |  |  |  |  |
| v5-local |  |  |  |  |  |  |  |

Lỗi đặc thù của model nhỏ (đếm từ run JSON):

| Failure Pattern | Count | Example Case | Fix Tried | Helped? |
|---|---|---|---|---|
| wrong / hallucinated tool |  |  |  |  |
| invalid JSON args (`_invalid_json_arguments`) |  |  |  |  |
| no tool call / answered directly |  |  |  |  |
| missed `clarify` |  |  |  |  |
| repeated / unnecessary calls |  |  |  |  |

- Cái gì giúp model nhỏ gọi tool đúng hơn nhất? Bằng chứng?
- Bản prompt tối ưu cho local chạy trên model cloud thì sao?
- Khi nào nhóm sẽ chọn model local thay vì cloud cho agent này?

## 5. Khó khăn và cách xử lý

> Khó khăn chính và cách nhóm xử lý. Nếu gặp lỗi kỹ thuật (provider lỗi, hết quota API, tool không chạy), mô tả lỗi và dẫn bằng chứng: run JSON, log, ảnh chụp.

-

## 6. Tổng hợp đóng góp

Chi tiết đóng góp của từng thành viên nằm trong [TEAM.md](../../TEAM.md) và các báo cáo cá nhân `report/team/MSSV_HoTen.md`.

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- Fix nào thuộc `system_prompt.md`?
- Fix nào thuộc `tools.yaml`?
- Failure nào cần review thủ công thay vì chấm tự động?
- Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?

## 8. Tài liệu tham khảo

-
