"""
DỰ ÁN: DỊCH VỤ TRA CỨU DANH BẠ NHÂN SỰ NỘI BỘ (HR DIRECTORY SERVICE)
Mô tả: Hệ thống cung cấp API cho ứng dụng Web và Mobile nội bộ để nhân viên
tìm kiếm thông tin liên hệ và phòng ban của đồng nghiệp trong công ty.
"""

from typing import List, Optional
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel

app = FastAPI(title="Internal HR Directory API", version="1.0.0")

# ==========================================
# CƠ SỞ DỮ LIỆU GIẢ LẬP (Mô hình ORM / Domain Entity)
# ==========================================
class UserEntity:
    """Mô hình đại diện cho một bản ghi User đầy đủ trong cơ sở dữ liệu."""
    def __init__(self, id: int, username: str, full_name: str, email: str, 
                 department: str, role: str, salary: int, ssn: str, 
                 hashed_password: str, reset_token: Optional[str] = None):
        self.id = id
        self.username = username
        self.full_name = full_name
        self.email = email
        self.department = department
        self.role = role
        self.salary = salary
        self.ssn = ssn  # Số định danh cá nhân / CCCD
        self.hashed_password = hashed_password
        self.reset_token = reset_token

# Dữ liệu mẫu nhân viên
FAKE_DATABASE: List[UserEntity] = [
    UserEntity(
        id=1,
        username="ceo_nguyen",
        full_name="Nguyễn Văn A",
        email="a.nguyen@corp.internal",
        department="Executive",
        role="CEO",
        salary=150000000,
        ssn="001090012345",
        hashed_password="$2b$12$e80yq9j6w1oX1jKx2mQ9seX0J1gR...",
        reset_token="s3cr3t_r3s3t_t0k3n_ceo_99"
    ),
    UserEntity(
        id=2,
        username="dev_tran",
        full_name="Trần Thị B",
        email="b.tran@corp.internal",
        department="Engineering",
        role="Senior Developer",
        salary=45000000,
        ssn="001095098765",
        hashed_password="$2b$12$k10L9v...hashedpassword...",
        reset_token=None
    )
]

# ==========================================
# API ENDPOINTS
# ==========================================

@app.get("/api/v1/employees/search")
def search_employees(keyword: str = Query(..., description="Từ khóa tìm kiếm theo tên hoặc phòng ban")):
    """
    Tìm kiếm nhân viên trong danh bạ công ty theo từ khóa.
    """
    keyword_lower = keyword.lower()
    results = [
        user for user in FAKE_DATABASE
        if keyword_lower in user.full_name.lower() or keyword_lower in user.department.lower()
    ]
    return {"total": len(results), "employees": results}


@app.get("/api/v1/employees/{employee_id}")
def get_employee_detail(employee_id: int):
    """
    Lấy thông tin chi tiết của một nhân viên theo ID.
    """
    user = next((u for u in FAKE_DATABASE if u.id == employee_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="Không tìm thấy nhân viên")
    return user
