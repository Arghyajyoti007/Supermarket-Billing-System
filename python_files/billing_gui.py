import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk, ImageEnhance
import billing_application_for_supermarket as backend
import qr_scanner

# --- COLOR PALETTE DEFINITION ---
COLOR_BG = "#121212"  # Near Black
COLOR_SURFACE = "#1E1E1E"  # Dark Grey Surface
COLOR_PRIMARY = "#254F22"  # Dark Green (Header/Branding)
COLOR_ACCENT = "#A03A13"  # Rust (Action Buttons)
COLOR_HIGHLIGHT = "#F5824A"  # Orange (Focus/Totals)
COLOR_TEXT = "#EDE4C2"  # Cream (Typography)


class StarMartTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("STAR MART | POS SYSTEM v3.0")
        self.root.state('zoomed')
        self.root.configure(bg=COLOR_BG)

        self.current_customer = None
        self.total_payable = 0.0

        self.setup_styles()
        self.apply_background()
        self.create_layout()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Professional Treeview (The Cart)
        style.configure("Treeview",
                        background=COLOR_SURFACE,
                        foreground=COLOR_TEXT,
                        fieldbackground=COLOR_SURFACE,
                        rowheight=40,
                        borderwidth=0,
                        font=("Segoe UI", 11))

        style.configure("Treeview.Heading",
                        background=COLOR_PRIMARY,
                        foreground=COLOR_TEXT,
                        font=("Segoe UI", 12, "bold"),
                        borderwidth=1)

        style.map("Treeview", background=[('selected', COLOR_ACCENT)])

    def apply_background(self):
        try:
            # Use bg3.jpg for a high-end store texture
            bg_img = Image.open("bg3.jpg")
            # Get screen dimensions
            w = self.root.winfo_screenwidth()
            h = self.root.winfo_screenheight()
            bg_img = bg_img.resize((w, h), Image.Resampling.LANCZOS)

            # Heavy darkening for professional contrast
            enhancer = ImageEnhance.Brightness(bg_img)
            bg_img = enhancer.enhance(0.15)

            self.bg_photo = ImageTk.PhotoImage(bg_img)
            tk.Label(self.root, image=self.bg_photo).place(relwidth=1, relheight=1)
        except:
            pass

    def create_layout(self):
        # 1. TOP HEADER (Branding)
        header = tk.Frame(self.root, bg=COLOR_PRIMARY, height=70)
        header.pack(fill="x", side="top")

        try:
            logo = Image.open("logo.png").resize((50, 50), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(logo)
            tk.Label(header, image=self.logo_img, bg=COLOR_PRIMARY).pack(side="left", padx=20)
        except:
            pass

        tk.Label(header, text="STAR MART | PREMIUM RETAIL TERMINAL",
                 font=("Segoe UI Light", 22), fg=COLOR_TEXT, bg=COLOR_PRIMARY).pack(side="left")

        # 2. MAIN WORKSPACE
        workspace = tk.Frame(self.root, bg="")
        workspace.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.95, relheight=0.8)

        # LEFT PANEL: Customer & Status (30% width)
        self.side_panel = tk.Frame(workspace, bg=COLOR_SURFACE, bd=1, relief="solid")
        self.side_panel.place(relx=0, rely=0, relwidth=0.28, relheight=1)

        tk.Label(self.side_panel, text="TERMINAL ACCESS", font=("Segoe UI", 14, "bold"),
                 bg=COLOR_SURFACE, fg=COLOR_HIGHLIGHT).pack(pady=(30, 10))

        tk.Label(self.side_panel, text="MOBILE NUMBER", font=("Segoe UI", 9),
                 bg=COLOR_SURFACE, fg="#888888").pack()

        self.phone_var = tk.StringVar()
        self.phone_entry = tk.Entry(self.side_panel, textvariable=self.phone_var, font=("Consolas", 20),
                                    bg="#121212", fg=COLOR_HIGHLIGHT, insertbackground="white",
                                    justify="center", bd=0)
        self.phone_entry.pack(pady=10, padx=30, fill="x")
        self.phone_entry.bind("<Return>", lambda e: self.identify_customer())

        self.btn_auth = tk.Button(self.side_panel, text="AUTHORIZE SESSION", bg=COLOR_ACCENT, fg=COLOR_TEXT,
                                  font=("Segoe UI", 11, "bold"), bd=0, pady=12, cursor="hand2",
                                  command=self.identify_customer)
        self.btn_auth.pack(pady=10, padx=30, fill="x")

        # This slot changes based on User Status (Welcome vs Registration)
        self.dynamic_slot = tk.Frame(self.side_panel, bg=COLOR_SURFACE)
        self.dynamic_slot.pack(fill="both", expand=True, padx=20, pady=20)

        # RIGHT PANEL: The Cart (70% width)
        cart_container = tk.Frame(workspace, bg=COLOR_BG, bd=1, relief="solid")
        cart_container.place(relx=0.3, rely=0, relwidth=0.7, relheight=1)

        self.tree = ttk.Treeview(cart_container, columns=("p", "n", "pr", "q", "t"), show="headings")
        cols = {"p": "ID", "n": "ITEM DESCRIPTION", "pr": "UNIT PRICE", "q": "QTY", "t": "SUBTOTAL"}
        for c, h in cols.items():
            self.tree.heading(c, text=h)
            self.tree.column(c, anchor="center", width=100)
        self.tree.pack(fill="both", expand=True)

        # 3. FOOTER (Totals & Final Actions)
        footer = tk.Frame(self.root, bg="#000000", height=100)
        footer.pack(fill="x", side="bottom")

        # Visual indicator of connection
        tk.Label(footer, text="● SYSTEM ONLINE", fg="#00FF00", bg="#000", font=("Arial", 8)).pack(side="left", padx=20)

        self.lbl_total = tk.Label(footer, text="TOTAL: ₹ 0.00", font=("Consolas", 36, "bold"),
                                  fg=COLOR_HIGHLIGHT, bg="#000")
        self.lbl_total.pack(side="right", padx=50)

        self.btn_scan = tk.Button(footer, text="SCAN PRODUCT", bg=COLOR_PRIMARY, fg=COLOR_TEXT,
                                  font=("Segoe UI", 14, "bold"), state="disabled", width=18, bd=0,
                                  command=self.handle_scan)
        self.btn_scan.pack(side="left", padx=10, pady=20)

        self.btn_pay = tk.Button(footer, text="FINALIZE BILL", bg=COLOR_HIGHLIGHT, fg="#000",
                                 font=("Segoe UI", 14, "bold"), state="disabled", width=18, bd=0,
                                 command=self.handle_checkout)
        self.btn_pay.pack(side="left", padx=10, pady=20)

    # --- ACTION LOGIC ---

    def identify_customer(self):
        ph = self.phone_var.get().strip()
        if not ph: return

        try:
            user = backend.data_retrieve(ph)
            if user:
                self.current_customer = user
                self.set_billing_state(f"AUTHORIZED: {user[1].upper()}")
            else:
                self.show_registration_form(ph)
        except Exception as e:
            messagebox.showerror("System Error", f"Database Link Failed: {e}")

    def show_registration_form(self, ph):
        for w in self.dynamic_slot.winfo_children(): w.destroy()

        form = tk.Frame(self.dynamic_slot, bg="#252525", padx=15, pady=15, bd=1, relief="solid")
        form.pack(fill="x")

        tk.Label(form, text="NEW CUSTOMER REGISTRATION", bg="#252525", fg=COLOR_HIGHLIGHT,
                 font=("Segoe UI", 9, "bold")).pack(pady=(0, 10))

        tk.Label(form, text="Full Name", bg="#252525", fg="#AAA", font=("Segoe UI", 8)).pack(anchor="w")
        name_ent = tk.Entry(form, bg=COLOR_BG, fg="white", bd=0);
        name_ent.pack(fill="x", pady=5)

        tk.Label(form, text="Address", bg="#252525", fg="#AAA", font=("Segoe UI", 8)).pack(anchor="w")
        addr_ent = tk.Entry(form, bg=COLOR_BG, fg="white", bd=0);
        addr_ent.pack(fill="x", pady=5)

        def submit():
            if name_ent.get() and addr_ent.get():
                backend.customer_entry(name_ent.get(), addr_ent.get(), ph)
                self.current_customer = backend.data_retrieve(ph)
                self.set_billing_state(f"NEW USER: {name_ent.get().upper()}")
            else:
                messagebox.showwarning("Incomplete", "Please provide name and address.")

        tk.Button(form, text="REGISTER & OPEN CART", bg=COLOR_PRIMARY, fg=COLOR_TEXT,
                  font=("Segoe UI", 10, "bold"), bd=0, pady=8, command=submit).pack(fill="x", pady=10)

    def set_billing_state(self, message):
        for w in self.dynamic_slot.winfo_children(): w.destroy()

        # Success Badge
        badge = tk.Frame(self.dynamic_slot, bg=COLOR_PRIMARY, padx=10, pady=20)
        badge.pack(fill="x")
        tk.Label(badge, text=message, font=("Segoe UI", 11, "bold"), bg=COLOR_PRIMARY, fg=COLOR_TEXT,
                 wraplength=200).pack()

        self.btn_scan.config(state="normal")
        self.btn_pay.config(state="normal")
        self.phone_entry.config(state="disabled")
        self.btn_auth.config(state="disabled")

    def handle_scan(self):
        qr_data = qr_scanner.qr_code_scanner()
        if qr_data:
            pid = qr_data.split("\t")[0]
            p = backend.product_details_retrieve(pid)
            if p:
                qty = simpledialog.askinteger("Quantity", f"Adding {p[1]}\nEnter Quantity:", initialvalue=1, minvalue=1)
                if qty and p[3] >= qty:
                    line_total = float(p[2]) * qty
                    self.tree.insert("", "end", values=(p[0], p[1], f"₹{p[2]}", qty, f"₹{line_total:.2f}"))

                    self.total_payable += line_total
                    self.lbl_total.config(text=f"TOTAL: ₹ {self.total_payable:.2f}")

                    # Update Database
                    backend.update_stock(pid, p[3] - qty)
                    backend.bill_data_entry(self.current_customer[0], self.current_customer[1], pid, qty)
                else:
                    messagebox.showerror("Stock Error", "Insufficient stock available.")

    def handle_checkout(self):
        gst = simpledialog.askfloat("Taxation", "Enter GST %:", initialvalue=18.0)
        gst = gst if gst is not None else 0.0
        final_amt = self.total_payable + (self.total_payable * (gst / 100))

        backend.data_analysis_entry(self.current_customer[3], self.total_payable, final_amt)
        import pdf_generator
        pdf_generator.generate_bill_pdf(self.current_customer[3])

        messagebox.showinfo("POS Terminal", f"Transaction Finalized.\nFinal Payable: ₹{final_amt:.2f}")
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = StarMartTerminal(root)
    root.mainloop()
