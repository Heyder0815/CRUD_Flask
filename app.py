from flask import Flask
from flask import render_template,request,jsonify
import pyodbc

app = Flask(__name__)

def conectar_sql_server():
    try:
        conn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server};'
            'SERVER=HEYDER-MARTINEZ\\SQLEXPRESS;'
            'DATABASE=datacore;'
            'Trusted_Connection=yes;'
        )
        print("✅ Conectado a SQL Server")
        return conn
    except Exception as e:
        print("❌ Error de conexión:", e)
        return None

@app.route('/')
def index():
    
    conn = conectar_sql_server()
    if conn:
        cursor = conn.cursor()
        cursor.execute("select * from terceros_ventas where eliminado = '0'")  # Ajusta con tu tabla
        vendedores = cursor.fetchall()
        conn.close()
    else:
        vendedores = []
        
    return render_template('empleados/index.html', vendedores=vendedores)

@app.route('/create')
def create():
    
    return render_template('empleados/create.html')

@app.route('/update', methods=['POST'])
def actualizar():
    id = request.form.get('id')
    concepto_2 = request.form.get('concepto_2')
    descripcion = request.form.get('descripcion')
    activo = request.form.get('activo')
    linea = request.form.get('linea')
    coordinacion = request.form.get('coordinacion')
    nit_coord = request.form.get('nit_cordinador')
    coordinador = request.form.get('cordinador')
    correo_coord = request.form.get('correo_coord')
    cel_coord = request.form.get('cel_coord')
    ext_coord = request.form.get('ext_coord')
    nit_ejecutivo = request.form.get('nit_ejecutivo')
    ejecutivo = request.form.get('ejecutivo')
    correo_ejec = request.form.get('correo_ejec')
    cel_ejec = request.form.get('cel_ejec')
    ext_ejec = request.form.get('ext_ejec')

    try:
        conn = conectar_sql_server()
        cursor = conn.cursor()
        sql = """
        UPDATE terceros_ventas 
        SET concepto_2 = ?, descripcion = ?, activo = ?, linea = ?, coodinacion = ?, nit_coord = ?, coordinador = ?, correo_coord = ?, cel_coord = ?, ext_coord = ?, nit_ejecutivo = ?, ejecutivo = ?, correo_ejec = ?, cel_ejec = ?, ext_ejec = ? 
        WHERE id = ?
        """

        # ✅ Parámetros en el mismo orden que los ?
        params = (
            concepto_2, descripcion, activo, linea, coordinacion, nit_coord,
            coordinador, correo_coord, cel_coord, ext_coord, nit_ejecutivo,
            ejecutivo, correo_ejec, cel_ejec, ext_ejec, id
        )

        cursor.execute(sql, params)
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Usuario actualizado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
  
@app.route('/store', methods=['POST'])
def insertar():
    concepto_2 = request.form.get('concepto_2')
    descripcion = request.form.get('descripcion')
    activo = request.form.get('activo')
    linea = request.form.get('linea')
    coordinacion = request.form.get('coordinacion')
    nit_cordinador = request.form.get('nit_cordinador')
    cordinador = request.form.get('cordinador')
    correo_coord = request.form.get('correo_coord')
    cel_coord = request.form.get('cel_coord')
    ext_coord = request.form.get('ext_coord')
    nit_ejecutivo = request.form.get('nit_ejecutivo')
    ejecutivo = request.form.get('ejecutivo')
    correo_ejec = request.form.get('correo_ejec')
    cel_ejec = request.form.get('cel_ejec')
    ext_ejec = request.form.get('ext_ejec')

    try:
        conn = conectar_sql_server()
        cursor = conn.cursor()

        # Insertar datos con parámetros
        cursor.execute(
            "INSERT INTO terceros_ventas (concepto_2, descripcion, activo, linea, coodinacion, nit_coord, coordinador, correo_coord, cel_coord, ext_coord, nit_ejecutivo, ejecutivo, correo_ejec, cel_ejec, ext_ejec ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (concepto_2, descripcion, activo, linea, coordinacion,
            nit_cordinador, cordinador, correo_coord, cel_coord, ext_coord,
            nit_ejecutivo, ejecutivo, correo_ejec, cel_ejec, ext_ejec)
        )
        conn.commit()
        cursor.close()
        conn.close()

        return jsonify({"mensaje": "Usuario insertado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/eliminar/<int:id>')
def eliminar(id):
    id = int(id)
    conn = conectar_sql_server()
        
    try:
        conn = conectar_sql_server()
        cursor = conn.cursor()
        cursor.execute("update terceros_ventas set eliminado = '1' where id = ?",(id,))  # Ajusta con tu tabla
        conn.commit()
        cursor.close()
        conn.close()
        
        return jsonify({"mensaje": "Registro eliminado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        
@app.route('/edit/<int:id>') 
def edit(id): 
    
    conn = conectar_sql_server()
    cursor = conn.cursor()
    cursor.execute("select * from terceros_ventas where id = ?",(id,))
    empleados = cursor.fetchall()
    conn.close()
    
    return render_template('empleados/edit.html',empleados=empleados)
          
   
if __name__ == '__main__':
    app.run(debug=True)