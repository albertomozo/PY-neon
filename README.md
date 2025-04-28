 **aplicación web sencilla usando Flask** (el micro-framework más popular de Python para web), que:

- Muestra un listado de categorías.
- Debajo de cada categoría, muestra los productos asociados.
- Cada producto tiene un botón para ver sus propiedades (atributos).
- Al pulsar el botón, se muestran las propiedades del producto seleccionado.

Este ejemplo usa **psycopg2** para conectarse a PostgreSQL (Neon) y **Bootstrap** para un diseño agradable.

---

## 1. **Instala dependencias**

```bash
pip install flask psycopg2-binary
```


---

## 2. **Código completo (`app.py`)**

```python
from flask import Flask, render_template, request
import psycopg2

# Configuración de tu base de datos Neon
DB_URL = "postgresql://USUARIO:CONTRASEÑA@ep-tunombre-host.neon.tech/NOMBRE_BD?sslmode=require"

app = Flask(__name__)

def get_connection():
    return psycopg2.connect(DB_URL)

@app.route('/')
def index():
    conn = get_connection()
    cur = conn.cursor()
    # Obtener todas las categorías
    cur.execute("SELECT categoria_id, nombre FROM categorias_hw ORDER BY nombre;")
    categorias = cur.fetchall()

    # Obtener todos los productos agrupados por categoría
    cur.execute("""
        SELECT producto_id, nombre, categoria_id
        FROM productos_hw
        ORDER BY categoria_id, nombre;
    """)
    productos = cur.fetchall()
    conn.close()

    # Organizar productos por categoría
    productos_por_categoria = {}
    for prod in productos:
        productos_por_categoria.setdefault(prod[2], []).append(prod)

    return render_template('index.html', categorias=categorias, productos_por_categoria=productos_por_categoria)

@app.route('/producto/<int:producto_id>')
def ver_producto(producto_id):
    conn = get_connection()
    cur = conn.cursor()
    # Obtener información básica del producto
    cur.execute("""
        SELECT p.nombre, p.fabricante, p.modelo, c.nombre, s.nombre, p.precio_sugerido
        FROM productos_hw p
        LEFT JOIN categorias_hw c ON p.categoria_id = c.categoria_id
        LEFT JOIN subcategorias_hw s ON p.subcategoria_id = s.subcategoria_id
        WHERE p.producto_id = %s
    """, (producto_id,))
    prod = cur.fetchone()

    # Obtener atributos del producto
    cur.execute("""
        SELECT a.nombre, pa.valor
        FROM producto_atributos pa
        JOIN atributos_hw a ON pa.atributo_id = a.atributo_id
        WHERE pa.producto_id = %s
    """, (producto_id,))
    atributos = cur.fetchall()
    conn.close()

    return render_template('producto.html', prod=prod, atributos=atribos)

if __name__ == '__main__':
    app.run(debug=True)
```


---

## 3. **Plantilla principal (`templates/index.html`)**

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Categorías y Productos</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
</head>
<body class="container">
    <h1 class="my-4">Catálogo de Hardware</h1>
    {% for cat in categorias %}
        <div class="card mb-3">
            <div class="card-header bg-primary text-white">
                <strong>{{ cat[1] }}</strong>
            </div>
            <ul class="list-group list-group-flush">
                {% for prod in productos_por_categoria.get(cat[0], []) %}
                    <li class="list-group-item d-flex justify-content-between align-items-center">
                        {{ prod[1] }}
                        <a href="{{ url_for('ver_producto', producto_id=prod[0]) }}" class="btn btn-info btn-sm">Ver propiedades</a>
                    </li>
                {% else %}
                    <li class="list-group-item">No hay productos en esta categoría.</li>
                {% endfor %}
            </ul>
        </div>
    {% endfor %}
</body>
</html>
```


---

## 4. **Plantilla de propiedades (`templates/producto.html`)**

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Propiedades del producto</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css">
</head>
<body class="container">
    <h2 class="my-4">Propiedades de {{ prod[0] }}</h2>
    <ul class="list-group mb-3">
        <li class="list-group-item"><strong>Fabricante:</strong> {{ prod[1] }}</li>
        <li class="list-group-item"><strong>Modelo:</strong> {{ prod[2] }}</li>
        <li class="list-group-item"><strong>Categoría:</strong> {{ prod[3] }}</li>
        <li class="list-group-item"><strong>Subcategoría:</strong> {{ prod[4] or 'N/A' }}</li>
        <li class="list-group-item"><strong>Precio:</strong> €{{ prod[5] }}</li>
    </ul>
    <h4>Atributos técnicos:</h4>
    <ul class="list-group">
        {% for atributo in atributos %}
            <li class="list-group-item">
                <strong>{{ atributo[0] }}:</strong> {{ atributo[1] }}
            </li>
        {% else %}
            <li class="list-group-item">Sin atributos técnicos registrados.</li>
        {% endfor %}
    </ul>
    <a href="{{ url_for('index') }}" class="btn btn-secondary mt-3">Volver al catálogo</a>
</body>
</html>
```


---

## 5. **Cómo usarlo**

1. Guarda el código Python como `app.py`.
2. Crea una carpeta `templates` y dentro de ella, los archivos `index.html` y `producto.html`.
3. Cambia la variable `DB_URL` con tu cadena de conexión real de Neon.
4. Ejecuta el servidor:

```bash
python app.py
```

5. Accede a [http://localhost:5000](http://localhost:5000) en tu navegador.



