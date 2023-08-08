# Custom DataBase modules
from DBapi import DataBase
from DBerrors import *
# Graphical modules"
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.simpledialog import askstring
from tkinter.messagebox import showerror, showinfo, askyesnocancel
from tkinter import *
# Module for saving and loading the configuration
from configparser import ConfigParser
# Other modules
import os, sys, time, threading, locale

__db: DataBase
__fileName: str
__accountsList: list[list[Text]] = []
__accountsListTop: list[Text] = []
__config: ConfigParser = ConfigParser()
__DEFAULT_CONFIG_PATH = ".dbcache"
__DEFAULT_CONFIG: dict[str, dict[str, ...]] = {
    "OTHER": {
        "database_path": ""
    },
    "ROOT": {
        "geometry": "1080x720+200+200",
        "width": "1080",
        "width_indent": "200",
        "heigth": "720",
        "heigth_indent": "200"
    },
    "MENU_CHOICE": {
        "geometry": "520x135+400+200",
        "width": "520",
        "width_indent": "720",
        "heigth": "135",
        "heigth_indent": "410"
    }
}

def __loadConfig(filename: str=__DEFAULT_CONFIG_PATH) -> None:
    if not os.path.isfile(filename):
        for __key, __value in __DEFAULT_CONFIG.items():
            __config[__key] = __value
        return
    __config.read(filename)

__loadConfig(filename=".dbcache")

def __saveConfig(filename: str=__DEFAULT_CONFIG_PATH) -> None:
    with open(filename, 'w') as __configFile:
        __config.write(__configFile)

def __saveAndQuit(_=None) -> None:
    __saveDataBase()
    __quit(0)

def __askForSave(_=None) -> None:
    if __lastModifiedTime > __lastSavedTime:
        __answer = askyesnocancel(title=__translations("__askForSave", "title"), message=__translations("__askForSave", "message"), icon="warning")
        if __answer is None:
            return
        elif __answer:
            __saveAndQuit()
    __quit(0)

def __quit(code: int = -1) -> None:
    __root.destroy()
    __root.quit()
    __saveConfig()
    sys.exit(code)

def __saveDataBase() -> None:
    global __lastSavedTime
    __db.saveDatabase()
    __lastSavedTime = time.monotonic_ns()

def __loadDataBase() -> bool:
    global __db, __fileName
    __fileName = askopenfilename(filetypes=[(__translations("__loadDataBaseFile", "db"), ".db"), (__translations("__loadDataBaseFile", "*"), "*.*")], title=__translations("__loadDataBaseFile", "title"), initialdir=os.getcwd(), parent=__root)
    if __fileName == "" or __fileName == ".db":
        return False
    __password = askstring(title=__translations("__loadDataBaseAskPassword", "title"), prompt=__translations("__loadDataBaseAskPassword", "message"), show="*", parent=__root)
    try:
        __db = DataBase(__fileName, __password)
        __config["OTHER"]["database_path"] = __fileName
    except PasswordError:
        showerror(title=__translations("__loadDataBaseBadPassword", "title"), message=__translations("__loadDataBaseBadPassword", "message"))
        return False
    return True

def __loadNewDataBase() -> bool:
    global __db, __fileName
    __fileName = asksaveasfilename(confirmoverwrite=True, filetypes=[(__translations("__loadNewDataBaseFile", "db"), ".db"), (__translations("__loadNewDataBaseFile", "*"), "*.*")], defaultextension=".db", title=__translations("__loadNewDataBaseFile", "title"), initialdir=os.getcwd())
    if __fileName == "":
        return False
    try:
        __password = askstring(title=__translations("__loadNewDataBaseAskPassword", "title"), prompt=__translations("__loadNewDataBaseAskPassword", "message"), show="*", parent=__root)
        __db = DataBase(__fileName, __password)
        __db.infos = ("language", __DEFAULT_LANGUAGE)
    except Exception as e:
        showerror(title=__translations("__loadNewDataBaseErrorMessage"), message=str(e))
        return False
    return True

def __updateListAccounts():
    global __accountsList
    __length = __root.winfo_width()
    __sizes = {0: int(__length / 360), 1: int(__length / 74), 2: int(__length / 65), 3: int(__length / 60.5),4: int(__length / 58), 5: int(__length / 51)}
    for __x in __accountsList:
        for __y in __x:
            if hasattr(__y, 'destroy'):
                __y.destroy()
    for account in __accountsListTop:
        account.destroy()
    __accountsList = [[Text() for _ in range(len(__sizes.keys())+1)] for _ in range(len(__db.currentAccounts))]
    __accountsListTop.append(Text(__rootFrame, width=__sizes[0], height=1, fg="black", font=(__FONT, __FONT_SIZE, __FONT_STYLE)))
    __accountsListTop[-1].tag_configure("center", justify='center')
    __accountsListTop[-1].insert(END, __translations("__updateListId"))
    __accountsListTop[-1].tag_add("center", 1.0, "end")
    __accountsListTop[-1].config(state=DISABLED)
    __accountsListTop[-1].grid(row=0, column=0)
    __accountsListTop.append(Text(__rootFrame, width=__sizes[1], height=1, fg="black", font=(__FONT, __FONT_SIZE, __FONT_STYLE)))
    __accountsListTop[-1].tag_configure("center", justify='center')
    __accountsListTop[-1].insert(END, __translations("__updateListTitle"))
    __accountsListTop[-1].tag_add("center", 1.0, "end")
    __accountsListTop[-1].config(state=DISABLED)
    __accountsListTop[-1].grid(row=0, column=1)
    __accountsListTop.append(Text(__rootFrame, width=__sizes[2], height=1, fg="black", font=(__FONT, __FONT_SIZE, __FONT_STYLE)))
    __accountsListTop[-1].tag_configure("center", justify='center')
    __accountsListTop[-1].insert(END, __translations("__updateListUser"))
    __accountsListTop[-1].tag_add("center", 1.0, "end")
    __accountsListTop[-1].config(state=DISABLED)
    __accountsListTop[-1].grid(row=0, column=2)
    __accountsListTop.append(Text(__rootFrame, width=__sizes[3], height=1, fg="black", font=(__FONT, __FONT_SIZE, __FONT_STYLE)))
    __accountsListTop[-1].tag_configure("center", justify='center')
    __accountsListTop[-1].insert(END, __translations("__updateListPassword"))
    __accountsListTop[-1].tag_add("center", 1.0, "end")
    __accountsListTop[-1].config(state=DISABLED)
    __accountsListTop[-1].grid(row=0, column=3)
    __accountsListTop.append(Text(__rootFrame, width=__sizes[4], height=1, fg="black", font=(__FONT, __FONT_SIZE, __FONT_STYLE)))
    __accountsListTop[-1].tag_configure("center", justify='center')
    __accountsListTop[-1].insert(END, __translations("__updateListUrl"))
    __accountsListTop[-1].tag_add("center", 1.0, "end")
    __accountsListTop[-1].config(state=DISABLED)
    __accountsListTop[-1].grid(row=0, column=4)
    __accountsListTop.append(Text(__rootFrame, width=__sizes[5], height=1, fg="black", font=(__FONT, __FONT_SIZE, __FONT_STYLE)))
    __accountsListTop[-1].tag_configure("center", justify='center')
    __accountsListTop[-1].insert(END, __translations("__updateListNote"))
    __accountsListTop[-1].tag_add("center", 1.0, "end")
    __accountsListTop[-1].config(state=DISABLED)
    __accountsListTop[-1].grid(row=0, column=5)
    for __i in range(5):
        for __y in range(len(__db.currentAccounts)):
            __value = StringVar()
            __value.set(__db.currentAccounts[__y][__i])
            __valueEntry = Text(__rootFrame, width=__sizes[__i + 1], height=1, fg="black", font=(__FONT, __FONT_SIZE))
            if __i == 2:
                if __showPassword.get():
                    __valueEntry.insert(END, __db.currentAccounts[__y][__i])
                else :
                    __valueEntry.insert(END, "".join(["*" for _ in range(len(__db.currentAccounts[__y][__i]))]))
            else:
                __valueEntry.tag_configure("center", justify='center')
                __valueEntry.insert(END, __db.currentAccounts[__y][__i])
                __valueEntry.tag_add("center", 1.0, "end")
            __valueEntry.config(state=DISABLED)
            __accountsList[__y][__i+1] = __valueEntry
            __accountsList[__y][__i+1].bind("<Button-3>", __rootShowRightClickMenuLambda(__y))
            __accountsList[__y][__i+1].grid(row=__y+1, column=__i+1)
    for __i in range(len(__db.currentAccounts)):
        __idEntry = Text(__rootFrame, width=__sizes[0], height=1, fg="black", font=(__FONT, __FONT_SIZE))
        __idEntry.tag_configure("center", justify='center')
        __idEntry.insert(END, str(__i))
        __idEntry.tag_add("center", 1.0, "end")
        __idEntry.config(state=DISABLED)
        __accountsList[__i][0] = __idEntry
        __accountsList[__i][0].bind("<Button-3>", __rootShowRightClickMenuLambda(__i))
        __accountsList[__i][0].grid(row=__i + 1, column=0)
    __reloadTranslations()

