from apps.coupon.models import Coupon
from apps.newsletter.models import Subscriber
from apps.store.models import Category, Product

from django.test import TestCase

class TestCoupon(TestCase):
    def create_coupon(self, code="test", value=123, active = False, num_available=20, num_used=20):
        return Coupon.objects.create(code=code, value=value, active=active, num_available=num_available, num_used=num_used)

    def test_CouponCreation(self):
        w = self.create_coupon()
        self.assertTrue(isinstance(w, Coupon))
        self.assertEqual(w.__str__(), w.code)

    def test_can_use(self):
        w = self.create_coupon()
        is_active = False
        if w.active == False:
            is_active = False
            self.assertEqual(w.active, is_active)
        if w.num_used >= w.num_available and w.num_available != 0:
            is_active = False
        self.assertEqual(w.can_use(), is_active)

    def test_use(self):
        w = self.create_coupon(active=True)

        if w.num_used == w.num_available:
            w.active = False
            self.assertEqual(w.active, False)

class TestNewsletter(TestCase):
    def create_sub(self, email="adam@gmail.com"):
        return Subscriber.objects.create(email=email)

    def test_return(self):
        s = self.create_sub()
        self.assertTrue(isinstance(s, Subscriber))
        self.assertEqual(s.__str__(), s.email)



class TestCategory(TestCase):
    def createCategory(self, title='title', slug='slug', is_featured=True):
        return Category.objects.create(title=title, slug=slug, is_featured=is_featured)

    def test_return_titlec(self):
        c = self.createCategory()
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(c.__str__(), c.title)

    def test_url(self):
        c = self.createCategory()
        self.assertTrue(isinstance(c, Category))
        self.assertEqual(c.get_absolute_url(), '/%s/' % (c.slug))

class TestProduct(TestCase):
    def createCategory(self, title='title', slug='slug', is_featured=True):
        return Category.objects.create(title=title, slug=slug, is_featured=is_featured)

    def createProduct(self, title='title', slug='slug', description='desc', price=11.29, is_featured=True, num_available=20):
        c = self.createCategory()
        return Product.objects.create(category=c, title=title, slug=slug, description=description, price=price, is_featured=is_featured, num_available=num_available)

    def test_return_titlep(self):
        p = self.createProduct()
        self.assertTrue(isinstance(p, Product))
        self.assertEqual(p.__str__(), p.title)

    def test_url_p(self):
        p = self.createProduct()
        self.assertTrue(isinstance(p, Product))
        self.assertEqual(p.get_absolute_url(), '/%s/%s/' % (p.category.slug, p.slug))

    def test_thumbnail(self):
        p = self.createProduct()
        if p.thumbnail:
            self.assertEqual(p.get_thumbnail(), p.thumbnail.url)
        else:
            if p.image:
                p.thumbnail = p.thumbnail.make_thumbnail(p.image)
                p.save()
                self.assertEqual(p.get_thumbnail(), p.thumbnail.url)
            else:
                self.assertEqual(p.get_thumbnail(), '')


