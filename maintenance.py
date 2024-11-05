from datetime import datetime, timedelta
import json

def generate_weeks():
    weeks = []
    year = datetime.now().year
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)

    while start_date <= end_date:
        week_end = start_date + timedelta(days=6)
        if week_end > end_date:
            week_end = end_date
        
        if start_date.month == week_end.month:
            week_str = f"{start_date.strftime('%B')} {start_date.day} - {week_end.day}"
        else:
            week_str = f"{start_date.strftime('%B')} {start_date.day} - {week_end.strftime('%B')} {week_end.day}"

        weeks.append(week_str)
        start_date = week_end + timedelta(days=1)

    return weeks

class Maintenance:
    def __init__(self, info_file="info.txt", calendar_file="calendar.txt"):
        self.info_file = info_file
        self.calendar_file = calendar_file
        self.weeks_of_year = generate_weeks()
        self.info = self.get_info() if self.file_exists(self.info_file) else {}
        self.calendar = self.get_calendar() if self.file_exists(self.calendar_file) else [None] * len(self.weeks_of_year)

    def file_exists(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8'):
                return True
        except FileNotFoundError:
            return False
        
    def sort_info(self):
        self.info = dict(sorted(self.info.items()))
        self.save_info()

    def add_info(self, parameter, new_info):
        if parameter not in self.info:
            self.info[parameter] = new_info
            self.sort_info()
            self.update_calendar()
            return None
        else:
            return "Erro: Informação já incluída."
    
    def remove_info(self, parameter):
        if parameter in self.info:
            del self.info[parameter]
            self.sort_info()
            self.update_calendar()
            return None
        else:
            return "Erro: Informação não encontrada."

    def get_info(self):
        if not self.file_exists(self.info_file):
            return {}

        with open(self.info_file, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    def save_info(self):
        with open(self.info_file, 'w', encoding='utf-8') as file:
            json.dump(self.info, file, ensure_ascii=False, indent=4)
    
    def get_calendar(self):
        if not self.file_exists(self.calendar_file):
            return [None] * len(self.weeks_of_year)

        with open(self.calendar_file, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]
    
    def update_calendar(self):
        if not self.info:
            return "Erro: Nenhuma informação disponível para preencher o calendário"

        self.calendar = [None] * len(self.weeks_of_year)

        for i, week in enumerate(self.weeks_of_year):
            info_key = list(self.info.keys())[i % len(self.info)]
            self.calendar[i] = f"{week}: {info_key}"
        
        self.save_calendar()

    def save_calendar(self):
        with open(self.calendar_file, 'w', encoding='utf-8') as file:
            for entry in self.calendar:
                if entry:  # Avoid writing None values
                    file.write(f"{entry}\n")