def __clearClipboard(seconds: int, content: str):
    time.sleep(seconds)
    if content == __root.clipboard_get():
        __root.clipboard_clear()
        __root.clipboard_append("")

def __cancelLastAction(_ = None) -> None:
    if len(__lastActions) == 0:
        return
    __last: list[str, int, list, int] = __lastActions[-1]
    if __last[0] == "modify":
        __lastActions.pop()
        __toSend = [__last[1], *__last[2], __last[3]]
        __rootButtonModifyAccount(None, __toSend)
        __lastActions.pop()
    elif __last[0] == "add":
        __lastActions.pop()
        __toSend = [__last[1], __last[3]]
        __rootButtonRemoveAccount(None, __toSend)
        __lastActions.pop()
    elif __last[0] == "remove":
        __lastActions.pop()
        __values = []
        for __i in range(int(__last[1]), len(__db.currentAccounts)):
            try:
                __values.append(__db.getAccount(__i))
            except ValueError as err :
                print(f"Error:{err} ; Index:{__i} ; Acocunts:{__db.currentAccounts} ; Values;{__values} ; __last:{__last}")
        for _ in range(int(__last[1]), len(__db.currentAccounts)):
            __rootButtonRemoveAccount(None, [int(__last[1]), None])
            __lastActions.pop()
        __toSend = [*__last[2], __last[3]]
        __rootButtonAddAccount(None, __toSend)
        __lastActions.pop()
        for __i in range(len(__values)):
            __toSend = [*__values[__i], __last[3]]
            __rootButtonAddAccount(None, __toSend)
            __lastActions.pop()
    else:
        raise ValueError(f'Error : __last[0] value "{__last[0]}" is not valid.')
    __updateListAccounts()

def __getLanguage() -> str:
    __systemLanguage, _ = locale.getlocale()
    __systemLanguage = __systemLanguage[:2].lower()
    if __systemLanguage in __LANGUAGES_AVAILABLE:
        return __systemLanguage
    return __DEFAULT_LANGUAGE

def __verifyIfIdExist(__id: int | str) -> bool:
    return int(__id) < len(__db.currentAccounts)

def __menuChoiceDBLoad() -> None:
    __result = __loadDataBase()
    if __result:
        __menuChoiceDBRoot.withdraw()
        __updateListAccounts()
        __root.deiconify()
        __root.bind("<Configure>", __rootUpdates)

def __menuChoiceDBNew() -> None:
    __result = __loadNewDataBase()
    if __result:
        __menuChoiceDBRoot.withdraw()
        __updateListAccounts()
        __root.deiconify()
        __root.bind("<Configure>", __rootUpdates)

def __menuChoiceDB(isInit: bool = False) -> None:
    __menuChoiceDBRoot.geometry(__config["MENU_CHOICE"]["geometry"])
    __menuChoiceDBRoot.resizable(True, True)
    __menuChoiceDBRoot.iconbitmap(__ressource_path(__ICON))
    __menuChoiceDBRoot.protocol("WM_DELETE_WINDOW", __quit)
    __menuChoiceDBRoot.bind("<Configure>", lambda _=None : __windowUpdates(__menuChoiceDBRoot, "MENU_CHOICE"))
    __menuChoiceDBRoot["bg"] = "white"
    # Top button to change language
    __menuChoiceDBMenubuttons = Frame(__menuChoiceDBRoot, background="white", width=__config["MENU_CHOICE"]["width"], height=25)
    __menuChoiceDBMenubuttons.pack(padx=0, pady=0, anchor="nw")
    __menuChoiceDBMenubuttons.pack_propagate(False)
    __menuChoiceDBTopMenubuttonLanguage = Menubutton(__menuChoiceDBRoot, bg="white", textvariable=__stringVars["__rootTopMenubuttonLanguageVar"])
    __menuChoiceDBTopMenubuttonLanguage.pack(in_=__menuChoiceDBMenubuttons, padx=5, side=LEFT)
    __menuChoiceDBTopMenuLanguage = Menu(__menuChoiceDBTopMenubuttonLanguage, tearoff=0)
    __menuChoiceDBTopMenuLanguage.add_checkbutton(label="Français", command=lambda: __rootButtonLanguage("fr", isInit), onvalue=True, offvalue=False, variable=__languageCheckMarks[__LANGUAGES_AVAILABLE.index("fr")])
    __menuChoiceDBTopMenuLanguage.add_checkbutton(label="English", command=lambda: __rootButtonLanguage("en", isInit), onvalue=True, offvalue=False, variable=__languageCheckMarks[__LANGUAGES_AVAILABLE.index("en")])
    __menuChoiceDBTopMenubuttonLanguage.configure(menu=__menuChoiceDBTopMenuLanguage)
    __menuChoiceDBLabel1 = Label(__menuChoiceDBRoot, font=(__FONT, __FONT_SIZE), wraplength=int(__config["MENU_CHOICE"]["width"]), background="white", textvariable=__stringVars["__menuChoiceDBLabel1Var"])
    __menuChoiceDBLabel1.pack(padx=0, pady=15)
    __menuChoiceDBBoutons = Frame(__menuChoiceDBRoot, background="white")
    __menuChoiceDBBoutons.pack(padx=5, pady=5)
    __menuChoiceDBBouton1 = Button(__menuChoiceDBBoutons, command=__menuChoiceDBLoad, textvariable=__stringVars["__menuChoiceDBBouton1Var"])
    __menuChoiceDBBouton1.grid(padx=5, pady=5, column=0, row=0)
    __menuChoiceDBBouton2 = Button(__menuChoiceDBBoutons, command=__menuChoiceDBNew, textvariable=__stringVars["__menuChoiceDBBouton2Var"])
    __menuChoiceDBBouton2.grid(padx=5, pady=5, column=1, row=0)
    __menuChoiceDBRoot.mainloop()

