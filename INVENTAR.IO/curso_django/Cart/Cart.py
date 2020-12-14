class Cart:
    def __init__(self,request):
        self.request = request
        self.session = request.session
        cart = self.session.get("cart")
        fact = self.session.get("fact")
        if not cart:
            cart = self.session['cart'] = {}
        if not fact:
            fact = self.session['fact'] = {}
        self.cart = cart

    def add (self,product,units):
        if  str(product.id) not in self.cart.keys():
            self.cart[product.id] = {
                "product_id": product.id,
                "name": product.name,
                "price": int(product.exit_price)*int(units),
                "units": units,
            }
        else:
            for key,value in self.cart.items():
                if key == str(product.id):
                    value['units'] = int(value['units']) + int(units)
                    value['price'] += int(product.exit_price) * int(units)
                    break
        self.fact = self.calc()
        self.save()

    def save(self):
        self.session["cart"] = self.cart
        self.session["fact"] = self.fact
        self.session.modified = True

    def remove(self,product):
        product_id = str(product.id)
        if  product_id in self.cart:
            del self.cart[product_id]
            self.fact = self.calc()
            self.save()

    def clear(self):
        self.session["cart"] = {}
        self.session["fact"] = {}
        self.session.modified = True

    def calc(self):
        total = 0
        for key, value in self.cart.items():
            total = total + value['price']
        iva = 19
        subtotal = int(total - (total * (iva * 0.01)))
        return {"total": total, "iva": iva, "subtotal": subtotal}

    def discount(self,discount):
        total = 0
        for key, value in self.cart.items():
            total = total + value['price']
        iva = 19
        total = total - (total * (int(discount) * 0.01))
        subtotal = int(total - (total * (iva * 0.01)))
        self.fact = {"total": total, "iva": iva, "subtotal": subtotal,"discount":discount}
        self.save()


