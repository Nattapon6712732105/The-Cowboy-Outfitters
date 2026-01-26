from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from vercel.models import Employee, Customer

class Command(BaseCommand):
    help = 'Initialize test data for CowboyShop'

    def handle(self, *args, **options):
        # Create admin superuser
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser('admin', 'admin@cowboy.com', 'admin123')
            Employee.objects.create(
                employee_id='EMP-0001',
                user=admin_user,
                phone='0891234567',
                department='Management'
            )
            self.stdout.write(self.style.SUCCESS('Created admin superuser: admin / admin123'))
        else:
            self.stdout.write(self.style.WARNING('Admin user already exists'))

        # Create employee test user
        if not User.objects.filter(username='employee1').exists():
            emp_user = User.objects.create_user('employee1', 'emp1@cowboy.com', 'employee123')
            emp_user.first_name = 'Somchai'
            emp_user.last_name = 'Jaidee'
            emp_user.save()
            Employee.objects.create(
                employee_id='EMP-0002',
                user=emp_user,
                phone='0892345678',
                department='Sales'
            )
            self.stdout.write(self.style.SUCCESS('Created employee test user: employee1 / employee123'))
        else:
            self.stdout.write(self.style.WARNING('Employee user already exists'))

        # Create customer test user
        if not User.objects.filter(username='customer1').exists():
            cust_user = User.objects.create_user('customer1', 'cust1@gmail.com', 'customer123')
            cust_user.first_name = 'Sinchai'
            cust_user.last_name = 'Wongsamon'
            cust_user.save()
            Customer.objects.create(
                user=cust_user,
                phone='0893456789',
                address='123 Srinakarin Road, Bangkok'
            )
            self.stdout.write(self.style.SUCCESS('Created customer test user: cust1@gmail.com / customer123'))
        else:
            self.stdout.write(self.style.WARNING('Customer user already exists'))

        self.stdout.write(self.style.SUCCESS('\n========== Login Information =========='))
        self.stdout.write('Admin Dashboard: http://127.0.0.1:8000/admin/')
        self.stdout.write('Admin Login: admin / admin123')
        self.stdout.write('\nEmployee Login: employee1 / employee123')
        self.stdout.write('Customer Login: cust1@gmail.com / customer123')
        self.stdout.write('========================================\n')
