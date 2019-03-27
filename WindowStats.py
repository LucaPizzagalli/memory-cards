import tkinter as tk
import matplotlib
#matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.figure import Figure
from datetime import datetime
import numpy as np

class Slider(tk.Frame):
    def __init__(self, master, windo):
        tk.Frame.__init__(self, master)
        self.number = 1.0/60
        self.slide = tk.Scale(self, from_=-4, to=1, resolution=0.1, command=self.setValue, orient=tk.HORIZONTAL, showvalue=0)
        self.text = tk.Label(self)
        self.slide.pack(side=tk.RIGHT, expand=1, fill=tk.X)
        self.text.pack(side=tk.TOP, fill=tk.BOTH)
        self.windo = windo

    def setValue(self, val):
        self.number = np.power(10, float(val))
        self.text.configure(text="{:.4f}".format(self.number))
        self.windo.update_list()

    def get(self):
        return self.number

class WindowStats:

    def __init__(self, db, root, main_wind):
        self.db = db
        self.main_wind = main_wind
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=1)
        root.geometry('1200x600+60+60')
        root.title("Statistics")
        self.subtop_label = None
        self.subtop_listbox = None

        tk.Grid.columnconfigure(self.main_frame, 0, weight=0)
        tk.Grid.columnconfigure(self.main_frame, 1, weight=0)
        tk.Grid.columnconfigure(self.main_frame, 2, weight=1)
        tk.Grid.rowconfigure(self.main_frame, 0, weight=1)
        tk.Grid.rowconfigure(self.main_frame, 1, weight=1)

        query = self.db.execute("SELECT DISTINCT topic FROM concepts_table ORDER BY ID DESC")
        self.topics_list = [row[0] for row in query]
        self.topics_list.reverse()
        self.top_label = tk.LabelFrame(self.main_frame, text='Topics')
        self.top_label.grid(row=0, column=0)
        if self.topics_list:
            self.top_listbox = tk.Listbox(self.top_label, exportselection=False, selectmode=tk.MULTIPLE, height=30, width=15)
            for topic in self.topics_list:
                self.top_listbox.insert(0, topic)
            self.top_listbox.bind('<<ListboxSelect>>', self.select_topics)
            self.top_listbox.grid(row=0, column=0)

        self.graph_frame = tk.Frame(self.main_frame)
        self.graph_frame.grid(row=0, column=2, rowspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
        tk.Grid.columnconfigure(self.graph_frame, 0, weight=1)
        tk.Grid.rowconfigure(self.graph_frame, 0, weight=1)
        tk.Grid.rowconfigure(self.graph_frame, 1, weight=0)
        self.fig = Figure(figsize=(5, 5), dpi=100)
        self.subplt = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, self.graph_frame)
        self.canvas.get_tk_widget().grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.scale = Slider(self.graph_frame, self)
        self.scale.grid(row=1, column=0, sticky=tk.N+tk.S+tk.E+tk.W)

        self.select_topics()

        self.undo_edit_button = tk.Button(self.main_frame, text='Back', command=self.undo_edit)
        self.undo_edit_button.grid(row=1, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

    def select_topics(self, _=None):
        self.selected_tops = []
        self.selected_subtops = []
        for index in self.top_listbox.curselection():
            self.selected_tops.append(self.top_listbox.get(index))
        if len(self.selected_tops) == 1:
            self.subtop_label = tk.LabelFrame(self.main_frame, text='SubTopics')
            self.subtop_label.grid(row=0, column=1)
            self.subtop_listbox = tk.Listbox(self.subtop_label, exportselection=False, selectmode=tk.MULTIPLE, height=30, width=15)
            self.subtop_listbox.bind('<<ListboxSelect>>', self.select_sub_topics)
            self.subtop_listbox.grid(row=0, column=0)

            query = self.db.execute("SELECT DISTINCT subtopic FROM concepts_table WHERE topic = '" + self.selected_tops[0] + "' ORDER BY ID DESC")
            subtopics_disponibili = [row[0] for row in query]
            subtopics_disponibili.reverse()
            for subtopic in subtopics_disponibili:
                self.subtop_listbox.insert(0, subtopic)
            self.subtop_listbox.select_set(0, len(subtopics_disponibili))
            self.select_sub_topics()
        else:
            if self.subtop_label:
                self.subtop_label.destroy()
            self.subtop_label = None
            if self.subtop_listbox:
                self.subtop_listbox.destroy()
            self.subtop_listbox = None
            self.update_list()

    def select_sub_topics(self, _=None):
        self.selected_subtops = []
        index_tupla = self.subtop_listbox.curselection()
        for index in index_tupla:
            self.selected_subtops.append(self.subtop_listbox.get(index))
        self.update_list()

    def update_list(self, _=None):
        stringa = "topic IN ('" + "', '".join(self.selected_tops) + "')"
        stringa2 = ""
        if len(self.selected_tops) == 1:
            stringa2 = "AND subtopic IN ('" + "', '".join(self.selected_subtops) + "')"
        query = self.db.execute("SELECT ID, topic, subtopic, qs_path, qs_params, ans_path, ans_params, ans2_path, ans2_params FROM concepts_table WHERE " + stringa + stringa2)
        self.subplt.clear()
        delta = self.scale.get()
        for conc in query:
            query2 = self.db.execute("SELECT outcome, date FROM tests_table WHERE concept_ID = " + str(conc[0]) + " ORDER BY date DESC")
            esiti = []
            dates = []
            origin = datetime.now()
            tmp = query2.fetchone()
            if tmp:
                x = -(origin - datetime.strptime(tmp[1], '%Y-%m-%d %H:%M:%S')).total_seconds()/86400
                time = x + (-x % delta)
                slot_value = tmp[0] - 1.5
                slot_n = 1
                for caso in query2:
                    x = -(origin - datetime.strptime(caso[1], '%Y-%m-%d %H:%M:%S')).total_seconds()/86400
                    if x >= time - delta:
                        slot_value += caso[0] - 1.5
                        slot_n += 1
                    else:
                        esiti.append(slot_value / slot_n)
                        dates.append(time-delta/2)
                        time = x + (-x % delta)
                        slot_value = caso[0] - 1.5
                        slot_n = 1
                esiti.append(slot_value / slot_n)
                dates.append(time-delta/2)
                self.subplt.plot(dates, esiti)
        self.canvas.draw()

    def undo_edit(self):
        self.main_wind.update()
        self.main_wind.update_topics()
        self.main_frame.destroy()
