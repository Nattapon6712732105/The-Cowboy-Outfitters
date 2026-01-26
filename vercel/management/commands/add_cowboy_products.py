from django.core.management.base import BaseCommand
from vercel.models import Product

class Command(BaseCommand):
    help = 'เพิ่มสินค้าคาวบอยตัวอย่างลงในฐานข้อมูล'

    def handle(self, *args, **options):
        products_data = [
            {
                'name': 'หมวกคาวบอยหนังแท้',
                'category': 'hat',
                'price': 2500,
                'description': 'หมวกหนังแท้สีน้ำตาลคลาสสิก ทนทานและสวยงาม',
            },
            {
                'name': 'รองเท้าบูทตะวันตก',
                'category': 'shoes',
                'price': 4500,
                'description': 'รองเท้าบูทหนังแกะ สลักลวดลายดั้งเดิม',
            },
            {
                'name': 'เสื้อเชิ้ตลายสก๊อต',
                'category': 'clothes',
                'price': 1200,
                'description': 'เสื้อเชิ้ตผ้าฝ้ายระบายอากาศดี ลายสก๊อตแดง',
            },
            {
                'name': 'เข็มขัดหัวกระทิง',
                'category': 'accessories',
                'price': 1800,
                'description': 'เข็มขัดหนังเกรดพรีเมียม หัวกระทิงโลหะสำริด',
            },
            {
                'name': 'แจ็คเก็ตยีนส์',
                'category': 'clothes',
                'price': 3200,
                'description': 'แจ็คเก็ตยีนส์ฟอกสี สไตล์วินเทจคลาสสิก',
            },
            {
                'name': 'เชือกบ่วงบาศ',
                'category': 'equipment',
                'price': 850,
                'description': 'เชือกคุณภาพสูงสำหรับการฝึกซ้อม และการใช้งาน',
            },
            {
                'name': 'ที่ปม หนังแท้',
                'category': 'accessories',
                'price': 950,
                'description': 'ที่ปมหนังแท้ดีไซน์แบบเดิม ใช้ได้นาน',
            },
            {
                'name': 'เสื้อเชิ้ตผ้าเรยอน',
                'category': 'clothes',
                'price': 1500,
                'description': 'เสื้อเชิ้ตสีกรมท่า ผ้านิ่มสวมใส่สะบายๆ',
            },
            {
                'name': 'หมวกฟอร์ดสีดำ',
                'category': 'hat',
                'price': 2200,
                'description': 'หมวกฟอร์ดสีดำ กันแดดได้ดี',
            },
            {
                'name': 'กางเกงยีนส์',
                'category': 'clothes',
                'price': 2000,
                'description': 'กางเกงยีนส์ฟอก สวมใส่สบาย',
            },
            {
                'name': 'สร้อยหนังแท้',
                'category': 'accessories',
                'price': 1100,
                'description': 'สร้อยหนังแท้ติดขนาดเล็ก ผ้าดีไซน์สวย',
            },
            {
                'name': 'หมวกเสตสัน',
                'category': 'hat',
                'price': 3500,
                'description': 'หมวกเสตสันแท้ หนังแท้สีครีม คุณภาพสูง',
            },
        ]

        count = 0
        for product_data in products_data:
            # ตรวจสอบว่ามีสินค้านี้อยู่แล้วหรือไม่
            existing = Product.objects.filter(name=product_data['name']).exists()
            if not existing:
                Product.objects.create(**product_data)
                count += 1
                self.stdout.write(f"✓ เพิ่ม: {product_data['name']}")
            else:
                self.stdout.write(f"⚠ มีแล้ว: {product_data['name']}")

        self.stdout.write(self.style.SUCCESS(f'\n✅ เพิ่มสินค้าสำเร็จ {count} รายการ'))
