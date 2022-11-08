from ..tickets.models import Ticket
from django.db import connection


class TicketReport:
    def __init__(self):
        self.pending_per_date = []
        self.on_course_per_date = []
        self.done_per_date = []
        self.rejected_per_date = []
        self.dates = []
        self.total_per_date = []
        self.total_pending = 0
        self.total_on_course = 0
        self.total_done = 0
        self.total_rejected = 0
        self.total_tickets = 0
        self.has_content = False

    @staticmethod
    def format_dates(date):
        """ Simplemente formate las fechas al format dd-mm-YYYY """
        if date is not None:
            date = date[-2:] + "-" + date[5:-3] + "-" + date[0:4]
            return date

    def report_by_dates(self, start_date, end_date):
        """ Obtiene todos los tickets en las fechas pasadas como parametro """

        dates_between_query = """
            SELECT COUNT(CASE WHEN t.status = 1 THEN true END) as pending,
                COUNT(CASE WHEN t.status = 2 THEN true END) as on_course,
                COUNT(CASE WHEN t.status = 3 THEN true END) as done,
                COUNT(CASE WHEN t.status = 4 THEN true END) as rejected,
                t.created_at::DATE as fecha
            FROM tickets_ticket t
            WHERE t.created_at BETWEEN %s AND %s
            GROUP BY fecha
            ORDER BY fecha;
        """

        try:
            with connection.cursor() as cursor:
                """ Se obtienen los datos del query """
                cursor.execute(dates_between_query, [start_date, end_date])
                row = cursor.fetchall()

            # se itera por fechas
            for day in row:
                pending = day[0]
                on_course = day[1]
                done = day[2]
                rejected = day[3]
                date = str(day[4])
                date = self.format_dates(date)

                # Se obtiene el total por cada status
                self.total_pending += pending
                self.total_on_course += on_course
                self.total_done += done
                self.total_rejected += rejected

                # Se crean los arrays que guardan los datos por dia para luego iterar en el reporte
                self.pending_per_date.append(pending)
                self.on_course_per_date.append(on_course)
                self.done_per_date.append(done)
                self.rejected_per_date.append(rejected)
                self.dates.append(date)

                # Se guarda el total de los tickets por dia
                self.total_per_date.append(pending + on_course + done + rejected)

            # se setea a true para saber que existen datos y el reporte se renderice con datos
            self.has_content = True
            self.total_tickets = sum(self.total_per_date)
        except Exception as e:
            raise Exception(e)