def __rootUpdates(_=None):
    global __lastWidth
    __currentWidth = __root.winfo_width()
    __windowUpdates(__root, "ROOT")
    if __currentWidth != __lastWidth:
        __lastWidth = __currentWidth
        __rootTopMenubuttons.config(width=__currentWidth)
        __updateListAccounts()

def __windowUpdates(window: Toplevel | Tk, windowName: str):
    windowName = windowName.upper()
    __config[windowName]["geometry"] = str(window.geometry())
    __config[windowName]["width"] = str(window.winfo_width())
    __config[windowName]["width_indent"] = str(__root.winfo_x())
    __config[windowName]["heigth"] = str(window.winfo_height())
    __config[windowName]["heigth_indent"] = str(__root.winfo_y())

def __rootButtonSaveDataBase(_ = None) -> None:
    __saveDataBase()
    showinfo(title=__translations("__rootButtonSaveDataBase", "title"), message=__translations("__rootButtonSaveDataBase", "message"))

def __rootButtonLoadDataBase(_ = None) -> None:
    __root.withdraw()
    __menuChoiceDBRoot.deiconify()
    __menuChoiceDB()

def __rootButtonChangePassword() -> bool:
    global __lastModifiedTime
    __oldPassword = askstring(title=__translations("__rootButtonChangePasswordOldPassword", "title"), prompt=__translations("__rootButtonChangePasswordOldPassword", "message"), show="*", parent=__root)
    if __oldPassword is None:
        return False
    __newPassword = askstring(title=__translations("__rootButtonChangePasswordNewPassword", "title"), prompt=__translations("__rootButtonChangePasswordNewPassword", "message"), show="*", parent=__root)
    if __newPassword is None:
        return False
    try:
        __db.changePassword(__oldPassword, __newPassword)
        __lastModifiedTime = time.monotonic_ns()
    except PasswordError:
        showerror(title=__translations("__rootButtonChangePasswordBadPassword", "title"), message=__translations("__rootButtonChangePasswordBadPassword", "message"))
        return False
    return True

def __rootButtonAddAccount(_ = None, __customValues: list=None):
    def __addAccount(__title: str, __username: str, __password: str, __url: str, __note: str, __lastTimeModified: int | None = None) -> None:
        global __lastModifiedTime
        __db.addAccount(__title, __username, __password, __url, __note)
        __lastActions.append(["add", len(__db.currentAccounts)-1, [], __lastModifiedTime])
        if __lastTimeModified is not None:
            __lastModifiedTime = __lastTimeModified
        else:
            __lastModifiedTime = time.monotonic_ns()
        __shutdown()
    def __shutdown() -> None:
        __buttonAccountRootAdd.withdraw()
        __updateListAccounts()
    if __customValues is not None:
        __addAccount(*__customValues)
        return
    __buttonAccountRootAdd.deiconify()
    __buttonAccountRootAdd.geometry('300x135')
    __buttonAccountRootAdd.iconbitmap(__ressource_path(__ICON))
    __buttonAccountRootAdd.protocol("WM_DELETE_WINDOW", __shutdown)
    __buttonAccountRootAdd.resizable(False, False)
    Label(__buttonAccountRootAdd, textvariable=__stringVars["__buttonAccountRootAddTitleVar"]).grid(row=0, column=0, sticky="w")
    __title = StringVar()
    __entryTitle = Entry(__buttonAccountRootAdd, textvariable=__title)
    __entryTitle.grid(row=0, column=1)
    __entryTitle.focus_set()
    Label(__buttonAccountRootAdd, textvariable=__stringVars["__buttonAccountRootAddUserVar"]).grid(row=1, column=0, sticky="w")
    __username = StringVar()
    Entry(__buttonAccountRootAdd, textvariable=__username).grid(row=1, column=1)
    Label(__buttonAccountRootAdd, textvariable=__stringVars["__buttonAccountRootAddPasswordVar"]).grid(row=2, column=0, sticky="w")
    __password = StringVar()
    Entry(__buttonAccountRootAdd, textvariable=__password, show='*').grid(row=2, column=1)
    Label(__buttonAccountRootAdd, textvariable=__stringVars["__buttonAccountRootAddUrlVar"]).grid(row=3, column=0, sticky="w")
    __url = StringVar()
    Entry(__buttonAccountRootAdd, textvariable=__url).grid(row=3, column=1)
    Label(__buttonAccountRootAdd, textvariable=__stringVars["__buttonAccountRootAddNoteVar"]).grid(row=4, column=0, sticky="w")
    __note = StringVar()
    Entry(__buttonAccountRootAdd, textvariable=__note).grid(row=4, column=1)
    Button(__buttonAccountRootAdd, command=lambda : __addAccount(__title.get(), __username.get(), __password.get(), __url.get(), __note.get()), textvariable=__stringVars["__buttonAccountRootAddButtonVar"]).grid(row=5, column=1)
    __buttonAccountRootAdd.mainloop()

