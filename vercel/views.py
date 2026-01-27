from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from .models import Order, Customer, Employee, Booking, Product
from django.utils import timezone

# Create your views here.
def home(request):
    # ดึงสินค้าทั้งหมดที่เปิดใช้งาน
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'products': products,
    }
    return render(request, "home.html", context)

def product(request):
    # ดึงสินค้าทั้งหมดที่เปิดใช้งาน
    products = Product.objects.filter(is_active=True).order_by('-created_at')
    
    context = {
        'products': products,
    }
    return render(request, "cat.html", context)

def employee(request):
    return render(request, "employee.html")

@require_http_methods(["GET", "POST"])
def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        # ตรวจสอบอีเมลและรหัสผ่าน
        if email and password:
            # ใช้ Django authentication - หา user จาก email แล้ว authenticate ด้วย username
            from django.contrib.auth.models import User
            try:
                user = User.objects.get(email=email)
                user = authenticate(request, username=user.username, password=password)
                if user is not None:
                    auth_login(request, user)
                    # สร้าง Customer profile ถ้ายังไม่มี
                    Customer.objects.get_or_create(user=user)
                    return redirect('/profile')
                else:
                    return render(request, "login.html", {'error': 'รหัสผ่านไม่ถูกต้อง'})
            except User.DoesNotExist:
                return render(request, "login.html", {'error': 'ไม่พบอีเมลนี้ในระบบ'})
        else:
            return render(request, "login.html", {'error': 'กรุณากรอกอีเมลและรหัสผ่าน'})
    
    return render(request, "login.html")

@login_required(login_url='/login')
def logout(request):
    """ออกจากระบบ"""
    auth_logout(request)
    return redirect('/')

@require_http_methods(["GET", "POST"])
def register(request):
    """สมัครบัญชี"""
    if request.method == "POST":
        from django.contrib.auth.models import User
        
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        
        # ตรวจสอบ
        if not all([first_name, email, password, password_confirm]):
            return render(request, "register.html", {'error': 'กรุณากรอกข้อมูลให้ครบถ้วน'})
        
        if password != password_confirm:
            return render(request, "register.html", {'error': 'รหัสผ่านไม่ตรงกัน'})
        
        if len(password) < 6:
            return render(request, "register.html", {'error': 'รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร'})
        
        # ตรวจสอบอีเมลซ้ำ
        if User.objects.filter(email=email).exists():
            return render(request, "register.html", {'error': 'อีเมลนี้มีการใช้งานแล้ว'})
        
        try:
            # สร้าง User
            user = User.objects.create_user(
                username=email,  # ใช้อีเมลเป็น username
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name
            )
            
            # สร้าง Customer profile
            Customer.objects.create(user=user)
            
            # Auto-login หลังสมัครสำเร็จ
            auth_login(request, user)
            return redirect('/profile')
            
        except Exception as e:
            return render(request, "register.html", {'error': f'เกิดข้อผิดพลาด: {str(e)}'})
    
    return render(request, "register.html")


@login_required(login_url='/login')
@require_http_methods(["GET", "POST"])
def profile(request):
    """หน้าบัญชีลูกค้า - ต้องล็อกอินก่อน"""
    customer, created = Customer.objects.get_or_create(user=request.user)
    
    if request.method == "POST":
        # อัปเดตข้อมูลลูกค้า
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        
        customer.phone = phone
        customer.address = address
        customer.save()
        
        return JsonResponse({'success': True, 'message': 'บันทึกข้อมูลสำเร็จ'})
    
    # ดึงข้อมูลคำสั่งซื้อของลูกค้า
    orders = Order.objects.filter(customer=customer).order_by('-created_at')
    
    # ดึงข้อมูลการจองของลูกค้า
    bookings = Booking.objects.filter(customer=customer).order_by('-created_at')
    
    context = {
        'customer': customer,
        'orders': orders,
        'bookings': bookings,
        'total_orders': orders.count(),
    }
    return render(request, "profile.html", context)

@require_http_methods(["GET", "POST"])
def employee_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # ตรวจสอบชื่อผู้ใช้และรหัสผ่านพนักงาน
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                request.session['is_employee'] = True
                return redirect('/employee-sell')
            else:
                return render(request, "employee.html", {'error': 'ชื่อผู้ใช้หรือรหัสผ่านไม่ถูกต้อง'})
        else:
            return render(request, "employee.html", {'error': 'กรุณากรอกชื่อผู้ใช้และรหัสผ่าน'})
    
    return render(request, "employee.html")

