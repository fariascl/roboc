import db


class Recordatorio:
    def __init__(self):
        self.conn = db.get_db()

    def create_recordatorio(self, usuario_id, asunto, fecha):
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO recordatorio(usuario_id, asunto, fecha, status, created_at) VALUES (%s,%s,%s,'on', NOW());"
            cursor.execute(query, (usuario_id, asunto, fecha,))
            self.conn.commit()
            cursor.close()
            self.conn.close()
            return "Recordatorio creado exitosamente"
        except:
            return "Hubo un problema para crear el recordatorio, inténtelo más tarde"

    def get_recordatorios(self, usuario_id):
        try:

            cursor = self.conn.cursor()
            query = "SELECT id, asunto, fecha, status, created_at, usuario_id FROM recordatorio WHERE usuario_id = %s ORDER BY created_at DESC;"
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
        import datetime
        _now = datetime.datetime.now()
        dia = _now.day
        mes = _now.month
        anio = _now.year
        hora = _now.hour
        minuto = _now.minute
        now = f"{anio}-{mes}-{dia} {hora}:{minuto}"
        print(now)
        try:
            cursor = self.conn.cursor()
            query = "SELECT usuario_id, asunto, fecha, created_at, status FROM recordatorio WHERE fecha = %s;"
            cursor.execute(query, (now,))
            res = cursor.fetchall()
            cursor.close()
            self.conn.close()
            return res
        except Exception as e:
            print(f"asdas: {e}")
            return -1
            # return "Hubo un problema para ejecutar el recordatorio creado, inténtelo más tarde"

    def get_last_recordatorio(self, usuario_id):
        try:
            cursor = self.conn.cursor()
            query = "SELECT id, asunto, fecha, status, created_at FROM recordatorio WHERE usuario_id = %s ORDER BY created_at DESC LIMIT 1;"
            cursor.execute(query, (usuario_id,))
            last_recordatorio = cursor.fetchone()
            cursor.close()
            return last_recordatorio
        except Exception as e:
            msg = f"Hubo un problema ({e}) para obtener el último recordatorio"
            return msg

    def stop_recordatorio(self, usuario_id):
        last_recordatorio = self.get_last_recordatorio(usuario_id)
        if last_recordatorio:
            last_id = last_recordatorio[0]
            try:
                cursor = self.conn.cursor()
                query = "UPDATE recordatorio SET status='off' WHERE id = %s;"
                cursor.execute(query, (last_id),)
                self.conn.commit()
                cursor.close()
                self.conn.close()
                return "El recordatorio ha sido apagado :)"
            except Exception as e:
                return f"Hubo un error ({e}) al apagar el recordatorio"
        else:
            return "No hay recordatorios"