def __rootButtonModifyAccount(_ = None, __customValues: list=None, __customId: int | None = None) -> None:
    def __modifyAccount(__id: str, __newTitle: str, __newUsername: str, __newPassword: str, __newUrl: str, __newNote: str, __lastTimeModified: int | None = None) -> None:
        global __lastModifiedTime
        if __newTitle == "":
            __newTitle = None
        if __newUsername == "":
            __newUsername = None
        if __newPassword == "":
            __newPassword = None
        if __newUrl == "":
            __newUrl = None
        if __newNote == "":
            __newNote = None
        if not __verifyIfIdExist(int(__id)):
            showerror(title=__translations("showerror_id_incorrect", "title"), message=__translations("showerror_id_incorrect", "message"))
            return
        __old = __db.getAccount(int(__id)).copy()
        __db.modifyAccount(int(__id), __newTitle, __newUsername, __newPassword, __newUrl, __newNote)
        __lastActions.append(["modify", int(__id), __old, __lastModifiedTime])
        if __lastTimeModified is not None:
            __lastModifiedTime = __lastTimeModified
        else:
            __lastModifiedTime = time.monotonic_ns()
        __shutdown()
    def __shutdown() -> None:
        __buttonAccountRootModify.withdraw()
        __updateListAccounts()
    if __customValues is not None:
        __modifyAccount(*__customValues)
        return
    __buttonAccountRootModify.deiconify()
    __buttonAccountRootModify.geometry('375x160')
    __buttonAccountRootModify.iconbitmap(__ressource_path(__ICON))
    __buttonAccountRootModify.protocol("WM_DELETE_WINDOW", __shutdown)
    __buttonAccountRootModify.resizable(False, False)
    Label(__buttonAccountRootModify, textvariable=__stringVars["__buttonAccountRootModifyIdVar"]).grid(row=0, column=0, sticky="w")
    __id = StringVar()
    __entryId = Entry(__buttonAccountRootModify, textvariable=__id)
    __entryId.grid(row=0, column=1)
    __entryId.focus_set()
    Label(__buttonAccountRootModify, textvariable=__stringVars["__buttonAccountRootModifyTitleVar"]).grid(row=1, column=0, sticky="w")
    __title = StringVar()
    __entryTitle = Entry(__buttonAccountRootModify, textvariable=__title)
    __entryTitle.grid(row=1, column=1)
    if __customId is not None:
        __id.set(str(__customId))
        __entryId.config(state="disabled")
        __entryTitle.focus_set()
    Label(__buttonAccountRootModify, textvariable=__stringVars["__buttonAccountRootModifyUserVar"]).grid(row=2, column=0, sticky="w")
    __username = StringVar()
    Entry(__buttonAccountRootModify, textvariable=__username).grid(row=2, column=1)
    Label(__buttonAccountRootModify, textvariable=__stringVars["__buttonAccountRootModifyPasswordVar"]).grid(row=3, column=0, sticky="w")
    __password = StringVar()
    Entry(__buttonAccountRootModify, textvariable=__password, show='*').grid(row=3, column=1)
    Label(__buttonAccountRootModify, textvariable=__stringVars["__buttonAccountRootModifyUrlVar"]).grid(row=4, column=0, sticky="w")
    __url = StringVar()
    Entry(__buttonAccountRootModify, textvariable=__url).grid(row=4, column=1)
    Label(__buttonAccountRootModify, textvariable=__stringVars["__buttonAccountRootModifyNoteVar"]).grid(row=5, column=0, sticky="w")
    __note = StringVar()
    Entry(__buttonAccountRootModify, textvariable=__note).grid(row=5, column=1)
    Button(__buttonAccountRootModify, command=lambda: __modifyAccount(__id.get(), __title.get(), __username.get(), __password.get(), __url.get(), __note.get()), textvariable=__stringVars["__buttonAccountRootModifyButtonVar"]).grid(row=6, column=1)
    __buttonAccountRootModify.mainloop()

def __rootButtonRemoveAccount(_ = None, __customRemove: list | None = None, __customId: int | None = None) -> None:
    def __removeAccount(__number: str, __lastTimeModified: int | None = None):
        global __lastModifiedTime
        if not __verifyIfIdExist(int(__number)):
            showerror(title=__translations("showerror_id_incorrect", "title"), message=__translations("showerror_id_incorrect", "message"))
            return
        __old = __db.getAccount(int(__number))
        __db.removeAccount(int(__number))
        __lastActions.append(["remove", int(__number), __old, __lastModifiedTime])
        if __lastTimeModified is not None:
            __lastModifiedTime = __lastTimeModified
        else:
            __lastModifiedTime = time.monotonic_ns()
        __shutdown()
    def __shutdown():
        __buttonAccountRootRemove.withdraw()
        __updateListAccounts()
    if __customRemove is not None:
        __removeAccount(__customRemove[0], __customRemove[1])
        return
    __buttonAccountRootRemove.deiconify()
    __buttonAccountRootRemove.geometry('230x75')
    __buttonAccountRootRemove.iconbitmap(__ressource_path(__ICON))
    __buttonAccountRootRemove.protocol("WM_DELETE_WINDOW", __shutdown)
    __buttonAccountRootRemove.resizable(False, False)
    Label(__buttonAccountRootRemove, textvariable=__stringVars["__buttonAccountRootRemoveIdVar"]).grid(row=1, column=0)
    __number = StringVar()
    __entryId = Entry(__buttonAccountRootRemove, textvariable=__number)
    __entryId.grid(row=2, column=0)
    __entryId.focus_set()
    __button = Button(__buttonAccountRootRemove, command=lambda: __removeAccount(__number.get()), textvariable=__stringVars["__buttonAccountRootRemoveButtonVar"])
    __button.grid(row=3, column=0)
    if __customId is not None:
        __number.set(str(__customId))
        __entryId.config(state="disabled")
        __button.focus_set()
    __buttonAccountRootRemove.mainloop()

def __rootButtonLanguage(language: str = "en", dontUpdateAccounts: bool = False):
    global __language
    __language = language
    for __bool in __languageCheckMarks:
        __bool.set(False)
    __languageCheckMarks[__LANGUAGES_AVAILABLE.index(__language)].set(True)
    __reloadTranslations()
    if not dontUpdateAccounts:
        __updateListAccounts()

def __rootShowRightClickMenuLambda(__id):
    return lambda __event : __rootShowRightClickMenu(int(__id), __event)

def __rootShowRightClickMenu(__id: int, __event):
    __rootRightClickMenu.delete(0, "end")
    __rootRightClickMenu.add_command(label=__translations("__rootRigthClickMenu", "title"), command=lambda: __rootShowRightClickMenuCopyInformation(__id, "title"))
    __rootRightClickMenu.add_command(label=__translations("__rootRigthClickMenu", "username"), command=lambda : __rootShowRightClickMenuCopyInformation(__id, "username"))
    __rootRightClickMenu.add_command(label=__translations("__rootRigthClickMenu", "password"), command=lambda : __rootShowRightClickMenuCopyInformation(__id, "password"))
    __rootRightClickMenu.add_command(label=__translations("__rootRigthClickMenu", "url"), command=lambda : __rootShowRightClickMenuCopyInformation(__id, "url"))
    __rootRightClickMenu.add_command(label=__translations("__rootRigthClickMenu", "note"), command=lambda : __rootShowRightClickMenuCopyInformation(__id, "note"))
    __rootRightClickMenu.add_separator()
    __rootRightClickMenu.add_command(label=__translations("__rootRigthClickMenu", "modify"), command=lambda: __rootButtonModifyAccount(__customId=__id))
    __rootRightClickMenu.add_command(label=__translations("__rootRigthClickMenu", "remove"), command=lambda : __rootButtonRemoveAccount(__customId=__id))
    __rootRightClickMenu.tk_popup(__event.x_root, __event.y_root, 0)
    __rootRightClickMenu.grab_release()

