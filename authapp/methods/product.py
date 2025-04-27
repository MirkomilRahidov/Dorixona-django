from django.db import models


from methodism import custom_response as cr, error_messages, MESSAGE
def add_card(request, params):
    from home.model.card import Card
    from home.model.order import Order
    from home.model.products import Medicine
    from home.model.products import Category
    if 'product_id' not in params:
        return  cr(False,message=MESSAGE['DataNotFull'])
    
    
    product= Medicine.objects.filter(id=params['product_id']).first()
    if not product:
        return cr(False,message=MESSAGE['NotData'])
    
    card = Card.objects.get_or_create(product=params['product_id'], quantity = params.get('qt',1)[0], user = request.user)
    card.quantity = params.get('qt',card.quantity)
    card.save()
    
    return cr(True, message=f"Cardga qoshildi{product.title}")    

def get_card(request, params):
    from home.model.card import Card

    card = Card.objects.filter(product__id=params['product_id'], user=request.user).first()
    if not card:
        return cr(False, message=MESSAGE['NotData'])

    return cr(True, message="Mahsulot topildi", data={
        "product": card.product.id,
        "quantity": card.quantity
    })


def delete_card(request,params):
    from home.model.card import Card
    from home.model.order import Order
    from home.model.products import Medicine
    from home.model.products import Category
    
    card = Card.objects.filter(post__id=params['product_id']).first()
    
    if not card:
        return cr(False,message=MESSAGE['NotData'])
    
    card.delete()
    
    return cr(True,message='Ochirildi')

def order(request, params):
    from home.model.card import Card
    from home.model.order import Order
    from home.model.products import Medicine
    from home.model.products import Category
    
    cards = Card.object.filter(user=request.user, status=True)
    
    if not card.exists():
        return cr(False,"Savatingizda hali hichnima yoq")
    
    # order = Order.objects.create(user=request.user, card=card)
    
    for card in cards:
        order.objects.create(user=request.user,card=card,price=card.post.price * card.quantity)
    card.delete()
    return cr(True,message='Zakaz berildi')
    
def get_order(request, params):
    from home.model.order import Order

    order = Order.objects.filter(id=params.get('order_id'), user=request.user).first()
    if not order:
        return cr(False, message=MESSAGE['NotData'])

    return cr(True, message="Buyurtma topildi", data={
        "order_id": order.id,
        "status": order.status,
        "price": order.price
    })

def qabul_qil_order(request, params):
    from home.model.order import Order

    order = Order.objects.filter(id=params.get('order_id'), user=request.user).first()
    if not order:
        return cr(False, message=MESSAGE['NotData'])

    order.status = 'qabul_qilindi'
    order.save()

    return cr(True, message="Buyurtma qabul qilindi")

def add_like(request, params):
    from home.model.products import Like
    from home.model.products import Medicine

    product = Medicine.objects.filter(id=params.get('product_id')).first()
    if not product:
        return cr(False, message=MESSAGE['NotData'])
    
    like, created = Like.objects.get_or_create(user=request.user, product=product)
    if not created:
        return cr(False, message="Siz allaqachon like bosgansiz.")

    return cr(True, message="Like bosildi.")

def remove_like(request, params):
    from home.model.products import Like

    like = Like.objects.filter(user=request.user, product_id=params.get('product_id')).first()
    if not like:
        return cr(False, message="Siz hali like bosmagansiz.")
    
    like.delete()
    return cr(True, message="Like olib tashlandi.")


    