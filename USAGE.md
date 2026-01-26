# 📋 วิธีการใช้งานระบบ CowboyShop

## ✅ ระบบได้ถูกสร้างขึ้นแล้ว!

ระบบสั่งซื้อสินค้าแบบใช้งานได้จริง พร้อม Database, Login, และการจัดการคำสั่งซื้อ

---

## 🚀 เริ่มใช้งาน

### 1. เปิด Django Server
```bash
python manage.py runserver
```
ไปที่: **http://127.0.0.1:8000**

---

## 👥 ข้อมูลการเข้าสู่ระบบ

### Admin Dashboard (จัดการทั้งระบบ)
- **URL**: http://127.0.0.1:8000/admin/
- **Username**: `admin`
- **Password**: `admin123`

### Employee (พนักงาน - ตรวจสอบคำสั่งซื้อ)
- **Login Page**: http://127.0.0.1:8000/employee
- **Username**: `employee1`
- **Password**: `employee123`

### Customer (ลูกค้า - สั่งซื้อสินค้า)
- **Login Page**: http://127.0.0.1:8000/login
- **Email**: `cust1@gmail.com`
- **Password**: `customer123`

---

## 📍 ขั้นตอนการใช้งาน

### ขั้นตอนที่ 1: ลูกค้า (Customer) ล็อกอิน
```
1. ไปที่ /login
2. ใส่: cust1@gmail.com และ customer123
3. กด "เข้าสู่ระบบ"
```

### ขั้นตอนที่ 2: ลูกค้าสั่งซื้อสินค้า
```
1. ไปที่ /shop (จะบังคับให้ login ก่อน)
2. ใส่ข้อมูลการสั่งซื้อ:
   - ชื่อสินค้า (อิสระ)
   - จำนวน
   - ราคาต่อหน่วย
   - ชื่อลูกค้า (ชื่ออิสระ)
   - เบอร์โทรศัพท์
3. กด "ยืนยันการสั่งซื้อ"
4. จะได้ Order ID เช่น ORD-20250126-001
```

### ขั้นตอนที่ 3: พนักงาน (Employee) ตรวจสอบคำสั่งซื้อ
```
1. ไปที่ /employee
2. ใส่: employee1 และ employee123
3. กด "เข้าสู่ระบบ"
4. จะไปไปที่ /employee-sell (ตารางคำสั่งซื้อ)
5. ดูรายการคำสั่งซื้อทั้งหมด
   - สถานะ: รอตรวจสอบ / อนุมัติ / ปฏิเสธ / จัดส่ง
   - สามารถกรอง, ค้นหา, ดูรายละเอียด
```

### ขั้นตอนที่ 4: Admin จัดการข้อมูล
```
1. ไปที่ /admin/
2. ใส่: admin / admin123
3. จัดการ:
   - Employees (พนักงาน)
   - Customers (ลูกค้า)
   - Orders (คำสั่งซื้อ)
   - อนุมัติ/ปฏิเสธ คำสั่งซื้อ
```

---

## 🗄️ ฐานข้อมูล (Database)

### ตาราง Employees (พนักงาน)
```
- employee_id: EMP-0001, EMP-0002, ...
- user: ชื่อผู้ใช้
- phone: เบอร์โทรศัพท์
- department: แผนก
```

### ตาราง Customers (ลูกค้า)
```
- user: ลิงก์ไป User
- phone: เบอร์โทรศัพท์
- address: ที่อยู่
```

### ตาราง Orders (คำสั่งซื้อ)
```
- order_id: ORD-20250126-001 (อัตโนมัติ)
- customer: ลิงก์ไป Customer
- product_name: ชื่อสินค้า (อิสระ)
- quantity: จำนวน
- unit_price: ราคาต่อหน่วย
- total_price: ราคารวม (คำนวณอัตโนมัติ)
- customer_name: ชื่อลูกค้า (ชื่ออิสระ)
- customer_phone: เบอร์โทรศัพท์
- status: pending/approved/rejected/shipped
- created_at: วันที่สั่งซื้อ
- approved_by: พนักงานที่อนุมัติ
- approved_at: วันที่อนุมัติ
```

---

## 🎯 ฟีเจอร์ที่ทำแล้ว

✅ **Login/Register System**
- Login สำหรับลูกค้า (email)
- Login สำหรับพนักงาน (username)
- Django authentication

✅ **Customer Features**
- สั่งซื้อสินค้าแบบอิสระ (ไม่ต้องเลือกจากรูป)
- ใส่ชื่อสินค้าเอง
- ใส่ราคาเอง
- ใส่ชื่อลูกค้าอิสระ
- ใส่เบอร์โทรศัพท์

✅ **Employee Features**
- ตารางแสดงคำสั่งซื้อทั้งหมด
- สถานะสี (รอตรวจสอบ/อนุมัติ/ปฏิเสธ/จัดส่ง)
- ฟิลเตอร์ตามสถานะ
- ค้นหาตามชื่อลูกค้าหรือเลขออเดอร์
- วันที่

✅ **Admin Features**
- Django Admin Panel
- จัดการ Employees
- จัดการ Customers
- จัดการ Orders
- อนุมัติ/ปฏิเสธ
- เก็บพนักงานที่อนุมัติ

✅ **Database**
- SQLite (db.sqlite3)
- ทำ migrations แล้ว
- สร้าง superuser แล้ว

---

## 🔧 Technical Stack

- **Backend**: Django 5.2.6
- **Database**: SQLite
- **Frontend**: Tailwind CSS
- **Icons**: Lucide
- **Authentication**: Django built-in auth

---

## 📝 ไฟล์ที่สำคัญ

```
cowboy/
├── manage.py              # Django management
├── db.sqlite3             # Database
├── init_data.py          # Script สร้างข้อมูล
│
├── vercel/               # App หลัก
│   ├── models.py         # Employee, Customer, Order
│   ├── views.py          # Logic ทั้งหมด
│   ├── urls.py           # Routes
│   ├── admin.py          # Admin config
│   └── migrations/       # Migration files
│
└── templates/            # HTML templates
    ├── login.html        # Login สำหรับ Customer
    ├── employee.html     # Login สำหรับ Employee
    ├── employeesell.html # ตารางคำสั่งซื้อ
    ├── shop.html         # ฟอร์มสั่งซื้อ
    └── ...
```

---

## 🐛 การแก้ไขปัญหา

### ถ้า Port 8000 ถูกใช้งาน
```bash
python manage.py runserver 8001
```

### ถ้าต้องการสร้าง Employee/Customer เพิ่มเติม
```bash
python manage.py createsuperuser
```

### ถ้าต้องการ Reset Database
```bash
del db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## ✨ หมายเหตุ

- Order ID สร้างอัตโนมัติ: `ORD-YYYYMMDD-XXX`
- ราคารวม (total_price) คำนวณอัตโนมัติ: quantity × unit_price
- ทุกอย่างใช้งานได้กับ `python manage.py runserver`
- ระบบเก็บ Order ทั้งหมดในตาราง (ไม่ใช่เพียงแสดง)

---

**ระบบพร้อมใช้งาน! 🎉**
