from django.contrib.auth.models import User
from vercel.models import Employee, Customer

# สร้าง admin superuser
if not User.objects.filter(username='admin').exists():
    admin_user = User.objects.create_superuser('admin', 'admin@cowboy.com', 'admin123')
    Employee.objects.create(
        employee_id='EMP-0001',
        user=admin_user,
        phone='0891234567',
        department='Management'
    )
    print("✓ สร้าง superuser สำเร็จ (username: admin, password: admin123)")
else:
    print("✓ superuser มีอยู่แล้ว")

# สร้าง employee ทดสอบ
if not User.objects.filter(username='employee1').exists():
    emp_user = User.objects.create_user('employee1', 'emp1@cowboy.com', 'employee123')
    emp_user.first_name = 'สมชาย'
    emp_user.last_name = 'ใจดี'
    emp_user.save()
    Employee.objects.create(
        employee_id='EMP-0002',
        user=emp_user,
        phone='0892345678',
        department='Sales'
    )
    print("✓ สร้าง employee ทดสอบสำเร็จ (username: employee1, password: employee123)")
else:
    print("✓ employee มีอยู่แล้ว")

# สร้าง customer ทดสอบ
if not User.objects.filter(username='customer1').exists():
    cust_user = User.objects.create_user('customer1', 'cust1@gmail.com', 'customer123')
    cust_user.first_name = 'สินใจ'
    cust_user.last_name = 'วงศ์มณฑ์'
    cust_user.save()
    Customer.objects.create(
        user=cust_user,
        phone='0893456789',
        address='123 ถนนศรีนครินทร์ แขวงวัฒนา เขตบางนา กรุงเทพฯ'
    )
    print("✓ สร้าง customer ทดสอบสำเร็จ (username: customer1, password: customer123)")
else:
    print("✓ customer มีอยู่แล้ว")

print("\n========== ข้อมูลการเข้าสู่ระบบ ==========")
print("Admin Dashboard: http://127.0.0.1:8000/admin/")
print("Admin Login: admin / admin123")
print("\nEmployee Login: employee1 / employee123")
print("Customer Login: customer1@gmail.com / customer123")
print("\n========================================")
