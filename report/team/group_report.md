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

### 3.1. Phân tích nguyên nhân gốc rễ (Root Cause Analysis ở v0)
1. **Lỗi trong System Prompt gốc (`system_promptV0.md`):** Chứa nhiều chỉ thị phản khuôn mẫu (anti-patterns) như *"just make a sensible guess"*, *"pick a well-known account like Sam Altman"*, *"just go ahead and do it"*. Điều này khiến mô hình liên tục hallucinate khi thiếu thông tin đầu vào (R10, R11) và tự tiện kích hoạt tool gửi tin nguy hiểm (R12, R14).
2. **Lỗi trong Tool Definitions gốc (`toolsV0.yaml`):** Các mô tả tool quá ngắn gọn (1 dòng), không nêu rõ điều kiện biên: khi nào nên dùng, khi nào cấm dùng (`DÙNG KHI` / `KHÔNG DÙNG KHI`), không định nghĩa rõ cách ánh xạ định danh và kiểu dữ liệu trả lời của `clarify`.

### 3.2. Quá trình tối ưu hóa
- **v1 (Sửa `artifacts/system_prompt.md`):** Xóa bỏ hoàn toàn lệnh đoán mò; thiết lập **4 Kỷ luật vận hành cốt lõi (Critical Operational Rules)**:
  - *Rule 1 (Missing Information):* Thiếu dữ liệu mục tiêu bắt buộc gọi `clarify` với `response_type: "text"`, cấm đoán mò.
  - *Rule 2 (Confirmation Boundary):* Mọi hành động gửi/đăng tải ra ngoài phải xin xác nhận qua `clarify` với `response_type: "yes_no"`.
  - *Rule 3 (Multi-Tool):* Đồng thời gọi nhiều công cụ khi yêu cầu nhiều nguồn dữ liệu.
  - *Rule 4 (Out-of-Scope):* Từ chối gọi tool cho câu hỏi toán học, lập trình thuần túy hoặc câu hỏi meta.
- **v2 (Sửa `artifacts/tools.yaml`):** Khắc phục regression xuất hiện ở v1 (R01 bị hỏi clarify vô cớ vì Rule 1 quá cứng):
  - Bổ sung cấu trúc `DÙNG KHI` và `KHÔNG DÙNG KHI` cho toàn bộ 10 công cụ.
  - Tích hợp nguyên tắc ánh xạ tự động tên người nổi tiếng sang handle (ví dụ: Sam Altman $\rightarrow$ `sama`) trực tiếp vào mô tả `timeline`, đồng thời bổ sung ngoại lệ cấm gọi `clarify` nếu đã có tên định danh suy luận được.
  - Siết chặt mô tả ranh giới của tool `send` và chuẩn hóa mô tả các trường enum (`Latest`/`Top`, `day`/`week`).
- **v3 (Sửa `artifacts/system_prompt.md`):** Giải quyết dứt điểm xung đột ranh giới tại R12 và lỗi trích xuất tham số tại R03:
  - Nâng **Confirmation Boundary lên độ ưu tiên cao nhất (Highest Priority)**: Khi người dùng yêu cầu đăng tin, bất kể có thiếu nội dung hay không, bắt buộc hỏi `yes_no` trước tiên, cấm hỏi `text`.
  - Thêm quy tắc **Argument Extraction & Hygiene**: Chuẩn hóa tham số tìm kiếm, cấm nhồi nhét từ chỉ thời gian ("hôm nay", "tuần này") hoặc từ chỉ thể loại ("tin tức", "news") vào trường `query` của tool `lookup`.
- **v4 (Sửa `artifacts/tools.yaml`):** Đăng ký tool mới `hackernews` với mô tả rõ ràng: gọi khi người dùng nhắc tới Hacker News/HN; không nhầm lẫn với `lookup` hay `timeline`.

