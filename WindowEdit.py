import tkinter as tk
import sys, os

class AutoScrollbar(tk.Scrollbar):

    def set(self, low, high):
        if float(low) <= 0.0 and float(high) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        tk.Scrollbar.set(self, low, high)

class WindowEdit:

    def __init__(self, db, root, main_wind, topics_disponibili):
        root.geometry('1300x600+60+60')
        root.title("Edit Tests")
        self.db = db
        self.main_wind = main_wind
        self.frame1 = tk.Frame(root)
        self.frame1.pack(fill=tk.BOTH, expand=1)
        tk.Grid.columnconfigure(self.frame1, 0, weight=0)
        tk.Grid.columnconfigure(self.frame1, 1, weight=0)
        tk.Grid.columnconfigure(self.frame1, 2, weight=0)
        tk.Grid.columnconfigure(self.frame1, 3, weight=3)
        tk.Grid.rowconfigure(self.frame1, 0, weight=1)
        tk.Grid.rowconfigure(self.frame1, 1, weight=1)

        self.top_label = tk.LabelFrame(self.frame1, text='Topics')
        self.top_label.grid(row=0, column=0)
        if topics_disponibili:
            self.top_listbox = tk.Listbox(self.top_label, exportselection=False, selectmode=tk.MULTIPLE, height=30, width=20)
            for topic in topics_disponibili:
                self.top_listbox.insert(0, topic)
            self.top_listbox.bind('<<ListboxSelect>>', self.select_topics)
            self.top_listbox.select_set(0, len(topics_disponibili))
            self.top_listbox.grid(row=0, column=0, columnspan=2)
        self.edit_top_name_entry = None
        self.edit_top_name_button = None
        self.subtop_label = None
        self.subtop_listbox = None
        self.edit_subtop_name_entry = None
        self.edit_subtop_name_button = None

        self.vscrollbar = AutoScrollbar(self.frame1)
        self.vscrollbar.grid(row=0, column=2, rowspan=2, sticky=tk.N+tk.S)
        self.canvas = tk.Canvas(self.frame1, yscrollcommand=self.vscrollbar.set)
        self.canvas.grid(row=0, column=3, rowspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.vscrollbar.config(command=self.canvas.yview)
        self.frame2 = tk.Frame(self.canvas)
        self.canvas_frame = self.canvas.create_window(0, 0, anchor=tk.NW, window=self.frame2)
        self.topic_list = []
        self.subtopic_list = []
        self.file_list = [[], [], []]
        self.edit_list = []
        self.remove_list = []
        self.param_list = [[], [], []]
        self.e_topic_list = []
        self.e_subtopic_list = []
        self.e_file_list = [[], [], []]
        self.e_param_list = [[], [], []]
        self.e_topic_list_var = None
        self.e_subtopic_list_var = None
        self.undo_edit_button = tk.Button(self.frame1, text='Back', command=self.undo_edit)
        self.undo_edit_button.grid(row=1, column=0, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.selected_tops = []
        self.selected_subtops = []
        self.id_list = []
        self.select_topics()

    def select_topics(self, _=None):
        self.selected_tops = []
        self.selected_subtops = []
        index_tupla = self.top_listbox.curselection()
        for index in index_tupla:
            self.selected_tops.append(self.top_listbox.get(index))
        if len(self.selected_tops) == 1:
            self.edit_top_name_entry = tk.Entry(self.top_label, width=10)
            self.edit_top_name_entry.insert(0, self.selected_tops[0])
            self.edit_top_name_entry.grid(row=1, column=0)
            self.edit_top_name_button = tk.Button(self.top_label, command=self.edit_topic_name, text='Edit name')
            self.edit_top_name_button.grid(row=1, column=1)

            self.subtop_label = tk.LabelFrame(self.frame1, text='SubTopics')
            self.subtop_label.grid(row=0, column=1)
            self.subtop_listbox = tk.Listbox(self.subtop_label, exportselection=False, selectmode=tk.MULTIPLE, height=30, width=20)
            self.subtop_listbox.bind('<<ListboxSelect>>', self.select_sub_topics)
            self.subtop_listbox.grid(row=0, column=0, columnspan=2)

            #self.subtop_listbox.delete(0, self.subtop_listbox.size())
            query = self.db.execute("SELECT DISTINCT subtopic FROM concepts_table WHERE topic = '" + self.selected_tops[0] + "' ORDER BY ID DESC")
            subtopics_disponibili = [row[0] for row in query]
            subtopics_disponibili.reverse()
            for subtopic in subtopics_disponibili:
                self.subtop_listbox.insert(0, subtopic)
            self.subtop_listbox.select_set(0, len(subtopics_disponibili))
            self.select_sub_topics()
        else:
            if self.edit_top_name_entry:
                self.edit_top_name_entry.destroy()
            self.edit_top_name_entry = None
            if self.edit_top_name_button:
                self.edit_top_name_button.destroy()
            self.edit_top_name_button = None
            if self.subtop_label:
                self.subtop_label.destroy()
            self.subtop_label = None
            if self.subtop_listbox:
                self.subtop_listbox.destroy()
            self.subtop_listbox = None
            if self.edit_subtop_name_entry:
                self.edit_subtop_name_entry.destroy()
            self.edit_subtop_name_entry = None
            if self.edit_subtop_name_button:
                self.edit_subtop_name_button.destroy()
            self.edit_subtop_name_button = None
            self.update_list()

    def select_sub_topics(self, _=None):
        self.selected_subtops = []
        index_tupla = self.subtop_listbox.curselection()
        for index in index_tupla:
            self.selected_subtops.append(self.subtop_listbox.get(index))
        if len(self.selected_subtops) == 1:
            self.edit_subtop_name_entry = tk.Entry(self.subtop_label, width=10)
            self.edit_subtop_name_entry.grid(row=1, column=0)
            self.edit_subtop_name_entry.insert(0, self.selected_subtops[0])
            self.edit_subtop_name_button = tk.Button(self.subtop_label, command=self.edit_subtopic_name, text='Edit name')
            self.edit_subtop_name_button.grid(row=1, column=1)
        else:
            if self.edit_subtop_name_entry:
                self.edit_subtop_name_entry.destroy()
            self.edit_subtop_name_entry = None
            if self.edit_subtop_name_button:
                self.edit_subtop_name_button.destroy()
            self.edit_subtop_name_button = None
        self.update_list()

    def update_list(self):
        for widget in self.topic_list + self.subtopic_list + self.edit_list + self.remove_list + self.e_topic_list + self.e_subtopic_list + [itm for sub in (self.file_list + self.param_list + self.e_file_list + self.e_param_list) for itm in sub]:
            if widget:
                widget.destroy()
        self.topic_list = []
        self.subtopic_list = []
        self.file_list = [[], [], []]
        self.param_list = [[], [], []]
        self.id_list = []
        self.edit_list = []
        self.remove_list = []
        self.e_topic_list = []
        self.e_subtopic_list = []
        self.e_file_list = [[], [], []]
        self.e_param_list = [[], [], []]

        stringa = "topic IN ('" + "', '".join(self.selected_tops) + "')"
        if len(self.selected_tops) == 1:
            stringa2 = "AND subtopic IN ('" + "', '".join(self.selected_subtops) + "')"
        else:
            stringa2 = ""
        query = self.db.execute("SELECT ID, topic, subtopic, qs_path, qs_params, ans_path, ans_params, ans2_path, ans2_params FROM concepts_table WHERE " + stringa + stringa2 + " ORDER BY ID DESC")
        concepts_list = [row for row in query]
        tk.Grid.columnconfigure(self.frame2, 0, weight=0)
        tk.Grid.columnconfigure(self.frame2, 1, weight=0)
        tk.Grid.columnconfigure(self.frame2, 2, weight=2)
        tk.Grid.columnconfigure(self.frame2, 3, weight=2)
        tk.Grid.columnconfigure(self.frame2, 4, weight=3)
        tk.Grid.columnconfigure(self.frame2, 5, weight=1)
        tk.Grid.columnconfigure(self.frame2, 6, weight=3)
        tk.Grid.columnconfigure(self.frame2, 7, weight=1)
        tk.Grid.columnconfigure(self.frame2, 8, weight=3)
        tk.Grid.columnconfigure(self.frame2, 9, weight=1)
        N = len(concepts_list)
        for i in range(N):
            self.remove_list.append(tk.Button(self.frame2, command=lambda k=i: self.remove_concept(k), text='Rmv', padx=2))
            self.remove_list[i].grid(row=i, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
            self.edit_list.append(tk.Button(self.frame2, command=lambda j=i: self.edit_concept(j), text='Edit', padx=4))
            self.edit_list[i].grid(row=i, column=1, sticky=tk.N+tk.S+tk.E+tk.W)
            self.id_list.append(concepts_list[i][0])
            self.topic_list.append(tk.Label(self.frame2, text=concepts_list[i][1]))
            self.topic_list[i].grid(row=i, column=2)
            self.subtopic_list.append(tk.Label(self.frame2, text=concepts_list[i][2], bg='#cccccc', pady=6))
            self.subtopic_list[i].grid(row=i, column=3, sticky=tk.N+tk.S+tk.E+tk.W)
            for j in range(3):
                self.file_list[j].append(tk.Label(self.frame2, text=concepts_list[i][3+2*j][-25:]))
                self.file_list[j][i].grid(row=i, column=4+j*2)
                self.param_list[j].append(tk.Label(self.frame2, text=concepts_list[i][4+2*j], bg='#cccccc', pady=6))
                self.param_list[j][i].grid(row=i, column=5+j*2, sticky=tk.N+tk.S+tk.E+tk.W)
        self.e_topic_list = [None]*N
        self.e_subtopic_list = [None]*N
        self.e_file_list = [[None]*N, [None]*N, [None]*N]
        self.e_param_list = [[None]*N, [None]*N, [None]*N]
        self.e_topic_list_var = [None]*N
        self.e_subtopic_list_var = [None]*N

        self.frame2.update_idletasks()######sfarfallio
        self.canvas.config(scrollregion=self.canvas.bbox('all'))
        if sys.platform.startswith('darwin'):
            self.canvas.bind_all('<MouseWheel>', self._on_mousewheel_osx)
        elif os.name == 'posix':
            self.canvas.bind_all('<Button-4>', self._on_mousewheel_unix_up)
            self.canvas.bind_all('<Button-5>', self._on_mousewheel_unix_down)
        elif os.name == 'nt':
            self.canvas.bind_all('<MouseWheel>', self._on_mousewheel_wd)
        self.canvas.bind('<Configure>', self.resize_canvas)

    def resize_canvas(self, event):
        self.canvas.itemconfig(self.canvas_frame, width=event.width)

    def _on_mousewheel_wd(self, event):
        self.canvas.yview_scroll(-1*(event.delta/120), 'units')

    def _on_mousewheel_osx(self, event):
        self.canvas.yview_scroll(-1*(event.delta), 'units')

    def _on_mousewheel_unix_up(self, _):
        if self.canvas:
            self.canvas.yview_scroll(-1, 'units')
    def _on_mousewheel_unix_down(self, _):
        if self.canvas:
            self.canvas.yview_scroll(1, 'units')

    def edit_topic_name(self):
        newname = self.edit_top_name_entry.get().strip()
        self.db.execute("UPDATE concepts_table SET topic = '" + newname + "' WHERE topic = '" + self.selected_tops[0] + "'")
        self.db.commit()
        self.selected_tops[0] = newname
        oldindex = self.top_listbox.curselection()[0]
        self.top_listbox.delete(oldindex, oldindex)
        self.top_listbox.insert(oldindex, newname)
        self.top_listbox.select_set(oldindex)
        self.update_list()

    def edit_subtopic_name(self):
        newname = self.edit_subtop_name_entry.get().strip()
        self.db.execute("UPDATE concepts_table SET subtopic = '" + newname + "' WHERE subtopic = '" + self.selected_subtops[0] + "'")
        self.db.commit()
        self.selected_subtops[0] = newname
        oldindex = self.subtop_listbox.curselection()[0]
        self.subtop_listbox.delete(oldindex, oldindex)
        self.subtop_listbox.insert(oldindex, newname)
        self.subtop_listbox.select_set(oldindex)
        self.update_list()

    def update_edit_subtopic(self, i):
        if self.e_subtopic_list[i]:
            self.e_subtopic_list[i].destroy()
        self.e_subtopic_list[i] = None
        query = self.db.execute("SELECT DISTINCT subtopic FROM concepts_table WHERE topic = '" + self.e_topic_list_var[i].get() + "' ORDER BY ID DESC")
        subtopics_disponibili = [row[0] for row in query]
        self.e_subtopic_list_var[i] = tk.StringVar()
        self.e_subtopic_list_var[i].set(subtopics_disponibili[0])
        self.e_subtopic_list[i] = tk.OptionMenu(self.frame2, self.e_subtopic_list_var[i], *subtopics_disponibili)
        self.e_subtopic_list[i].grid(row=i, column=3)

    def edit_concept(self, i):
        if self.edit_list[i].cget('text') == 'Edit':
            query = self.db.execute("SELECT DISTINCT topic FROM concepts_table ORDER BY ID DESC")
            topics_disponibili = [row[0] for row in query]
            query = self.db.execute("SELECT qs_path,ans_path,ans2_path FROM concepts_table WHERE ID = " + str(self.id_list[i]))
            file_path = query.fetchone()

            self.edit_list[i].config(text='Conf')
            self.remove_list[i].config(text='Undo')
            self.topic_list[i].grid_remove()
            self.subtopic_list[i].grid_remove()
            for j in range(3):
                self.file_list[j][i].grid_remove()
                self.param_list[j][i].grid_remove()
            self.e_topic_list_var[i] = tk.StringVar()
            self.e_topic_list_var[i].set(self.topic_list[i].cget('text'))
            self.e_topic_list[i] = tk.OptionMenu(self.frame2, self.e_topic_list_var[i], *topics_disponibili,
                command=lambda j=i: self.update_edit_subtopic(i))
            self.e_topic_list[i].grid(row=i, column=2)
            self.update_edit_subtopic(i)
            for j in range(3):
                self.e_file_list[j][i] = tk.Text(self.frame2, height=2, width=24)
                self.e_file_list[j][i].insert(tk.END, file_path[j])
                self.e_file_list[j][i].grid(row=i, column=4+2*j)
                self.e_param_list[j][i] = tk.Entry(self.frame2, width=3)
                self.e_param_list[j][i].insert(0, self.param_list[j][i].cget('text'))
                self.e_param_list[j][i].grid(row=i, column=5+2*j)
        else:
            topic = self.e_topic_list_var[i].get()
            subtopic = self.e_subtopic_list_var[i].get()
            file_path = [self.e_file_list[j][i].get(1.0, tk.END).strip() for j in range(3)]
            param = [self.e_param_list[j][i].get().strip() for j in range(3)]
            self.db.execute("UPDATE concepts_table SET topic = '" + topic + "', subtopic = '" + subtopic + "', qs_path = '" + file_path[0] + "', ans_path = '" + file_path[1] + "', ans2_path = '" + file_path[2] + "', qs_params = '" + param[0] + "', ans_params = '" + param[1] + "', ans2_params = '" + param[2] + "' WHERE ID = " + str(self.id_list[i]))
            self.db.commit()
            self.topic_list[i].config(text=topic)
            self.subtopic_list[i].config(text=subtopic)

            self.edit_list[i].config(text='Edit')
            self.remove_list[i].config(text='Rmv')
            self.e_topic_list[i].destroy()
            self.e_subtopic_list[i].destroy()
            self.e_topic_list_var[i] = None
            self.e_topic_list[i] = None
            self.e_subtopic_list_var[i] = None
            self.e_subtopic_list[i] = None
            self.topic_list[i].grid(row=i, column=2)
            self.subtopic_list[i].grid(row=i, column=3)
            for j in range(3):
                self.file_list[j][i].config(text=file_path[j][-25:])
                self.param_list[j][i].config(text=param[j])
                self.e_file_list[j][i].destroy()
                self.e_param_list[j][i].destroy()
                self.e_file_list[j][i] = None
                self.e_param_list[j][i] = None
                self.file_list[j][i].grid(row=i, column=4+j*2)
                self.param_list[j][i].grid(row=i, column=5+j*2)

        self.frame2.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

    def remove_concept(self, i):
        request = self.remove_list[i].cget('text')
        if request == 'Rmv':
            self.remove_list[i].config(text='Sure?')
        elif request == 'Sure?':
            self.db.execute("DELETE FROM concepts_table WHERE ID = " + str(self.id_list[i]))
            self.db.commit()

            for widget in [self.remove_list[i]] + [self.edit_list[i]] + [self.topic_list[i]] + [self.subtopic_list[i]] + [el[i] for el in self.file_list] + [el[i] for el in self.param_list] + [self.e_topic_list[i]] + [self.e_subtopic_list[i]] + [el[i] for el in self.e_file_list] + [el[i] for el in self.e_param_list]:
                if widget:
                    widget.destroy()
            self.remove_list[i] = None
            self.edit_list[i] = None
            self.topic_list[i] = None
            self.subtopic_list[i] = None
            self.e_topic_list_var[i] = None
            self.e_topic_list[i] = None
            self.e_subtopic_list_var[i] = None
            self.e_subtopic_list[i] = None
            for j in range(3):
                self.file_list[j][i] = None
                self.param_list[j][i] = None
                self.e_file_list[j][i] = None
                self.e_param_list[j][i] = None
        else:
            self.remove_list[i].config(text='Rmv')
            self.edit_list[i].config(text='Edit')
            self.e_topic_list[i].destroy()
            self.e_subtopic_list[i].destroy()
            self.e_topic_list_var[i] = None
            self.e_topic_list[i] = None
            self.e_subtopic_list_var[i] = None
            self.e_subtopic_list[i] = None
            self.topic_list[i].grid(row=i, column=2)
            self.subtopic_list[i].grid(row=i, column=3)
            for j in range(3):
                self.e_file_list[j][i].destroy()
                self.e_param_list[j][i].destroy()
                self.e_file_list[j][i] = None
                self.e_param_list[j][i] = None
                self.file_list[j][i].grid(row=i, column=4+j*2)
                self.param_list[j][i].grid(row=i, column=5+j*2)

    def undo_edit(self):
        self.canvas = None
        self.main_wind.update()
        self.main_wind.update_topics()
        self.frame1.destroy()