@login_required(login_url='/login')
@require_http_methods(["GET", "POST"])
def create_order(request):
    """สั่งซื้อสินค้า - ต้องล็อกอินก่อน"""
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        quantity = request.POST.get('quantity')
        unit_price = request.POST.get('unit_price')
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        notes = request.POST.get('notes', '')
        receipt_image = request.FILES.get('receipt_image')
        
        # Validate
        if not all([product_name, quantity, unit_price, customer_name, customer_phone]):
            return JsonResponse({'success': False, 'message': 'กรุณากรอกข้อมูลให้ครบถ้วน'})
        
        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
            
            # ดึง Customer profile
            customer, created = Customer.objects.get_or_create(user=request.user)
            
            # สร้าง Order
            order = Order.objects.create(
                customer=customer,
                product_name=product_name,
                quantity=quantity,
                unit_price=unit_price,
                customer_name=customer_name,
                customer_phone=customer_phone,
                notes=notes,
                receipt_image=receipt_image if receipt_image else None,
                status='pending'
            )
            
            return JsonResponse({
                'success': True, 
                'message': f'สั่งซื้อสำเร็จ! เลขออเดอร์: {order.order_id}',
                'order_id': order.order_id
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'})
    
    return render(request, "shop.html")

def chat(request):
    """หน้า Contact - ไม่ต้องล็อกอิน"""
    return render(request, "chat.html")

@login_required(login_url='/login')
def shop(request):
    """หน้าสั่งซื้อ - ต้องล็อกอินก่อน"""
    return render(request, "shop.html")

@login_required(login_url='/login')
def booking(request):
    """หน้าจองสินค้า - บันทึกว่าจะซื้อที่หลัง"""
    if request.method == "POST":
        from django.contrib.auth.models import User
        
        product_name = request.POST.get('product_name', '').strip()
        quantity = request.POST.get('quantity', '1')
        unit_price = request.POST.get('unit_price', '0')
        notes = request.POST.get('notes', '').strip()
        
        # ตรวจสอบข้อมูลพื้นฐาน
        if not product_name or not quantity or not unit_price:
            return render(request, "booking.html", {'error': 'กรุณากรอกข้อมูลให้ครบถ้วน'})
        
        try:
            quantity = int(quantity)
            unit_price = float(unit_price)
            
            if quantity <= 0 or unit_price < 0:
                return render(request, "booking.html", {'error': 'ปริมาณและราคาต้องมากกว่า 0'})
            
            # ได้ Customer จาก user
            customer = Customer.objects.get(user=request.user)
            
            # สร้างการจอง
            from .models import Booking
            booking = Booking.objects.create(
                customer=customer,
                product_name=product_name,
                quantity=quantity,
                unit_price=unit_price,
                notes=notes
            )
            
            return render(request, "booking.html", {
                'success': True,
                'message': f'จองสินค้าสำเร็จ! รหัสการจอง: {booking.booking_id}',
                'booking_id': booking.booking_id
            })
            
        except ValueError:
            return render(request, "booking.html", {'error': 'ปริมาณและราคาต้องเป็นตัวเลข'})
        except Customer.DoesNotExist:
            return redirect('/profile')
        except Exception as e:
            return render(request, "booking.html", {'error': f'เกิดข้อผิดพลาด: {str(e)}'})
    
    return render(request, "booking.html")

@login_required(login_url='/employee')
@login_required(login_url='/employee')
def update_order_status(request, order_id):
    """อัปเดตสถานะออเดอร์ - เฉพาะพนักงาน"""
    if request.method == "POST":
        try:
            order = Order.objects.get(order_id=order_id)
            new_status = request.POST.get('status')
            
            if new_status in dict(Order.STATUS_CHOICES):
                order.status = new_status
                
                # หากอนุมัติ ให้บันทึก employee ที่อนุมัติ
                if new_status == 'approved':
                    try:
                        employee = Employee.objects.get(user=request.user)
                        order.approved_by = employee
                        order.approved_at = timezone.now()
                    except Employee.DoesNotExist:
                        pass
                
                order.save()
                # ส่ง JSON response สำหรับ AJAX, หรือ redirect สำหรับ form submission
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': 'อัปเดตสถานะสำเร็จ'})
                else:
                    return redirect('/employee-sell')
            else:
                return JsonResponse({'success': False, 'message': 'สถานะไม่ถูกต้อง'})
        except Order.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'ไม่พบออเดอร์นี้'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})

