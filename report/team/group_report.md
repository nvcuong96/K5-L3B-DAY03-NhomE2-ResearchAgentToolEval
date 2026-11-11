# Báo cáo nhóm — Day 03 Research Agent Tool Eval

> Báo cáo gồm 2 phần có hạn khác nhau:
> - **Phần A (mục 2)** — giới thiệu agent, ngắn gọn 1 trang. **Xong trước Team showdown (16:30)** để team khác hiểu nhanh agent có tool gì, làm được gì. Có thể làm thêm poster `report/team/poster.html` hoặc `poster.svg`.
> - **Phần B (mục 3–7)** — chi tiết và bằng chứng, dựa trên log thật. Hoàn thiện trước deadline nộp bài.
>
> Mỗi bảng phải trỏ được tới file thật: run JSON, transcript, commit. Cách chấm xem [RUBRIC.md](../../RUBRIC.md).

## 1. Thông tin nhóm

- Tên nhóm: Nhóm E2
- Lớp: L3B
- Repo nhóm: `K5-L3B-DAY03-NhomE2-ResearchAgentToolEval`
- Thành viên và phân công: xem [TEAM.md](../../TEAM.md)
- Provider/model dùng cho v0–v4: Groq (`openai/gpt-oss-20b`)

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

### 3.1. Tối ưu System Prompt (`artifacts/system_prompt.md`)
- **v1**: Bổ sung quy tắc định tuyến cơ bản (routing rules), phân tách rõ nhiệm vụ tra cứu tin tức thời sự chung (`lookup`) và đọc bài viết theo URL (`fetch`), tránh việc agent tự suy diễn hoặc gọi tool sai.
- **v3**: Thiết lập ranh giới an toàn nghiêm ngặt (confirmation boundary): Khi người dùng yêu cầu gửi tin ra ngoài (`send`), agent tuyệt đối không được gọi `send` trực tiếp mà bắt buộc phải gọi `clarify` với `response_type="yes_no"` để người dùng xác nhận rõ ràng.

### 3.2. Cải tiến Tool Declarations (`artifacts/tools.yaml`)
- **v2**: Chuẩn hóa schema tham số, thêm enum chặt chẽ cho `search_type` (`Latest`, `Top`), `timeframe` (`day`, `week`, `month`, `year`), `topic` (`general`, `news`). Bổ sung hướng dẫn mapping tự động các tên nhân vật nổi tiếng sang Twitter handle (ví dụ: Sam Altman -> `sama`, Elon Musk -> `elonmusk`).
- **v4**: Đăng ký tool mới `hackernews` với mô tả rõ ràng: gọi khi người dùng nhắc tới Hacker News/HN; không nhầm lẫn với `lookup` hay `timeline`.

### 3.3. Tool mới tự phát triển: `hackernews` (`tools/hackernews/`)
- **Người phụ trách chính**: Nguyễn Văn Cường (Trưởng nhóm).
- **Chức năng**: Tích hợp trực tiếp với Firebase API chính thức của Hacker News (`https://hacker-news.firebaseio.com/v0/`) để lấy danh sách bài viết nổi bật (`top`), mới nhất (`new`), hoặc hay nhất (`best`) kèm điểm số (`score`), số lượng bình luận (`descendants`) và liên kết gốc. Bổ sung URL dự phòng trỏ về trang thảo luận Hacker News nếu bài viết không có link riêng (`https://news.ycombinator.com/item?id=...`).
- **Khi nào gọi**: Agent gọi khi người dùng hỏi tin tức trên Hacker News / HN. Tool có sẵn cơ chế bắt lỗi timeout, fallback enum và chuẩn hóa kiểu dữ liệu trả về theo format dùng chung của hệ thống.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| v0 | baseline | Đánh giá baseline ban đầu chưa tối ưu prompt & tools.yaml | 0.00 | 0.50 | `runs/v0_B_base_groq_20261110T183250185623.json` |
| v1 | system_prompt.md | Thêm rule routing trong system prompt giúp giảm lỗi `wrong_tool` và thiếu thông tin | 0.50 | 0.75 | `runs/v1_B_base_groq_20261110T191431050855.json` |
| v2 | tools.yaml | Chuẩn hóa schema, mô tả tham số và mapping handle giúp khắc phục `wrong_arg_value` | 0.75 | 0.84 | `runs/v2_B_base_groq_20261110T192238230794.json` |
| v3 | system_prompt.md | Thiết lập ranh giới xác nhận yes/no trước khi `send`, làm rõ tool boundaries | 0.84 | 0.95 | `runs/v3_B_base_groq_20261110T193156877236.json` |
| v4 | tools.yaml & code | Đánh giá bộ test case nhóm với tool mới `hackernews`, đạt routing tuyệt đối | 0.95 | 0.80 | `runs/v4_B_group_groq_20261111T075843555174.json` |

### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run v0 `runs/v0_B_base_groq_20261110T183250185623.json`.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| `R01_user_tweets_routing` | wrong_arg_value | `timeline` | Model lấy handle `samaltman` thay vì `sama` | Thêm ví dụ mapping cụ thể `Sam Altman -> sama` trong description của `timeline` |
| `R10_missing_handle` | missing_info | `timeline` | Thiếu handle nhưng model tự bịa và gọi `timeline` | Bổ sung quy tắc trong prompt: thiếu handle bắt buộc gọi `clarify` |
| `R11_missing_url` | missing_info | `fetch` | Thiếu link nhưng model tự gọi `fetch` | Thêm rule: thiếu URL cụ thể phải dừng lại hỏi người dùng bằng `clarify` |
| `R12_confirm_before_send` | wrong_boundary | `send` | Chưa có xác nhận nhưng model tự ý gọi tool `send` | Thiết lập boundary bắt buộc gọi `clarify` với `response_type="yes_no"` |
| `R14_out_of_scope_coding` | out_of_scope | `send` | Yêu cầu viết code ngoài phạm vi nhưng agent gọi nhầm `send` | Thêm chỉ dẫn từ chối lịch sự, không gọi tool khi gặp câu hỏi ngoài phạm vi |

### B3. Team Eval Cases

Liệt kê đúng 10 case trong `starter_v0/data/eval_group.json` (5 single turn + 5 multi turn). Run file: `runs/v4_B_group_groq_20261111T075843555174.json`.

| Case ID | What It Tests | Expected Tool/Behavior | Result |
|---|---|---|---|
| `G01_hackernews_top_default` | Nhắc tới tin hot Hacker News -> phải gọi tool `hackernews` | `hackernews` | PASS |
| `G02_hackernews_new_limit` | Lấy 10 bài mới trên Hacker News -> route vào `hackernews` với `limit=10` | `hackernews` | PASS |
| `G03_arxiv_papers_search` | Yêu cầu bài báo nghiên cứu trên arXiv -> route vào `papers` với query LLMs | `papers` | PASS |
| `G04_policy_internal_lookup` | Hỏi quy định nội bộ công ty về bảo mật -> route vào `policy` với `policy_area='data_privacy'` | `policy` | PASS |
| `G05_unconfirmed_send_boundary` | Yêu cầu gửi tin ra ngoài nhưng chưa xác nhận -> gọi `clarify` hỏi yes/no | `clarify` | PASS |
| `G06_multiturn_switch_to_hackernews` | Chuyển từ mạng xã hội sang xem bài trên Hacker News (limit=3) | `hackernews` | PASS |
| `G07_multiturn_clarify_then_fetch` | Ban đầu thiếu URL, khi người dùng bổ sung ở turn 2 -> route `fetch` đúng URL | `fetch` | PASS |
| `G08_multiturn_author_to_timeline` | Đổi tác giả từ Sam Altman sang Elon Musk và lấy 7 tweet | `timeline` | PASS |
| `G09_multiturn_format_then_confirmed_send` | Đã có nội dung và người dùng xác nhận ở turn 3 -> gọi `send` | `send` | FAIL (model gọi lại clarify) |
| `G10_multiturn_arxiv_read_paper` | Carry over ID bài báo arXiv và chỉ định đọc 4 trang -> `paper_text` | `paper_text` | FAIL (nhầm query ID) |

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
| Tool mới (`tools/hackernews/`) | `starter_v0/tools/hackernews/tool.py`, `TOOL.md` (Commits `c12890d`, `01c232a` - Nguyễn Văn Cường) | Lấy tin hot/mới nhất từ Hacker News Firebase API kèm điểm số, comment | Giới hạn `limit` từ 1 đến 20, fallback an toàn khi ngoài phạm vi |
| Unit test tool mới & suite Step 4b (≥ 3 test/tool) | `starter_v0/tests/test_tools_todo.py` (`pytest` 87 passed, 0 failed) | Đầy đủ test cho toàn bộ tool có sẵn và 3+ regression tests cho tool mới: happy path, input xấu (sai kiểu/ngoài enum), failure timeout | Tool bắt mọi Exception và trả về dict error `{tool, error, message}`, tuyệt đối không raise |
| UI (lệnh chạy + link dùng thử) | `starter_v0/app.py`, `requirements.txt` | Streamlit chat tương tác trực quan, hiển thị tool calls, tự lưu transcript | Sidebar cấu hình API key, model linh hoạt, bắt lỗi provider |