### 3.3. Tool mới tự phát triển: `hackernews` (`tools/hackernews/`)
- **Người phụ trách chính**: Nguyễn Văn Cường (Trưởng nhóm).
- **Chức năng**: Tích hợp trực tiếp với Firebase API chính thức của Hacker News (`https://hacker-news.firebaseio.com/v0/`) để lấy danh sách bài viết nổi bật (`top`), mới nhất (`new`), hoặc hay nhất (`best`) kèm điểm số (`score`), số lượng bình luận (`descendants`) và liên kết gốc. Bổ sung URL dự phòng trỏ về trang thảo luận Hacker News nếu bài viết không có link riêng (`https://news.ycombinator.com/item?id=...`).
- **Khi nào gọi**: Agent gọi khi người dùng hỏi tin tức trên Hacker News / HN. Tool có sẵn cơ chế bắt lỗi timeout, fallback enum và chuẩn hóa kiểu dữ liệu trả về theo format dùng chung của hệ thống.

## 4. Kết quả — PHẦN B: Chi tiết và bằng chứng

### B1. Version Evidence

Lấy từ `starter_v0/artifacts/version_log.csv` và `starter_v0/runs/*.json`. Chỉ dùng run có `provider_error_cases == 0` và `measured_cases == total_cases`.

| Version | Changed Artifact | Hypothesis | Metric Before | Metric After | Run File |
|---|---|---|---:|---:|---|
| **v0** | Baseline | Thiết lập điểm chuẩn baseline ban đầu trên tập `eval_base`. Prompt gốc chứa anti-pattern đoán mò sẽ gây ảo giác URL/handle và vi phạm ranh giới gửi tin. | N/A | **0.6316** | `runs/v0_B_base_groq_20261111T072931159418.json` |
| **v1** | `artifacts/system_prompt.md` | Bổ sung 4 quy tắc vận hành nghiêm ngặt (hỏi clarify khi thiếu input, xác nhận yes/no trước khi gửi, cấm gọi tool cho coding/math), agent sẽ dừng hallucination và tăng case accuracy lên $\ge 0.70$. | 0.6316 | **0.75** | `runs/v1_B_base_groq_20261111T073608906435.json` |
| **v2** | `artifacts/tools.yaml` | Tái cấu trúc mô tả `tools.yaml` theo cú pháp 'DÙNG KHI/KHÔNG DÙNG KHI' và tích hợp tri thức ánh xạ handle người nổi tiếng vào tool `timeline`, sẽ khắc phục regression R01 và đưa case accuracy lên $\ge 0.80$. | 0.75 | **0.85** | `runs/v2_B_base_groq_20261111T074338943173.json` |
| **v3** | `artifacts/system_prompt.md` | Đưa Confirmation Boundary lên Highest Priority (ép buộc `yes_no` trước kể cả khi thiếu body text) và bổ sung quy chuẩn Argument Hygiene (lọc sạch từ khóa thời gian/thể loại khỏi query), agent sẽ giải quyết dứt điểm R12, R03 và đạt accuracy $\ge 0.90$. | 0.85 | **0.95** | `runs/v3_B_base_groq_20261111T075054533765.json` |
| v4 | tools.yaml & code | Đánh giá bộ test case nhóm với tool mới `hackernews`, đạt routing tuyệt đối | N/A | **0.80** | `runs/v4_B_group_groq_20261111T075843555174.json` |


*Ghi chú số liệu đo lường:*
- v0: $12/19$ pass ($63.16\%$), 1 case lỗi nhà cung cấp API (R13 gặp HTTP 400 Bad Request).
- v1: $15/20$ pass ($75.00\%$), 0 provider error, giải quyết R10, R11, R14, M05, M06 nhưng phát sinh regression tại R01.
- v2: $17/20$ pass ($85.00\%$), 0 provider error, multiturn đạt $100\%$ ($6/6$), giải quyết hoàn toàn regression R01 và M02.
- v3: $19/20$ pass ($95.00\%$), 0 provider error, giải quyết hoàn toàn R03 và R12.
### B2. Failure Analysis

