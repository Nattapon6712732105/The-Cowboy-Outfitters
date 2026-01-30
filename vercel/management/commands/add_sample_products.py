from django.core.management.base import BaseCommand
from vercel.models import Product
from django.contrib.auth.models import User
import random

class Command(BaseCommand):
    help = 'เพิ่มสินค้าตัวอย่าง 20 ชิ้น'

    def handle(self, *args, **options):
        # ข้อมูลสินค้าตัวอย่าง
        products_data = [
            # หมวก (hat)
            {'name': 'หมวกคาวบอยแบบคลาสสิก', 'category': 'hat', 'price': 1200, 'discount': 0, 'desc': 'หมวกแบบคาวบอยคลาสสิก ทำจากหนังแท้คุณภาพดี'},
            {'name': 'หมวกคาวบอยสีเข้ม', 'category': 'hat', 'price': 1350, 'discount': 10, 'desc': 'หมวกสีดำจมป่น ผ้าดีมาก'},
            {'name': 'หมวกคาวบอยวินเทจ', 'category': 'hat', 'price': 1500, 'discount': 0, 'desc': 'หมวกสไตล์วินเทจ เหมาะสำหรับสไตล์เก่า'},
            {'name': 'หมวกคาวบอยสีแสด', 'category': 'hat', 'price': 1400, 'discount': 15, 'desc': 'สีแสดสวย ใส่สบาย'},
            
            # รองเท้า (shoes)
            {'name': 'รองเท้าบูทคาวบอยหนัง', 'category': 'shoes', 'price': 3200, 'discount': 0, 'desc': 'บูทหนังแท้ คุณภาพดี ใส่สบายเท้า'},
            {'name': 'รองเท้าบูทคาวบอยสีน้ำตาล', 'category': 'shoes', 'price': 3500, 'discount': 20, 'desc': 'สีน้ำตาลคลาสสิก ใส่ลุยได้'},
            {'name': 'รองเท้าบูทคาวบอยสีดำ', 'category': 'shoes', 'price': 3400, 'discount': 0, 'desc': 'ใส่ได้ทั้งวันทำงาน'},
            {'name': 'รองเท้าบูทหนังสแควร์โตห์', 'category': 'shoes', 'price': 4000, 'discount': 10, 'desc': 'บูทสไตล์เวสเทิร์น'},
            
            # เสื้อผ้า (clothes)
            {'name': 'เสื้อเชิ้ตคาวบอยลายสก็อต', 'category': 'clothes', 'price': 890, 'discount': 0, 'desc': 'เสื้อเชิ้ตลายสก็อตแบบคาวบอย'},
            {'name': 'เสื้อเชิ้ตคาวบอยสีขาว', 'category': 'clothes', 'price': 850, 'discount': 5, 'desc': 'เสื้อขาวพื้น ใส่ได้บ่อย'},
            {'name': 'เสื้อเชิ้ตคาวบอยสีแดง', 'category': 'clothes', 'price': 950, 'discount': 0, 'desc': 'เสื้อสีแดงสดใส'},
            {'name': 'หากเท่าคาวบอยหนัง', 'category': 'clothes', 'price': 2500, 'discount': 15, 'desc': 'หากเท่าหนังแท้เหมาะสำหรับอุดมการณ์'},
            
            # เครื่องประดับ (accessories)
            {'name': 'หัวเข็มขัดคาวบอยเงิน', 'category': 'accessories', 'price': 450, 'discount': 0, 'desc': 'หัวเข็มขัดเงินสวย ใส่ได้นาน'},
            {'name': 'หัวเข็มขัดคาวบอยทอง', 'category': 'accessories', 'price': 500, 'discount': 10, 'desc': 'สีทองคลาสสิก'},
            {'name': 'สร้อยนาคอคาวบอย', 'category': 'accessories', 'price': 650, 'discount': 0, 'desc': 'สร้อยสไตล์เวสเทิร์น'},
            {'name': 'พวงกุญแจหนังคาวบอย', 'category': 'accessories', 'price': 300, 'discount': 20, 'desc': 'พวงกุญแจหนังแท้'},
            
            # อุปกรณ์ (equipment)
            {'name': 'อานม้าคาวบอย', 'category': 'equipment', 'price': 8500, 'discount': 0, 'desc': 'อานม้าหนังแท้คุณภาพสูง'},
            {'name': 'หนังสัดเชือก', 'category': 'equipment', 'price': 1200, 'discount': 5, 'desc': 'เชือกหนังแท้ คุณภาพดี'},
            {'name': 'ดาบคาวบอย', 'category': 'equipment', 'price': 2800, 'discount': 0, 'desc': 'ดาบสไตล์คาวบอย'},
            {'name': 'ชุดเครื่องหนังสำเร็จรูป', 'category': 'equipment', 'price': 5500, 'discount': 25, 'desc': 'ชุดหนังสำเร็จรูปสำหรับมือใหม่'},
        ]

        # ดึง admin user
        try:
            admin_user = User.objects.get(username='admin')
        except User.DoesNotExist:
            admin_user = User.objects.first()

        # เพิ่มสินค้า
        created_count = 0
        for product_data in products_data:
            try:
                product = Product.objects.create(
                    name=product_data['name'],
                    category=product_data['category'],
                    price=product_data['price'],
                    discount_percent=product_data['discount'],
                    description=product_data['desc'],
                    stock=random.randint(5, 30),  # สต็อกแบบสุ่ม 5-30 ชิ้น
                    is_active=True,
                    created_by=admin_user
                )
                created_count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ เพิ่ม: {product.product_id} - {product.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'✗ ผิดพลาด: {product_data["name"]} - {str(e)}'))

        self.stdout.write(self.style.SUCCESS(f'\n✅ สำเร็จ! เพิ่มสินค้า {created_count} ชิ้น'))
