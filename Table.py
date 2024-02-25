import tkinter as tk
class Table:

    def __init__(self, root,columnsName, rows, columns, data):
        self.root = root
        self.columnsName =columnsName
        self.rows = rows
        self.columns = columns
        self.data = data

        # Create a frame to hold the table and scrollbar
        self.table_frame = tk.Frame(root , pady=10)
        self.table_frame.pack()

        # Create a canvas to hold the table
        self.canvas = tk.Canvas(self.table_frame)
        self.canvas.pack(side="left")

        # Create a scrollbar and associate it with the canvas
        self.scrollbar = tk.Scrollbar(self.table_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar.pack(side="right" , fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame to hold the table content
        self.table_content = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.table_content, anchor="nw")

        # Create the table
        self.create_table()

        # Configure the canvas to update the scroll region when the content changes
        self.table_content.bind("<Configure>", self.on_frame_configure)

    def create_table(self):
        
        for i in range(4):
            entry = tk.Entry(self.table_content, width=8, fg='black', font=('Arial', 16, 'bold'))
            entry.grid(row=0, column=i)
            entry.insert(tk.END, self.columnsName[i])
            entry.configure(state="readonly")
        # Code for creating table
        for i in range(self.rows):
            for j in range(self.columns):
                entry = tk.Entry(self.table_content, width=8, fg='black', font=('Arial', 16, 'bold'))
                entry.grid(row=i+1, column=j)
                entry.insert(tk.END, self.data[i][j])
                entry.configure(state="readonly")

    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