Lấy từ `results[*].result.failures` trong run JSON.

| Case ID | Failure Type | Actual Tool Calls | What Failed | Fix |
|---|---|---|---|---|
| **R01** *(v1)* | `wrong_tool` | `clarify(question="Could you confirm Sam Altman's Twitter handle?", response_type="text")` | **Regression:** Agent bắt bẻ hỏi lại handle của Sam Altman thay vì tự quy đổi thành `sama` do Rule 1 ở prompt v1 quá cứng nhắc. | Cập nhật `tools.yaml` (v2): Thêm hướng dẫn tự quy đổi tên người nổi tiếng vào tool `timeline` và loại trừ trong `clarify`. |
| **R03** *(v0, v1, v2)* | `wrong_arg_value` | `lookup(query="AI news today", timeframe="day", topic="news")` | Tham số `query` bị thừa từ `"news today"` trong khi đã được khai báo ở `topic="news"` và `timeframe="day"`. | Cập nhật `system_prompt.md` (v3): Bổ sung quy tắc Argument Hygiene, cấm đưa từ chỉ thời gian/thể loại vào `query`. |
| **R10** *(v0)* | `missing_info` | `timeline(limit=5, screenname="sama")` | Người dùng không nói rõ của ai nhưng agent tự ý đoán mò tài khoản Sam Altman (`sama`). | Cập nhật `system_prompt.md` (v1): Bắt buộc gọi `clarify(response_type="text")` khi thiếu đối tượng. |
| **R11** *(v0)* | `missing_info` | `fetch(url="https://www.bbc.com/news/technology-66812345")` | Yêu cầu tóm tắt nhưng không có link, agent tự bịa ra link BBC để đọc. | Cập nhật `system_prompt.md` (v1): Cấm đoán mò URL, bắt buộc gọi `clarify` xin đường link bài viết. |
| **R12** *(v0)* | `wrong_boundary` | `lookup(query="AI news", timeframe="week", topic="news")` | Yêu cầu đăng tin Telegram nhưng agent lại tự ý đi search tin tức thay vì xin xác nhận gửi. | Cập nhật `system_prompt.md` (v1): Bắt buộc xin xác nhận trước khi thực hiện hành động ghi/gửi. |
| **R12** *(v1, v2)* | `wrong_boundary` | `clarify(question="Bạn có thể cung cấp nội dung bản tin...", response_type="text")` | Xung đột ranh giới: Agent thấy chưa có nội dung nên ưu tiên hỏi `text` thay vì hỏi xác nhận `yes_no`. | Cập nhật `system_prompt.md` (v3): Thiết lập Confirmation Boundary là Highest Priority, luôn ép kiểu `yes_no` trước. |
| **R13** *(v0)* | `provider_error` | *(Không gọi được tool nào)* | Lỗi `BadRequestError: 400 - Tool choice is required, but model did not call a tool` do Groq API xử lý parallel thất bại. | Cập nhật System Prompt (v1, v2, v3) yêu cầu gọi song song độc lập. |
| **R13** *(v1, v2, v3)* | `wrong_tool` | `lookup(query="AI", timeframe="day", topic="news")` | Agent chỉ gọi tool `lookup` mà bỏ quên tool `social_search` khi người dùng yêu cầu cả web và tweet. | Giới hạn cố hữu của model nhỏ trên Groq khi sinh multi-tool trong 1 turn; cần few-shot ví dụ parallel tool calls. |
| **R14** *(v0)* | `out_of_scope` | `send(text="def fibonacci(n)...")` | Câu hỏi yêu cầu viết code Fibonacci nhưng agent lại tự tiện kích hoạt tool `send` gửi mã nguồn lên Telegram. | Cập nhật `system_prompt.md` (v1): Thiết lập quy tắc Out-of-Scope, trả lời trực tiếp bằng text, cấm gọi tool. |
| **M05** *(v0)* | `wrong_arg_value` | `timeline(limit=10, screenname="elonmusk")` | Sau 3 turns, agent không cập nhật `limit=3` theo yêu cầu sửa đổi của người dùng mà giữ nguyên `limit=10`. | Cập nhật `system_prompt.md` (v1): Tối ưu ngữ cảnh multiturn và ghi đè tham số. |
| **M06** *(v0)* | `wrong_tool` | `lookup(query="OpenAI news", timeframe="week", topic="news")` | Chuyển từ Twitter sang Web News bị dính từ khóa thừa `OpenAI news` thay vì `OpenAI`. | Cập nhật `system_prompt.md` (v1) và `tools.yaml` (v2) chuẩn hóa topic search. |

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

