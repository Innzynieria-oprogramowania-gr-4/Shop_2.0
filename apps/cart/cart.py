from django.conf import settings

from apps.store.models import Product

#kod klasy Cart pozwalającej na zarządzanie koszykiem na zkaupy
class Cart(object):
    #zainicjowanie koszyka na zakupy wraz z obiektem request
    def __init__(self, request):
        #przechowywanie bieżącej sesji
        self.session = request.session
        #pobranie koszyka na zakupy z bieżącej sesji
        cart = self.session.get(settings.CART_SESSION_ID)
        #zapis pustego koszyka na zakupy w sesji
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        
        self.cart = cart
    # w metodzie __iter__() pobieramy egzemplarze Product, które reprezentują
    # produkty znajdujące się w koszyku
    def __iter__(self):
        #pobranie obiektów produktów i dodanie do koszyka na zakupy
        product_ids = self.cart.keys()        
        product_clean_ids = []

        #iteracja przez produkty w koszyku
        for p in product_ids:
            product_clean_ids.append(p)

            self.cart[str(p)]['product'] = Product.objects.get(pk=p)

        for item in self.cart.values():
            #dodajemy atrybut total_price dla każdego produktu
            item['total_price'] = float(item['price']) * int(item['quantity'])

            yield item

# obliczanie wszystkich elementów w koszyku na zakupy
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
# metoda pozwalająca na dodanie produktu do koszyka lub zmianę ilości
    def add(self, product, quantity=1, update_quantity=False):
        product_id = str(product.id)
        price = product.price

        print('Product_id:', product_id)

        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': price, 'id': product_id}
        
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] = self.cart[product_id]['quantity'] + 1
        
        self.save()

    # sprawdza czy w koszyku są produkty
    def has_product(self, product_id):
        if str(product_id) in self.cart:
            return True
        else:
            return False
    #  cs hnusunięcie produktu z koszyka na zakupy
    def remove(self, product_id):
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()
    #oznaczanie sesji jako "zmodyfikowanej", aby upewnić sie o jej zapisaniu
    def save(self):
        self.session[settings.CART_SESSION_ID] = self.cart
        self.session.modified = True
    # usunięcie koszyka na zakuy z sesji
    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True

    def get_total_length(self):
        return sum(int(item['quantity']) for item in self.cart.values())
    
    def get_total_cost(self):
        return sum(float(item['total_price']) for item in self)