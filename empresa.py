from datetime import datetime, timedelta

class Empresa:
    def __init__(self, funcionario_file="funcionario.txt", calendario_file="calendario.txt"):
        self.funcionario_file = funcionario_file
        self.calendario_file = calendario_file
        self.semanas_do_ano = self.gerar_semanas_do_ano()
        self.funcionarios = self.load_funcionarios() if self.file_exists(funcionario_file) else []
        self.calendario = self.load_calendario() if self.file_exists(calendario_file) else [None] * len(self.semanas_do_ano)

    def file_exists(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8'):
                return True
        except FileNotFoundError:
            return False

    def ordenarFuncionarios(self):
        self.funcionarios = sorted(self.funcionarios)
        self.save_funcionarios()

    def gerar_semanas_do_ano(self):
        semanas = []
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

            semanas.append(week_str)
            start_date = week_end + timedelta(days=1)

        return semanas

    def preencherCalendario(self):
        if not self.funcionarios:
            return "Erro: Nenhum funcionário disponível para preencher o calendário."

        self.ordenarFuncionarios()
        
        for i in range(len(self.semanas_do_ano)):
            employee = self.funcionarios[i % len(self.funcionarios)]
            self.calendario[i] = f"{self.semanas_do_ano[i]}: {employee}"
        
        self.save_calendario()
        return None

    def adicionarFuncionario(self, nomeFunc: str):
        if nomeFunc not in self.funcionarios:
            self.funcionarios.append(nomeFunc)
            self.save_funcionarios()
            self.preencherCalendario()
            return None
        else:
            return "Erro: Funcionário já está incluído."

    def retirarFuncionario(self, nomeFunc: str):
        if nomeFunc in self.funcionarios:
            self.funcionarios.remove(nomeFunc)
            self.save_funcionarios()
            self.preencherCalendario()
            return None
        else:
            return "Erro: Funcionário não encontrado."

    def save_calendario(self):
        with open(self.calendario_file, 'w', encoding='utf-8') as file:
            for item in self.calendario:
                if item:  # Avoid writing None values
                    file.write(f"{item}\n")

    def load_calendario(self):
        if not self.file_exists(self.calendario_file):
            return [None] * len(self.semanas_do_ano)  # Return empty calendar if file does not exist

        with open(self.calendario_file, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]

    def save_funcionarios(self):
        with open(self.funcionario_file, 'w', encoding='utf-8') as file:
            for funcionario in self.funcionarios:
                file.write(f"{funcionario}\n")

    def load_funcionarios(self):
        if not self.file_exists(self.funcionario_file):
            return []  # Return empty list if file does not exist

        with open(self.funcionario_file, 'r', encoding='utf-8') as file:
            return [line.strip() for line in file.readlines()]

