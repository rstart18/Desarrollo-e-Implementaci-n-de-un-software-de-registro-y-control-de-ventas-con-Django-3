from django.http import HttpResponse
from django.conf import settings
from io import BytesIO
from reportlab.pdfgen import canvas
from django.views.generic import View
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from Almacen.models import Productos


class ReporteProductosPDF(View):

    def cabecera(self, pdf):
        archivo_imagen = settings.MEDIA_ROOT + '/img/logo/logo_django.png'
        pdf.drawImage(archivo_imagen, 40, 750, 120, 90, preserveAspectRatio=True)
        pdf.setFont("Helvetica", 16)
        pdf.drawString(230, 790, u"REPORTE DE INVENTARIO")

    def tabla(self, pdf, y):
        encabezados = ('id', 'Nombre', 'Unidades', 'P.entrada', 'P.salida', 'Proveedor', 'Categoria')
        detalles = [(producto.id, producto.name, producto.units, producto.enter_price, producto.exit_price, producto.Proveedor, producto.Categoria) for producto in
                    Productos.objects.all()]
        detalle_orden = Table([encabezados] + detalles, colWidths=[1 * cm, 4 * cm, 2 * cm, 2 * cm, 2 * cm, 3 * cm, 2 * cm])
        detalle_orden.setStyle(TableStyle(
            [
                ('ALIGN', (0, 0), (0, 0), 'CENTER'),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 0), (-10, -10), 8),
            ]
        ))
        detalle_orden.wrapOn(pdf, 800, 600)
        detalle_orden.drawOn(pdf, 60, y)

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type='application/pdf')
        buffer = BytesIO()
        pdf = canvas.Canvas(buffer)
        self.cabecera(pdf)
        y = 600
        self.tabla(pdf, y)
        pdf.showPage()
        pdf.save()
        pdf = buffer.getvalue()
        buffer.close()
        response.write(pdf)
        return response