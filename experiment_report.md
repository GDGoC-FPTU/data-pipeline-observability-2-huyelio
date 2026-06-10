# Experiment Report: Data Quality Impact on AI Agent

**Student ID:** AI20K-1010
**Name:** Trần Quang Huy
**Date:** 2026-06-10

---

## 1. Kết quả thí nghiệm

Query dùng để test: `What is the best electronic product?`

| Scenario | Agent Response | Accuracy (1-10) | Notes |
|----------|----------------|-----------------|-------|
| Clean Data (`processed_data.csv`) | Agent: Based on my data, the best choice is Laptop at $1200.0. | 9 | Dữ liệu đã qua ETL, category được chuẩn hóa, record có price <= 0 và category rỗng đã bị loại. |
| Garbage Data (`garbage_data.csv`) | Agent: Based on my data, the best choice is Nuclear Reactor at $999999. | 2 | Agent bị ảnh hưởng bởi outlier cực lớn và không có bước validate chất lượng dữ liệu. |

---

## 2. Phân tích & nhận xét (phan tich nhan xet)

Agent trả lời sai khi dùng Garbage Data vì logic của agent chỉ lọc category electronics và lấy item có price cao nhất. Khi dữ liệu có outlier như Nuclear Reactor giá 999999, agent xem đây là lựa chọn tốt nhất mặc dù record này không phù hợp với ngữ cảnh mua sản phẩm điện tử thông thường. Ngoài ra garbage data còn có duplicate ID, price sai kiểu dữ liệu, null values và category thiếu. Những lỗi này làm pipeline hoặc agent mất khả năng so sánh công bằng, dễ bị nhiễu, và đưa ra câu trả lời có vẻ hợp lý về mặt cú pháp nhưng sai về mặt nghĩa. Nếu không có validation, prompt tốt vẫn không thể sửa được nền tảng dữ liệu kém chất lượng.

---

## 3. Kết luận

**Quality Data > Quality Prompt?** Đồng ý. Prompt có thể hướng dẫn agent cách trả lời, nhưng kết quả cuối cùng vẫn phụ thuộc vào dữ liệu mà agent đọc được. Dữ liệu sạch giúp agent đưa ra câu trả lời ổn định, dễ kiểm chứng và ít bị outlier hoặc record lỗi dẫn dắt sai.
