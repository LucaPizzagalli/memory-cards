'''
Classe che genera la finestra con il menu' principale di Memory
'''
import tkinter as tk
import os
from WindowEdit import WindowEdit
from WindowAddConcept import WindowAddConcept
from WindowPerformTest import WindowPerformTest
from WindowStats import WindowStats

class WindowMain:

    def __init__(self, db, programs, root):
        self.db = db
        self.programs = programs
        self.root = root
        self._topics_disponibili = []
        self._selected_topics = []

        self.frame1 = tk.Frame(self.root)
        self.frame1.pack(fill=tk.BOTH, expand=1)
        for i in range(3):
            tk.Grid.columnconfigure(self.frame1, i, weight=1)
        for i in range(3):
            tk.Grid.rowconfigure(self.frame1, i, weight=1)

        self.top_label = tk.Label(self.frame1, text='Topic')
        self.top_label.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
        self.top_listbox = tk.Listbox(self.frame1, selectmode=tk.MULTIPLE, width=15)
        self.top_listbox.grid(row=1, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        self.subtop_label = tk.Label(self.frame1, text='SubTopic')
        self.subtop_label.grid(row=0, column=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.subtop_listbox = tk.Listbox(self.frame1, selectmode=tk.MULTIPLE, width=15)
        self.subtop_listbox.grid(row=1, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

        self.test_button = tk.Button(self.frame1, text='Test', command=self.init_perform_test_wind)
        self.test_button.grid(row=0, column=0, rowspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        self.add_button = tk.Button(self.frame1, text='Add', command=self.init_add_concept_wind)
        self.add_button.grid(row=2, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.edit_button = tk.Button(self.frame1, text='Edit', command=self.init_edit_wind)
        self.edit_button.grid(row=2, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

        self.stats_button = tk.Button(self.frame1, text='Stats', command=self.init_stats_wind)
        self.stats_button.grid(row=2, column=2, sticky=tk.N+tk.S+tk.E+tk.W)

        self.update()
        self.update_topics()

    def update(self):
        self.root.geometry('500x250+350+250')
        self.root.title("Memory")
        self.frame1.pack(fill=tk.BOTH, expand=1)

    def init_add_concept_wind(self):
        '''sostituisce la main window con l'add_concept window'''
        self.frame1.pack_forget()
        WindowAddConcept(self.db, self.programs, self.root, self, self._topics_disponibili)

    def init_edit_wind(self):
        self.frame1.pack_forget()
        WindowEdit(self.db, self.root, self, self._topics_disponibili)

    def init_stats_wind(self):
        self.frame1.pack_forget()
        WindowStats(self.db, self.root, self)

    def init_perform_test_wind(self):
        self.update_topics_disponibili()
        self.frame1.pack_forget()
        WindowPerformTest(self.db, self.programs, self.root, self, self._topics_disponibili)

    def update_topics(self):
        self.top_listbox.delete(0, self.top_listbox.size())
        query = self.db.execute("SELECT DISTINCT topic FROM concepts_table ORDER BY ID DESC")
        self._topics_disponibili = [row[0] for row in query]
        self._topics_disponibili.reverse()
        for topic in self._topics_disponibili:
            self.top_listbox.insert(0, topic)
        self.top_listbox.select_set(0, len(self._topics_disponibili))

    def update_topics_disponibili(self):
        self._topics_disponibili = []
        index_tupla = self.top_listbox.curselection()
        for index in index_tupla:
            self._topics_disponibili.append(self.top_listbox.get(index))

    def __del__(self):
        self.db.close()
