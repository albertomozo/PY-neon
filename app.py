from flask import Flask, render_template, request
import psycopg2

# Configuración de tu base de datos Neon
DB_URL = "postgresql://nondb?sslmode=require"

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

    return render_template('producto.html', prod=prod, atributos=atributos)

if __name__ == '__main__':
    app.run(debug=True)
