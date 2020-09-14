from py_librus_api import Librus
from tkinter import *
from PIL import ImageTk, Image
import json

def readFromFile(name='data.json'):
    with open(name, 'r') as file:
        data = json.loads(file.read())
    return data

def writeToFile(data, name='data.json'):
    with open(name, 'w') as file:
        file.write(json.dumps(data))

def changeData(event):
    global root3, lE, pE, data
    good = True
    if lE.get()=='' and lE.get()!='!ready':
        lE.insert(0, 'Wypelnij to pole')
        good = False
    if pE.get()=='' and pE.get()!='!ready':
        pE.insert(0, 'Wypelnij to pole')
        good = False

    if good:
        if not lE.get()=='!ready':
            data['login']=lE.get()
        if not pE.get()=='!ready':
            data['password']=pE.get()
        data['first'] = True
        writeToFile(data)
        root3.destroy()

def changeSet(d):
    global root3, lE, pE, data
    data = d
    root3 = Tk(); root3.title('Zmień ustawienia'); root3.geometry("400x500")
    Label(root3, text='Podaj login').place(relx=0, rely=0.2, relwidth=0.5, relheight=0.2)
    lE = Entry(root3, justify='center'); lE.place(relx=0.55, rely=0.25, relwidth=0.4, relheight=0.1)
    Label(root3, text='Podaj haslo').place(relx=0, rely=0.4, relwidth=0.5, relheight=0.2)
    pE = Entry(root3, justify='center'); pE.place(relx=0.55, rely=0.45, relwidth=0.4, relheight=0.1)
    Label(root3, text="Nacisnij ENTER, aby zatwierdzic", font=('Arial', 13, 'normal')).place(relx=0, rely=0.75, relwidth=1, relheight=0.1)
    root3.bind('<Return>', changeData); root3.mainloop()

data = readFromFile()

if not data['first']:
    changeSet(data)

if not data['first'] or (data['login'] or data['password'])=='':
    sys.exit()

multi = False
newAvg,error,bAG,bAG2,avgLabel,label2,bLibrus,equalC,numberC=None,None,None,None,None,None,None,None,None

def getActGrade(grade):
    if len(grade)<=1:
        return int(grade)
    elif grade[1]=="+":
        return int(grade[0])+0.5
    elif grade[1]=='-':
        return int(grade[0])-0.25

def getFromLibrus(choice, grades):
    equal = 0; number = 0
    for gr in grades[choice]:
        try:
            if getActGrade(gr['Grade'])>0:
                number += int(gr['Weight'])
                equal += getActGrade(gr['Grade'])*int(gr['Weight'])
        except:
            pass
    return equal, number

def multiTrue():
    global multi, bAG
    multi = True
    if bAG:
        bAG.place_forget()
    addGrade()

def check(event):
    global e1, e2, root2, equal, number, bAG, newAvg, multi, bAG2, equalC, numberC, choice, data
    good = True; g, w = e1.get(), e2.get()
    if len(g)==1 or len(g)==3:
        try:
            grade = float(g)
            if grade < 1 or grade > 6:
                good = False; e1.delete(0, 'end'); e1.insert(0, 'Zla wartosc oceny')
        except ValueError:
            good = False; e1.delete(0, 'end'); e1.insert(0, 'Ocena nie moze byc litera')
    else:
        good = False; e1.delete(0, 'end'); e1.insert(0, 'Nieprawidlowa ocena')

    try:
        weight = int(w)
        if weight < 1 and weight > 3:
            good = False; e2.delete(0, 'end'); e2.insert(0, 'Zla wartosc wagi')
    except ValueError:
        good = False; e2.delete(0, 'end'); e2.insert(0, 'Waga musi byc calkowita')
    if good:
        if not multi:
            equalC = equal; numberC = number
        equalC += grade*weight; numberC += weight;
        newText = 'Nowa srednia twoich ocen to: %.2f' % round(equalC/numberC, 2); root2.destroy()
        if not newAvg:
            newAvg = Label(root, text=newText, font=('Arial', 13, 'bold'),bg='white')
        else:
            newAvg.config(text=newText)
        newAvg.place(relx=0.3, rely=0.4, relwidth=0.4, relheight=0.1)
        if not multi:
            if bAG:
                bAG.place_forget()
            bAG.config(text='Zmien ocene'); bAG.place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.1)
        if not bAG2:
            bAG2 = Button(root, text='Doddaj kolejna ocene', command=multiTrue, bg='#e5e5e5', bd=0)
            bAG2.bind('<Enter>', on_enter); bAG2.bind('<Leave>', on_leave)
        bAG2.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.1)

def addGrade():
    global bLibrus, bAG, label2, avgLabel, e1, e2, root2, bAG2
    if label2:
        label2.destroy()
    bLibrus.place_forget(); avgLabel.place(relx=0.3, rely=0.3, relwidth=0.4, relheight=0.1)
    if not bAG2:
        bAG.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.1)
    root2 = Tk(); root2.title('Dodaj ocene'); root2.geometry("400x500")
    Label(root2, text="Podaj ocene (4+ -> 4.5)").place(relx=0, rely=0.3, relwidth=0.5, relheight=0.1)
    e1 = Entry(root2, justify='center'); e1.place(relx=0.55, rely=0.3, relwidth=0.4, relheight=0.1)
    Label(root2, text="Podaj wage (max 3)").place(relx=0, rely=0.4, relwidth=0.5, relheight=0.1)
    e2 = Entry(root2, justify='center'); e2.place(relx=0.55, rely=0.4, relwidth=0.4, relheight=0.1)
    Label(root2, text="Nacisnij ENTER, aby zatwierdzic", font=('Arial', 13, 'normal')).place(relx=0, rely=0.5, relwidth=1, relheight=0.1)
    root2.bind('<Return>', check); root2.mainloop()

