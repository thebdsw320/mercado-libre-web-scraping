# Web Scraper de Mercado Libre en Python

## Requisitos
- Python 3.7>=
- Modulos especificados en ```requirements.txt```

## ¿Cómo correr el programa?
```bash
$ python3 -m venv {NOMBRE_AMBIENTE}
```
Para usos prácticos, el nombre del ambiente será ```env```.
```bash
$ source env/bin/activate
(env) $ pip install -r requirements.txt 
(env) $ python3 scraper.py
```

Después de eso el programa te pedirá la palabra que quieres buscar (ej. smartwach). También te dirá si quieres filtrar por productos marcados con **Envío gratis** o con **Envío Full**. 

Te mostrará cúantos productos encontró con esas características y después te pedirá un nombre para el directorio en donde se guardaran las imagenes de los productos.

El programa arroja un archivo con formato **.xlsx** que muestra:
1. Nombre del producto
2. Precio 
3. Link del producto 
4. Link de la imagen del producto

NOTA: En el repo también se encuentra el driver, en este caso estoy usando el de Firefox, por practicidad, lo dejo por ahí para que todo funcione correctamente.