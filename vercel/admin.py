from django.contrib import admin
from .models import Employee, Customer, Order, Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'category', 'price', 'stock', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('product_id', 'name', 'description')
    readonly_fields = ('product_id', 'created_at', 'updated_at')
    fieldsets = (
        ('ข้อมูลสินค้า', {
            'fields': ('product_id', 'name', 'category', 'price', 'stock', 'is_active')
        }),
        ('รายละเอียด', {
            'fields': ('description', 'image')
        }),
        ('การจัดการ', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'phone', 'department', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('employee_id', 'user__username', 'user__first_name')
    readonly_fields = ('created_at',)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'customer_name', 'product_name', 'quantity', 'total_price', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_id', 'customer_name', 'product_name', 'customer_phone')
    readonly_fields = ('order_id', 'created_at', 'updated_at', 'approved_at', 'receipt_image_preview')
    
    fieldsets = (
        ('ข้อมูลคำสั่งซื้อ', {
            'fields': ('order_id', 'customer', 'product_name', 'quantity', 'unit_price', 'total_price', 'created_at', 'updated_at')
        }),
        ('ข้อมูลลูกค้า', {
            'fields': ('customer_name', 'customer_phone')
        }),
        ('สลีปโอนเงิน', {
            'fields': ('receipt_image', 'receipt_image_preview')
        }),
        ('สถานะและการอนุมัติ', {
            'fields': ('status', 'approved_by', 'approved_at', 'notes')
        }),
    )
    
    def receipt_image_preview(self, obj):
        """แสดงตัวอย่างรูปภาพสลีป"""
        if obj.receipt_image:
            from django.utils.html import format_html
            return format_html(
                '<img src="{}" width="300" height="auto" style="border:1px solid #ddd; padding:5px; border-radius:5px;" />',
                obj.receipt_image.url
            )
        return 'ไม่มีรูปภาพ'
    receipt_image_preview.short_description = 'ตัวอย่างรูปภาพ'
    
    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data and obj.status == 'approved':
            from .models import Employee
            from django.utils import timezone
            try:
                employee = Employee.objects.get(user=request.user)
                obj.approved_by = employee
                obj.approved_at = timezone.now()
            except Employee.DoesNotExist:
                pass
        super().save_model(request, obj, form, change)