def __rootShowRightClickMenuCopyInformation(__id: int, __informationType: str):
    __root.clipboard_clear()
    if __informationType == "title":
        __root.clipboard_append(__accountsList[__id][1].get("1.0",'end-1c'))
        showinfo(title=__translations("__rootRigthClickMenuInfoTitle", "title"), message=__translations("__rootRigthClickMenuInfoMessage", "title"))
    elif __informationType == "username":
        __root.clipboard_append(__accountsList[__id][2].get("1.0",'end-1c'))
        showinfo(title=__translations("__rootRigthClickMenuInfoTitle", "username"), message=__translations("__rootRigthClickMenuInfoMessage", "username"))
    elif __informationType == "password":
        __root.clipboard_append(__accountsList[__id][3].get("1.0",'end-1c'))
        threading.Thread(target=lambda: __clearClipboard(30, __accountsList[__id][3].get("1.0",'end-1c'))).start()
        showinfo(title=__translations("__rootRigthClickMenuInfoTitle", "password"), message=__translations("__rootRigthClickMenuInfoMessage", "password"))
    elif __informationType == "url":
        __root.clipboard_append(__accountsList[__id][4].get("1.0",'end-1c'))
        showinfo(title=__translations("__rootRigthClickMenuInfoTitle", "url"), message=__translations("__rootRigthClickMenuInfoMessage", "url"))
    elif __informationType == "note":
        __root.clipboard_append(__accountsList[__id][5].get("1.0",'end-1c'))
        showinfo(title=__translations("__rootRigthClickMenuInfoTitle", "note"), message=__translations("__rootRigthClickMenuInfoMessage", "note"))
    else:
        raise ValueError(f"Error : Iccorect value for __informationType : '{__informationType}'")

