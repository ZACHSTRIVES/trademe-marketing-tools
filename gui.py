from collections import defaultdict
from tkinter import *
from tkinter import messagebox, filedialog
from tkinter.ttk import Progressbar, Treeview
from engine import *
import xlwt
import random
from tkinter.filedialog import asksaveasfilename

cols = ['Item', 'Qty.', 'Price', 'URL']


class gui:
    def __init__(self):
        self.root = Tk()
        self.root.title("TradeMe Marketing Tool   V0.1")
        self.root.geometry("1000x300")
        self.get_label = Label(self.root, text='Front Page Gui')
        self.url_entry = Entry(self.root, width=90)
        self.button_get = Button(self.root, text='Fetch', command=self.handle_fetch)
        self.progress = Progressbar(self.root, orient=HORIZONTAL, length=500)
        self.progress.config(mode='determinate', maximum=100, value=1)
        self.ybar = Scrollbar(self.root, orient='vertical')
        self.tree = Treeview(self.root, show='headings', columns=cols, yscrollcommand=self.ybar.set)
        self.ybar['command'] = self.tree.yview

        self.tree.heading('Item', text='Item')  # 行标题
        self.tree.column('Item', width=300, anchor='w')
        self.tree.heading('Qty.', text='Qty.')  # 行标题
        self.tree.column('Qty.', width=50, anchor='w')
        self.tree.heading('Price', text='Price')  # 行标题
        self.tree.column('Price', width=150, anchor='w')
        self.tree.heading('URL', text='URL')  # 行标题
        self.tree.column('URL', width=400, anchor='w')

        self.button_save = Button(self.root, text='Save Excel', command=self.save_excel)

        # grid
        self.url_entry.grid(row=2, column=0, sticky=W)
        self.button_get.grid(row=2, column=1, sticky=W)
        self.progress.grid(row=3, column=0)
        self.tree.grid(row=4, column=0)  # grid方案
        self.ybar.grid(row=4, column=1, sticky='ns')
        self.button_save.grid(row=3, column=1)

        self.dataset = []

        self.root.mainloop()

    def handle_fetch(self):
        print("开始执行")
        try:
            dicts = {}
            urls = get_all_page_url_of_store(self.url_entry.get())
            for url in urls:
                item_ids = get_id_of_page(url)
                for id in item_ids:
                    item_url = "https://www.trademe.co.nz/a/marketplace/listing/" + id
                    item_dict = {"url": item_url, "count": 1}
                    if id in dicts.keys():
                        dicts[id]["count"] += 1
                    else:
                        dicts[id] = item_dict
            sorted_dict = sorted(dicts.items(), key=lambda x: x[1]['count'], reverse=True)
            result = []
            count = 1

            for dic in sorted_dict:
                if count < 101:
                    count += 1
                    r_dic = dic[1]
                    t_p = get_item_title_price(r_dic['url'])
                    r_dic['title'] = t_p[0]
                    r_dic['price'] = t_p[1]
                    result.append(r_dic)
                    self.tree.insert("", "end", values=(r_dic['title'], r_dic['count'], r_dic['price'], r_dic['url']))
                    self.progress['value'] = count
                    self.root.update()
                else:
                    break

        except Exception as e:
            print(e)

    def save_excel(self):
        file_path = filedialog.asksaveasfilename(title=u'保存文件')
        wb = xlwt.Workbook()
        ws = wb.add_sheet('init')
        ws.write(0, 0, cols[0])
        ws.write(0, 1, cols[1])
        ws.write(0, 2, cols[2])
        ws.write(0, 3, cols[3])
        row = 1
        for itm in self.tree.get_children():
            ws.write(row, 0, self.tree.item(itm)['values'][0])
            ws.write(row, 1, self.tree.item(itm)['values'][1])
            ws.write(row, 2, self.tree.item(itm)['values'][2])
            ws.write(row, 3, self.tree.item(itm)['values'][3])
            row += 1
        wb.save(file_path+'.xls')
        messagebox.showinfo('Notice', 'Save Success')
