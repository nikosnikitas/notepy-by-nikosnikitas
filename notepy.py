from tkinter import *
from tkinter import messagebox
from tkinter import filedialog as fd
from tkinter import ttk
import os
import webbrowser

#--- making the user interface using tkinter ---
#--- using the Notepy class we create an app object which runs when the program starts ---
#--- the Notepy class is an extensions of Tk class ---
class Notepy(Tk):
	def __init__(self):

		#--- the selected widget --- 
		self.selectedWidget = None

		#--- the opened file name ---
		self.filename = None

		self.checkOpenF()

		#--- the self.window ---
		self.win = Tk()

		self.win.geometry("640x480")
		self.win.resizable(True, True)
		#--- the menu self.bar ---
		self.bar = Menu(self.win)

		#--- the file menu ---
		self.fmenu = Menu(self.bar, tearoff = 0)

		self.fmenu.add_command(label="{:<16}".format("New"), accelerator="Ctrl+N",command=self.makeNew)
		self.fmenu.add_command(label="{:<16}".format("Open"), accelerator="Ctrl+O", command=self.openFile)
		self.fmenu.add_command(label="{:<16}".format("Save"), accelerator="Ctrl+S", command=self.saveFile)
		self.fmenu.add_command(label="{:<16}".format("Save as"), accelerator="Alt+S", command=self.saveAs)

		self.fmenu.add_separator()
		self.fmenu.add_command(label="{:<16}".format("Exit"), accelerator="Alt + F4", command=self.win.destroy)

		#--- the edit menu ---
		self.emenu = Menu(self.bar, tearoff = 0)

		self.emenu.add_command(label="{:<16}".format("Cut"), accelerator="Ctrl + X", command=self.cutText)
		self.emenu.add_command(label="{:<16}".format("Copy"), accelerator="Ctrl + C", command=self.copyText)
		self.emenu.add_command(label="{:<16}".format("Paste"),accelerator="Ctrl + V", command=self.pasteText)

		self.emenu.add_separator()
		self.emenu.add_command(label="{:<16}".format("Select All"),accelerator="Ctrl + A", command=self.selectAllText)

		#--- the help menu ---
		self.hmenu = Menu(self.bar, tearoff = 0)
		self.hmenu.add_command(label="{:<16}".format("Documentation"), accelerator="F11", command=self.showDoc)

		self.hmenu.add_separator()
		self.hmenu.add_command(label="{:<16}".format("Credits"), accelerator="F12", command=self.showCredits)

		self.hmenu.bind("F11", self.showDoc)
		self.hmenu.bind("F12", self.showCredits)

		#--- theme menu ---
		self.tmenu = Menu(self.bar, tearoff=0)

		#--- theme selection ---
		self.tmenu.add_command(label="{:<16}".format("Switch Light/Dark Theme"), accelerator="F6", command=self.changeTheme)

		#--- right click menu ---
		self.rclkmenu = Menu(self.win, tearoff=0)
		#--- string formatting to make the text in right context menu have a distance ---
		self.rclkmenu.add_command(label="{:<16}".format("Cut"), accelerator="Ctrl+X", command=self.cutText)
		self.rclkmenu.add_command(label="{:<16}".format("Copy"), accelerator="Ctrl+C", command=self.copyText)
		self.rclkmenu.add_command(label="{:<16}".format("Paste"), accelerator="Ctrl+V", command=self.pasteText)

		self.rclkmenu.add_separator()
		self.rclkmenu.add_command(label="{:<16} {:>32}".format("Select All","Ctrl + A"), underline=4, accelerator="Ctrl+A", command=self.selectAllText)

		self.bar.add_cascade(label="File", menu=self.fmenu)
		self.bar.add_cascade(label="Edit", menu=self.emenu)
		self.bar.add_cascade(label="Help", menu=self.hmenu)
		self.bar.add_cascade(label="Options", menu=self.tmenu)

		#--- vertical and horizontal scrollbars ---
		self.vscrollbar = Scrollbar(self.win, orient="vertical")
		self.vscrollbar.pack(side=RIGHT, fill=Y)

		self.hscrollbar = Scrollbar(self.win, orient="horizontal")
		self.hscrollbar.pack(side=BOTTOM, fill=X)

		#--- making the text ---
		self.txt = Text(self.win, bg="white", fg="black", wrap=WORD, width=640, height=480, insertbackground="black", font = ("Sans-Serif", "16"), yscrollcommand = self.vscrollbar.set, xscrollcommand = self.hscrollbar.set)
		self.txt.bind("<Button-3>", self.showRightClickMenu)
		self.txt.bind("<Control-A>", self.selectAllText)
		self.txt.pack()

		#--- configuring the scrollbars ---
		self.vscrollbar.config(command=self.txt.yview)
		self.hscrollbar.config(command=self.txt.xview)

		self.win.title("{:<16}".format("Notepy - The Python-made Notepad by nikosnikitas"))

		self.win.config(menu=self.bar)
		self.win.mainloop()
	
		#--- on right click of the mouse we show a menu to the user ---	
	def showRightClickMenu(self, event):
		
		self.rclkmenu.post(event.x_root, event.y_root)
		self.selectedWidget = event.widget

	#--- cuts text to clipboard ---
	def cutText(self, event=None):
		try:
			self.txt.selection_get()
			self.txt.event_generate("<<Cut>>")
		except:
			messagebox.showwarning("Warning","Please select the text first.")

	#--- copies the selected text to clipboard ---
	def copyText(self, event=None):
		try:
			self.txt.selection_get()
			self.txt.event_generate("<<Copy>>")
		except:
			messagebox.showwarning("Warning","Please select the text first.")

	#--- pastes text from clipboard to the editor ---
	def pasteText(self, event=None):
		self.txt.event_generate("<<Paste>>")

	#--- selects all text in the editor ---
	def selectAllText(self, event=None):
		#--- adding a tag to make a selected text ---
		self.txt.tag_add('sel', '1.0', 'end')
		return "break"


	#--- shows documentation ---
	def showDoc(self):
		docwin = Tk()
		docwin.title("Notepy Documentation")
		docwin.geometry("640x480")
		lbl = Label(docwin, text="Notepy - The Python-made Notepad")
		lbl.pack()
		details = Label(docwin, text="Made with ♥ in Python 3\n You may use this as your notepad.\nWith basic functionalities like Cut, Copy, Paste.\nYou can create and edit text files with ease.\n HOW TO USE\n File - Here you can:\n 1. NEW - open a new Notepy\n OPEN a new file\n SAVE the current file\n SAVE AS a file with a different name\n EXIT the application.\n Edit - here you can: CUT text (after selecting it)\nCOPY text (after selecting it)\n PASTE text from your clipboard.\n SELECT ALL text.\n Help - here you can:\n DOCUMENTATION - read the application's documentation and get help.\n CREDITS - Learn about the application's developer and contact him.\n Options - here you can:\n SWITCH LIGHT/DARK THEME - Change the theme from light to dark and vice versa.")
		details.pack()
		docwin.mainloop()

	#--- open a URL in the browser ---
	def openUrl(self, url2open):
		webbrowser.open_new(url2open)

	#--- shows credits ---
	def showCredits(self):
		credwin = Tk()
		credwin.title("Notepy Credits")
		credwin.geometry("420x200")

		lbl = Label(credwin, text="Notepy - The Python-made Notepad")
		lbl.pack()
		
		ghLinkLbl = Label(credwin, text="You may find the code of this project and more at my GitHub: ")
		ghLinkLbl.pack()
		
		ghLink = Label(credwin, text="nikosnikitas", fg="blue", cursor="hand2")
		ghLink.pack()
		ghLink.bind(
		"<Button-1>",
		lambda x: self.openUrl("https://github.com/nikosnikitas")
		)
		
		ldLinkLbl = Label(credwin, text="Let's connect on Linkedin")
		ldLinkLbl.pack()
		
		ldLink = Label(credwin, text="Nikos-Nikitas", fg="blue", cursor="hand2")
		ldLink.pack()
		ldLink.bind(
		"<Button-1>",
		lambda x: self.openUrl("https://www.linkedin.com/in/nikos-nikitas-g-0a81931b5")
		)
		
		credits = Label(credwin, text="Made with ♥ by Nikos-Nikitas")
		credits.pack()
		credwin.mainloop()

	#--- make a new file ---
	def makeNew(self):
		os.system("python main.py")

	#--- open a file ---
	def openFile(self):
		self.txt.delete("1.0", END)
		ft = [("Text Files", "*.txt"),("Python Files","*.py"), ("All Files","*")]
		fn = fd.Open(filetypes=ft)
		self.filename = fn
		files = fn.show()
		
		if files != "":
			contents = self.readF(files)
			self.txt.insert(END, contents)

	#--- read file ---
	def readF(self,f):
		flnm = open(f, "r")
		fcontent = flnm.read()
		self.filename = flnm
		return fcontent

	#--- save current file --- //ToDo: implement this functionality
	def saveFile(self):

		try:
			self.saveFile = open("New File.self.txt","w")
			self.saveFile.write(self.txt.get("1.0", "end"))
			self.saveFile.close()

		except:
			messagebox.shoself.winfo("Hey!","No Open File")

	#--- save as a different file ---
	def saveAs(self):
		fl = fd.askself.saveAsself.filename(defaultextension=".self.txt")
		
		if fl is None:
			return

		whatToSave = self.txt.get("1.0","end")
		
		with open(fl, "w") as sf:
			sf.write(whatToSave)
		sf.close()

	#--- checks for open file and opens one ---
	def checkOpenF(self):
		
		filecount = 0

		if self.filename == None:
			self.filename = open("New File.txt","w")
			return str(self.filename.name)
		
		if self.filename == "New File.txt":
			filecount += 1
			self.filename = open(f"New File.self.txt{filecount}","w")
			return str(self.filename.name)

	#--- get theme and change theme ---
	def changeTheme(self):
		
		if self.txt["bg"] == "white":
			self.txt.config(bg="black", fg="white", insertbackground="white")
			self.txt.update()
		else:
			self.txt.config(bg="white", fg="black", insertbackground="black")
			self.txt.update()

		if self.bar["bg"] == "white":
			self.bar.config(bg="black", fg="white")
			self.bar.update()
		else:
			self.bar.config(bg="white", fg="black")
			self.bar.update()

