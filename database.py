import sqlite3
import pytz
import os
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


class Database:

    filename = os.environ.get('DATABASE')
    repo = os.environ.get('DATABASE_REPO')
    splitted_filename = filename.split('/')
    dirs = splitted_filename[:len(splitted_filename) - 1] if len(splitted_filename) > 1 else None
    BASE_DIR = os.path.dirname(Path(filename).resolve())
    db_path = os.path.join(BASE_DIR, filename)
    
    conn = None

    def __init__(self):
        '''if self.dirs:
            for dir in self.dirs:
                os.mkdir(dir)
                if dir != self.dirs[-1]:
                    os.chdir(dir)'''
        if not os.exists('data'):
            os.system(f'git clone {self.repo} data')
        else:
            os.chdir('data')
            os.system('git pull')
            os.chdir('../')

        self.create_connection(self.filename)

        try:
            self.conn.execute('''
                CREATE TABLE IF NOT EXISTS registros(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    fecha DATE,
                    descripcion TEXT NOT NULL,
                    ultimo_precio REAL,
                    cantidad INTEGER,
                    moneda TEXT,
                    ganancia_porcentaje REAL,
                    valorizado REAL,
                    simbolo TEXT,
                    variacion_diaria REAL,
                    ganancia REAL
                )
            ''')

            # Guarda los cambios y cierra la conexión
            self.conn.commit()

            print("Base de datos creada!\n")
        except:
            print("Conexion establecida con la Base de datos\n")
    
    def _generate_timestamp(self):
        '''Gets current date and time'''
        fecha_hora_actual = datetime.now()

        # formatear la fecha y hora como una cadena para usar como nombre de archivo
        formato = "%Y-%m-%d_%H-%M-%S"  # Cambia el formato según tus necesidades
        nombre_archivo = fecha_hora_actual.strftime(formato)

        return nombre_archivo
    
    def _get_date(self):
        return datetime.now().strftime('%Y-%m-%d')

    def current_datetime(self):
        fecha_hora_actual = datetime.now()
        hora = fecha_hora_actual.astimezone(
         pytz.timezone('America/Argentina/Buenos_Aires')).strftime('%H:%M')

        return f'[{hora} hs]'

    def create_connection(self, db_file):
        try:
            self.conn = sqlite3.connect(db_file)
            return True
        except sqlite3.Error as e:
            print(e)
        return False

    def query(self, q):
        self.create_connection(self.filename)

        resultado = self.conn.execute(q)

        print(resultado.fetchall())

    def query_all(self):
        self.create_connection(self.filename)

        resultado = self.conn.execute("SELECT * FROM registros")

        print(resultado.fetchall())

    def query_month(self, month=None, draw=False):
        '''Format: Y-mm'''
        self.create_connection(self.filename)

        if month is None:
            # Obtiene el mes actual en formato 'YYYY-MM'
            month = datetime.now().strftime('%Y-%m')

        # Realiza la consulta para obtener la sumatoria de trabajos del mes actual
        query = "SELECT SUM(cantidad) FROM registros WHERE strftime('%Y-%m', fecha) = ?"
        resultado = self.conn.execute(query, (month, ))

        # Imprime la sumatoria de trabajos del mes actual
        sumatoria = resultado.fetchone()[0]
        print(f"El total de trabajos del mes {month} es: {sumatoria}")

        # Realiza la consulta para obtener todos los registros del mes actual
        query = "SELECT * FROM registros WHERE strftime('%Y-%m', fecha) = ? ORDER BY fecha DESC, id DESC"
        resultado = self.conn.execute(query, (month, ))
        registros = resultado.fetchall()

        # Cierra la conexión
        self.close()

        if draw:
            self.draw_table(registros)

        return registros

    def draw_table(self, regs):
        if len(regs) == 0:
            print("\nAun no hay registros para este mes")
        else:
            # Imprime cada registro del mes actual
            month = regs[0][1][5:7]
            print(f"\n\nRegistros del mes {month}:\n")
            print("  id  |   Fecha    | Cantidad | Comentarios")
            print("-" * 70)
            for registro in regs:
                fecha_descompuesta = registro[1].split("-")
                fecha_formateada = f"{fecha_descompuesta[2]}/{fecha_descompuesta[1]}/{fecha_descompuesta[0]}"
                relleno_id = str(registro[0]).zfill(3)
                print(
                 f"  {relleno_id} | {fecha_formateada} |    {str(registro[2]).zfill(2)}    | {'-' if registro[3] == None else registro[3]}"
                )

    def add_dict_data(self, data):
        for i, record in enumerate(data):
            self.add_data(
                self._get_date(), record['descripcion'], record['ultimo_precio'],
                record['cantidad'], record['moneda'],
                record['ganancia_porcentaje'], record['valorizado'],
                record['simbolo'], record['variacion_diaria'],
                record['ganancia']
            )
            
            print(f'Saved record {i + 1}/{len(data)}')

    def add_data(self, date: str, descripcion: str, ultimo_precio: float,
                 cantidad: int, moneda: str, ganancia_porcentaje: float,
                 valorizado: float, simbolo: str, variacion_diaria: float,
                 ganancia: float):
        self.create_connection(self.filename)

        try:
            self.conn.execute("""
                INSERT INTO registros (fecha, descripcion, ultimo_precio,
                cantidad, moneda, ganancia_porcentaje, valorizado,
                simbolo, variacion_diaria, ganancia)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (date, descripcion, ultimo_precio, cantidad, moneda,
                 ganancia_porcentaje, valorizado, simbolo,
                 variacion_diaria, ganancia)
            )

            self.conn.commit()

        except Exception as e:
            print(str(e))

        finally:
            self.close()

            print(f'{self.current_datetime()} Carga exitosa!')

    def edit_date(self, id_number, new_date):
        self.create_connection(self.filename)

        # Ejecutar la sentencia SQL para modificar el campo
        self.conn.execute("UPDATE registros SET fecha = ? WHERE id = ?",
                          (new_date, id_number))

        # Hace commit de los cambios realizados en la base de datos
        self.conn.commit()

        # Cierra la conexión
        self.close()

    def edit_quantity(self, id_number, new_quantity):
        self.create_connection(self.filename)

        # Ejecutar la sentencia SQL para modificar el campo
        self.conn.execute("UPDATE registros SET cantidad = ? WHERE id = ?",
                          (new_quantity, id_number))

        # Hace commit de los cambios realizados en la base de datos
        self.conn.commit()

        self.close()

    def edit(self, id_number, new_date, new_quantity):
        self.conn.execute(
         "UPDATE registros SET fecha = ?, cantidad = ? WHERE id = ?",
         (new_date, new_quantity, id_number))

        # Hace commit de los cambios realizados en la base de datos
        self.conn.commit()

        self.close()

    def delete_current_month(self):
        self.create_connection(self.filename)

        # Obtiene el mes actual en formato 'YYYY-MM'
        mes_actual = datetime.now().strftime('%Y-%m')

        # Borra todos los registros del mes actual
        query = "DELETE FROM registros WHERE strftime('%Y-%m', fecha) = ?"
        self.conn.execute(query, (mes_actual, ))

        # Guarda los cambios y cierra la conexión
        self.conn.commit()

        mes_actual = datetime.now().strftime('%m')
        print(f'Se han borrado los datos del mes {mes_actual}')

        self.close()

    def delete_by_id(self, id_number):
        self.create_connection(self.filename)

        try:
            if id_number == list(id_number):
                for record in id_number:
                    # Borra todos los registros del mes actual
                    query = "DELETE FROM registros WHERE id = ?"
                    self.conn.execute(query, (record, ))

                    # Guarda los cambios y cierra la conexión
                    self.conn.commit()

                    print(f'Se ha borrado el registro con ID={record}')
        except TypeError:
            query = "DELETE FROM registros WHERE id = ?"
            self.conn.execute(query, (id_number, ))

            self.conn.commit()

            print(f'Se ha borrado el registro con ID={id_number}')
        finally:
            self.close()

    def delete(self):
        os.remove(self.filename)

        print("Base de datos eliminada!")

    def close(self):
        self.conn.close()


def main():
    db = Database()
    #db.add_data(12, 'Agencia Rafaela', '2023-08-11')
    #db.query_all()
    #db.query("SELECT * FROM registros ORDER BY fecha DESC")
    #db.delete_by_id(25)

    #db.delete()


if __name__ == "__main__":
    main()
