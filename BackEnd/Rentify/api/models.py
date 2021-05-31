from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from datetime import datetime
from datetime import date


class WeekDay(models.Model):
    DAYS = [
        (0, 'Monday'),
        (1, 'Tuesday'),
        (2, 'Wednesday'),
        (3, 'Thursday'),
        (4, 'Friday'),
        (5, 'Saturday'),
        (6, 'Sunday')
    ]
    day_number = models.IntegerField(choices=DAYS)

    def day_name(self):
        return self.DAYS[self.day_number][1]

    def __str__(self):
        return self.day_name()


class Company(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(default="")
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company')
    active_days = models.ManyToManyField(WeekDay, related_name='open_companies', blank=True)
    # TODO: add active days to endpoints
    open_from = models.TimeField(default=None, null=True)
    close_at = models.TimeField(default=None, null=True)

    def has_active_plan(self):
        if len(self.subscriptions.all()) == 0:
            return False
        latest_plan = self.subscriptions.order_by('-starts')[0]
        if latest_plan.starts <= date.today() < latest_plan.ends:
            return True
        else:
            return False

    def __str__(self):
        return self.title


def store_directory_path(instance, filename):
    return 'store_{}/profile/{}'.format(instance.company.pk, filename)


class CompanyImage(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to=store_directory_path)

    def __str__(self):
        return "company id {}".format(self.company.pk)


class CompanySubscription(models.Model):
    plan_title = models.CharField(max_length=50)
    starts = models.DateField()
    ends = models.DateField()
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='subscriptions')

    def __str__(self):
        return "from {} to {} for company {}".format(self.starts, self.ends, self.company.pk)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='customer')

    def __str__(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)


class ContactInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contactInfo')

    def __str__(self):
        return "for user {}".format(self.user)


class PhoneNumber(models.Model):
    title = models.CharField(max_length=120)
    number = models.CharField(max_length=10)
    display = models.BooleanField(default=False)
    contactInfo = models.ForeignKey(ContactInfo, on_delete=models.CASCADE, related_name='phoneNumbers')

    def __str__(self):
        return "{} is {} for user {}".format(self.title, self.number, self.contactInfo.user)


class Address(models.Model):
    title = models.CharField(max_length=120)
    address = models.TextField()
    display = models.BooleanField(default=False)
    contactInfo = models.ForeignKey(ContactInfo, on_delete=models.CASCADE, related_name='addresses')

    def __str__(self):
        return "{} is {} for user {}".format(self.title, self.address, self.contactInfo.user)
    # number = models.IntegerField()
    # building_name = models.CharField(max_length=120)
    # house_number = models.CharField(max_length=120)
    # alley = models.CharField(max_length=120)
    # street = models.CharField(max_length=120)
    # neighbourhood = models.CharField(max_length=120)
    # city = models.CharField(max_length=120)
    # restrict = models.CharField(max_length=120)
    # country = models.CharField(max_length=120)
    # contact_info = models.ForeignKey('ContactInfo', on_delete=models.CASCADE, related_name='addresses')


class Invoice(models.Model):
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    tax = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    basket = models.OneToOneField('Basket', on_delete=models.CASCADE, related_name='invoice')

    def total_price(self):
        return sum([item.price() * item.quantity for item in self.basket.items()])

    def order_price(self):
        return self.total_price() + self.tax - self.discount

    def __str__(self):
        return "Invoice {} for basket {}".format(self.pk, self.basket.__str__())


class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=120, unique=True)
    parent_category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subCategories')

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=120, unique=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(default="")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    # remaining = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    needed_deposit = models.DecimalField(default=0, max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    category = models.ForeignKey(Category, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    sub_category = models.ForeignKey(SubCategory, related_name='products', on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='products', blank=True)

    def num_of_ratings(self):
        return len(self.ratings.all())

    def avg_ratings(self):
        ratings = self.ratings.all()
        if len(ratings) == 0:
            return 0
        else:
            return sum([rating.stars for rating in ratings]) / len(ratings)

    def is_available(self, requested_number=1):
        items = self.items.all()
        count = 0
        for item in items:
            if item.state() == 'In Progress':
                count += 1
        return self.quantity >= count + requested_number

    def __str__(self):
        return self.title


def product_directory_path(instance, filename):
    return 'store_{}/product_{}/{}'.format(instance.product.company.pk, instance.product.pk, filename)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    img = models.ImageField(upload_to=product_directory_path)

    def __str__(self):
        return "for product {}".format(self.product.pk)