def __translations(option1: str, option2: str = None):
    __lang: int | str = __language
    __translation: dict[str, dict[str, dict[str, str]]] = {
        # Fatal error Window
        "__rootFatalError": {
            "title": {
                "fr": "Le programme a rencontrer une erreur fatale",
                "en": "The program has encountered a fatal error"
            },
            "message": {
                "fr": "Le programme a rencontrer une erreur fatale et va donc s'arreter.",
                "en": "The program has encountered a fatal error and will shutdown."
            }
        },
        # Showerror if id is incorrect
        "showerror_id_incorrect": {
            "title": {
                "fr": "Identifiant incorrect",
                "en": "Incorrect ID"
            },
            "message": {
                "fr": "L'identifiant que vous avez entré est incorrect.",
                "en": "The username you entered is incorrect."
            }
        },
        # Root Window
        "__root.title": {
            "fr": "Gestionnaire de mots de passes",
            "en": "Password Manager"
        },
        "__rootTopMenubuttonFileVar": {
            "fr": "Fichier",
            "en": "File"
        },
        "__rootTopMenuFile": {
            "cancel": {
                "fr": "Annuler (Ctrl+Z)",
                "en": "Cancel (Ctrl+Z)"
            },
            "save": {
                "fr": "Sauvegarder (Ctrl+S)",
                "en": "Save (Ctrl+S)"
            },
            "load": {
                "fr": "Charger (Ctrl+O)",
                "en": "Load (Ctrl+O)"
            },
            "quit": {
                "fr": "Quitter (Alt+F4)",
                "en": "Quit (Alt+F4)"
            }
        },
        "__rootTopMenubuttonEditVar": {
            "fr": "Editer la BDD",
            "en": "Edit the DB"
        },
        "__rootTopMenuEdit": {
            "changepassword": {
                "fr": "Changer le mot de passe",
                "en": "Change the password"
            },
            "showpassword": {
                "fr": "Afficher les mots de passe",
                "en": "Show passwords"
            },
            "activatetopmost": {
                "fr": "Fenêtre toujours au premier plan",
                "en": "Window always on top"
            }
        },
        "__rootTopMenubuttonAccountVar": {
            "fr": "Gérer les comptes",
            "en": "Manage Accounts"
        },
        "__rootTopMenuAccount": {
            "add": {
                "fr": "Ajouter un compte (Ctrl+A)",
                "en": "Add an account (Ctrl+A)"
            },
            "modify": {
                "fr": "Modifier un compte (Ctrl+M)",
                "en": "Modify an account (Ctrl+M)"
            },
            "remove": {
                "fr": "Supprimer un compte (Ctrl+R)",
                "en": "Remove an account (Ctrl+R)"
            }
        },
        "__rootTopMenubuttonLanguageVar": {
            "fr": "Langue (Language)",
            "en": "Language"
        },
        # Root Window Right Click Menu
        "__rootRigthClickMenu": {
            "title": {
                "fr": "Copier le titre",
                "en": "Copy title"
            },
            "username": {
                "fr": "Copier l'utilisateur",
                "en": "Copy username"
            },
            "password": {
                "fr": "Copier mot de passe",
                "en": "Copy password"
            },
            "url": {
                "fr": "Copier l'URL",
                "en": "Copy URL"
            },
            "note": {
                "fr": "Copier la note",
                "en": "Copy note"
            },
            "remove": {
                "fr": "Supprimer le compte",
                "en": "Remove account"
            },
            "modify": {
                "fr": "Modifier le compte",
                "en": "Modify account"
            }
        },
        "__rootRigthClickMenuInfoTitle": {
            "title": {
                "fr": "Titre copier",
                "en": "Title copied"
            },
            "username": {
                "fr": "Nom utilisateur copier",
                "en": "Username copied"
            },
            "password": {
                "fr": "Mot de passe copier",
                "en": "Password copied"
            },
            "url": {
                "fr": "URL copier",
                "en": "URL copied"
            },
            "note": {
                "fr": "Note copier",
                "en": "Note copied"
            }
        },
        "__rootRigthClickMenuInfoMessage": {
            "title": {
                "fr": "Le titre a bien été copier.",
                "en": "The title has correctly been copied."
            },
            "username": {
                "fr": "Le nom d'utilisateur a bien été copier.",
                "en": "The username has correctly been copied."
            },
            "password": {
                "fr": "Le mot de passe a bien été copier.",
                "en": "The password has correctly been copied."
            },
            "url": {
                "fr": "L'URL a bien été copier.",
                "en": "The URL has correctly been copied."
            },
            "note": {
                "fr": "La note a bien été copier.",
                "en": "The note has correctly been copied."
            }
        },
        # Add account Window
        "__buttonAccountRootAdd.title": {
            "fr": "Ajouter un compte",
            "en": "Add an account"
        },
        "__buttonAccountRootAddTitleVar": {
            "fr": "Entrez le titre :",
            "en": "Enter a title :"
        },
        "__buttonAccountRootAddUserVar": {
            "fr": "Entrez le nom d'utilisateur :",
            "en": "Enter a username :"
        },
        "__buttonAccountRootAddPasswordVar": {
            "fr": "Entrez le mot de passe :",
            "en": "Enter a password :"
        },
        "__buttonAccountRootAddUrlVar": {
            "fr": "Entrez l'URL :",
            "en": "Enter the URL :"
        },
        "__buttonAccountRootAddNoteVar": {
            "fr": "Entrez la note :",
            "en": "Enter the note :"
        },
        "__buttonAccountRootAddButtonVar": {
            "fr": "Ajouter un compte",
            "en": "Add an account :"
        },
        # Modify Account Window
        "__buttonAccountRootModify.title": {
            "fr": "Modifer un compte",
            "en": "Modify an account"
        },
        "__buttonAccountRootModifyIdVar": {
            "fr": "Identifiant du compte à modifier :",
            "en": "ID of the account to modify:"
        },
        "__buttonAccountRootModifyTitleVar": {
            "fr": "Entrez le nouveau titre :",
            "en": "Enter the new title :"
        },
        "__buttonAccountRootModifyUserVar": {
            "fr": "Entrez le nouveau nom de l'utilisateur :",
            "en": "Enter the new name for the username :"
        },
        "__buttonAccountRootModifyPasswordVar": {
            "fr": "Entrez le nouveau mot de passe :",
            "en": "Enter the new password :"
        },
        "__buttonAccountRootModifyUrlVar": {
            "fr": "Entrez la nouvelle URL du site :",
            "en": "Enter the new URL for the site :"
        },
        "__buttonAccountRootModifyNoteVar": {
            "fr": "Entrez la nouvelle note :",
            "en": "Enter the new note :"
        },
        "__buttonAccountRootModifyButtonVar": {
            "fr": "Modifier un compte",
            "en": "Modify an account"
        },
        # Remove Account Window
        "__buttonAccountRootRemove.title": {
            "fr": "Supprimer un compte",
            "en": "Remove an account"
        },
        "__buttonAccountRootRemoveIdVar": {
            "fr": "Entrez le numéro du compte a supprimer :",
            "en": "Enter the account number to delete :"
        },
        "__buttonAccountRootRemoveButtonVar": {
            "fr": "Supprimer un compte",
            "en": "Delete an account"
        },
        # Choice DB Window
        "__menuChoiceDBRoot.title": {
            "fr": "Choisissez le mode d'ouverture de votre Base De Données",
            "en": "Choose the way to open your Database"
        },
        "__menuChoiceDBLabel1Var": {
            "fr": "Veuillez choisir comment ouvrir la Base De Données :",
            "en": "Please choose how to open the Database:"
        },
        "__menuChoiceDBBouton1Var": {
            "fr": "Ouvrir une BDD existante",
            "en": "Open an existing DB"
        },
        "__menuChoiceDBBouton2Var": {
            "fr": "Créer une nouvelle BDD",
            "en": "Create a new DB"
        },
        # update List
        "__updateListId": {
            "fr": "ID",
            "en": "ID"
        },
        "__updateListTitle": {
            "fr": "Titre",
            "en": "Title"
        },
        "__updateListUser": {
            "fr": "Utilisateur",
            "en": "User"
        },
        "__updateListPassword": {
            "fr": "Mot de passe",
            "en": "Password"
        },
        "__updateListUrl": {
            "fr": "Url",
            "en": "Url"
        },
        "__updateListNote": {
            "fr": "Note",
            "en": "Note"
        },
        # Load DB window
        "__loadDataBaseFile": {
            "db": {
                "fr": "Fichier base de données",
                "en": "Database file"
            },
            "*": {
                "fr": "Autre fichier",
                "en": "Other file"
            },
            "title": {
                "fr": "Séléctionnez fichier de base de données",
                "en": "Select the database file"
            }
        },
        "__loadDataBaseAskPassword": {
            "title": {
                "fr": "Entrer votre mot de passe",
                "en": "Enter your password"
            },
            "message": {
                "fr": "Veuillez saisisir le mot de passe pour la Base De Donnée :",
                "en": "Please enter the DataBase password :"
            }
        },
        "__loadDataBaseBadPassword": {
            "title": {
                "fr": "Mauvais mot de passe",
                "en": "Bad password"
            },
            "message": {
                "fr": "Vous avez entrez un mauvais mot de passe.",
                "en": "You have enter a bad password."
            }
        },
        "__loadNewDataBaseFile": {
            "db": {
                "fr": "Fichier base de données",
                "en": "Database file"
            },
            "*": {
                "fr": "Autre fichier",
                "en": "Other file"
            },
            "title": {
                "fr": "Saisissez le chemin de la nouvelle base de données",
                "en": "Enter the path of the new database"
            }
        },
        "__loadNewDataBaseAskPassword": {
            "title": {
                "fr": "Entrer votre mot de passe",
                "en": "Enter your password"
            },
            "message": {
                "fr": "Veuillez saisisir le mot de passe pour la Base De Donnée :",
                "en": "Please enter the DataBase password :"
            }
        },
        "__loadNewDataBaseErrorMessage": {
            "fr": "Le programme a rencontrer une erreur",
            "en": "The program as encounter an error"
        },
        # Ask for save Window
        "__askForSave": {
            "title": {
                "fr": "Enregistrer les modifications",
                "en": "Save modifications"
            },
            "message": {
                "fr": "Voulez-vous enregistrer les modifications de la Base De Données ?",
                "en": "Do you want to save the DataBase modifications ?"
            }
        },
        # Save confirmation Window
        "__rootButtonSaveDataBase": {
            "title": {
                "fr": "Base De Données sauvegarder",
                "en": "DataBase saved"
            },
            "message": {
                "fr": "La Base De Données a été sauvegarder.",
                "en": "The DataBase has been saved."
            }
        },
        # Change DataBase password Window
        "__rootButtonChangePasswordOldPassword": {
            "title": {
                "fr": "Entrez votre ancien mot de passe",
                "en": "Enter your old password"
            },
            "message": {
                "fr": "Veuillez entrez votre ancien mot de passe :",
                "en": "Please enter your old password :"
            }
        },
        "__rootButtonChangePasswordNewPassword": {
            "title": {
                "fr": "Entrez votre nouveau mot de passe",
                "en": "Enter your new password"
            },
            "message": {
                "fr": "Veuillez entrez votre nouveau mot de passe :",
                "en": "Please enter your new password :"
            }
        },
        "__rootButtonChangePasswordBadPassword": {
            "title": {
                "fr": "Mauvais mot de passe",
                "en": "Bad password"
            },
            "message": {
                "fr": "L'ancien mot de passe que vous avez entrez n'est pas correct.",
                "en": "The old password you entered is not correct."
            }
        }
    }
    if option2 is None:
        return __translation[option1][__language]
    return __translation[option1][option2][__language]

