import datetime


class PersonData:

    def __init__(self, data, date_time):
        self.index = len(data) - 1
        self.data = data
        self.date_time = date_time
        self.unknown = {"color": "secondary", "info": "Нет данных"}

    def check_date(self, date):

        while self.index >= 0 and date < self.data[self.index].pub_date:
            self.index -= 1

        if self.index < 0:
            return [self.unknown]

        return [{"color": self.data[self.index].user_location.table_class, "info": f"{self.data[self.index].user_location}\n{self.data[self.index].description}"}]

    def get_calendar(self):
        data_status = []

        for date in self.date_time:

            data_status.extend(self.check_date(date=date))

        return data_status