class NotepyGr(Tk):
	def __init__(self):

		#--- the selected widget --- 
		self.selectedWidget = None

		#--- the opened file name ---
		self.filename = None

		self.checkOpenF()

		#--- the self.window ---
		self.win = Tk()

		self.win.geometry("640x480")
		self.win.resizable(True, True)
		#--- the menu self.bar ---
		self.bar = Menu(self.win)

		#--- the file menu ---
		self.fmenu = Menu(self.bar, tearoff = 0)

		self.fmenu.add_command(label="{:<16}".format("Νέο"), accelerator="Ctrl+N",command=self.makeNew)
		self.fmenu.add_command(label="{:<16}".format("Άνοιγμα"), accelerator="Ctrl+O", command=self.openFile)
		self.fmenu.add_command(label="{:<16}".format("Αποθήκευση"), accelerator="Ctrl+S", command=self.saveFile)
		self.fmenu.add_command(label="{:<16}".format("Αποθήκευση ως"), accelerator="Alt+S", command=self.saveAs)

		self.fmenu.add_separator()
		self.fmenu.add_command(label="{:<16}".format("Έξοδος"), accelerator="Alt + F4", command=self.win.destroy)

		#--- the edit menu ---
		self.emenu = Menu(self.bar, tearoff = 0)

		self.emenu.add_command(label="{:<16}".format("Αποκοπή"), accelerator="Ctrl + X", command=self.cutText)
		self.emenu.add_command(label="{:<16}".format("Αντιγραφή"), accelerator="Ctrl + C", command=self.copyText)
		self.emenu.add_command(label="{:<16}".format("Επικόλληση"),accelerator="Ctrl + V", command=self.pasteText)

		self.emenu.add_separator()
		self.emenu.add_command(label="{:<16}".format("Επιλογή όλων"),accelerator="Ctrl + A", command=self.selectAllText)

		#--- the help menu ---
		self.hmenu = Menu(self.bar, tearoff = 0)
		self.hmenu.add_command(label="{:<16}".format("Εγχειρίδιο"), accelerator="F11", command=self.showDoc)

		self.hmenu.add_separator()
		self.hmenu.add_command(label="{:<16}".format("Ευχαριστίες"), accelerator="F12", command=self.showCredits)

		self.hmenu.bind("F11", self.showDoc)
		self.hmenu.bind("F12", self.showCredits)

		#--- theme menu ---
		self.tmenu = Menu(self.bar, tearoff=0)

		#--- theme selection ---
		self.tmenu.add_command(label="{:<16}".format("Αλλαγή Θέματος Φωτεινό/Σκοτεινό"), accelerator="F6", command=self.changeTheme)

		#--- right click menu ---
		self.rclkmenu = Menu(self.win, tearoff=0)
		#--- string formatting to make the text in right context menu have a distance ---
		self.rclkmenu.add_command(label="{:<16}".format("Αποκοπή"), accelerator="Ctrl+X", command=self.cutText)
		self.rclkmenu.add_command(label="{:<16}".format("Αντιγραφή"), accelerator="Ctrl+C", command=self.copyText)
		self.rclkmenu.add_command(label="{:<16}".format("Επικόλληση"), accelerator="Ctrl+V", command=self.pasteText)

		self.rclkmenu.add_separator()
		self.rclkmenu.add_command(label="{:<16} {:>32}".format("Επιλογή όλων","Ctrl + A"), underline=4, accelerator="Ctrl+A", command=self.selectAllText)

		self.bar.add_cascade(label="Αρχείο", menu=self.fmenu)
		self.bar.add_cascade(label="Επεξεργασία", menu=self.emenu)
		self.bar.add_cascade(label="Βοήθεια", menu=self.hmenu)
		self.bar.add_cascade(label="Ρυθμίσεις", menu=self.tmenu)

		#--- vertical and horizontal scrollbars ---
		self.vscrollbar = Scrollbar(self.win, orient="vertical")
		self.vscrollbar.pack(side=RIGHT, fill=Y)

		self.hscrollbar = Scrollbar(self.win, orient="horizontal")
		self.hscrollbar.pack(side=BOTTOM, fill=X)

		#--- making the text ---
		self.txt = Text(self.win, bg="white", fg="black", wrap=WORD, width=640, height=480, insertbackground="black", font = ("Sans-Serif", "16"), yscrollcommand = self.vscrollbar.set, xscrollcommand = self.hscrollbar.set)
		self.txt.bind("<Button-3>", self.showRightClickMenu)
		self.txt.bind("<Control-A>", self.selectAllText)
		self.txt.pack()

		#--- configuring the scrollbars ---
		self.vscrollbar.config(command=self.txt.yview)
		self.hscrollbar.config(command=self.txt.xview)

		self.win.title("{:<16}".format("Notepy - Το Σημειωματάριο σε Python από τον Νίκο-Νικήτα (GitHub: nikosnikitas)"))

		self.win.config(menu=self.bar)
		self.win.mainloop()
	
		#--- on right click of the mouse we show a menu to the user ---	
	def showRightClickMenu(self, event):
		
		self.rclkmenu.post(event.x_root, event.y_root)
		self.selectedWidget = event.widget

	#--- cuts text to clipboard ---
	def cutText(self, event=None):
		try:
			self.txt.selection_get()
			self.txt.event_generate("<<Cut>>")
		except:
			messagebox.showwarning("Ειδοποίηση","Επιλέξτε το κείμενο πρώτα.")

	#--- copies the selected text to clipboard ---
	def copyText(self, event=None):
		try:
			self.txt.selection_get()
			self.txt.event_generate("<<Copy>>")
		except:
			messagebox.showwarning("Ειδοποίηση","Επιλέξτε το κείμενο πρώτα.")

	#--- pastes text from clipboard to the editor ---
	def pasteText(self, event=None):
		self.txt.event_generate("<<Paste>>")

	#--- selects all text in the editor ---
	def selectAllText(self, event=None):
		#--- adding a tag to make a selected text ---
		self.txt.tag_add('sel', '1.0', 'end')
		return "break"


	#--- shows documentation ---
	def showDoc(self):
		docwin = Tk()
		docwin.title("Εγχειρίδιο του Notepy")
		docwin.geometry("640x480")
		lbl = Label(docwin, text="Notepy - Το Σημειωματάριο σε Python")
		lbl.pack()
		details = Label(docwin, text="""Φτιαγμένο με ♥ σε Python 3\n Μπορείτε να το χρησιμοποιήσετε ως το σημειωματάριό σας.\nΜε δυο θέματα να επιλέξετε, και βασικές επιλογές επεξεργασίας αρχείων κειμένου και Python.\nΜπορείτε εύκολα να επεξεργαστείτε και να δημιουργήσετε αρχεία.\n Αρχείο \n NEO - Ανοίγει νέο κενό σημειωματάριο.\n ΑΝΟΙΓΜΑ - Ανοίγει ένα αρχείο από τον υπολογιστή.\n ΑΠΟΘΗΚΕΥΣΗ - Αποθηκεύει το τρέχον αρχείο.\n ΑΠΟΘΗΚΕΥΣΗ ΩΣ διαφορετικό αρχείο.\n ΕΞΟΔΟΣ από το πρόγραμμα.\n Επεξεργασία\n ΑΠΟΚΟΠΗ του επιλεγμένου κειμένου.\nΑΝΤΙΓΡΑΦΗ του επιλεγμένου κειμένου.\nΕΠΙΚΟΛΛΗΣΗ κειμένου από το πρόχειρο\n ΕΠΙΛΟΓΗ ΟΛΟΥ του κειμένου\n Βοήθεια\n ΕΓΧΕΙΡΙΔΙΟ - Οδηγίες χρήσης του προγράμματος και γενικές πληροφορίες.\nΕΥΧΑΡΙΣΤΙΕΣ - Σχετικά με τον προγραμματιστή που ανέπτυξε αυτή την εφαρμογή και στοιχεία επικοινωνίας.\n Ρυθμίσεις\n ΑΛΛΑΓΗ ΘΕΜΑΤΟΣ Φωτεινό/Σκοτεινό - Αλλάζει το θέμα του προγράμματος και του κειμένου από φωτεινό σε σκοτεινό και αντίστροφα.""")
		details.pack()
		docwin.mainloop()

	#--- open a URL in the browser ---
	def openUrl(self, url2open):
		webbrowser.open_new(url2open)

	#--- shows credits ---
	def showCredits(self):
		credwin = Tk()
		credwin.title("Ευχαριστίες για το Notepy")
		credwin.geometry("360x180")

		lbl = Label(credwin, text="Notepy - Το Σημειωματάριο σε Python")
		lbl.pack()
		
		ghLinkLbl = Label(credwin, text="Βρείτε τον κώδικα αυτού του προγράμματος και πολλών άλλων στο GitHub μου: ")
		ghLinkLbl.pack()
		
		ghLink = Label(credwin, text="nikosnikitas", fg="blue", cursor="hand2")
		ghLink.pack()
		ghLink.bind(
		"<Button-1>",
		lambda x: self.openUrl("https://github.com/nikosnikitas")
		)
		
		ldLinkLbl = Label(credwin, text="Βρείτε με στο Linkedin")
		ldLinkLbl.pack()
		
		ldLink = Label(credwin, text="Nikos-Nikitas", fg="blue", cursor="hand2")
		ldLink.pack()
		ldLink.bind(
		"<Button-1>",
		lambda x: self.openUrl("https://www.linkedin.com/in/nikos-nikitas-g-0a81931b5")
		)
		
		credits = Label(credwin, text="Φτιαγμένο με ♥ από τον Νίκο-Νικήτα.")
		credits.pack()
		credwin.mainloop()

	#--- make a new file ---
	def makeNew(self):
		os.system("python main.py")

	#--- open a file ---
	def openFile(self):
		self.txt.delete("1.0", END)
		ft = [("Αρχεία Κειμένου", "*self.txt"),("Αρχεία Python","*.py"), ("Όλα τα Αρχεία","*")]
		fn = fd.Open(filetypes=ft)
		self.filename = fn
		files = fn.show()
		
		if files != "":
			contents = self.readF(files)
			self.txt.insert(END, contents)

	#--- read file ---
	def readF(self,f):
		flnm = open(f, "r")
		fcontent = flnm.read()
		self.filename = flnm
		return fcontent

	#--- save current file --- //ToDo: implement this functionality
	def saveFile(self):

		try:
			self.saveFile = open("New File.self.txt","w")
			self.saveFile.write(self.txt.get("1.0", "end"))
			self.saveFile.close()

		except:
			messagebox.shoself.winfo("Hey!","No Open File")

	#--- save as a different file ---
	def saveAs(self):
		fl = fd.askself.saveAsself.filename(defaultextension=".self.txt")
		
		if fl is None:
			return

		whatToSave = self.txt.get("1.0","end")
		
		with open(fl, "w") as sf:
			sf.write(whatToSave)
		sf.close()

	#--- checks for open file and opens one ---
	def checkOpenF(self):
		
		filecount = 0

		if self.filename == None:
			self.filename = open("New File.txt","w")
			return str(self.filename.name)
		
		if self.filename == "New File.txt":
			filecount += 1
			self.filename = open(f"New File.self.txt{filecount}","w")
			return str(self.filename.name)

	#--- get theme and change theme ---
	def changeTheme(self):
		
		if self.txt["bg"] == "white":
			self.txt.config(bg="black", fg="white", insertbackground="white")
			self.txt.update()
		else:
			self.txt.config(bg="white", fg="black", insertbackground="black")
			self.txt.update()

		if self.bar["bg"] == "white":
			self.bar.config(bg="black", fg="white")
			self.bar.update()
		else:
			self.bar.config(bg="white", fg="black")
			self.bar.update()