def __reloadTranslations():
    # Root Window
    __root.title(__translations("__root.title"))
    # Top menu File button
    __stringVars["__rootTopMenubuttonFileVar"].set(__translations("__rootTopMenubuttonFileVar"))
    __rootTopMenuFile.delete(0, "end")
    if len(__lastActions) == 0:
        __rootTopMenuFile.add_command(label=__translations("__rootTopMenuFile", "cancel"), command=__cancelLastAction, state=DISABLED)
    else:
        __rootTopMenuFile.add_command(label=__translations("__rootTopMenuFile", "cancel"), command=__cancelLastAction)
    __rootTopMenuFile.add_separator()
    __rootTopMenuFile.add_command(label=__translations("__rootTopMenuFile", "save"), command=__rootButtonSaveDataBase)
    __rootTopMenuFile.add_command(label=__translations("__rootTopMenuFile", "load"), command=__rootButtonLoadDataBase)
    __rootTopMenuFile.add_command(label=__translations("__rootTopMenuFile", "quit"), command=__askForSave)
    __rootTopMenubuttonFile.configure(menu=__rootTopMenuFile)
    # Top menu Edit button
    __stringVars["__rootTopMenubuttonEditVar"].set(__translations("__rootTopMenubuttonEditVar"))
    __rootTopMenuEdit.delete(0, "end")
    __rootTopMenuEdit.add_command(label=__translations("__rootTopMenuEdit", "changepassword"), command=__rootButtonChangePassword)
    __rootTopMenuEdit.add_checkbutton(label=__translations("__rootTopMenuEdit", "showpassword"), command=__updateListAccounts, onvalue=True, offvalue=False, variable=__showPassword)
    __rootTopMenuEdit.add_checkbutton(label=__translations("__rootTopMenuEdit", "activatetopmost"), command=lambda : __root.attributes('-topmost', __activateTopMost.get()), onvalue=True, offvalue=False, variable=__activateTopMost)
    __rootTopMenubuttonEdit.configure(menu=__rootTopMenuEdit)
    # Top menu Account button
    __stringVars["__rootTopMenubuttonAccountVar"].set(__translations("__rootTopMenubuttonAccountVar"))
    __rootTopMenuAccount.delete(0, "end")
    __rootTopMenuAccount.add_command(label=__translations("__rootTopMenuAccount", "add"), command=__rootButtonAddAccount)
    __rootTopMenuAccount.add_command(label=__translations("__rootTopMenuAccount", "modify"), command=__rootButtonModifyAccount)
    __rootTopMenuAccount.add_command(label=__translations("__rootTopMenuAccount", "remove"), command=__rootButtonRemoveAccount)
    __rootTopMenubuttonAccount.configure(menu=__rootTopMenuAccount)
    # Top menu Language button
    __stringVars["__rootTopMenubuttonLanguageVar"].set(__translations("__rootTopMenubuttonLanguageVar"))
    # Add account
    __buttonAccountRootAdd.title(__translations("__buttonAccountRootAdd.title"))
    __stringVars["__buttonAccountRootAddTitleVar"].set(__translations("__buttonAccountRootAddTitleVar"))
    __stringVars["__buttonAccountRootAddUserVar"].set(__translations("__buttonAccountRootAddUserVar"))
    __stringVars["__buttonAccountRootAddPasswordVar"].set(__translations("__buttonAccountRootAddPasswordVar"))
    __stringVars["__buttonAccountRootAddUrlVar"].set(__translations("__buttonAccountRootAddUrlVar"))
    __stringVars["__buttonAccountRootAddNoteVar"].set(__translations("__buttonAccountRootAddNoteVar"))
    __stringVars["__buttonAccountRootAddButtonVar"].set(__translations("__buttonAccountRootAddButtonVar"))
    # Modify account
    __buttonAccountRootModify.title(__translations("__buttonAccountRootModify.title"))
    __stringVars["__buttonAccountRootModifyIdVar"].set(__translations("__buttonAccountRootModifyIdVar"))
    __stringVars["__buttonAccountRootModifyTitleVar"].set(__translations("__buttonAccountRootModifyTitleVar"))
    __stringVars["__buttonAccountRootModifyUserVar"].set(__translations("__buttonAccountRootModifyUserVar"))
    __stringVars["__buttonAccountRootModifyPasswordVar"].set(__translations("__buttonAccountRootModifyPasswordVar"))
    __stringVars["__buttonAccountRootModifyUrlVar"].set(__translations("__buttonAccountRootModifyUrlVar"))
    __stringVars["__buttonAccountRootModifyNoteVar"].set(__translations("__buttonAccountRootModifyNoteVar"))
    __stringVars["__buttonAccountRootModifyButtonVar"].set(__translations("__buttonAccountRootModifyButtonVar"))
    # Remove account
    __buttonAccountRootRemove.title(__translations("__buttonAccountRootRemove.title"))
    __stringVars["__buttonAccountRootRemoveIdVar"].set(__translations("__buttonAccountRootRemoveIdVar"))
    __stringVars["__buttonAccountRootRemoveButtonVar"].set(__translations("__buttonAccountRootRemoveButtonVar"))
    # Choice DB window
    __menuChoiceDBRoot.title(__translations("__menuChoiceDBRoot.title"))
    __stringVars["__menuChoiceDBLabel1Var"].set(__translations("__menuChoiceDBLabel1Var"))
    __stringVars["__menuChoiceDBBouton1Var"].set(__translations("__menuChoiceDBBouton1Var"))
    __stringVars["__menuChoiceDBBouton2Var"].set(__translations("__menuChoiceDBBouton2Var"))

def __loadStringVars():
    # Root page
    __stringVars["__rootTopMenubuttonFileVar"] = StringVar()
    __stringVars["__rootTopMenubuttonEditVar"] = StringVar()
    __stringVars["__rootTopMenubuttonAccountVar"] = StringVar()
    __stringVars["__rootTopMenubuttonLanguageVar"] = StringVar()
    # Add account page
    __stringVars["__buttonAccountRootAddTitleVar"] = StringVar()
    __stringVars["__buttonAccountRootAddUserVar"] = StringVar()
    __stringVars["__buttonAccountRootAddPasswordVar"] = StringVar()
    __stringVars["__buttonAccountRootAddUrlVar"] = StringVar()
    __stringVars["__buttonAccountRootAddNoteVar"] = StringVar()
    __stringVars["__buttonAccountRootAddButtonVar"] = StringVar()
    # Modify account page
    __stringVars["__buttonAccountRootModifyIdVar"] = StringVar()
    __stringVars["__buttonAccountRootModifyTitleVar"] = StringVar()
    __stringVars["__buttonAccountRootModifyUserVar"] = StringVar()
    __stringVars["__buttonAccountRootModifyPasswordVar"] = StringVar()
    __stringVars["__buttonAccountRootModifyUrlVar"] = StringVar()
    __stringVars["__buttonAccountRootModifyNoteVar"] = StringVar()
    __stringVars["__buttonAccountRootModifyButtonVar"] = StringVar()
    __stringVars["__buttonAccountRootModifyButtonVar"]= StringVar()
    # Remove account page
    __stringVars["__buttonAccountRootRemoveIdVar"] = StringVar()
    __stringVars["__buttonAccountRootRemoveButtonVar"] = StringVar()
    # Choice DB page
    __stringVars["__menuChoiceDBLabel1Var"] = StringVar()
    __stringVars["__menuChoiceDBBouton1Var"] = StringVar()
    __stringVars["__menuChoiceDBBouton2Var"] = StringVar()
    # Update List
    __stringVars["__updateListId"] = StringVar()
    __stringVars["__updateListTitle"] = StringVar()
    __stringVars["__updateListUser"] = StringVar()
    __stringVars["__updateListPassword"] = StringVar()
    __stringVars["__updateListUrl"] = StringVar()
    __stringVars["__updateListNote"] = StringVar()

