import customtkinter as ctk
from tkinter import ttk, messagebox

from inventory_manager import InventoryManager
from storage import JsonStore


class AppGUI(ctk.CTk):

    def __init__(self):
        super().__init__()
        self.title("Inventory Management System")
        self.geometry("900x600")

        self.store = JsonStore("data/inventory.json")
        self.manager = InventoryManager()
        self.manager.load_from_dicts(self.store.load())

        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        self.inventory_tab = self.tabview.add("Inventory")
        self.billing_tab = self.tabview.add("Billing")

        self._build_inventory_tab()
        self._build_billing_tab()

        self.refresh_inventory_table()

    def _build_inventory_tab(self):
        form = ctk.CTkFrame(self.inventory_tab)
        form.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(form, text="Product Form", font=ctk.CTkFont(size=16, weight="bold")).pack(pady=(10, 5))

        self.name_var = ctk.StringVar()
        self.price_var = ctk.StringVar()
        self.qty_var = ctk.StringVar()
        self.selected_id = None

        ctk.CTkLabel(form, text="Name").pack(anchor="w", padx=10)
        ctk.CTkEntry(form, textvariable=self.name_var, width=250).pack(padx=10, pady=(0, 10))

        ctk.CTkLabel(form, text="Price").pack(anchor="w", padx=10)
        ctk.CTkEntry(form, textvariable=self.price_var, width=250).pack(padx=10, pady=(0, 10))

        ctk.CTkLabel(form, text="Quantity").pack(anchor="w", padx=10)
        ctk.CTkEntry(form, textvariable=self.qty_var, width=250).pack(padx=10, pady=(0, 10))

        btn_row = ctk.CTkFrame(form, fg_color="transparent")
        btn_row.pack(pady=5)

        ctk.CTkButton(btn_row, text="Add", command=self.on_add).grid(row=0, column=0, padx=5)
        ctk.CTkButton(btn_row, text="Update", command=self.on_update).grid(row=0, column=1, padx=5)
        ctk.CTkButton(btn_row, text="Delete", command=self.on_delete).grid(row=0, column=2, padx=5)

        ctk.CTkButton(form, text="Clear Form", command=self.clear_form).pack(pady=(10, 5))
        ctk.CTkButton(form, text="Save to File", command=self.save_inventory).pack(pady=(5, 10))

        self.report_label = ctk.CTkLabel(form, text="", justify="left")
        self.report_label.pack(padx=10, pady=(10, 10), anchor="w")

        right = ctk.CTkFrame(self.inventory_tab)
        right.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        top_controls = ctk.CTkFrame(right, fg_color="transparent")
        top_controls.pack(fill="x", pady=(5, 5))

        self.search_var = ctk.StringVar()
        ctk.CTkEntry(top_controls, textvariable=self.search_var, placeholder_text="Search name...").pack(side="left", padx=(0, 10))
        ctk.CTkButton(top_controls, text="Search", command=self.on_search).pack(side="left")

        self.sort_var = ctk.StringVar(value="name")
        ctk.CTkOptionMenu(top_controls, values=["name", "price", "qty"], variable=self.sort_var).pack(side="left", padx=10)
        ctk.CTkButton(top_controls, text="Sort", command=self.on_sort).pack(side="left")

        self.tree = ttk.Treeview(right, columns=("id", "name", "price", "qty"), show="headings")
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Name")
        self.tree.heading("price", text="Price")
        self.tree.heading("qty", text="Qty")

        self.tree.column("id", width=60, anchor="center")
        self.tree.column("name", width=250)
        self.tree.column("price", width=100, anchor="e")
        self.tree.column("qty", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select_product)

    def _build_billing_tab(self):
        ctk.CTkLabel(
            self.billing_tab,
            text="Billing screen comes next.",
            justify="left"
        ).pack(padx=20, pady=20, anchor="w")

    def refresh_inventory_table(self, rows=None):
        for item in self.tree.get_children():
            self.tree.delete(item)

        products = rows if rows is not None else self.manager.products
        for p in products:
            self.tree.insert("", "end", values=(p.id, p.name, f"{p.price:.2f}", p.qty))

        total_value = self.manager.total_inventory_value()
        low_count = len(self.manager.low_stock(threshold=5))
        self.report_label.configure(
            text=f"Report:\n- Total inventory value: {total_value:.2f}\n- Low stock (<=5): {low_count}"
        )

    def clear_form(self):
        self.selected_id = None
        self.name_var.set("")
        self.price_var.set("")
        self.qty_var.set("")

    def _read_form(self):
        name = self.name_var.get()
        try:
            price = float(self.price_var.get())
            qty = int(self.qty_var.get())
        except ValueError:
            raise ValueError("Price must be a number and Quantity must be an integer.")
        return name, price, qty

    def on_add(self):
        try:
            name, price, qty = self._read_form()
            self.manager.add_product(name, price, qty)
            self.refresh_inventory_table()
            self.clear_form()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_update(self):
        if self.selected_id is None:
            messagebox.showwarning("Select", "Select a product from the table first.")
            return
        try:
            name, price, qty = self._read_form()
            ok = self.manager.update_product(self.selected_id, name, price, qty)
            if not ok:
                messagebox.showerror("Error", "Product not found.")
            self.refresh_inventory_table()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def on_delete(self):
        if self.selected_id is None:
            messagebox.showwarning("Select", "Select a product from the table first.")
            return
        if not messagebox.askyesno("Confirm", "Delete selected product?"):
            return
        ok = self.manager.delete_product(self.selected_id)
        if not ok:
            messagebox.showerror("Error", "Product not found.")
        self.refresh_inventory_table()
        self.clear_form()

    def on_search(self):
        results = self.manager.search_by_name(self.search_var.get())
        self.refresh_inventory_table(results)

    def on_sort(self):
        results = self.manager.sort_products(self.sort_var.get())
        self.refresh_inventory_table(results)

    def on_select_product(self, _event):
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.selected_id = int(values[0])
        self.name_var.set(values[1])
        self.price_var.set(values[2])
        self.qty_var.set(values[3])

    def save_inventory(self):
        self.store.save(self.manager.to_dicts())
        messagebox.showinfo("Saved", "Inventory saved to data/inventory.json")