def echoAvg():
    global avgLabel, bAG, error, bAG2, label2, strVar, bLibrus, newAvg, choice, equal, number, multi
    if newAvg:
        newAvg.place_forget()
    choice = strVar.get()
    if error:
        error.destroy(); error = None
    if bAG2:
        bAG2.place_forget()
    if avgLabel:
        avgLabel.destroy()
    choice = strVar.get(); equal, number = getFromLibrus(choice, grades)
    try:
        label2.destroy()
        label2 = Label(root, text='Wybrales: '+choice, font=('Arial', 13, 'normal'), bg='white')
        label2.place(relx=0.35, rely=0.3, relwidth=0.3, relheight=0.1)
        avgText = 'Aktualna srednia twoich ocen to: %.2f' % round(equal/number, 2)
        avgLabel = Label(root, text=avgText, font=('Arial', 13, 'bold'), bg='white')
        avgLabel.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)
        if not bAG:
            bAG = Button(root, text='Dodaj ocene do sredniej', command=addGrade, bg='#e5e5e5', bd=0)
        bAG.place(relx=0.4, rely=0.6, relwidth=0.2, relheight=0.1); bAG.bind('<Enter>', on_enter); bAG.bind('<Leave>', on_leave)
        bAG.config(text="Dodaj ocenę")
        multi=False; equalC = equal; numberC = number
    except ZeroDivisionError:
        error = Label(root, text='Nie znaleziono ocen', font=('Arial', 13, 'bold'), fg='red', bg='white')
        error.place(relx=0.3, rely=0.5, relwidth=0.4, relheight=0.1)
        if bAG:
            bAG.place_forget()

def getSub(event):
    global subEntry, label2, subs, error, bLibrus, bFile, bAG, newAvg, avgLabel, bAG2, strVar
    if newAvg:
        newAvg.place_forget()
    if avgLabel:
        avgLabel.destroy(); avgLabel = None
    if bAG:
        bAG.place_forget(); bAG.config(text='Dodaj ocenę')
    if bAG2:
        bAG2.place_forget()
    if label2:
        label2.destroy()
    if error:
        error.destroy()
    text = 'Wybrałeś: '+strVar.get(); label2 = Label(root, text=text, font=('Arial', 13, 'normal'),bg='white')
    label2.place(relx=0.35, rely=0.3, relwidth=0.3, relheight=0.1)
    if not bLibrus:
        bLibrus = Button(root, text='Wczytaj oceny z Librusa', command=echoAvg, bg='#e5e5e5', bd=0)
    bLibrus.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.1);bLibrus.bind('<Enter>', on_enter);bLibrus.bind('<Leave>', on_leave)

def startGetGrades():
    global label1, subEntry, root, getGrades, chngSet, strVar, subButton, grades
    label1 = Label(root, text='Podaj nazwę przedmiotu', bg='white')
    label1.place(relx=0.2, rely=0.2, relwidth=0.175, relheight=0.1)

    OPTIONS = list(grades.keys())
    strVar = StringVar(root)
    strVar.set(OPTIONS[0])
    subEntry = OptionMenu(root, strVar, *OPTIONS)
    subEntry.config(bg='#e5e5e5', bd=0)
    subEntry.place(relx=0.375, rely=0.2, relwidth=0.2, relheight=0.1)
    getGrades.place_forget()
    chngSet.place_forget()

    subButton = Button(root, text='Zatwierdź', bg='#e5e5e5', bd=0, justify='center', command=lambda:getSub(None))
    subButton.place(relx=0.6, rely=0.2, relwidth=0.2, relheight=0.1)
    subButton.bind('<Enter>', on_enter); subButton.bind('<Leave>', on_leave)
    root.bind('<Return>', getSub)

grades = None
root = Tk(); root.title('Librus bot'); root.geometry("1000x400"); librus = Librus()
librus.login(data['login'], data['password']); grades = librus.get_grades()

#right side
img = Image.open('logo0.png');img = img.resize((500, 200), Image.ANTIALIAS)
backg = ImageTk.PhotoImage(img);back1 = Label(root, image=backg)
back1.place(relx=0, rely=0, relwidth=0.5, relheight=0.5)
back1.image = backg;back2 = Label(root, image=backg)
back2.place(relx=0, rely=0.5, relwidth=0.5, relheight=0.5);back2.image = backg

#left side
img = Image.open('logo1.png');img = img.resize((500, 200), Image.ANTIALIAS)
backg = ImageTk.PhotoImage(img);back3 = Label(root, image=backg);back3.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.5)
back4 = Label(root, image=backg);back4.place(relx=0.5, rely=0.5, relwidth=0.5, relheight=0.5)
def on_enter(event):
    event.widget.config(bg='#f5f5f5')
def on_leave(event):
    event.widget.config(bg='#e5e5e5')
getGrades = Button(root, text='Policz srednia', command=startGetGrades, bg='#e5e5e5', bd=0)
getGrades.place(relx=0.4, rely=0.4, relwidth=0.2, relheight=0.1);getGrades.bind('<Enter>', on_enter); getGrades.bind('<Leave>', on_leave)
chngSet = Button(root, text='Zmien ustawienia', command=lambda:changeSet(data), bg='#e5e5e5', bd=0)
chngSet.place(relx=0.4, rely=0.5, relwidth=0.2, relheight=0.1);chngSet.bind('<Enter>', on_enter); chngSet.bind('<Leave>', on_leave)
root.mainloop()
