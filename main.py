import logging
import sys
from tkinter import filedialog as fd
from tkinter import messagebox as mb

from src.fileio import VacanciesManager
from src.gui import EditorWindow, StartWindow
from src.hh_api import HH

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    sw = StartWindow()
    sw.mainloop()

    try:
        if sw.fp:
            logging.info(f"Filepath: {sw.fp}")
        else:
            logging.info("File will be created")
    except AttributeError:
        logging.info("File dialogue interrupted by user")
        sys.exit()

    vm = VacanciesManager(sw.fp)
    hh = HH()

    ew = EditorWindow(vm, hh)
    ew.mainloop()

    # if ew.vm.path:
    #     ew.vm.save()
    #     mb.showinfo(
    #         title='HH-parser',
    #         message=f'Изменения сохранены в {ew.vm.path}'
    #     )
    # else:

    path = fd.asksaveasfilename(
        initialfile="example.json", filetypes=(("JSON файл", ".json"),)
    )

    if path:
        ew.vm.save(path)
        mb.showinfo(
            title="HH-parser", message=f"Файл успешно сохранён как {ew.vm.path}"
        )
    else:
        mb.showinfo(
            title="HH-parser", message="Файл не был выбран, результат не будет сохранён"
        )