def __ressource_path(__relative_path):
    __base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(__base_path, __relative_path)

__root = Tk()
__ICON = "PySecPassIcon.ico"
__ICON_PNG = "PySecPassIcon.png"
__FONT = "Arial"
__FONT_SIZE = 16
__FONT_STYLE = "bold"
__LANGUAGES_AVAILABLE = ["fr", "en"]
__DEFAULT_LANGUAGE = "en"
__VERSION = "1.1.3.6"
__LAST_DATABASE: str = __config["OTHER"]["database_path"]
__lastModifiedTime = 0
__lastSavedTime = 0
__showPassword = BooleanVar()
__showPassword.set(False)
__activateTopMost = BooleanVar()
__activateTopMost.set(False)
__languageCheckMarks = [BooleanVar() for _ in range(len(__LANGUAGES_AVAILABLE))]
__language = __getLanguage()
__languageCheckMarks[__LANGUAGES_AVAILABLE.index(__language)].set(True)
__stringVars: dict[str, StringVar] = {}
__lastActions: list[list[str, int, list, int]] = []
__lastWidth = __config["ROOT"]["width"]
__loadStringVars()
# Root Window
__root.geometry(__config["ROOT"]["geometry"])
__root.resizable(True, True)
__root.iconbitmap(__ressource_path(__ICON), __ressource_path(__ICON))
# Root page Right click menu
__rootRightClickMenu = Menu(__root, tearoff=0)
# __root.iconphoto(True, PhotoImage(file=sys.executable))
__root.iconphoto(True, PhotoImage(file=__ressource_path(__ICON_PNG)), PhotoImage(file=__ressource_path(__ICON_PNG)))
__root.protocol("WM_DELETE_WINDOW", __askForSave)
__root.config()
# Top menu buttons:
__rootTopMenubuttons = Frame(__root, background="white", width=__config["ROOT"]["width"], height=25)
__rootTopMenubuttons.pack(padx=0, pady=0, anchor="nw")
__rootTopMenubuttons.pack_propagate(False)
# Top menu File button
__rootTopMenubuttonFile = Menubutton(__root, bg="white", textvariable=__stringVars["__rootTopMenubuttonFileVar"])
__rootTopMenubuttonFile.pack(in_=__rootTopMenubuttons, padx=5, side=LEFT)
__rootTopMenuFile = Menu(__rootTopMenubuttonFile, tearoff=0)
# Top menu Edit button
__rootTopMenubuttonEdit = Menubutton(__root, bg="white", textvariable=__stringVars["__rootTopMenubuttonEditVar"])
__rootTopMenubuttonEdit.pack(in_=__rootTopMenubuttons, padx=5, side=LEFT)
__rootTopMenuEdit = Menu(__rootTopMenubuttonEdit, tearoff=0)
# Top menu Account button
__rootTopMenubuttonAccount = Menubutton(__root, bg="white", textvariable=__stringVars["__rootTopMenubuttonAccountVar"])
__rootTopMenubuttonAccount.pack(in_=__rootTopMenubuttons, padx=5, side=LEFT)
__rootTopMenuAccount = Menu(__rootTopMenubuttonAccount, tearoff=0)
# Top menu Language button
__rootTopMenubuttonLanguage = Menubutton(__root, bg="white", textvariable=__stringVars["__rootTopMenubuttonLanguageVar"])
__rootTopMenubuttonLanguage.pack(in_=__rootTopMenubuttons, padx=5, side=LEFT)
__rootTopMenuLanguage = Menu(__rootTopMenubuttonLanguage, tearoff=0)
__rootTopMenuLanguage.add_checkbutton(label="Français", command=lambda : __rootButtonLanguage("fr"), onvalue=True, offvalue=False, variable=__languageCheckMarks[__LANGUAGES_AVAILABLE.index("fr")])
__rootTopMenuLanguage.add_checkbutton(label="English", command=lambda : __rootButtonLanguage("en"), onvalue=True, offvalue=False, variable=__languageCheckMarks[__LANGUAGES_AVAILABLE.index("en")])
__rootTopMenubuttonLanguage.configure(menu=__rootTopMenuLanguage)
# Keyboard shortcuts
__root.bind("<Control-s>", __rootButtonSaveDataBase)
__root.bind("<Control-o>", __rootButtonLoadDataBase)
__root.bind("<Alt-F4>", __askForSave)
__root.bind("<Control-a>", __rootButtonAddAccount)
__root.bind("<Control-m>", __rootButtonModifyAccount)
__root.bind("<Control-r>", __rootButtonRemoveAccount)
__root.bind("<Control-z>", __cancelLastAction)
# Other
__rootFrame = Frame(__root)
__rootFrame.pack()
#__rootLabel1 = Label(__root, text="", font=("poppins", 15), wraplength=int(__HEIGHT))
__root.withdraw()
try:
    __menuChoiceDBRoot = Toplevel(__root)
    __buttonAccountRootAdd = Toplevel(__root)
    __buttonAccountRootAdd.withdraw()
    __buttonAccountRootRemove = Toplevel(__root)
    __buttonAccountRootRemove.withdraw()
    __buttonAccountRootModify = Toplevel(__root)
    __buttonAccountRootModify.withdraw()
    __reloadTranslations()
    if __LAST_DATABASE == "":
        __menuChoiceDB(isInit=True)
    else:
        __menuChoiceDBRoot.withdraw()
        __tempPassword = askstring(title=__translations("__loadDataBaseAskPassword", "title"), prompt=__translations("__loadDataBaseAskPassword", "message"), show="*", parent=__root)
        __LAST_DATABASE: str = str(__LAST_DATABASE)
        try:
            if __tempPassword is None:
                __menuChoiceDBRoot.deiconify()
                __menuChoiceDB(isInit=True)
            else:
                __db = DataBase(__LAST_DATABASE, __tempPassword)
                __root.bind("<Configure>", __rootUpdates)
                __updateListAccounts()
                __root.deiconify()
        except PasswordError:
            showerror(title=__translations("__loadDataBaseBadPassword", "title"), message=__translations("__loadDataBaseBadPassword", "message"))
            __menuChoiceDBRoot.deiconify()
            __menuChoiceDB()
    __root.mainloop()
except FatalError as fatal:
    showerror(title=__translations("__rootFatalError", "title"), message=str(fatal))
    __quit(code=-1)
except KeyboardInterrupt:
    showerror(title=__translations("__rootFatalError", "title"), message=__translations("__rootFatalError", "message"))
    __quit(code=-1)
