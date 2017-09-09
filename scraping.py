#!/usr/bin/env python
# -​*- coding: utf-8 -*​-

# ESTE SCRAPER SOLO TRAE LOS ANUNCIOS DESTACADOS.

from lxml import html
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# sitio web
web= requests.get('http://www.buscador5900.com/index.php')
# obtengo el DOM del sitio.
dom = html.fromstring(web.content)

# guardo en variables los id grupo y rubro para construir las url
id_grupo = dom.xpath('//*[@class="rubros_fondo"]/div[@class="rubro"]/@id_grupo')
id_rubro = dom.xpath('//*[@class="rubros_fondo"]/div[@class="rubro"]/@id_rubro')

# funcion para escribir en un archivo data.txt
def EscribirEnArchivo(data):
    archivo = open("data.txt","a")
    archivo.write(data)
    archivo.close()

print "Procesando..."

# recorro cada posible url del sitio conformada por los id grupo y rubro
for a,b in zip(id_grupo, id_rubro):
    # con zip concateno la url con los parametros de busqueda.
    site = "http://www.buscador5900.com/index.php?"
    url = "%sid_grupo=%s&id_rubro=%s" % (site, a, b)

    page = requests.get(url)
    tree = html.fromstring(page.content)

    # guardo en variables los datos extraidos con xpath para luego estructurar los datos.
    nombre = tree.xpath('//*[@class="destacado_fondo"]/div[2]/div[@class="destacado_razon"]/text()')
    descripcion = tree.xpath('//*[@class="destacado_fondo"]/div[2]/div[@class="destacado_descripcion"]/text()')
    direccion = tree.xpath('//*[@class="destacado_fondo"]/div[2]/div[@class="destacado_direccion"]/text()')
    telefono = tree.xpath('//*[@class="destacado_fondo"]/div[2]/div[@class="destacado_tel"]/text()')

    # estructuro los datos y los almaceno usando la función para escribir en el archivo txt.
    for i in range(len(nombre)):
        anuncio = "\nNombre: {0:s} \nDescripcion: {1:s} \nDireccion: {2:s} \nTelefono: {3:s} \n".format(nombre[i], descripcion[i], direccion[i], telefono[i])

        EscribirEnArchivo(anuncio)
print "Proceso Terminado."