@login_required(login_url='/employee')
def employeesell(request):
    """ตารางคำสั่งซื้อ - เฉพาะพนักงาน"""
    # ดึงข้อมูลคำสั่งซื้อทั้งหมด
    orders = Order.objects.select_related('customer', 'approved_by').all()
    
    # Filter by status ถ้ามี
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Filter by date ถ้ามี
    date_filter = request.GET.get('date', '')
    if date_filter:
        orders = orders.filter(created_at__date=date_filter)
    
    # Search ถ้ามี
    search = request.GET.get('search', '')
    if search:
        orders = orders.filter(
            customer_name__icontains=search
        ) | orders.filter(
            order_id__icontains=search
        )
    
    context = {
        'orders': orders,
        'total_orders': Order.objects.count(),
    }
    return render(request, "employeesell.html", context)

@login_required(login_url='/employee')
@require_http_methods(["GET", "POST"])
def add_product(request):
    """หน้าเพิ่มสินค้า - เฉพาะพนักงาน"""
    if request.method == "POST":
        name = request.POST.get('name', '').strip()
        category = request.POST.get('category', '')
        price = request.POST.get('price', '')
        description = request.POST.get('description', '').strip()
        stock = request.POST.get('stock', '0')
        image = request.FILES.get('image', None)
        
        # ตรวจสอบข้อมูล
        if not name or not category or not price:
            return render(request, "add_product.html", {
                'error': 'กรุณากรอกชื่อสินค้า หมวดหมู่ และราคา'
            })
        
        try:
            price = float(price)
            stock = int(stock)
            
            if price < 0 or stock < 0:
                return render(request, "add_product.html", {
                    'error': 'ราคาและจำนวนต้องมากกว่า 0'
                })
            
            # สร้างสินค้า
            product = Product.objects.create(
                name=name,
                category=category,
                price=price,
                description=description,
                stock=stock,
                image=image,
                created_by=request.user
            )
            
            return render(request, "add_product.html", {
                'success': True,
                'message': f'เพิ่มสินค้าสำเร็จ! รหัส: {product.product_id}',
                'product_id': product.product_id
            })
        
        except ValueError:
            return render(request, "add_product.html", {
                'error': 'ราคาและจำนวนต้องเป็นตัวเลข'
            })
        except Exception as e:
            return render(request, "add_product.html", {
                'error': f'เกิดข้อผิดพลาด: {str(e)}'
            })
    
    context = {
        'categories': Product.CATEGORY_CHOICES
    }
    return render(request, "add_product.html", context)

@login_required(login_url='/login')
def cancel_booking(request, booking_id):
    """ยกเลิกการจอง"""
    try:
        booking = Booking.objects.get(booking_id=booking_id)
        
        # ตรวจสอบว่าเป็นเจ้าของการจองหรือไม่
        if booking.customer.user != request.user:
            return JsonResponse({'success': False, 'message': 'ไม่มีสิทธิ์ยกเลิกการจองนี้'})
        
        # ตรวจสอบสถานะ - สามารถยกเลิกได้เฉพาะ pending และ confirmed
        if booking.status not in ['pending', 'confirmed']:
            return JsonResponse({'success': False, 'message': f'ไม่สามารถยกเลิกการจองได้ (สถานะ: {booking.get_status_display()})'})
        
        booking.status = 'cancelled'
        booking.save()
        
        return redirect('/profile')
    
    except Booking.DoesNotExist:
        return redirect('/profile')
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'})


@login_required(login_url='/employee')
@require_http_methods(["POST", "DELETE"])
def delete_product(request, product_id):
    """ลบสินค้า - เฉพาะพนักงาน"""
    try:
        product = Product.objects.get(product_id=product_id)
        
        # ตรวจสอบว่าเป็นผู้สร้างหรือพนักงาน
        try:
            employee = Employee.objects.get(user=request.user)
            # พนักงานสามารถลบได้
        except Employee.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'เฉพาะพนักงานเท่านั้นที่ลบได้'}, status=403)
        
        product.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': f'ลบสินค้า {product.name} สำเร็จ'})
        else:
            return redirect('/product')
    
    except Product.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'ไม่พบสินค้านี้'}, status=404)
    except Exception as e:
        return JsonResponse({'success': False, 'message': f'เกิดข้อผิดพลาด: {str(e)}'}, status=500)


@login_required(login_url='/employee')
@require_http_methods(["GET"])
def manage_product(request):
    """หน้าจัดการสินค้า - เฉพาะพนักงาน"""
    # ตรวจสอบว่าเป็นพนักงานหรือ admin
    try:
        Employee.objects.get(user=request.user)
    except Employee.DoesNotExist:
        # ถ้าไม่ใช่พนักงาน ลองตรวจสอบ is_staff
        if not request.user.is_staff:
            return redirect('/employee-login')
    
    # ดึงสินค้าทั้งหมด
    products = Product.objects.all().order_by('-created_at')
    
    context = {
        'products': products,
    }
    return render(request, "manage_product.html", context)
