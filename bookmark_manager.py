import os
import time
from tkinter import *
from tkinter import ttk
            
root = Tk()
content = Frame(root)
content.grid(column=0, row=0, sticky=(N,W,E,S), padx=10, pady=10)
editFrame = Frame(content)
editFrame.grid(column=1, row=0, sticky=(N,E,S,W), padx=20, pady=5)
bmFrame = Frame(content)
bmFrame.grid(column=0, row=0, sticky=(N,E,W,S))

def quit(*args):
    root.destroy()

def saveFile(*args):
    global bmListTuple
    bmListTuple = tuple(sorted(bmListTuple, key=str.lower))
    with open('bookmarks.txt', 'w') as f:
        for line in bmListTuple:
            f.write(line + '\n')
    quit()

def edit(*args):
    idlb = lb.curselection()
    item = int(idlb[0])
    bmItemStr = str(bmListTuple[item])
    bmItemStr = bmItemStr.split(', ')
    nameEdit = bmItemStr[0]
    addrEdit = bmItemStr[1]
    clear()
    nameEntry.insert(10, nameEdit)
    addrEntry.insert(10, addrEdit)
    confirmLbl['text'] = "Not saved"

def clear():
    nameEntry.delete(0,END)
    addrEntry.delete(0,END)

def delete():
    global bmListTuple
    idlb = lb.curselection()
    if not len(idlb) == 0:
        item = int(idlb[0])
        bmList = list(bmListTuple)
        bmList.pop(item)
        bmListTuple = tuple(bmList)
        bmListTuple = tuple(sorted(bmListTuple, key=str.lower))
        bmListCopy.set(value=bmListTuple)
        clear()
    else:
        confirmLbl['text'] = "You didn't select anything"

def openWebsite(*args):
    import webbrowser
    idlb = lb.curselection()
    item = int(idlb[0])
    bmItemStr = str(bmListTuple[item])
    bmItemStr = bmItemStr.split(', ')
    address = bmItemStr[1]
    webbrowser.open(address)

def save(*args):
    global bmListTuple
    fname = 'bookmarks.txt'
    line = '%s, %s'
    nameText = nameEntry.get()
    addressText = addrEntry.get()
    if len(nameText)==0 or len(addressText)==0:
        confirmLbl['text'] = 'No data entered'
    else:
        bmListSet = set(bmListTuple)
        bmListSet.add(line  % (nameText, addressText))
        bmListTuple = tuple(bmListSet)
        bmListTuple = tuple(sorted(bmListTuple, key=str.lower))
        bmListCopy.set(value=bmListTuple)
        clear()
        confirmLbl['text'] = 'Saved'
    
def openSave(*args):
    fname = 'bookmarks.txt'
    f = open(fname)
    bmList = f.read()
    bmList = bmList.split('\n')
    bmList.remove('')
    bmListSet = set(bmList)
    bmListTuple = tuple(bmListSet)
    bmListTuple = tuple(sorted(bmListTuple, key=str.lower))
    return bmListTuple

bmListTuple = openSave()
bmListCopy = StringVar(value=bmListTuple)

lb = Listbox(bmFrame, listvariable=bmListCopy, activestyle='none')
scrollbar = ttk.Scrollbar(bmFrame, orient=VERTICAL, command=lb.yview)
nameEntry = ttk.Entry(editFrame)
addrEntry = ttk.Entry(editFrame)
nameLbl = ttk.Label(editFrame, text='Name: ')
addrLbl = ttk.Label(editFrame, text='Web Address: ')
confirmLbl = ttk.Label(editFrame, text='Status')
saveBtn = ttk.Button(editFrame, text='Save', command=save)
deleteBtn = ttk.Button(editFrame, text='Delete', command=delete)
openBtn = ttk.Button(editFrame, text='Open', command=openWebsite)
clearBtn = ttk.Button(editFrame, text='Clear', command=clear)

nameEntry.grid(column=1, row=0)
addrEntry.grid(column=1, row=1, pady=10)
addrLbl.grid(column=0, row=1, sticky=(E))
nameLbl.grid(column=0, row=0, sticky=(E))
confirmLbl.grid(column=1, row=4, columnspan=2)
saveBtn.grid(column=0, row=2)
deleteBtn.grid(column=0, row=3)
openBtn.grid(column=1, row=2)
clearBtn.grid(column=1, row=3, pady=10)
lb.grid(column=0, row=0, sticky=(N,E,S,W))
scrollbar.grid(column=1, row=0, sticky=(N,S))
ttk.Sizegrip().grid(column=1, row=1, sticky=(S,E))

root.grid_columnconfigure(0, weight=1)
root.grid_rowconfigure(0, weight=1)
bmFrame.grid_columnconfigure(0, weight=1, minsize=300)
bmFrame.grid_rowconfigure(0, weight=1)
content.grid_columnconfigure(0, weight=1)
content.grid_rowconfigure(0, weight=1)

lb['yscrollcommand'] = scrollbar.set

from sys import platform
if platform == "linux":
    root.configure(background='gray')
    bmFrame.configure(background='gray')
    editFrame.configure(background='gray')
    content.configure(background='gray')

lb.bind('<<ListboxSelect>>', edit)
lb.bind('<Double-1>', openWebsite)
root.bind('<Return>', save)
root.bind('q', quit)
root.protocol("WM_DELETE_WINDOW", saveFile)

root.title("Bookmark Manager")

root.mainloop()
