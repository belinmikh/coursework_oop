from tkinter import (
    BooleanVar,
    Button,
    Checkbutton,
    Entry,
    Frame,
    IntVar,
    Label,
    Spinbox,
    Tk,
    W,
)
from tkinter import filedialog as fd
from tkinter import messagebox as mb
from tkinter.ttk import Notebook

import tabulate

from src.fileio import VacanciesManager
from src.hh_api import HH
from src.models import Vacancy


class StartWindow(Tk):
    fp: str | None

    def __init__(self):
        super().__init__()

        self.title("HH-parser")
        self.geometry("470x315")
        self.resizable(width=False, height=False)

        self.config(bg="gray60")

        btn_new = Button(
            self,
            command=self.without_fp,
            text="Создать новый файл",
            font=("Arial", 24, "bold"),
        )
        btn_new.place(x=25, y=25, width=420, height=120)

        btn_exist = Button(
            self,
            command=self.choose_fp,
            text="Выбрать существующий",
            font=("Arial", 24, "bold"),
        )
        btn_exist.place(x=25, y=170, width=420, height=120)

    def without_fp(self):
        self.fp = None
        self.destroy()

    def choose_fp(self):
        self.fp = fd.askopenfilename(filetypes=(("JSON файл", ".json"),))
        if self.fp:
            self.destroy()


class EditorWindow(Tk):
    only_with_salary: BooleanVar
    txt: Entry
    spin: IntVar

    vm: VacanciesManager
    hh: HH

    def __init__(self, vm: VacanciesManager, hh: HH):
        super().__init__()

        if not isinstance(vm, VacanciesManager):
            raise TypeError("VacanciesManager object expected")
        if not isinstance(hh, HH):
            raise TypeError("HH object expected")

        self.vm = vm
        self.hh = hh

        self.title("HH-parser")
        self.geometry("400x210")
        self.resizable(width=False, height=False)

        tab_control = Notebook(self)

        tab0 = Frame(tab_control)
        tab1 = Frame(tab_control)
        tab2 = Frame(tab_control)

        tab_control.add(tab0, text="Поиск вакансий")
        tab_control.add(tab1, text="Фильтрация и сортировка")
        tab_control.add(tab2, text="Просмотр")

        # tab0

        lbl_decor = Label(tab0, text="hh.ru", font=("Arial", 24, "bold"), bg="gray95")
        lbl_decor.place(x=290, y=70)

        lbl_txt = Label(tab0, text="Вакансия должна включать:", font=("Arial", 12))
        lbl_txt.place(x=0, y=0, width=250, height=50)

        self.txt = Entry(tab0, width=25)
        self.txt.place(x=10, y=50, width=250, height=30)

        self.only_with_salary = BooleanVar()
        self.only_with_salary.set(False)

        ows = Checkbutton(
            tab0,
            text="Только в рублёвой з/п",
            font=("Arial", 12),
            variable=self.only_with_salary,
            anchor=W,
        )
        ows.place(x=10, y=80, width=250, height=50)

        btn_get = Button(
            tab0, text="Выполнить поиск", font=("Arial", 12), command=self.hh_get
        )
        btn_get.place(x=10, y=120, width=250, height=50)

        # tab1

        btn_sort_asc = Button(
            tab1,
            text="Отсортировать по возрастанию з/п",
            font=("Arial", 12),
            command=self.sort_asc,
        )
        btn_sort_asc.place(x=10, y=5, width=380, height=50)

        btn_sort_desc = Button(
            tab1,
            text="Отсортировать по убыванию з/п",
            font=("Arial", 12),
            command=self.sort_desc,
        )
        btn_sort_desc.place(x=10, y=65, width=380, height=50)

        btn_filter = Button(
            tab1,
            text="Оставить только вакансии с указанной з/п",
            font=("Arial", 12),
            command=self.filter,
        )
        btn_filter.place(x=10, y=125, width=380, height=50)

        # tab2

        btn_spin = Button(
            tab2,
            text="Вывести топ вакансий по з/п",
            font=("Arial", 12),
            command=self.top,
        )
        btn_spin.place(x=110, y=35)

        self.spin = IntVar()

        spin = Spinbox(tab2, from_=1, to=10, width=5, textvariable=self.spin)
        spin.place(x=50, y=40)

        # bake

        tab_control.pack(expand=1, fill="both")

    # tab0

    def hh_get(self):

        new_vacs = self.hh.get(self.txt.get())
        i = 0
        if self.only_with_salary.get():
            for v in new_vacs:
                new_v = Vacancy.from_dict(v)
                if (new_v.salary_to or new_v.salary_from) and (
                    new_v.salary_currency in ["RUB", "RUR"]
                ):
                    self.vm.add(new_v)
                    i += 1
        else:
            for v in new_vacs:
                self.vm.add(Vacancy.from_dict(v))
                i += 1

        if i > 0:
            msg = f'Добавлено {i} вакансий по запросу "{self.txt.get()}"'
        else:
            msg = "Таких вакансий не существует либо произошла ошибка"

        mb.showinfo(title="HH-parser", message=msg)

    # tab1

    def sort_asc(self):
        self.vm.sort(reverse=False)
        mb.showinfo(
            title="HH-parser",
            message=f"{len(self.vm.vacancies)} вакансий успешно отсортированы по возрастанию з/п"
            "\n(внимание, сортировка не учитывает валюту!)",
        )

    def sort_desc(self):
        self.vm.sort()
        mb.showinfo(
            title="HH-parser",
            message=f"{len(self.vm.vacancies)} вакансий успешно отсортированы по убыванию з/п"
            "\n(внимание, сортировка не учитывает валюту!)",
        )

    def filter(self):
        prev_len = len(self.vm.vacancies)
        self.vm.filter()
        mb.showinfo(
            title="HH-parser",
            message=f"{prev_len - len(self.vm.vacancies)} вакансий без указанной з/п успешно удалены"
            f"\n({prev_len} -> {len(self.vm.vacancies)})",
        )

    # tab2

    def top(self):
        top_vacs = sorted(self.vm.vacancies, reverse=True)[: self.spin.get()]
        msg = f"Топ {self.spin.get()} вакансий по з/п:\n\n"
        top_vacs_table = tabulate.tabulate(
            [
                [
                    v.name,
                    v.salary_from or " ",
                    v.salary_to or " ",
                    v.salary_currency or " ",
                    v.url,
                ]
                for v in top_vacs
            ],
            headers=["Название", "от", "до", "валюта", "ссылка"],
            tablefmt="grid",
        )

        print(msg + top_vacs_table)

        mb.showinfo(title="HH-parser", message="Вакансии выведены в консоль")
