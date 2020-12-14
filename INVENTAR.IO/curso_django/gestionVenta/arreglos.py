from Almacen.models import Productos


def eliminarVaciosLista(lista):
    for i in lista:
        if i == '':
            lista.remove(i)
    return lista

def crearDicSale(units,products,prices):
    dic = {}
    i = 0
    for p in products:
        producto = Productos.objects.get(id=p)
        dic[p] = {
            'id': products[i],
            'product': producto.name,
            'units': units[i],
            'prices': prices[i],
        }
        i+=1
    return  dic