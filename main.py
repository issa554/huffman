import os
import tkinter as tk
from tkinter import ttk ,filedialog ,messagebox 
from huffman import HuffmanCoding
from Table import Table

def on_tab_change(event):
    tab_id = notebook.select()
    if tab_id:  # Check if a tab is selected
        index = notebook.index(tab_id)
# Create the main window

def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()
def com():
    path = filedialog.askopenfilename(title="Select a file", filetypes=[ ("All files", "*.*")] )

    if path and  path.endswith(".huf"):
        messagebox.showerror("File not Accept","This file is already Compressed") 
        return   
    if(path):
        size = os.path.getsize(path)
        if size == 0:
            messagebox.showerror("File not Accept","This file is Empty !!") 
            return  
        entry.config(state="normal")
        entry.delete(0, tk.END)
    # Set new text
        entry.insert(0, path)
        entry.config(state="disabled")
        h = HuffmanCoding()
        h.compress(path)
        columnsName = ["Char", "Code","Len", "Freq"]
        notebook.tab(1, state='normal') 
        notebook.tab(0, state='normal') 
        clear_frame(statistics)
        clear_frame(header)
        filename, file_extension = os.path.splitext(path)
        sizebefor = os.path.getsize(path)
        sizeafter = os.path.getsize(filename+".huf")
        Label = tk.Label(header , text="The Size Before Compressed : "+str(sizebefor) , font=18)
        Labe2 = tk.Label(header , text="The Size After Compressed : "+str(sizeafter) , font=18)
        result = (1-((sizeafter/sizebefor)))*100
        result_formatted = "{:.2f}".format(result)  # Two decimal places
        Labe3 = tk.Label(header , text="The Percentage Of  New File : "+str(result_formatted)+"%" , font=18)
        headerr = h.header
        headerEn = tk.Text(header, width=40, height=10, wrap=tk.WORD )
        headerEn.insert("1.0", headerr)  # Inserting the initial text
        headerEn.configure(state="disabled")
        Label.pack(pady=(10,0))
        Labe2.pack()
        Labe3.pack()
        headerEn.pack()
        data=[]
        for i in range(len(h.codes)):
            if h.codes[i]!=None:
                data.append(h.codes[i])

        t = Table(statistics,columnsName,len(data),4,data)

def decom():
    path = filedialog.askopenfilename(
       title="Select a HUF file", filetypes=[ ("HUF files", "*.huf")] 
    )
    
    if(path):
        size = os.path.getsize(path)
        if size == 0:
            messagebox.showerror("File not Accept","This file is Empty !!") 
            return  
        entry.config(state="normal")
        entry.delete(0, tk.END)
    # Set new text
        entry.insert(0, path)
        entry.config(state="disabled")
        h = HuffmanCoding()
        h.decompress(path)
        clear_frame(statistics)
        clear_frame(header)
        notebook.select()  # Deselect the currently selected tab
        notebook.tab(1, state='disabled') 
        notebook.tab(0, state='disabled') 

root = tk.Tk()
root.title("Huffman Compress & Decompress")
root.geometry("500x600")
root.configure(background="#495057")

entry = tk.Entry(root, width=60 , state="disabled")
entry.pack(side="top", pady=20)
main = tk.Frame(root, bg="#495057")
main.pack(anchor="center" , pady=20)

comBtn = tk.Button(main , text="Compresse" ,font=16, command=com , bg="#f8f9fa" )
UncomBtn = tk.Button(main , text="Decompresse" ,font=16, command=decom , bg="#f8f9fa")
comBtn.grid(column= 0, row=0 , padx=(0,50))
UncomBtn.grid(column= 1 , row=0 , padx=(50,0))

style = ttk.Style()

# Configure the style with the desired options, including font settings
style.configure("Custom.TNotebook.Tab", font=("Helvetica", 16) )
style.configure("Custom.TNotebook", tabposition="n")
style.configure("Custom.TNotebook.Tab", padding=(70, 5))

# Create the notebook with the custom style
notebook = ttk.Notebook(root, style="Custom.TNotebook" )

# Create tabs
statistics = ttk.Frame(notebook)
header = ttk.Frame(notebook)

notebook.add(statistics, text="statistics")
notebook.add(header, text="Header" )
notebook.pack(expand=True, fill="both")
notebook.tab(0, state='disabled') 
notebook.tab(1, state='disabled') 




# Bind the event handler to tab change
notebook.bind("<<NotebookTabChanged>>", on_tab_change)

# Start the Tkinter event loop



root.mainloop()