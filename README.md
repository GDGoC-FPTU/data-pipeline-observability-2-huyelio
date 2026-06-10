[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=24112756&assignment_repo_type=AssignmentRepo)
# Day 10 Lab: Data Pipeline & Data Observability

**Student ID:** 2A202601010
**Student Email:** huytq1226@example.com
**Name:** Trần Quang Huy

---

## Mô tả

Bài lab này xây dựng một ETL pipeline đơn giản bằng Python. Pipeline đọc dữ liệu từ `raw_data.json`, validate để loại record có `price <= 0` hoặc `category` rỗng, transform dữ liệu bằng cách chuẩn hóa category sang Title Case, tính `discounted_price = price * 0.9`, thêm cột `processed_at`, sau đó ghi kết quả ra `processed_data.csv`.

Phần observability được thể hiện qua log số record đã đọc, số record hợp lệ, số record lỗi, số record đã transform và số record đã load. Ngoài ra, stress test so sánh agent khi dùng dữ liệu sạch và dữ liệu rác được ghi trong `experiment_report.md`.

---

## Cách chạy (How to Run)

### Prerequisites

```bash
pip install pandas pytest
```

### Chạy ETL Pipeline

```bash
python solution.py
```

Sau khi chạy, file `processed_data.csv` sẽ được tạo. Với dữ liệu mẫu hiện tại, pipeline đọc 5 records, giữ lại 3 records hợp lệ và loại 2 records lỗi.

### Chạy Agent Simulation (Stress Test)

```bash
python generate_garbage.py
python -c "from agent_simulation import simulate_agent_response; print(simulate_agent_response('What is the best electronic product?', 'processed_data.csv')); print(simulate_agent_response('What is the best electronic product?', 'garbage_data.csv'))"
```

Kết quả cho thấy clean data giúp agent chọn Laptop, còn garbage data làm agent chọn Nuclear Reactor do outlier giá quá lớn.

---

## Cấu trúc thư mục

```text
solution.py              # ETL Pipeline script
raw_data.json            # Input JSON data
processed_data.csv       # Output của pipeline
generate_garbage.py      # Tạo garbage_data.csv
agent_simulation.py      # Mô phỏng agent đọc CSV
experiment_report.md     # Báo cáo thí nghiệm
README.md                # File này
```

---

## Kết quả

Pipeline hoàn thành thành công:

- 5 records được extract từ JSON.
- 3 records hợp lệ được giữ lại.
- 2 records bị loại do price âm hoặc category rỗng.
- `discounted_price` và `processed_at` đã được thêm vào output CSV.
