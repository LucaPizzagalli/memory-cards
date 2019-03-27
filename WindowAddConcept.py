import tkinter as tk
import tkinter.filedialog as dialog
import os

class WindowAddConcept:

    def __init__(self, db, programs, root, main_wind, topics_disponibili):
        root.geometry('800x550+250+90')
        root.title("Add test")
        self.db = db
        self.programs = programs
        self.main_wind = main_wind
        self.frame1 = tk.Frame(root)
        self.frame1.pack(fill=tk.BOTH, expand=1)
        tk.Grid.columnconfigure(self.frame1, 0, weight=1)
        tk.Grid.columnconfigure(self.frame1, 1, weight=1)
        tk.Grid.columnconfigure(self.frame1, 2, weight=1)
        tk.Grid.columnconfigure(self.frame1, 3, weight=1)
        tk.Grid.rowconfigure(self.frame1, 0, weight=1)
        tk.Grid.rowconfigure(self.frame1, 1, weight=3)
        tk.Grid.rowconfigure(self.frame1, 2, weight=1)

        self.top_label = tk.LabelFrame(self.frame1, text='Topic')
        self.top_label.grid(row=0, column=0, rowspan=2)
        self.selected_top = ''
        if topics_disponibili:
            self.top_listbox = tk.Listbox(self.top_label, exportselection=False, height=27, width=25)
            for topic in topics_disponibili:
                self.top_listbox.insert(0, topic)
            self.top_listbox.select_set(0)
            self.selected_top = self.top_listbox.get(0).strip()
            self.top_listbox.bind('<<ListboxSelect>>', self.select_topic)
            self.top_listbox.grid(row=0, column=0, columnspan=2)
        self.top_new_label = tk.Label(self.top_label, text='New:')
        self.top_new_label.grid(row=1, column=0)
        self.top_new_entry = tk.Entry(self.top_label)
        self.top_new_entry.grid(row=1, column=1)

        self.subtop_label = tk.LabelFrame(self.frame1, text='SubTopic')
        self.subtop_label.grid(row=0, column=1, rowspan=2)
        self.selected_subtop = ''
        if topics_disponibili:
            self.subtop_listbox = tk.Listbox(self.subtop_label, exportselection=False, height=27, width=25)
            self.update_subtopics()
            self.subtop_listbox.bind('<<ListboxSelect>>', self.select_sub_topic)
            self.subtop_listbox.grid(row=0, column=0, columnspan=2)
        self.subtop_new_label = tk.Label(self.subtop_label, text='New:')
        self.subtop_new_label.grid(row=1, column=0)
        self.subtop_new_entry = tk.Entry(self.subtop_label)
        self.subtop_new_entry.grid(row=1, column=1)

        self.add_type = tk.IntVar()
        self.sigle_file_radio = tk.Radiobutton(self.frame1, text='Add single file',
            variable=self.add_type, value=1, indicatoron=0, command=self.select_single_file, padx=5, pady=5)
        self.sigle_file_radio.grid(row=0, column=2)
        self.multi_file_radio = tk.Radiobutton(self.frame1, text='Add a lot of files',
            variable=self.add_type, value=2, indicatoron=0, command=self.select_multi_file, padx=5, pady=5)
        self.multi_file_radio.grid(row=0, column=3)

        self.frame3 = tk.LabelFrame(self.frame1, text='Single File')
        self.frame3.grid(row=1, column=2, columnspan=2)
        tk.Grid.columnconfigure(self.frame3, 0, weight=1)
        tk.Grid.rowconfigure(self.frame3, 0, weight=1)
        tk.Grid.rowconfigure(self.frame3, 1, weight=1)

        self.file_label = [None, None, None]
        self.frame_param = [None, None, None]
        self.file_button = [None, None, None]
        self.file_text = [None, None, None]
        self.new_file_text = [None, None, None]
        self.selected_file = ['', '', '']
        self.error_file_label = None
        self.error_extens_label = None
        self.swich_create = [None, None, None]
        self.create_file = [tk.IntVar(), tk.IntVar(), tk.IntVar()]
        self.file_label[0] = tk.LabelFrame(self.frame3, text='Question')
        self.file_label[0].grid(row=0, column=0)
        self.file_label[1] = tk.LabelFrame(self.frame3, text='Answer')
        self.file_label[1].grid(row=1, column=0)
        self.file_label[2] = tk.Frame(self.file_label[1])
        self.add_swich = tk.Checkbutton(self.file_label[1], text="+", command=self.add_another_ans, indicatoron=0, padx=5, pady=5)
        self.add_swich.grid(row=3, column=0, columnspan=2)
        for i in range(3):
            self.frame_param[i] = tk.Frame(self.file_label[i])
            self.frame_param[i].grid(row=0, column=2, rowspan=3, sticky=tk.N+tk.S+tk.E+tk.W)
            self.file_button[i] = tk.Button(self.file_label[i], command=lambda copy=i: self.browse_file(copy), text='Select file')
            self.file_button[i].grid(row=0, column=0)
            self.swich_create[i] = tk.Checkbutton(self.file_label[i], text='New', variable=self.create_file[i], command=lambda copy2=i: self.new_file(copy2), indicatoron=0, padx=5, pady=5)
            self.swich_create[i].grid(row=0, column=1)
            self.file_text[i] = tk.Text(self.file_label[i], height=7, width=34)
            self.file_text[i].grid(row=1, column=0, columnspan=2)
            self.new_file_text[i] = tk.Text(self.file_label[i], height=6, width=34)
            self._file_update_flag = True
            self.file_text[i].bind('<<Modified>>', self.update_file_parameters)
        self.selected_prog = [None, None, None]
        self.param_labels = [[], [], []]
        self.param_entrys = [[], [], []]
        self.random_check = None
        if topics_disponibili:
            self.update_file()

        self.frame4 = tk.LabelFrame(self.frame1, text='Multi File')
        tk.Grid.columnconfigure(self.frame4, 0, weight=1)
        tk.Grid.columnconfigure(self.frame4, 1, weight=1)
        tk.Grid.columnconfigure(self.frame4, 2, weight=1)
        tk.Grid.rowconfigure(self.frame4, 0, weight=1)
        tk.Grid.rowconfigure(self.frame4, 1, weight=1)
        tk.Grid.rowconfigure(self.frame4, 2, weight=1)
        self.folder_label = tk.LabelFrame(self.frame4, text='Folder Path')
        self.folder_label.grid(row=0, column=0, rowspan=3)
        self.folder_button = tk.Button(self.folder_label, command=self.browse_folder, text='Select folder')
        self.folder_button.grid(row=0, column=0)
        self.folder_text = tk.Text(self.folder_label, height=7, width=24)
        self.folder_text.grid(row=1, column=0)
        self._folder_update_flag = True
        self.folder_text.bind('<<Modified>>', self.update_folder_parameters)
        self.error_folder_label = None
        self.selected_folder = ''
        if topics_disponibili:
            self.update_folder()

        self.sub_folder_var = tk.BooleanVar()
        self.sub_folder_radio = tk.Radiobutton(self.frame4, text='Add files in\nevery subfolder',
            variable=self.sub_folder_var, value=True)
        self.sub_folder_radio.grid(row=0, column=2)
        self.top_folder = tk.Radiobutton(self.frame4, text='Add only files\nin the top folder',
            variable=self.sub_folder_var, value=False)
        self.top_folder.grid(row=0, column=1)
        self.extension_label = tk.Label(self.frame4, text='Extension')
        self.extension_label.grid(row=1, column=1)
        self.extension_entry = tk.Entry(self.frame4, width=5)
        self.extension_entry.grid(row=1, column=2)
        self.extension_entry.insert(0, '.*')

        self.sigle_file_radio.invoke()

        frame_end_buttons = tk.Frame(self.frame1)
        frame_end_buttons.grid(row=2, column=0, columnspan=4, sticky=tk.N+tk.S+tk.E+tk.W)
        tk.Grid.rowconfigure(frame_end_buttons, 0, weight=1)
        tk.Grid.columnconfigure(frame_end_buttons, 0, weight=1)
        tk.Grid.columnconfigure(frame_end_buttons, 1, weight=1)
        self.confirm_add_button = tk.Button(frame_end_buttons, text='Add Test', command=self.confirm_add_topic)
        self.confirm_add_button.grid(row=0, column=0, sticky=tk.N+tk.S+tk.E+tk.W)
        self.undo_add_button = tk.Button(frame_end_buttons, text='Undo', command=self.undo_add_topic)
        self.undo_add_button.grid(row=0, column=1, sticky=tk.N+tk.S+tk.E+tk.W)

    def browse_file(self, tipo):
        file_path = self.file_text[tipo].get(1.0, tk.END).strip()
        file_path = file_path[: max(file_path.rfind('\\'), file_path.rfind('/'))]
        file_path = dialog.askopenfilename(title='Select file', initialdir=file_path)
        if file_path:
            self.file_text[tipo].delete(1.0, tk.END)
            self.file_text[tipo].insert(tk.END, file_path)
            self.selected_file[tipo] = file_path

    def new_file(self, tipo):
        if self.create_file[tipo].get():
            self.file_text[tipo].delete(1.0, tk.END)
            query = self.db.execute("SELECT MAX(ID) FROM concepts_table;")
            new_id = query.fetchone()[0]
            if new_id:
                new_id += 1
            else:
                new_id = 1
            stringhetta = 'Q'
            if tipo == 1:
                stringhetta = 'A'
            elif tipo == 2:
                stringhetta = 'S'
            self.selected_file[tipo] = os.path.join(os.path.dirname(__file__), 'Qst_Ans', stringhetta + str(new_id) + '.txt')
            self.file_text[tipo].insert(tk.END, self.selected_file[tipo])
            self.file_button[tipo]['state'] = 'disabled'
            self.file_text[tipo]['height'] = 1
            self.file_text[tipo]['state'] = 'disabled'
            self.new_file_text[tipo].grid(row=2, column=0, columnspan=2)
        else:
            self.new_file_text[tipo].grid_forget()
            self.file_button[tipo]['state'] = 'normal'
            self.file_text[tipo]['state'] = 'normal'
            self.file_text[tipo]['height'] = 7
            self.file_text[tipo].delete(1.0, tk.END)
            self.selected_file[tipo] = ''

    def add_another_ans(self):
        self.add_swich.grid_forget()
        self.file_label[2].grid(row=3, column=0, columnspan=2)

    def browse_folder(self):
        folder_path = self.folder_text.get(1.0, tk.END).strip()
        folder_path = dialog.askdirectory(title='Select Folder', initialdir=folder_path)
        if folder_path:
            self.folder_text.delete(1.0, tk.END)
            self.folder_text.insert(tk.END, folder_path)

    def select_topic(self, _):
        self.selected_top = self.top_listbox.get(self.top_listbox.curselection()).strip()
        self.update_subtopics()
        self.update_file()
        self.update_folder()

    def select_sub_topic(self, _):
        self.selected_subtop = self.subtop_listbox.get(self.subtop_listbox.curselection()).strip()
        self.update_file()
        self.update_folder()

    def select_single_file(self):
        self.frame4.grid_forget()
        self.frame3.grid(row=1, column=2, columnspan=2)

    def select_multi_file(self):
        self.frame3.grid_forget()
        self.frame4.grid(row=1, column=2, columnspan=2)

    def update_subtopics(self):
        self.subtop_listbox.delete(0, self.subtop_listbox.size())
        query = self.db.execute("SELECT DISTINCT subtopic FROM concepts_table WHERE topic = '" + self.selected_top + "' ORDER BY ID DESC")
        subtopics_disponibili = [row[0] for row in query]
        subtopics_disponibili.reverse()
        for subtopic in subtopics_disponibili:
            self.subtop_listbox.insert(0, subtopic)
        self.selected_subtop = self.subtop_listbox.get(0).strip()
        self.subtop_listbox.select_set(0)

    def update_file(self):
        query = self.db.execute("SELECT qs_path, ans_path FROM concepts_table WHERE topic = '" + self.selected_top + "' AND subtopic = '" + self.selected_subtop + "'" + "ORDER BY ID DESC LIMIT 1").fetchone()
        for i in range(2):
            self.selected_file[i] = query[i]
            self.file_text[i].delete(1.0, tk.END)
            self.file_text[i].insert(tk.END, self.selected_file[i])

    def update_folder(self):
        self.folder_text.delete(1.0, tk.END)
        query = self.db.execute("SELECT qs_path FROM concepts_table WHERE topic = '" + self.selected_top + "' AND subtopic = '" + self.selected_subtop + "'" + "ORDER BY ID DESC LIMIT 1")
        self.selected_folder = query.fetchone()[0]
        self.selected_folder = self.selected_folder[: max(self.selected_folder.rfind('\\'), self.selected_folder.rfind('/'))]
        self.folder_text.insert(tk.END, self.selected_folder)

    def update_file_parameters(self, _):
        for i in range(3):
            self.file_text[i].tk.call(self.file_text[i]._w, 'edit', 'modified', 0)
        if self._file_update_flag:
            if self.random_check:
                self.random_check.destroy()
            self.random_check = None
            if self.error_file_label:
                self.error_file_label.destroy()
            self.error_file_label = None
            if self.error_extens_label:
                self.error_extens_label.destroy()
            self.error_extens_label = None
            for i in range(3):
                for lab in self.param_labels[i]:
                    lab.destroy()
                for ent in self.param_entrys[i]:
                    ent.destroy()
                self.param_labels[i] = []
                self.param_entrys[i] = []
                self.selected_file[i] = self.file_text[i].get(1.0, tk.END).strip()
                if not self.create_file[i].get() and (not i or self.selected_file[i]):
                    temp = self.selected_file[i].split('.')
                    if len(temp) >= 2:
                        extension = '.' + temp[-1]
                        self.selected_prog[i] = None
                        for prog in self.programs:
                            if prog.get_extn() == extension:
                                self.selected_prog[i] = prog
                                break
                        if self.selected_prog[i]:
                            for att in self.selected_prog[i].get_strings():
                                if att[0] == '<' and att[-1] == '>' and att != '<File Path>':
                                    self.param_labels[i].append(tk.Label(self.frame_param[i], text=att[1:-1]))
                                    self.param_labels[i][-1].pack()
                                    self.param_entrys[i].append(tk.Entry(self.frame_param[i], width=5))
                                    self.param_entrys[i][-1].pack()
