# Báo cáo cá nhân — Nguyễn Văn Cường

## 1. Thông tin thành viên

- Họ tên: Nguyễn Văn Cường
- MSSV: 2A202603750
- Email: nvcuong9696@gmail.com

## 2. Phần việc phụ trách

- Thiết kế, cài đặt và tích hợp tool mới `hackernews` để lấy các bài viết top, mới nhất hoặc nổi bật nhất từ Hacker News.

## 3. Đóng góp cụ thể

- Viết `get_hn_stories` gọi public Hacker News Firebase API, giới hạn số bài trả về từ 1 đến 20 và chuẩn hóa dữ liệu thành tiêu đề, URL, nguồn, điểm số và số bình luận.
- Thêm URL dự phòng tới trang thảo luận Hacker News nếu bài viết không có URL riêng; kiểm tra loại bài viết hợp lệ và trả lỗi theo cấu trúc dùng chung khi API hoặc đầu vào gặp lỗi.
- Tạo `TOOL.md`, khai báo schema trong `tools.yaml` và đăng ký tool trong `tools/__init__.py`.
- Viết ba unit test bao phủ kết quả bình thường, loại bài viết không hợp lệ và lỗi mạng; các test giả lập lời gọi API để không phụ thuộc kết nối thật.

## 4. Bằng chứng

- File chính: [tool.py](../starter_v0/tools/hackernews/tool.py), [TOOL.md](../starter_v0/tools/hackernews/TOOL.md), [tools.yaml](../starter_v0/artifacts/tools.yaml), [__init__.py](../starter_v0/tools/__init__.py).
- Commit: `c12890d` (thêm tool và tích hợp); `01c232a` (hoàn thiện xử lý phản hồi và lỗi).
- AI/công cụ: dùng trợ lý lập trình để hỗ trợ lập trình tool, xác nhận AI đã làm theo đúng chuẩn cấu trúc file tool và hàm chưa;

## 5. Tự đánh giá

- Hoàn thành việc tạo tool theo cấu trúc dự án, mô tả rõ phạm vi sử dụng để tránh nhầm với tìm kiếm web, đọc URL hoặc tìm kiếm mạng xã hội.
- Các test hiện xác nhận logic và xử lý lỗi với phản hồi giả lập; chưa kiểm chứng trực tiếp độ ổn định của Hacker News API trong môi trường mạng thật.
- Nếu có thêm thời gian, tôi sẽ bổ sung kiểm tra giới hạn `limit` và các trường dữ liệu thiếu, đồng thời thử nghiệm tích hợp với API thật.
