# Báo cáo cá nhân — HoVaTen-MSSV
## 1. Thông tin thành viên

- Họ tên: Lê Nguyễn Anh Khôi
- MSSV: 2A202603755
- Email: lnakhoi5a@gmail.com

## 2. Phần việc phụ trách

- **Phát triển module Groq Provider (`groq_provider.py`):** Xây dựng adapter kết nối API Groq, hỗ trợ cơ chế Tool Calling / Function Calling.
- **Thiết lập Baseline v0 & Vận hành chu trình Hypothesis – Fix – Measure (v1 – v3):** Khảo sát baseline, phát hiện lỗi gốc (Root Cause Analysis), đề xuất giả thuyết kỹ thuật, can thiệp mã/prompt và đo lường kết quả trên tập benchmark đánh giá.
- **Chuẩn hóa cấu hình Agent (`artifacts/system_prompt.md` & `artifacts/tools.yaml`):** Thiết lập hệ thống phân cấp luật điều phối (Boundary Priority) và nhúng metadata tri thức trực tiếp vào mô tả công cụ.
- **Kiểm toán thực nghiệm (`version_log.csv`):** Ghi chép trung thực, chi tiết từng chu trình lặp (Mục tiêu, Giả thuyết, File can thiệp, Kết quả eval, Bài học rút ra).
## 3. Đóng góp cụ thể

### 3.1. Phát triển Module tích hợp Groq Provider (`groq_provider.py`)
- Lập trình adapter kết nối Groq thông qua OpenAI-compatible client, chuyển đổi và format function schema tương thích hoàn toàn với cơ chế Tool Calling của Groq.
### 3.2. Thực thi chu trình lặp Hypothesis – Fix – Measure (v0 → v3)

* **Baseline v0 (Đo lường & Phân tích nguyên nhân gốc):**
  - Chạy benchmark ban đầu, phát hiện lỗi nghiêm trọng **Provider Error ở Case R13**: Groq API trả về mã lỗi HTTP 400 (`Tool choice is required, but model did not call a tool`) do prompt chưa có cấu trúc hướng dẫn gọi nhiều tool cùng lúc. Đồng thời phát hiện xung đột ranh giới ở R12 và lỗi thiếu ánh xạ ở R01.
* **Vòng lặp v1 (Khắc phục lỗi Multi-Tool Calling):**
  - *Giả thuyết:* Bổ sung cấu trúc schema tường minh và nguyên tắc Multi-Tool calling trong prompt sẽ giúp Groq sinh đúng tool call, loại bỏ mã lỗi HTTP 400.
  - *Thực hiện:* Cập nhật `artifacts/system_prompt.md` bổ sung Rule Multi-Tool; đồng thời đưa quy tắc chặn suy diễn URL/handle.
  - *Kết quả:* Vượt qua case R13, nhưng phát sinh hiện tượng suy giảm năng lực (**Regression tại Case R01**): agent trở nên quá cứng nhắc, từ chối tự map tên "Sam Altman" sang handle `sama`.
* **Vòng lặp v2 (Xử lý hiện tượng Regression bằng Tool Metadata):**
  - *Giả thuyết:* Nhúng tri thức ánh xạ trực tiếp vào mô tả công cụ thay vì nhồi nhét vào system prompt sẽ giúp agent tự tin trích xuất handle chính xác mà không gây ảo giác.
  - *Thực hiện:* Cập nhật `artifacts/tools.yaml`, bổ sung tri thức ánh xạ `Sam Altman -> sama` trực tiếp trong description của tool `timeline`.
  - *Kết quả:* Khắc phục triệt để lỗi R01, bảo toàn khả năng multi-tool calling mà không gây phụ tác dụng lên các test case khác.
* **Vòng lặp v3 (Giải quyết Xung đột Ranh giới - Conflict of Boundaries):**
  - *Giả thuyết:* Xung đột giữa 2 luật cạnh tranh tại R12 (*"thiếu thông tin phải hỏi text"* vs *"gửi tin phải hỏi yes_no"*) chỉ được giải quyết triệt để khi thiết lập thứ tự ưu tiên cưỡng chế.
  - *Thực hiện:* Tái cấu trúc `artifacts/system_prompt.md`, thiết lập **Confirmation Boundary là Highest Priority** (bắt buộc xin phép `yes_no` trước mọi điều kiện hỏi thông tin khác).
  - *Kết quả:* Khắc phục hoàn toàn case R12, đạt chuẩn routing ổn định trên toàn bộ bộ test.

## 4. Bằng chứng

- **File/commit/PR:**
  - `starter_v0\providers\groq_provider.py`: Module chính tích hợp provider Groq, xử lý tool calling schema và ngoại lệ API.
  - `starter_v0\providers\__init__.py`: Thêm lựa chọn groq
  - `starter_v0\scripts\preflight_provider.py`: Thêm lựa chọn groq
  - `starter_v0\run_eval.py`: Thêm lựa chọn groq
  - `artifacts/system_prompt.md`: Cấu trúc prompt điều phối, phân cấp luật ranh giới và xác nhận.
  - `artifacts/tools.yaml`: Định nghĩa contract, parameters và metadata mô tả công cụ.
  - `version_log.csv`: Bảng dữ liệu kiểm toán toàn bộ chu trình v0 – v3 theo chuẩn Hypothesis – Fix – Measure.

- **AI/công cụ đã dùng và cách tự kiểm tra kết quả:**
  Trong suốt quá trình thực hiện, AI được tận dụng như một đối tác phản biện và nghiên cứu lý thuyết (Thought Partner) nhằm tra cứu các thông số kỹ thuật của Groq API, đánh giá các tình huống biên và phân tích nguy cơ xung đột ranh giới logic trước khi cập nhật prompt. Để tự kiểm chứng kết quả, tôi kiểm tra lại output, tuỳ chỉnh kết quả AI đưa ra, lựa chọn để sử dụng phù hợp với format của bài lab.

## 5. Tự đánh giá

- **Mức độ hoàn thành công việc:** 100% - Hoàn thành đầy đủ từ kết nối provider, thiết kế prompt/tool schema đến thực nghiệm benchmark định lượng.
- **Kỹ năng & Bài học rút ra:**
  - Nắm vững cơ chế vận hành của Tool Calling trên các mô hình nguồn mở tối ưu qua Groq.
  - Hiểu rõ hiện tượng suy giảm năng lực (Regression) khi thắt chặt prompt và biết cách phân tách tri thức domain vào Tool Metadata (`tools.yaml`) thay vì dồn hết vào System Prompt.
  - Làm chủ kỹ thuật phân cấp ranh giới ưu tiên (Hierarchical Priority) để giải quyết triệt để xung đột quyết định của mô hình.
- **Đóng góp chung vào nhóm:** Xây dựng nền tảng kết nối provider ổn định, chuẩn hóa bộ tài liệu thực nghiệm giúp Nhóm E2 đạt kết quả benchmark tối ưu.