# if att == '<Page>':
#     self.random_var = tk.IntVar()
#     self.random_var.set(-1)
#     self.random_check = tk.Checkbutton(self.frame2, text='Random', variable=self.random_var,
#         onvalue=(len(self.param_labels)-1), offvalue=(-len(self.param_labels)), 
#         command=self.set_random_page)
#     self.random_check.pack()
                        elif not self.error_extens_label:
                            self.error_extens_label = tk.Label(self.frame1, text='Extension ' + extension + ' not known.\n The file will be open with the\ndefault program associated')
                            self.error_extens_label.grid(row=2, column=0)
                    elif not self.error_extens_label:
                        self.error_extens_label = tk.Label(self.frame1, text='File has no extension.\n The file will be open with the\ndefault program associated')
                        self.error_extens_label.grid(row=2, column=0)
                    if not self.error_file_label and not os.path.isfile(self.selected_file[i]):
                        self.error_file_label = tk.Label(self.frame1, text='ERROR:\nthe file does not exist')
                        self.error_file_label.grid(row=2, column=2)
            self._file_update_flag = False
        else:
            self._file_update_flag = True

    def update_folder_parameters(self, _):
        self.folder_text.tk.call(self.folder_text._w, 'edit', 'modified', 0)
        if self._folder_update_flag:
            if self.error_folder_label:
                self.error_folder_label.destroy()
            self.error_folder_label = None
            self.selected_folder = self.folder_text.get(1.0, tk.END).strip()
            if not os.path.exists(self.selected_folder):
                self.error_folder_label = tk.Label(self.frame4, text='ERROR:\nthe folder does not exist')
                self.error_folder_label.grid(row=0, column=1, rowspan=3)
            self._folder_update_flag = False
        else:
            self._folder_update_flag = True

    def confirm_add_topic(self):
        for i in range(3):
            if self.create_file[i].get():
                ffile = open(self.file_text[i].get(1.0, tk.END).strip(), 'w')
                ffile.write(self.new_file_text[i].get(1.0, tk.END).strip())
                ffile.close()
        if self.top_new_entry.get():
            self.selected_top = self.top_new_entry.get().strip()
        if self.subtop_new_entry.get():
            self.selected_subtop = self.subtop_new_entry.get().strip()
        query = self.db.execute("SELECT MAX(ID) FROM concepts_table;")
        new_id = query.fetchone()[0]
        if new_id:
            new_id += 1
        else:
            new_id = 1
        if self.add_type.get() == 1:
            parameters = ['', '', '']
            for i in range(3):
                for j, entry in enumerate(self.param_entrys[i]):
                    att = entry.get().strip()
                    if att == 'rand':
                        self.db.execute("INSERT INTO meta_concepts_table (ID, checked_pages) VALUES (" + str(new_id) + ", '' );")
                    if j > 0:
                        parameters += ",*,"
                    parameters[i] += att
            self.db.execute("INSERT INTO concepts_table (ID,topic,subtopic,qs_path,ans_path,ans2_path,qs_params,ans_params,ans2_params) VALUES (" + str(new_id) + ", '" + self.selected_top + "', '" + self.selected_subtop + "', '" + self.selected_file[0] + "', '" + self.selected_file[1] + "', '" + self.selected_file[2] + "', '" + parameters[0] + "', '" + parameters[1] + "', '" + parameters[2] + "' );")
        else:
            extension = self.extension_entry.get().strip()
            if extension == ".*":
                extension = ""
            for root, _, files in os.walk(self.selected_folder):
                for afile in files:
                    if afile.endswith(extension):
                        parameters = ''
                        self.db.execute("INSERT INTO concepts_table (ID,topic,subtopic,qs_path) \
                          VALUES (" + str(new_id) + ", '" + self.selected_top + "', '" + self.selected_subtop + "', '" + os.path.join(root, afile) + "' );")
                        new_id += 1
                if not self.sub_folder_var.get():
                    break
        self.db.commit()
        self.main_wind.update()
        self.main_wind.update_topics()
        self.frame1.destroy()

    # def set_random_page(self):
    #     n = self.random_var.get()
    #     if n >= 0:
    #         self.param_entrys[n].delete(0, 'end')
    #         self.param_entrys[n].insert(0, 'rand')
    #         self.param_entrys[n].config(state=tk.DISABLED)
    #     else:
    #         self.param_entrys[-n-1].config(state=tk.NORMAL)
    #         self.param_entrys[n].delete(0, 'end')

    def undo_add_topic(self):
        self.main_wind.update()
        self.frame1.destroy()