**Tool unit tests:** 
- Đã hoàn thành toàn bộ challenge Step 4b (thay 17 stub `pytest.skip` bằng test offline thực tế) và bộ test chuyên sâu cho tool mới `hackernews` trong `tests/test_tools_todo.py`.
- **Ví dụ lỗi mà unit test bắt được nhưng eval không bắt được:**
  1. *Lỗi validate `story_type` và timeout:* Bộ regression test của Hiếu phát hiện khi truyền `story_type` sai enum thì tool vẫn gọi API thay vì trả lỗi ngay, và lỗi timeout bị raise Exception làm sập luồng thay vì trả về error dictionary `{tool, error, message}`. Điều này eval routing không thể bắt được vì eval chỉ kiểm tra tên tool gọi ra chứ không gọi code thật của tool. Sau khi phát hiện, tool đã được fix triệt để.
  2. *Lỗi ép kiểu `limit`:* Khi model truyền chuỗi `limit="not_a_number"`, unit test bắt được lỗi `TypeError` khi so sánh số với chuỗi, giúp nhóm bổ sung kiểm tra ép kiểu và fallback mặc định an toàn. Toàn bộ test suite hiện đạt **87 passed, 0 failed**.

### B5. Bonus Evidence

| Bonus | Evidence File | What Worked | Risk / Guardrail |
|---|---|---|---|
| `send` gửi thật lên Telegram sau xác nhận | `tools/send/tool.py`, `starter_v0/transcripts/v4_groq_20261111T065440457626.transcript.json` | Bot `@lab3_research_bot` gửi tin thật vào group Telegram `-1004487409127` sau xác nhận | Bắt buộc phải qua bước `clarify` (yes_no); có fallback tự động nếu Markdown parsing bị lỗi |

## 5. Khó khăn và cách xử lý

1. **Lỗi API Key & Model Mismatch trên Provider Groq:**
   - *Vấn đề:* Ban đầu khi chạy UI, ứng dụng gặp lỗi `RuntimeError: Missing API key env var: GROQ_API_KEY` do file `.env` chưa có cấu hình. Sau khi thêm key, gặp tiếp lỗi `401 AuthenticationError` do model mặc định bị đặt tên `openai/gpt-oss-20b` (format của OpenRouter) và tài khoản Groq chỉ có quyền truy cập một số model nhất định. Khi thử `llama-3.1-8b-instant` thì gặp `404 NotFoundError`.
   - *Cách xử lý:* Dùng script kiểm tra danh sách model khả dụng qua OpenAI client kết nối tới Groq, phát hiện tài khoản sử dụng được model `openai/gpt-oss-20b`. Đã cập nhật UI tự động chọn model theo provider và cấu hình fallback chính xác.

2. **Lỗi gửi tin nhắn Telegram (`chat not found` và `400 can't parse entities`):**
   - *Vấn đề:* Khi thử nghiệm tool `send`, Telegram API trả về mã lỗi 400 do sai chat ID của nhóm và do parser Markdown của Telegram bị xung đột với các ký tự `_` trong URL / tên tool.
   - *Cách xử lý:* Dùng Telegram `getUpdates` API để lấy ID chính xác của nhóm supergroup (`-1004487409127`). Đồng thời sửa hàm `send_telegram` trong `tools/send/tool.py`: nếu Telegram từ chối định dạng Markdown, hệ thống tự động gửi lại dưới dạng plain text an toàn, đảm bảo tin nhắn luôn đến được Telegram.

