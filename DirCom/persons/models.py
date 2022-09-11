import copy

from django.db import models
from django.db import connection


class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    document_number = models.IntegerField()
    address = models.CharField(max_length=300)
    city = models.CharField(max_length=50)
    status = models.CharField(max_length=30)

    @staticmethod
    def list_persons(status_filter):
        list_query = " SELECT id, first_name, last_name, address, city, document_number, " \
                     "status FROM persons_person "
        order_by = " ORDER BY id desc "
        if status_filter is not None:
            filter_status = " WHERE status = %s "
            final_query = list_query + filter_status + order_by
            with connection.cursor(final_query, [status_filter]) as cursor:
                cursor.execute()
                rows = cursor.fetchall()
        else:
            final_query = list_query + order_by
            with connection.cursor() as cursor:
                cursor.execute(final_query, [])
                rows = cursor.fetchall()

        person = {}
        person_list = []

        for row in rows:
            person['id'] = row[0]
            person['first_name'] = row[1]
            person['last_name'] = row[2]
            person['address'] = row[3]
            person['city'] = row[4]
            person['document_number'] = row[5]
            person['status'] = row[6]

            person_list.append(copy.deepcopy(person))

        return person_list

    @staticmethod
    def get_person(pk):
        get_query = " SELECT id, first_name, last_name, address, city, document_number, status " \
                    " FROM persons_person WHERE id = %s;"

        with connection.cursor(get_query, [pk]) as cursor:
            cursor.execute()
            row = cursor.fetchone()

        person = PersonClass(row[0], row[2], row[3], row[4], row[5], row[6])
        return person

    def __str__(self):
        self.first_name + self.last_name + str(self.document_number)


class PersonClass:
    def __init(self, person_id, first_name, last_name, address, city, document_number):
        self.persons = person_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.city = city
        self.document_number = document_number

    def validate_document_number(self):
        try:
            int(self.document_number)
            return True
        except Exception as e:
            print('Invalid Document', e)
            return False




