"""
==============================================================
Day 10 Lab: Build Your First Automated ETL Pipeline
==============================================================
Student ID: AI20K-1010
Name: Trần Quang Huy

Nhiệm vụ:
   1. Extract:   Đọc dữ liệu từ file JSON
   2. Validate:  Kiểm tra & loại bỏ dữ liệu không hợp lệ
   3. Transform: Chuẩn hóa category + tính giá giảm 10%
   4. Load:      Lưu kết quả ra file CSV

Chấm điểm tự động:
   - Script phải chạy KHÔNG LỖI (20d)
   - Validation: loại record giá <= 0, category rỗng (10d)
   - Transform: discounted_price + category Title Case (10d)
   - Logging: in số record processed/dropped (10d)
   - Timestamp: thêm cột processed_at (10d)
==============================================================
"""

import datetime
import json

import pandas as pd


# --- CONFIGURATION ---
SOURCE_FILE = 'raw_data.json'
OUTPUT_FILE = 'processed_data.csv'


def extract(file_path):
    """
    Task 1: Đọc dữ liệu JSON từ file.

    Gợi ý:
       - Dùng json.load() để đọc file JSON
       - Xử lý trường hợp file không tồn tại (FileNotFoundError)

    Returns:
        list: Danh sách các records (dictionaries)
    """
    print(f"Extracting data from {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"Extract error: file not found: {file_path}")
        return []
    except json.JSONDecodeError as exc:
        print(f"Extract error: invalid JSON in {file_path}: {exc}")
        return []

    if not isinstance(data, list):
        print("Extract error: JSON root must be a list of records.")
        return []

    print(f"Extract complete. {len(data)} records read.")
    return data


def validate(data):
    """
    Task 2: Kiểm tra chất lượng dữ liệu.

    Quy tắc validation:
       - Price phải > 0 (loại bỏ giá âm hoặc bằng 0)
       - Category không được rỗng

    Gợi ý:
       - Dùng record.get('price', 0) để lấy giá
       - Dùng record.get('category') để kiểm tra category
       - In ra số lượng record hợp lệ và không hợp lệ

    Returns:
        list: Danh sách các records hợp lệ
    """
    valid_records = []
    error_count = 0

    # Lặp qua data, kiểm tra từng record.
    # Giữ lại record hợp lệ, đếm record lỗi.
    for record in data:
        try:
            price = float(record.get('price', 0))
        except (TypeError, ValueError):
            error_count += 1
            continue

        category = record.get('category')
        if price <= 0 or category is None or str(category).strip() == '':
            error_count += 1
            continue

        clean_record = record.copy()
        clean_record['price'] = price
        clean_record['category'] = str(category).strip()
        valid_records.append(clean_record)

    print(f"Validation complete. {len(valid_records)} valid records, {error_count} error records dropped.")
    return valid_records


def transform(data):
    """
    Task 3: Áp dụng business logic.

    Yêu cầu:
       - Tính discounted_price = price * 0.9 (giảm 10%)
       - Chuẩn hóa category thành Title Case (ví dụ: "electronics" -> "Electronics")
       - Thêm cột processed_at = timestamp hiện tại

    Gợi ý:
       - Dùng pd.DataFrame(data) để tạo DataFrame
       - df['discounted_price'] = df['price'] * 0.9
       - df['category'] = df['category'].str.title()
       - df['processed_at'] = datetime.datetime.now().isoformat()

    Returns:
        pd.DataFrame: DataFrame đã được transform
    """
    df = pd.DataFrame(data)
    if df.empty:
        print("Transform complete. 0 records processed.")
        return df

    df['discounted_price'] = df['price'] * 0.9
    df['category'] = df['category'].astype(str).str.title()
    df['processed_at'] = datetime.datetime.now().isoformat()

    print(f"Transform complete. {len(df)} records processed.")
    return df


def load(df, output_path):
    """
    Task 4: Lưu DataFrame ra file CSV.

    Gợi ý:
       - df.to_csv(output_path, index=False)
    """
    df.to_csv(output_path, index=False)
    print(f"Data saved to {output_path}. {len(df)} records loaded.")


# ============================================================
# MAIN PIPELINE
# ============================================================
if __name__ == "__main__":
    print("=" * 50)
    print("ETL Pipeline Started...")
    print("=" * 50)

    # 1. Extract
    raw_data = extract(SOURCE_FILE)

    if raw_data:
        # 2. Validate
        clean_data = validate(raw_data)

        # 3. Transform
        final_df = transform(clean_data)

        # 4. Load
        if final_df is not None:
            load(final_df, OUTPUT_FILE)
            print(f"\nPipeline completed! {len(final_df)} records saved.")
        else:
            print("\nTransform returned None. Check your transform() function.")
    else:
        print("\nPipeline aborted: No data extracted.")