class Rating(models.Model):
    RATING_CHOICES = [
        (1, 'One Star'),
        (2, 'Two Stars'),
        (3, 'Three Stars'),
        (4, 'Four Stars'),
        (5, 'Five Stars'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='ratings')
    stars = models.IntegerField(choices=RATING_CHOICES)

    def __str__(self):
        return "User {} gave {} to product {}".format(self.user.username, self.stars, self.product.title)


class Basket(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='basket')

    def items(self):
        return self.customer.items.filter(status=Item.STATUS_CHOICES[0][0])

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Invoice.objects.create(basket=self)

    def __str__(self):
        return 'basket for customer {}'.format(self.customer.pk)


class Item(models.Model):
    STATUS_CHOICES = [
        ('Waiting for Payment', 'Waiting for Payment'),
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Refunded', 'Refunded')
    ]

    STATE_CHOICES = [
        ('Pending', 'Pending'),  # not yet confirmed for booking
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ]
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        related_name='items',
        null=True
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    # order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='items')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    start = models.DateTimeField()
    end = models.DateTimeField()

    creation_time = models.DateTimeField(auto_now_add=True)
    pending_time = models.DateTimeField(default=None, null=True)
    confirmed_time = models.DateTimeField(default=None, null=True)
    cancelled_time = models.DateTimeField(default=None, null=True)
    inporgress_time = models.DateTimeField(default=None, null=True)
    completed_time = models.DateTimeField(default=None, null=True)
    refunded_time = models.DateTimeField(default=None, null=True)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.status == self.STATUS_CHOICES[1][0]:
            self.pending_time = datetime.now()
        elif self.status == self.STATUS_CHOICES[2][0]:
            self.confirmed_time = datetime.now()
        elif self.status == self.STATUS_CHOICES[3][0]:
            self.cancelled_time = datetime.now()
        elif self.status == self.STATUS_CHOICES[4][0]:
            self.inporgress_time = datetime.now()
        elif self.status == self.STATUS_CHOICES[5][0]:
            self.completed_time = datetime.now()
        elif self.status == self.STATUS_CHOICES[6][0]:
            self.refunded_time = datetime.now()
        super().save(force_insert, force_update, using, update_fields)

    def company(self):
        return self.product.company.pk

    def duration(self):
        difference = (self.end - self.start)
        return difference.days*24 + difference.seconds//3600

    def check_availability(self):
        return self.product.is_available(self.quantity)

    def state(self):
        if self.status == self.STATUS_CHOICES[3][0] or self.status == self.STATUS_CHOICES[5][0] or self.status == self.STATUS_CHOICES[6][0]:
            return self.STATUS_CHOICES[2][0]
        if self.status == self.STATUS_CHOICES[1][0] or self.status == self.STATUS_CHOICES[2][0]:
            return self.STATE_CHOICES[1][0]
        else:
            return self.STATE_CHOICES[0][0]

    def price(self):
        fees = sorted(self.product.fees.all(), key=lambda x: x.duration())
        for fee in fees:
            if self.duration() <= fee.duration():
                return fee.price
        biggest_fee = fees[-1]
        price = biggest_fee.price * (self.duration() // biggest_fee.duration())
        if self.duration() % biggest_fee.duration() != 0:
            price += biggest_fee.price
        return price

    def __str__(self):
        # return str(self.duration())
        return '{} numbers of {} for customer {} from {} to {}'\
            .format(self.quantity, self.product.title, self.customer.pk, self.start, self.end)


class Order(models.Model):
    # currently not being used

    STATUS_CHOICES = [
        ('Waiting for Payment', 'Waiting for Payment'),
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        # ('Cancelled', 'Cancelled'),
        # ('In Progress', 'In Progress'),
        # ('Completed', 'Completed'),
        # ('Refunded', 'Refunded')
    ]
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    invoice = models.OneToOneField(Invoice, on_delete=models.CASCADE, related_name='order', null=True, blank=True)
    status = models.CharField(
        default=STATUS_CHOICES[0][0],
        max_length=20,
        choices=STATUS_CHOICES
    )
    creation_time = models.DateTimeField(auto_now_add=True)
    pending_time = models.DateTimeField(default=None, null=True)
    confirmed_time = models.DateTimeField(default=None, null=True)
    # cancelled_time = models.DateTimeField(default=None)
    # inporgress_time = models.DateTimeField(default=None)
    # completed_time = models.DateTimeField(default=None)
    # refunded_time = models.DateTimeField(default=None)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.status == self.STATUS_CHOICES[1][0]:
            self.pending_time = datetime.now()
        elif self.status == self.STATUS_CHOICES[2][0]:
            self.confirmed_time = datetime.now()
        # elif self.status == self.STATUS_CHOICES[3][0]:
        #     self.cancelled_time = datetime.now()
        # elif self.status == self.STATUS_CHOICES[4][0]:
        #     self.inporgress_time = datetime.now()
        # elif self.status == self.STATUS_CHOICES[5][0]:
        #     self.completed_time = datetime.now()
        # elif self.status == self.STATUS_CHOICES[6][0]:
        #     self.refunded_time = datetime.now()
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return 'Order with id {} is {}'.format(self.pk, self.status)


class Fee(models.Model):
    FEE_CHOICES = [
        (1, 'Hour'),
        (24, 'Day'),
        (168, 'Week'),
        (744, 'Month'),     # 31 days month
        (8760, 'Year')    # 365 days year
    ]
    time_unit = models.IntegerField(choices=FEE_CHOICES)
    amount = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='fees')

    def duration(self):
        return self.time_unit * self.amount

    def __str__(self):
        return '{} x {} for {}'.format(self.amount, self.time_unit, self.price)