## 6. Tổng hợp đóng góp

| Thành viên | MSSV | Vai trò chính & Phần việc | Đóng góp chi tiết |
|---|---|---|---|
| **Nguyễn Văn Cường** (Trưởng nhóm) | 2A202603750 | Trưởng nhóm, CP3 (Tool mới `hackernews`), Phân tích lỗi | Thiết kế và hiện thực tool `tools/hackernews/tool.py`, viết tài liệu `TOOL.md`, đăng ký schema trong `tools.yaml`; phân tích failure patterns qua `analysis/base_runs.csv`; viết 3 unit test cho `hackernews` (commits `c12890d`, `01c232a`); điều phối nhóm. Báo cáo: [2A202603750_NguyenVanCuong.md](2A202603750_NguyenVanCuong.md). |
| **Đoàn Công Hải** | 2A202603739 | CP4 (Eval nhóm), CP5 (UI & Báo cáo), Tích hợp Telegram | Thiết kế bộ 10 case `eval_group.json`; xây dựng giao diện Streamlit `app.py`; cấu hình và tích hợp bot Telegram gửi tin nhắn thật; tổng hợp live transcript và hoàn thiện báo cáo nhóm. |
| **Nguyễn Văn Hiếu** | 2A202603746 | Step 4b (Unit test offline & Regression tests) | Thay toàn bộ 17 stub `pytest.skip` trong `tests/test_tools_todo.py` bằng test offline hoàn chỉnh; viết bộ regression test cho tool `hackernews`, phát hiện 2 lỗi quan trọng về validation và timeout giúp hoàn thiện tool (suite đạt 87 passed). |
| **Lê Nguyễn Anh Khôi** | | CP1, CP2 (Tối ưu Prompt & Tools) | Thiết lập baseline v0, chạy lặp tối ưu prompt v1-v3; chuẩn hóa `system_prompt.md` và `tools.yaml`; ghi log `version_log.csv`. |

## 7. Hạn chế và hướng cải thiện — B6. Reflection

- **Fix nào thuộc `system_prompt.md`?**
  Các quy tắc về hành vi tổng thể, đặc biệt là **ranh giới an toàn (boundary)**: Bắt buộc phải hỏi xác nhận người dùng (`clarify` với `response_type="yes_no"`) trước khi gọi `send`, và nguyên tắc dừng lại hỏi khi thiếu thông tin quan trọng thay vì tự suy đoán.
- **Fix nào thuộc `tools.yaml`?**
  Mô tả chi tiết năng lực của từng tool, enum các giá trị hợp lệ của tham số, quy ước định dạng và hướng dẫn phân biệt rõ ràng giữa các tool tương tự nhau (ví dụ: `hackernews` vs `lookup`, `timeline` vs `social_search`).
- **Failure nào cần review thủ công thay vì chấm tự động?**
  Các câu trả lời có tính mở hoặc khi agent diễn đạt câu hỏi làm rõ (`clarify`) bằng nhiều cách hành văn khác nhau nhưng vẫn giữ đúng mục đích; hoặc khi agent tóm tắt bản tin một cách súc tích mà eval tự động chỉ so sánh chuỗi cứng.
- **Nếu có thêm một vòng, nhóm sẽ thử giả thuyết nào?**
  Thử nghiệm Few-shot ví dụ về Multi-turn trong System Prompt nhằm cải thiện độ chính xác ở các lượt hội thoại phức tạp (như case `G09` và `G10` khi chuyển đổi ngữ cảnh liên tục giữa tìm bài báo và xác nhận gửi tin).

## 8. Tài liệu tham khảo

- Tài liệu hướng dẫn Day 03 Research Agent Tool Eval: `README.md`, `CHECKPOINTS.md`, `RUBRIC.md`.
- Hacker News Firebase API: https://github.com/HackerNews/API
- Telegram Bot API Documentation: https://core.telegram.org/bots/api
- Groq Cloud API Documentation: https://console.groq.com/docs