3. **Sự cố Provider Error ở v0 (Case R13):**
   - *Vấn đề:* Groq API trả về mã lỗi HTTP 400 (`Tool choice is required, but model did not call a tool`) khi prompt không có cấu trúc hướng dẫn gọi nhiều tool.
   - *Cách xử lý:* Định hình lại schema tường minh và bổ sung nguyên tắc Multi-Tool calling trong prompt v1.

4. **Xung đột ranh giới (Conflict of Boundaries ở v1 và v2):**
   - *Vấn đề:* Tại case R12, agent đối mặt với 2 luật cạnh tranh: *"thiếu thông tin phải hỏi text"* và *"gửi tin phải hỏi yes_no"*. Mô hình chọn hỏi xin nội dung trước (`response_type="text"`), dẫn đến fail eval.
   - *Cách xử lý:* Tại prompt v3, nhóm thiết lập nguyên tắc phân cấp cưỡng chế: Confirmation Boundary là Highest Priority, bắt buộc xin phép `yes_no` trước mọi điều kiện khác.

5. **Hiện tượng suy giảm khả năng (Regression ở v1):**
   - *Vấn đề:* Khi đưa Rule 1 vào prompt v1 để chặn đoán mò URL/handle, agent lại trở nên "quá máy móc" và từ chối tự map tên Sam Altman sang `sama` (case R01).
   - *Cách xử lý:* Đưa tri thức ánh xạ trực tiếp vào mô tả tool `timeline` trong `tools.yaml` (v2) thay vì nhồi nhét vào prompt, giúp agent tự tin map handle mà không bị ảo giác.

## 6. Tổng hợp đóng góp

| Thành viên | MSSV | Vai trò chính & Phần việc | Đóng góp chi tiết |
|---|---|---|---|
| **Nguyễn Văn Cường** (Trưởng nhóm) | 2A202603750 | Trưởng nhóm, CP3 (Tool mới `hackernews`), Phân tích lỗi | Thiết kế và hiện thực tool `tools/hackernews/tool.py`, viết tài liệu `TOOL.md`, đăng ký schema trong `tools.yaml`; phân tích failure patterns qua `analysis/base_runs.csv`; viết 3 unit test cho `hackernews` (commits `c12890d`, `01c232a`); điều phối nhóm. Báo cáo: [2A202603750_NguyenVanCuong.md](2A202603750_NguyenVanCuong.md). |
| **Đoàn Công Hải** | 2A202603739 | CP4 (Eval nhóm), CP5 (UI & Báo cáo), Tích hợp Telegram | Thiết kế bộ 10 case `eval_group.json`; xây dựng giao diện Streamlit `app.py`; cấu hình và tích hợp bot Telegram gửi tin nhắn thật; tổng hợp live transcript và hoàn thiện báo cáo nhóm. |
| **Nguyễn Văn Hiếu** | 2A202603746 | Step 4b (Unit test offline & Regression tests) | Thay toàn bộ 17 stub `pytest.skip` trong `tests/test_tools_todo.py` bằng test offline hoàn chỉnh; viết bộ regression test cho tool `hackernews`, phát hiện 2 lỗi quan trọng về validation và timeout giúp hoàn thiện tool (suite đạt 87 passed). |
| **Lê Nguyễn Anh Khôi** | 2A202603755 | CP1, CP2 (Tối ưu Prompt & Tools) | Phát triển module tích hợp Groq Provider (`groq_provider.py`) hỗ trợ tool calling; thiết lập baseline v0, thực thi chu trình lặp hypothesis-fix-measure v1–v3; chuẩn hóa `artifacts/system_prompt.md`, `artifacts/tools.yaml` và ghi v0-v3 `version_log.csv`. Báo cáo: [2A202603755_LeNguyenAnhKhoi.md](2A202603755_LeNguyenAnhKhoi.md). |

