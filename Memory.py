#!/usr/bin/python3
'''
Memory e' un programma realizzato per studiare e ricordarsi cose
'''
import tkinter as tk
import os, sys
import sqlite3
from WindowMain import WindowMain
from WindowPerformTest import WindowPerformTest

class Program:

    def __init__(self, extension, path, strings):
        self._extension = extension
        self._path = path
        self._strings = strings

    def get_extn(self):
        return self._extension

    def get_path(self):
        return self._path

    def get_strings(self):
        return self._strings

    def __str__(self):
        return 'Extension: ' + self._extension + ' Path: ' + self._path + ' Parameters: ' + str(self._strings)

def load_programs():
    programs = []
    filename = os.path.join(os.path.dirname(__file__), 'Programs.txt')
    if os.path.isfile(filename):
        ffile = open(filename, 'r')
        text = ffile.readlines()
        ffile.close()
        for riga in text:
            if riga[0] != '#':
                parametri = riga.strip().split('\t|')
                lista = parametri[2].split(',*,')
                programs.append(Program(parametri[0], parametri[1], lista))
    else:
        ffile = open(filename, 'w+')
        ffile.write("#'.Extension'\t|'Program Path'\t|'Parameter 1',*,'Parameter 2',*,<'User Parameter 1'>")
    return programs

def setup_database():
    filename = os.path.join(os.path.dirname(__file__), 'Qst_Ans')
    if not os.path.exists(filename):
        os.makedirs(filename)
    database = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'memory.db'))
    database.execute('''CREATE TABLE IF NOT EXISTS concepts_table
        (ID integer PRIMARY KEY NOT NULL, topic text, subtopic text, qs_path text, ans_path text, ans2_path text, qs_params text, ans_params text, ans2_params text)''')
    database.execute('''CREATE TABLE IF NOT EXISTS meta_concepts_table
        (ID integer PRIMARY KEY NOT NULL, end_page integer, checked_pages text)''')
    database.execute('''CREATE TABLE IF NOT EXISTS tests_table
        (concept_ID integer NOT NULL, date text NOT NULL, outcome int NOT NULL);''')
    database.commit()
    return database

if __name__ == "__main__":
    programs = load_programs()
    database = setup_database()
    root = tk.Tk()
    N = len(sys.argv)
    if N == 1:
        WindowMain(database, programs, root)
    else:
        WindowPerformTest(database, programs, root, None, sys.argv[1:N])
    root.mainloop()