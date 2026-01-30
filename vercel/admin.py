from django.contrib import admin
from django.db.models import Sum, Count, Q
from .models import Employee, Customer, Order, Product, ContactMessage


# Dashboard Admin Class
class CowboyAdminSite(admin.AdminSite):
    site_header = "CowboyShop - ระบบจัดการ"
    site_title = "CowboyShop Admin"
    index_title = "ยินดีต้อนรับเข้าสู่ Admin Panel"
    
    def index(self, request, extra_context=None):
        """แสดง Dashboard ที่หน้า admin"""
        # คำนวณสถิติ
        total_orders = Order.objects.count()
        total_sales = Order.objects.aggregate(Sum('total_price'))['total_price__sum'] or 0
        total_customers = Customer.objects.count()
        total_products = Product.objects.count()
        unread_messages = ContactMessage.objects.filter(is_read=False).count()
        
        # สถิติตามสถานะ
        pending_orders = Order.objects.filter(status='pending').count()
        approved_orders = Order.objects.filter(status='approved').count()
        shipped_orders = Order.objects.filter(status='shipped').count()
        completed_orders = Order.objects.filter(status='completed').count()
        
        # ยอดขายเมื่อไม่นี้ (7 วันล่าสุด)
        from django.utils import timezone
        from datetime import timedelta
        week_ago = timezone.now() - timedelta(days=7)
        recent_sales = Order.objects.filter(created_at__gte=week_ago).aggregate(Sum('total_price'))['total_price__sum'] or 0
        
        extra_context = extra_context or {}
        extra_context.update({
            'total_orders': total_orders,
            'total_sales': f"{total_sales:,.2f}",
            'total_customers': total_customers,
            'total_products': total_products,
            'unread_messages': unread_messages,
            'pending_orders': pending_orders,
            'approved_orders': approved_orders,
            'shipped_orders': shipped_orders,
            'completed_orders': completed_orders,
            'recent_sales': f"{recent_sales:,.2f}",
        })
        
        return super().index(request, extra_context)


# สร้าง admin site ใหม่
cowboy_admin_site = CowboyAdminSite(name='cowboy_admin')

class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_id', 'name', 'category', 'price', 'discount_percent', 'stock', 'is_active', 'created_at')
    list_filter = ('category', 'is_active', 'created_at')
    search_fields = ('product_id', 'name', 'description')
    readonly_fields = ('product_id', 'created_at', 'updated_at')
    fieldsets = (
        ('ข้อมูลสินค้า', {
            'fields': ('product_id', 'name', 'category', 'price', 'discount_percent', 'stock', 'is_active')
        }),
        ('รายละเอียด', {
            'fields': ('description', 'image')
        }),
        ('การจัดการ', {
            'fields': ('created_by', 'created_at', 'updated_at')
        }),
    )

cowboy_admin_site.register(Product, ProductAdmin)

class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'user', 'phone', 'department', 'created_at')
    list_filter = ('department', 'created_at')
    search_fields = ('employee_id', 'user__username', 'user__first_name')
    readonly_fields = ('created_at',)

cowboy_admin_site.register(Employee, EmployeeAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'phone')
    readonly_fields = ('created_at',)

cowboy_admin_site.register(Customer, CustomerAdmin)

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

cowboy_admin_site.register(Order, OrderAdmin)

class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'is_read', 'created_at')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message', 'phone')
    readonly_fields = ('created_at', 'name', 'email', 'phone', 'subject', 'message')
    
    fieldsets = (
        ('ข้อมูลผู้ติดต่อ', {
            'fields': ('name', 'email', 'phone')
        }),
        ('เนื้อหา', {
            'fields': ('subject', 'message')
        }),
        ('สถานะ', {
            'fields': ('is_read', 'created_at')
        }),
    )
    
    def has_add_permission(self, request):
        """ไม่อนุญาตให้เพิ่มข้อความผ่าน admin"""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """เฉพาะ admin เท่านั้นที่ลบได้"""
        return request.user.is_superuser
    
    actions = ['mark_as_read', 'mark_as_unread']
    
    def mark_as_read(self, request, queryset):
        """ทำเครื่องหมายว่าอ่านแล้ว"""
        updated = queryset.update(is_read=True)
        self.message_user(request, f'ทำเครื่องหมายให้ {updated} ข้อความเป็น อ่านแล้ว')
    mark_as_read.short_description = 'ทำเครื่องหมายว่าอ่านแล้ว'
    
    def mark_as_unread(self, request, queryset):
        """ทำเครื่องหมายว่ายังไม่อ่าน"""
        updated = queryset.update(is_read=False)
        self.message_user(request, f'ทำเครื่องหมายให้ {updated} ข้อความเป็น ยังไม่อ่าน')
    mark_as_unread.short_description = 'ทำเครื่องหมายว่ายังไม่อ่าน'

cowboy_admin_site.register(ContactMessage, ContactMessageAdmin)