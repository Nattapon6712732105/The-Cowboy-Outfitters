from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
import uuid

class Product(models.Model):
    """ตารางสินค้า"""
    CATEGORY_CHOICES = [
        ('hat', 'หมวก'),
        ('shoes', 'รองเท้า'),
        ('clothes', 'เสื้อผ้า'),
        ('accessories', 'เครื่องประดับ'),
        ('equipment', 'อุปกรณ์'),
    ]
    
    product_id = models.CharField(max_length=50, unique=True, db_index=True)
    name = models.CharField(max_length=200)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="ลดราคาเป็นเปอร์เซ็นต์ (0-100)")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    stock = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.product_id} - {self.name}"
    
    def get_discounted_price(self):
        """คำนวณราคาหลังลดราคา"""
        if self.discount_percent > 0:
            discount_amount = self.price * (self.discount_percent / 100)
            return self.price - discount_amount
        return self.price
    get_discounted_price.short_description = "ราคาหลังลดราคา"
    
    def get_discount_amount(self):
        """คำนวณจำนวนเงินที่ลดราคา"""
        if self.discount_percent > 0:
            return self.price * (self.discount_percent / 100)
        return 0
    get_discount_amount.short_description = "จำนวนเงินลด"
    
    def save(self, *args, **kwargs):
        # ตรวจสอบค่า discount_percent
        if self.discount_percent < 0 or self.discount_percent > 100:
            raise ValueError("ส่วนลดต้องเป็นระหว่าง 0 ถึง 100 เปอร์เซ็นต์")
        if not self.product_id:
            # สร้าง product_id แบบอัตโนมัติ เช่น PRD-001, PRD-002, ...
            # หาหมายเลข product_id ที่มีค่ามากที่สุด
            try:
                last_product = Product.objects.filter(product_id__startswith='PRD-').order_by('-product_id').first()
                if last_product:
                    # ดึงหมายเลขจาก product_id เช่น "PRD-005" -> 5
                    last_num = int(last_product.product_id.split('-')[1])
                    new_num = last_num + 1
                else:
                    new_num = 1
            except (ValueError, IndexError):
                new_num = 1
            
            # สร้าง product_id ใหม่
            while True:
                self.product_id = f'PRD-{new_num:03d}'
                # ตรวจสอบว่า product_id นี้มีอยู่แล้วหรือไม่
                if not Product.objects.filter(product_id=self.product_id).exists():
                    break
                new_num += 1
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Products"
        ordering = ['-created_at']


class Employee(models.Model):
    """ตารางพนักงาน"""
    employee_id = models.CharField(max_length=50, unique=True, primary_key=True)  # รหัสพนักงาน EMP001
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    department = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee_id} - {self.user.get_full_name() or self.user.username}"
    
    class Meta:
        verbose_name_plural = "Employees"
        ordering = ['-created_at']


class Customer(models.Model):
    """ตารางลูกค้า"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}"
    
    class Meta:
        verbose_name_plural = "Customers"
        ordering = ['-created_at']


class Booking(models.Model):
    """ตารางการจอง - บันทึกสินค้าที่ลูกค้าสนใจซื้อทีหลัง"""
    STATUS_CHOICES = [
        ('pending', 'รอยืนยัน'),
        ('confirmed', 'ยืนยันแล้ว'),
        ('converted', 'แปลงเป็นคำสั่งซื้อ'),
        ('cancelled', 'ยกเลิก'),
    ]
    
    booking_id = models.CharField(max_length=50, unique=True, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.booking_id} - {self.customer.user.get_full_name()}"
    
    def save(self, *args, **kwargs):
        if not self.booking_id:
            # สร้าง booking_id แบบอัตโนมัติ เช่น BKG-20250126-001
            today = datetime.now().strftime('%Y%m%d')
            count = Booking.objects.filter(booking_id__startswith=f'BKG-{today}').count() + 1
            self.booking_id = f'BKG-{today}-{count:03d}'
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Bookings"
        ordering = ['-created_at']


class Order(models.Model):
    """ตารางคำสั่งซื้อ"""
    STATUS_CHOICES = [
        ('pending', 'รอการตรวจสอบ'),
        ('approved', 'อนุมัติแล้ว'),
        ('rejected', 'ปฏิเสธ'),
        ('shipped', 'จัดส่งแล้ว'),
        ('completed', 'สำเร็จ'),
    ]
    
    order_id = models.CharField(max_length=50, unique=True, db_index=True)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    product_name = models.CharField(max_length=200)
    quantity = models.IntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    customer_name = models.CharField(max_length=200)  # ชื่อลูกค้า
    customer_phone = models.CharField(max_length=20)  # เบอร์โทรศัพท์
    notes = models.TextField(blank=True)  # หมายเหตุเพิ่มเติม
    receipt_image = models.ImageField(upload_to='receipts/', null=True, blank=True)  # สลีปโอนเงิน
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_by = models.ForeignKey(Employee, null=True, blank=True, on_delete=models.SET_NULL)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.order_id} - {self.customer_name}"
    
    def save(self, *args, **kwargs):
        if not self.order_id:
            # สร้าง order_id แบบอัตโนมัติ เช่น ORD-20250126-001
            today = datetime.now().strftime('%Y%m%d')
            count = Order.objects.filter(order_id__startswith=f'ORD-{today}').count() + 1
            self.order_id = f'ORD-{today}-{count:03d}'
        
        # คำนวณราคารวม
        if self.quantity and self.unit_price:
            self.total_price = self.quantity * self.unit_price
        
        super().save(*args, **kwargs)
    
    class Meta:
        verbose_name_plural = "Orders"
        ordering = ['-created_at']

class ContactMessage(models.Model):
    """ตารางข้อความติดต่อจากฟอร์ม contact"""
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=300)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.subject} - {self.name} ({self.created_at.strftime('%d/%m/%Y')})"
    
    class Meta:
        verbose_name_plural = "Contact Messages"
        ordering = ['-created_at']