import db
import helpers
import datetime


class Recordatorio:
    def __init__(self):
        self.conn = db.get_db()

    def create_recordatorio(self, usuario_id, asunto, fecha):
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO recordatorio(usuario_id, asunto, fecha, status, created_at) VALUES (?,?,?,'on', datetime('now'));"
            cursor.execute(
                query,
                (
                    usuario_id,
                    asunto,
                    fecha,
                ),
            )
            self.conn.commit()
            cursor.close()
            self.conn.close()
            return "Recordatorio creado exitosamente"
        except Exception as e:
            msg = "Hubo un problema para crear el recordatorio, inténtelo más tarde"
            helpers.log_to_file("create_recordatorio", e, "ERROR")
            return msg

    def get_recordatorios(self, usuario_id):
        try:
            cursor = self.conn.cursor()
            query = "SELECT id, asunto, fecha, status, created_at, usuario_id FROM recordatorio WHERE usuario_id = ? ORDER BY created_at DESC;"
            cursor.execute(query, (usuario_id,))
            res = cursor.fetchall()
            # print(res)
            msg = "Historial de recordatorios\n"
            for row in res:
                _fecha = row[2]
                _fecha_fixed = f"{_fecha.day}-{_fecha.month}-{_fecha.year} {_fecha.hour}:{_fecha.minute}"
                _created_at = row[4]
                _created_at_fixed = f"{_created_at.day}-{_created_at.month}-{_created_at.year} {_created_at.hour}:{_created_at.minute}"

                msg += f"Asunto: {row[1]}\n Fecha recordatorio: {_fecha_fixed}\n Fecha creación: {_created_at_fixed}\n Estado: {row[3]}\n"
                msg += "\n"
                # print(msg)
            cursor.close()
            self.conn.close()
            return msg, res
        except Exception as e:
            return f"Hubo un problema ({e}) para mostrar tu historial de recordatorios, inténtelo más tarde"

    def execute_recordatorios(self):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        # print(now)

        try:
            cursor = self.conn.cursor()
            query = "SELECT usuario_id, asunto, fecha, created_at, status FROM recordatorio WHERE fecha = ?;"
            cursor.execute(query, (now,))
            res = cursor.fetchall()
            cursor.close()
            self.conn.close()  # Solo si no vas a seguir usando la conexión
            return res

        except Exception as e:
            msg = f"Error al consultar recordatorios: {e}"
            helpers.log_to_file("execute_recordatorio", e, "ERROR")
            return -1

    # return "Hubo un problema para ejecutar el recordatorio creado, inténtelo más tarde"

    def get_last_recordatorio(self, usuario_id):
        try:
            cursor = self.conn.cursor()
            query = "SELECT id, asunto, fecha, status, created_at FROM recordatorio WHERE usuario_id = ? ORDER BY created_at DESC LIMIT 1;"
            cursor.execute(query, (usuario_id,))
            last_recordatorio = cursor.fetchone()
            cursor.close()
            return last_recordatorio
        except Exception as e:
            msg = f"Hubo un problema ({e}) para obtener el último recordatorio"
            helpers.log_to_file("get_last_recordatorio", e, "ERROR")
            return msg

    def stop_recordatorio(self, usuario_id):
        last_recordatorio = self.get_last_recordatorio(usuario_id)
        if last_recordatorio:
            last_id = last_recordatorio[0]
            try:
                cursor = self.conn.cursor()
                query = "UPDATE recordatorio SET status='off' WHERE id = ?;"
                cursor.execute(query, (last_id,))
                self.conn.commit()
                cursor.close()
                self.conn.close()
                return "El recordatorio ha sido apagado :)"
            except Exception as e:
                helpers.log_to_file("stop_recordatorio", e, "ERROR")
                msg = f"Hubo un error ({e}) al apagar el recordatorio"
                return msg
        else:
            return "No hay recordatorios"
