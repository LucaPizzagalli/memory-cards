import tkinter as tk
import subprocess, os, sys
from datetime import datetime
import numpy as np

class WindowPerformTest:

    def __init__(self, db, programs, root, main_wind, topics_disponibili):
        self.db = db
        self.programs = programs
        self.main_wind = main_wind
        self.frame1 = tk.Frame(root)
        self.frame1.pack(fill=tk.BOTH, expand=1)
        self.outcome_button = list()
        self.esito_label = None
        self.answer_button = None
        self.none_button = None
        self.root = root
        root.geometry('500x250+350+250')
        root.title("Perform Test")

        if topics_disponibili:
            self.performed_concept = self.predict_difficult_test(topics_disponibili)
            query = self.db.execute("SELECT qs_path, ans_path, ans2_path, qs_params, ans_params, ans2_params FROM concepts_table WHERE ID = " + str(self.performed_concept))
            temp = query.fetchone()
            print("query")
            print(temp)
            parameters = []
            for i in range(3):
                parameters.append(temp[i])
            for i in [3, 4, 5]:
                if temp[i]:
                    parameters.append(temp[i].split(',*,'))
                else:
                    parameters.append([])

            # query = self.db.execute("SELECT end_page, checked_pages FROM meta_concepts_table WHERE ID = " + str(self.performed_concept))
            # meta = query.fetchone()
            # print(meta)
            # if meta:
            #     self.nuber_pages_label = tk.Label(self.frame1, text='Pages in file:')
            #     self.nuber_pages_label.grid(row=1, column=0)
            #     self.nuber_pages_entry = tk.Entry(self.frame1)
            #     self.nuber_pages_entry.grid(row=1, column=1)
            try:
                self.call_file(parameters[0], parameters[3])
                if not parameters[1] and not parameters[2]:
                    self.create_outcome_frame()
                else:
                    self.create_answer_frame(parameters)
            except OSError as errore:
                error_string = 'ERROR\n' + str(errore.strerror) + '\n' + str(errore.filename)
                error_label = tk.Label(self.frame1, text=error_string)
                error_label.pack()
        else:
            self.no_test_label = tk.Label(self.frame1, text='No test avaible')
            self.no_test_label.pack()
            none_button = tk.Button(self.frame1, text='Back', command=self.test_none)
            none_button.pack()

    def create_outcome_frame(self):
        for i in range(2):
            tk.Grid.rowconfigure(self.frame1, i, weight=1)
        for i in range(5):
            tk.Grid.columnconfigure(self.frame1, i, weight=1)
        self.esito_label = tk.Label(self.frame1, text='Outcome')
        self.esito_label.grid(row=0, column=0, columnspan=5, sticky=tk.N+tk.S+tk.E+tk.W)
        for i, label in enumerate(['Bad', 'Poor', 'Good', 'Excellent', 'None']):
            self.outcome_button.append(tk.Button(self.frame1, text=label, command=lambda copy=i: self.end_test(copy)))
            self.outcome_button[i].grid(row=1, column=i, sticky=tk.N+tk.S+tk.E+tk.W)

    def create_answer_frame(self, parameters):
        print('PREtemp:')
        print(parameters)
        tk.Grid.columnconfigure(self.frame1, 0, weight=1)
        tk.Grid.rowconfigure(self.frame1, 0, weight=3)
        tk.Grid.rowconfigure(self.frame1, 0, weight=1)
        self.answer_button = tk.Button(self.frame1, text='See answer', command=lambda: self.show_answer(parameters))
        self.answer_button.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.none_button = tk.Button(self.frame1, text='None', command=lambda: self.end_test(4))
        self.none_button.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

    def show_answer(self, parameters):
        print('temp:')
        print(parameters)
        if self.answer_button:
            self.answer_button.destroy()
        self.answer_button = None
        if self.none_button:
            self.none_button.destroy()
        self.none_button = None
        try:
            if parameters[1]:
                self.call_file(parameters[1], parameters[4])
            if parameters[2]:
                self.call_file(parameters[2], parameters[5])
            self.create_outcome_frame()
        except OSError as errore:
            error_string = 'ERROR\n' + str(errore.strerror) + '\n' + str(errore.filename)
            error_label = tk.Label(self.frame1, text=error_string)
            error_label.pack()
        
    def call_file(self, file_path, parameters):
        extension = '.' + file_path.split('.')[-1]
        current_program = None
        for prog in self.programs:
            if prog.get_extn() == extension:
                current_program = prog
                break
        if current_program:
            request = [current_program.get_path()]
            request.extend(current_program.get_strings())
            index = 0
            print(request)
            print('parameters:')
            print(parameters)
            for i, parte in enumerate(request):
                if request[i] == '<File Path>':
                    request[i] = file_path
                # if request[i] == '<Page>' and parameters[index] == 'rand':
                #     print('uuuuuuuuuu')
                #     request[i] = '77000'
                #     index += 1
                elif parte[0] == '<' and parte[-1] == '>':
                    request[i] = parameters[index]
                    index += 1
                else:
                    request[i] = parte.replace(' ', '|||')
            print(''.join(request).split('|||'))
            subprocess.Popen(''.join(request).split('|||'), stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        else:
            if sys.platform.startswith('darwin'):
                subprocess.Popen(('open', file_path))
            elif os.name == 'posix':
                subprocess.Popen(('xdg-open', file_path))
            elif os.name == 'nt':
                os.startfile(file_path)
    def test_none(self):
        self.frame1.destroy()
        if self.main_wind:
            self.main_wind.update()
        else:
            self.root.quit()

    def end_test(self, outcome):
        if outcome < 4:
            self.db.execute("INSERT INTO tests_table (concept_ID, date, outcome) VALUES (" + str(self.performed_concept) + ", '" + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "', " + str(outcome) + " )")
            self.db.commit()
        self.frame1.destroy()
        if self.main_wind:
            self.main_wind.update()
        else:
            self.root.quit()

    def predict_difficult_test(self, topics_disponibili):
        stringa = "('" + "', '".join(topics_disponibili) + "')"
        query = self.db.execute("SELECT ID FROM concepts_table WHERE topic IN " + stringa)
        prob = []
        for row in query:
            nquery = self.db.execute("SELECT outcome, date FROM tests_table WHERE concept_ID = " + str(row[0]))
            coeff = 0
            for caso in nquery:
                x = -(datetime.now() - datetime.strptime(caso[1], '%Y-%m-%d %H:%M:%S')).total_seconds()/10000
                ncoeff = (caso[0] - 1.5) * np.exp(x)
                if ncoeff < 0 and x < 3.6:
                    ncoeff *= -0.4 * (x-3.6) * (x-3.6)
                coeff += ncoeff
            prob.append((coeff, row[0]))
        return min(prob)[1]