## 7. Hạn chế và hướng cải thiện — B6. Reflection

### 1. Fix nào thuộc về `system_prompt.md`?
- Các quy định mang tính **nguyên tắc ứng xử, thẩm quyền và thứ tự ưu tiên chiến lược**:
  - Quy tắc Confirmation Boundary (mức độ ưu tiên cao nhất, cấm tự ý gửi tin).
  - Quy tắc phân loại Out-of-Scope (từ chối giải toán, lập trình để tránh kích hoạt tool nhầm).
  - Quy tắc Argument Hygiene (làm sạch từ khóa, không đưa yếu tố thời gian/thể loại vào trường `query`).

### 2. Fix nào thuộc về `tools.yaml`?
- Các quy định mang tính **năng lực kỹ thuật, ranh giới dữ liệu và hợp đồng giao tiếp (Contract)**:
  - Cấu trúc ranh giới hoạt động rõ ràng `DÙNG KHI / KHÔNG DÙNG KHI` cho từng tool.
  - Khả năng tự động quy đổi định danh người nổi tiếng sang handle chuyên biệt (`Sam Altman` $\rightarrow$ `sama`).
  - Định nghĩa kiểu dữ liệu chặt chẽ cho parameters (ví dụ: `response_type` enum gồm `text`, `yes_no`, `choice`).

### 3. Failure nào cần review thủ công thay vì chấm tự động?
- **Case R13 (Parallel Tool Calls):** Khi người dùng hỏi gộp hai nguồn dữ liệu, model `openai/gpt-oss-20b` gọi `lookup` để lấy tin trước và trả lời một phần, sau đó trong hội thoại thực tế người dùng có thể yêu cầu tiếp tweet. Hệ thống eval tự động chấm fail ngay trong single turn vì thiếu `social_search`, nhưng về mặt trải nghiệm hội thoại thực tế (human UX), câu trả lời vẫn có giá trị và hữu ích cho người dùng.

### 4. Nếu có thêm một vòng lặp (v4), nhóm sẽ thử giả thuyết nào?
- **Giả thuyết cho v4:** Bổ sung kỹ thuật **Few-shot Function Calling In-Context** vào `system_prompt.md` mô phỏng chính xác cặp cú pháp gọi song song hai công cụ `[{"name": "lookup", ...}, {"name": "social_search", ...}]`. Giả thuyết này kỳ vọng sẽ kích hoạt thành công khả năng parallel tool call của model mã nguồn mở trên Groq, giải quyết dứt điểm case R13 còn sót lại để nâng accuracy lên tuyệt đối $100\%$ ($20/20$).

## 8. Tài liệu tham khảo

- Tài liệu hướng dẫn Day 03 Research Agent Tool Eval: `README.md`, `CHECKPOINTS.md`, `RUBRIC.md`.
- Hacker News Firebase API: https://github.com/HackerNews/API
- Telegram Bot API Documentation: https://core.telegram.org/bots/api
- Groq Cloud API Documentation: https://console.groq.com/docs
- Benchmark Dataset — `starter_v0/data/eval_base.json` & `starter_v0/runs/*.json`.
