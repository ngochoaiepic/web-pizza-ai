import customtkinter as ctk
from tkinter import messagebox, ttk, filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd
from datetime import datetime
import json
import os

# Cấu hình giao diện hệ thống
ctk.set_appearance_mode("Dark")  
ctk.set_default_color_theme("blue")  

DATA_FILE = "pizza_ai_inventory.json"
USER_FILE = "pizza_users_db.json"
TRANSACTION_FILE = "pizza_transactions_db.json"
SUPPLIER_FILE = "pizza_suppliers_db.json"

SYSTEM_NAME = "Kho Cửa Hàng Pizza AI"
SYSTEM_ICON = "🤖 🍕"
ADMIN_SECRET_KEY = "AI-PIZZA-2026"

RECIPES = {
    "Pizza Hải Sản (Seafood)": {"NL001": 1, "NL002": 0.2, "NL003": 0.1}, # 1 Đế, 0.2kg Phô mai, 0.1L Sốt
    "Pizza Phô Mai (Double Cheese)": {"NL001": 1, "NL002": 0.4, "NL003": 0.05},
    "Pizza Thập Cẩm (Classic Mix)": {"NL001": 1, "NL002": 0.15, "NL003": 0.1}
}

# ==================== ĐỒNG BỘ ĐA NGÔN NGỮ ====================
LANGUAGES = {
    "vi": {
        "title": f"{SYSTEM_ICON} {SYSTEM_NAME}", "theme_dark": "Chế độ Tối", "theme_light": "Chế độ Sáng",
        "card_items_title": "📦 DANH MỤC NGUYÊN LIỆU", "card_items_val": "{} Mặt hàng",
        "card_qty_title": "📊 TỔNG LƯỢNG TỒN KHO", "card_qty_val": "{:,} Đơn vị",
        "card_value_title": "💰 TỔNG GIÁ TRỊ VỐN KHO", "card_value_val": "{:,} VNĐ",
        "form_header": "🛠️ CẬP NHẬT KHO PIZZA AI", "p_id": "Mã NL (VD: NL001)", "p_name": "Tên nguyên liệu", "p_qty": "Số lượng tồn", "p_price": "Giá vốn nhập", "p_expiry": "Hạn dùng (Ngày)",
        "p_shelf": "Vị trí kệ (VD: Tủ đông A)", "p_min": "Mức an toàn tối thiểu", "p_supplier": "Nhà cung cấp", "p_category": "Phân loại nhóm hàng",
        "btn_add": "➕ Thêm / Cập Nhật", "btn_delete": "🗑️ Xóa Nguyên Liệu", "btn_clear": "🔄 Làm Mới Ô Nhập", "btn_excel": "📊 Xuất Báo Cáo Excel", "btn_import": "📥 Nhập File Excel",
        "search_lbl": "🔍 Bộ lọc nâng cao:", "search_holder": "Tìm theo mã, tên, vị trí...", "btn_search": "Tìm Kiếm", "btn_all": "Tất Cả",
        "filter_low": "⚠️ Dưới mức an toàn", "filter_available": "✅ Đủ hàng", "filter_expired": "🚨 Hết hạn", "filter_high_val": "💎 Vốn cao (>1M)",
        "alert_title": "🚨 TRUNG TÂM CẢNH BÁO LIVE", "alert_empty": "✅ Hệ thống vận hành an toàn!", "alert_msg": "Cần nhập gấp: {}",
        "chart1_title": "XU HƯỚNG TỒN KHO THEO ĐƠN VỊ", "chart2_title": "CƠ CẤU PHÂN BỔ VỐN LƯU ĐỘNG",
        "log_header": "📜 NHẬT KÝ HỆ THỐNG THỜI GIAN THỰC (LIVE LOGS)", "log_time": "Thời gian", "log_action": "Thao tác hệ thống",
        "msg_err_num": "Số lượng, giá, hạn dùng, mức min phải là số!",
        "log_init": "Đăng nhập thành công. Tài khoản: {} ({})", "log_add": "Thêm mới mã {}", "log_up": "Cập nhật mã {}", "log_del": "Xóa mã {}", "log_import": "Nạp dữ liệu từ tệp Excel",
        "role_lbl": "Tài khoản:", "btn_estimate": "🔮 Dự báo năng lực sản xuất", "est_title": "🔮 KHẢ NĂNG SẢN XUẤT TRONG NGÀY",
        "day_unit": "ngày", "summary_title": "📊 HIỆU SUẤT KHO TRỰC TIẾP", "summary_health": "Trạng thái: An toàn", "summary_risk": "Trạng thái: Rủi ro cao",
        "col_id": "Mã NL", "col_name": "Tên Nguyên Liệu", "col_cat": "Phân Loại", "col_qty": "Số Lượng", "col_price": "Giá Nhập", "col_exp": "Hạn Dùng", "col_shelf": "Vị Trí Kệ", "col_min": "Mức Min", "col_supplier": "Nhà Cung Cấp",
        "btn_logout": "🚪 Đăng Xuất", "table_counter": "Đang hiển thị {} / {} mặt hàng",
        "login_btn": "ĐĂNG NHẬP HỆ THỐNG", "register_btn": "ĐĂNG KÝ TÀI KHOẢN", "has_account": "Đã có tài khoản? Đăng nhập", "no_account": "Chưa có tài khoản? Đăng ký ngay",
        "reg_success": "Đăng ký thành công tài khoản cấp bậc {}!", "role_select": "Chọn quyền hạn", "user_holder": "Tên tài khoản", "pass_holder": "Mật khẩu",
        "admin_key_holder": "Nhập mã bảo mật Admin xác thực", "ai_price_lbl": "💡 Giá bán đề xuất (AI): {} VNĐ",
        "btn_waste": "🗑️ Báo Cáo Hao Hụt/Hủy", "btn_auto_order": "🛒 Tự Động Đặt Hàng NCC", "log_logout": "Tài khoản {} đã đăng xuất thủ công.", "log_autologout": "Hệ thống tự động đăng xuất {} do treo máy quá lâu."
    },
    "en": {
        "title": f"{SYSTEM_ICON} {SYSTEM_NAME}", "theme_dark": "Dark Mode", "theme_light": "Light Mode",
        "card_items_title": "📦 INVENTORY CATEGORIES", "card_items_val": "{} Items",
        "card_qty_title": "📊 TOTAL STOCK QUANTITY", "card_qty_val": "{:,} Units",
        "card_value_title": "💰 TOTAL STOCK VALUE", "card_value_val": "{:,} VND",
        "form_header": "🛠️ AI PIZZA INVENTORY FORM", "p_id": "ID (e.g., NL001)", "p_name": "Ingredient Name", "p_qty": "Stock quantity", "p_price": "Cost price", "p_expiry": "Expiry (Days)",
        "p_shelf": "Shelf Location", "p_min": "Min Safe Level", "p_supplier": "Supplier Name", "p_category": "Item Category",
        "btn_add": "➕ Add / Update", "btn_delete": "🗑️ Delete Item", "btn_clear": "🔄 Clear Fields", "btn_excel": "📊 Export Excel", "btn_import": "📥 Import Excel",
        "search_lbl": "🔍 Advanced Filters:", "search_holder": "Search ID, name, shelf...", "btn_search": "Search", "btn_all": "All Items",
        "filter_low": "⚠️ Below Min", "filter_available": "✅ Healthy", "filter_expired": "🚨 Expired", "filter_high_val": "💎 High Val (>1M)",
        "alert_title": "🚨 LIVE SYSTEM ALERT CENTER", "alert_empty": "✅ All stock levels healthy!", "alert_msg": "Restock needed: {}",
        "chart1_title": "STOCK TREND BY UNITS", "chart2_title": "CAPITAL DISTRIBUTION ANALYSIS",
        "log_header": "📜 REAL-TIME SYSTEM LOGS", "log_time": "Timestamp", "log_action": "System Actions Log",
        "msg_err_num": "Qty, Price, Expiry, and Min must be numeric!",
        "log_init": "Login successful. Account: {} ({})", "log_add": "Added item {}", "log_up": "Updated item {}", "log_del": "Deleted item {}", "log_import": "Imported data from Excel file",
        "role_lbl": "Account:", "btn_estimate": "🔮 Production Output Estimator", "est_title": "🔮 MAXIMUM DAILY OUTPUT",
        "day_unit": "days", "summary_title": "📊 LIVE INVENTORY TURNOVER", "summary_health": "Status: Stable", "summary_risk": "Status: High Risk",
        "col_id": "ID", "col_name": "Ingredient Name", "col_cat": "Category", "col_qty": "Quantity", "col_price": "Price", "col_exp": "Expiry", "col_shelf": "Shelf", "col_min": "Min", "col_supplier": "Supplier",
        "btn_logout": "🚪 Logout", "table_counter": "Showing {} / {} items",
        "login_btn": "SYSTEM LOGIN", "register_btn": "CREATE NEW ACCOUNT", "has_account": "Already have an account? Login", "no_account": "Don't have an account? Register",
        "reg_success": "Successfully registered {} account!", "role_select": "Select Role", "user_holder": "Username", "pass_holder": "Password",
        "admin_key_holder": "Enter Admin Security Key", "ai_price_lbl": "💡 Suggested Price (AI): {} VND",
        "btn_waste": "🗑️ Report Wastage/Spoil", "btn_auto_order": "🛒 Auto procurement", "log_logout": "User {} logged out manually.", "log_autologout": "System auto-logged out {} due to inactivity."
    }
}

# Fallback languages if not defined (Fr, De, Ja can reuse English keys for clean execution)
for code in ["fr", "de", "ja"]:
    LANGUAGES[code] = LANGUAGES["en"]

# ==================== CỬA SỔ XÁC THỰC BẢO MẬT ====================
class AuthWindow(ctk.CTk):
    def __init__(self, on_auth_success):
        super().__init__()
        self.on_auth_success = on_auth_success
        self.current_lang = "vi"
        
        self.title(f"{SYSTEM_NAME} - ERP Gatekeeper")
        self.geometry("450x660")
        self.resizable(False, False)
        
        self.load_users_db()
        self.is_register_mode = False 
        
        self.lang_box = ctk.CTkComboBox(self, values=["Tiếng Việt", "English"], command=self.switch_language, width=120)
        self.lang_box.set("Tiếng Việt")
        self.lang_box.pack(anchor="ne", padx=15, pady=10)
        
        self.lbl_logo = ctk.CTkLabel(self, text=SYSTEM_ICON, font=ctk.CTkFont(size=55))
        self.lbl_logo.pack(pady=(10, 5))
        
        self.lbl_title = ctk.CTkLabel(self, text=SYSTEM_NAME, font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color="#f1c40f")
        self.lbl_title.pack(pady=2)
        
        self.entry_username = ctk.CTkEntry(self, width=300, height=38)
        self.entry_username.pack(pady=8)
        
        self.pass_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.pass_frame.pack(pady=8)
        
        self.entry_password = ctk.CTkEntry(self.pass_frame, show="*", width=255, height=38)
        self.entry_password.pack(side="left")
        
        self.btn_show_pass = ctk.CTkButton(self.pass_frame, text="👁️", width=40, height=38, fg_color="#34495e", hover_color="#2c3e50", command=self.toggle_password_visibility)
        self.btn_show_pass.pack(side="left", padx=(5, 0))
        
        self.role_combobox = ctk.CTkComboBox(self, values=["Admin", "Staff"], width=300, height=35, state="readonly", command=self.on_role_changed)
        self.entry_admin_key = ctk.CTkEntry(self, show="*", width=300, height=35, border_color="#e74c3c")
        
        self.btn_main_action = ctk.CTkButton(self, font=ctk.CTkFont(weight="bold"), fg_color="#2ecc71", hover_color="#27ae60", width=300, height=42, command=self.handle_auth)
        self.btn_main_action.pack(pady=20)
        
        self.btn_toggle_mode = ctk.CTkButton(self, text="", fg_color="transparent", text_color="#3498db", hover_color="#2c3e50", width=300, command=self.toggle_mode)
        self.btn_toggle_mode.pack(pady=5)
        
        self.update_ui_texts()

    def toggle_password_visibility(self):
        if self.entry_password.cget("show") == "*":
            self.entry_password.configure(show="")
            self.btn_show_pass.configure(fg_color="#1abc9c")
        else:
            self.entry_password.configure(show="*")
            self.btn_show_pass.configure(fg_color="#34495e")

    def load_users_db(self):
        if os.path.exists(USER_FILE):
            with open(USER_FILE, "r", encoding="utf-8") as f:
                self.users = json.load(f)
        else:
            self.users = {"admin": {"password": "123", "role": "Admin"}}
            self.save_users_db()

    def save_users_db(self):
        with open(USER_FILE, "w", encoding="utf-8") as f:
            json.dump(self.users, f, ensure_ascii=False, indent=4)

    def switch_language(self, choice):
        mapping = {"Tiếng Việt": "vi", "English": "en"}
        self.current_lang = mapping.get(choice, "vi")
        self.update_ui_texts()

    def update_ui_texts(self):
        lang = LANGUAGES[self.current_lang]
        self.entry_username.configure(placeholder_text=lang["user_holder"])
        self.entry_password.configure(placeholder_text=lang["pass_holder"])
        self.role_combobox.set(lang["role_select"])
        self.entry_admin_key.configure(placeholder_text=lang["admin_key_holder"])
        
        if self.is_register_mode:
            self.btn_main_action.configure(text=lang["register_btn"], fg_color="#e67e22", hover_color="#d35400")
            self.btn_toggle_mode.configure(text=lang["has_account"])
        else:
            self.btn_main_action.configure(text=lang["login_btn"], fg_color="#2ecc71", hover_color="#27ae60")
            self.btn_toggle_mode.configure(text=lang["no_account"])

    def on_role_changed(self, choice):
        if self.is_register_mode and choice == "Admin":
            self.entry_admin_key.pack(after=self.role_combobox, pady=8)
        else:
            self.entry_admin_key.pack_forget()

    def toggle_mode(self):
        self.is_register_mode = not self.is_register_mode
        self.entry_username.delete(0, 'end')
        self.entry_password.delete(0, 'end')
        self.entry_admin_key.delete(0, 'end')
        
        if self.is_register_mode:
            self.role_combobox.pack(after=self.pass_frame, pady=8)
        else:
            self.role_combobox.pack_forget()
            self.entry_admin_key.pack_forget()
            
        self.update_ui_texts()

    def handle_auth(self):
        lang = LANGUAGES[self.current_lang]
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()
        
        if not username or not password:
            messagebox.showerror("Error", "Vui lòng điền thông tin!")
            return
            
        if self.is_register_mode:
            role = self.role_combobox.get()
            if role == lang["role_select"] or not role:
                role = "Staff"
                
            if role == "Admin":
                input_key = self.entry_admin_key.get().strip()
                if input_key != ADMIN_SECRET_KEY:
                    messagebox.showerror("Access Denied", "Sai mã bảo mật xác thực cấp cao!")
                    return
                
            if username in self.users:
                messagebox.showerror("Error", "Tài khoản đã tồn tại!")
                return
                
            self.users[username] = {"password": password, "role": role}
            self.save_users_db()
            messagebox.showinfo("Success", lang["reg_success"].format(role))
            self.toggle_mode()
        else:
            if username in self.users and self.users[username]["password"] == password:
                user_role = self.users[username]["role"]
                self.destroy()
                run_main_app(username, user_role, self.current_lang)
            else:
                messagebox.showerror("Error", "Sai tài khoản hoặc mật khẩu hệ thống!")


# ==================== GIAO DIỆN CHÍNH ERP ====================
class EnterprisePizzaWarehouseApp(ctk.CTk):
    def __init__(self, username, role, init_lang):
        super().__init__()
        
        self.current_user = username
        self.current_role = role
        self.current_lang = init_lang 
        self.current_filter = "all"
        
        self.last_activity_time = datetime.now()
        self.inactivity_timeout = 600  # Treo máy 10 phút
        
        self.title(f"{SYSTEM_NAME} Enterprise ERP Platform")
        self.geometry("1580x980")
        self.state("zoomed") 
        
        self.load_data() 
        self.load_transactions()
        self.load_suppliers()
        self.setup_ui()
        self.log_message(LANGUAGES[self.current_lang]["log_init"].format(self.current_user, self.current_role), "SYSTEM")
        self.apply_role_permissions()
        self.update_ui_strings()
        
        self.bind_all("<Any-KeyPress>", self.reset_inactivity_timer)
        self.bind_all("<Any-ButtonPress>", self.reset_inactivity_timer)
        self.check_inactivity_loop()

    def reset_inactivity_timer(self, event=None):
        self.last_activity_time = datetime.now()

    def check_inactivity_loop(self):
        elapsed = (datetime.now() - self.last_activity_time).total_seconds()
        if elapsed > self.inactivity_timeout:
            self.auto_logout_trigger()
            return
        self.after(5000, self.check_inactivity_loop)

    def auto_logout_trigger(self):
        lang = LANGUAGES[self.current_lang]
        messagebox.showwarning("Security Timeout", lang["log_autologout"].format(self.current_user))
        self.destroy()
        auth_app = AuthWindow(on_auth_success=None)
        auth_app.mainloop()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.inventory = json.load(f)
            except:
                self.load_default_data()
        else:
            self.load_default_data()

    def load_default_data(self):
        self.inventory = [
            {"id": "NL001", "name": "Đế bánh Pizza (Size M)", "category": "Khô", "quantity": 45, "price": 15000, "expiry": 14, "shelf": "Kệ khô A", "min_level": 10, "supplier": "Công ty Hải Nam"},
            {"id": "NL002", "name": "Phô mai Mozzarella (kg)", "category": "Tươi lạnh", "quantity": 15, "price": 180000, "expiry": 30, "shelf": "Tủ đông B", "min_level": 5, "supplier": "Đại lý Anchor"},
            {"id": "NL003", "name": "Sốt cà chua đặc biệt (lít)", "category": "Đóng hộp", "quantity": 12, "price": 60000, "expiry": 7, "shelf": "Tủ mát A", "min_level": 4, "supplier": "Nông sản Việt"},
        ]
        self.save_data()

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.inventory, f, ensure_ascii=False, indent=4)

    def load_transactions(self):
        if os.path.exists(TRANSACTION_FILE):
            with open(TRANSACTION_FILE, "r", encoding="utf-8") as f:
                self.transactions = json.load(f)
        else:
            self.transactions = []

    def save_transactions(self):
        with open(TRANSACTION_FILE, "w", encoding="utf-8") as f:
            json.dump(self.transactions, f, ensure_ascii=False, indent=4)

    def load_suppliers(self):
        if os.path.exists(SUPPLIER_FILE):
            with open(SUPPLIER_FILE, "r", encoding="utf-8") as f:
                self.suppliers_list = json.load(f)
        else:
            self.suppliers_list = [
                {"name": "Công ty Hải Nam", "phone": "0987654321", "email": "hainam@pizza.com", "address": "TP. HCM"},
                {"name": "Đại lý Anchor", "phone": "0123456789", "email": "anchor@dairy.com", "address": "Bình Dương"},
                {"name": "Nông sản Việt", "phone": "0333444555", "email": "vietfarm@agri.vn", "address": "Đà Lạt"}
            ]
            self.save_suppliers()

    def save_suppliers(self):
        with open(SUPPLIER_FILE, "w", encoding="utf-8") as f:
            json.dump(self.suppliers_list, f, ensure_ascii=False, indent=4)

    def log_message(self, action_text, log_type="INVENTORY"):
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.log_tree.insert("", 0, values=(now_str.split(" ")[1], f"[{log_type}] {action_text}"))
        self.transactions.append({
            "timestamp": now_str,
            "user": self.current_user,
            "action": action_text,
            "type": log_type
        })
        self.save_transactions()
        self.update_ledger_table()

    def apply_role_permissions(self):
        if self.current_role == "Staff":
            self.btn_delete.configure(state="disabled", fg_color="#555555")
            self.btn_excel.configure(state="disabled", fg_color="#555555")
            self.btn_import.configure(state="disabled", fg_color="#555555")
            self.btn_auto_order.configure(state="disabled", fg_color="#555555")
            self.btn_backup.configure(state="disabled", fg_color="#555555")
            self.btn_restore.configure(state="disabled", fg_color="#555555")

    def change_language(self, choice):
        mapping = {"Tiếng Việt": "vi", "English": "en"}
        self.current_lang = mapping.get(choice, "vi")
        self.update_ui_strings()

    def update_ui_strings(self):
        lang = LANGUAGES[self.current_lang]
        self.title_label.configure(text=lang["title"])
        self.switch_theme.configure(text=lang["theme_dark"] if self.switch_theme.get()==1 else lang["theme_light"])
        self.form_header.configure(text=lang["form_header"])
        self.lbl_user_info.configure(text=f"{lang['role_lbl']} {self.current_user} ({self.current_role})")
        
        self.entry_id.configure(placeholder_text=lang["p_id"])
        self.entry_name.configure(placeholder_text=lang["p_name"])
        self.entry_qty.configure(placeholder_text=lang["p_qty"])
        self.entry_price.configure(placeholder_text=lang["p_price"])
        self.entry_expiry.configure(placeholder_text=lang["p_expiry"])
        self.entry_shelf.configure(placeholder_text=lang["p_shelf"])
        self.entry_min.configure(placeholder_text=lang["p_min"])
        self.entry_supplier.configure(placeholder_text=lang["p_supplier"])
        
        self.btn_add.configure(text=lang["btn_add"])
        self.btn_clear.configure(text=lang["btn_clear"])
        self.btn_logout.configure(text=lang["btn_logout"])
        self.btn_waste.configure(text=lang["btn_waste"])
        
        if self.current_role == "Admin":
            self.btn_delete.configure(text=lang["btn_delete"])
            self.btn_import.configure(text=lang["btn_import"])
            self.btn_excel.configure(text=lang["btn_excel"])
            self.btn_auto_order.configure(text=lang["btn_auto_order"])
        
        self.search_lbl.configure(text=lang["search_lbl"])
        self.entry_search.configure(placeholder_text=lang["search_holder"])
        self.btn_all.configure(text=lang["btn_all"])
        self.btn_filter_low.configure(text=lang["filter_low"])
        self.btn_filter_ok.configure(text=lang["filter_available"])
        self.btn_filter_exp.configure(text=lang["filter_expired"])
        self.btn_filter_high.configure(text=lang["filter_high_val"])
        
        self.lbl_alert_title.configure(text=lang["alert_title"])
        self.log_panel_header.configure(text=lang["log_header"])
        self.lbl_summary_title.configure(text=lang["summary_title"])
        
        columns_keys = ["col_id", "col_name", "col_cat", "col_qty", "col_price", "col_exp", "col_shelf", "col_min", "col_supplier"]
        for i, key in enumerate(columns_keys):
            self.tree.heading(f"col{i+1}", text=lang[key])
            
        self.update_table()

    def logout(self):
        self.destroy()
        auth_app = AuthWindow(on_auth_success=None)
        auth_app.mainloop()

    def setup_ui(self):
        lang = LANGUAGES[self.current_lang]
        
        top_bar = ctk.CTkFrame(self, height=65, corner_radius=0, fg_color="#1e272e")
        top_bar.pack(fill="x", side="top")
        
        self.title_label = ctk.CTkLabel(top_bar, text=lang["title"], font=ctk.CTkFont(family="Segoe UI", size=22, weight="bold"), text_color="#f1c40f")
        self.title_label.pack(side="left", padx=20, pady=15)
        
        self.lbl_user_info = ctk.CTkLabel(top_bar, text="", font=ctk.CTkFont(weight="bold"), text_color="#2ecc71")
        self.lbl_user_info.pack(side="right", padx=15)
        
        self.btn_logout = ctk.CTkButton(top_bar, text=lang["btn_logout"], width=80, height=28, fg_color="#e74c3c", hover_color="#c0392b", command=self.logout)
        self.btn_logout.pack(side="right", padx=10)
        
        self.combo_lang = ctk.CTkComboBox(top_bar, values=["Tiếng Việt", "English"], command=self.change_language, width=130, state="readonly")
        self.combo_lang.pack(side="right", padx=5)
        self.combo_lang.set("Tiếng Việt")
        
        self.switch_theme = ctk.CTkSwitch(top_bar, text=lang["theme_dark"], command=self.toggle_theme, text_color="white")
        self.switch_theme.pack(side="right", padx=15)
        self.switch_theme.select()

        # KPI CARDS
        stats_frame = ctk.CTkFrame(self, fg_color="transparent")
        stats_frame.pack(fill="x", padx=15, pady=10)
        
        self.card_lbl1, self.card_val1 = self.create_kpi_card(stats_frame, "#d35400")
        self.card_lbl2, self.card_val2 = self.create_kpi_card(stats_frame, "#27ae60")
        self.card_lbl3, self.card_val3 = self.create_kpi_card(stats_frame, "#8e44ad")
        
        self.card_alert = ctk.CTkFrame(stats_frame, fg_color="#2c3e50", height=85, width=320, corner_radius=12)
        self.card_alert.pack(side="left", expand=True, padx=5)
        self.card_alert.pack_propagate(False)
        self.lbl_alert_title = ctk.CTkLabel(self.card_alert, text=lang["alert_title"], font=ctk.CTkFont(size=11, weight="bold"), text_color="#e74c3c")
        self.lbl_alert_title.pack(anchor="w", padx=15, pady=(10, 2))
        self.lbl_alert_content = ctk.CTkLabel(self.card_alert, text="", font=ctk.CTkFont(size=12), text_color="#ecf0f1", justify="left")
        self.lbl_alert_content.pack(anchor="w", padx=15)

        # MAIN TABVIEW SYSTEM FOR MULTI-MODULE
        self.tabview = ctk.CTkTabview(self, corner_radius=12)
        self.tabview.pack(fill="both", expand=True, padx=15, pady=5)
        
        self.tab_inventory = self.tabview.add("📦 Quản lý Kho")
        self.tab_recipe = self.tabview.add("🍕 Định mức & COGS")
        self.tab_suppliers = self.tabview.add("📞 Nhà Cung Cấp")
        self.tab_ledger = self.tabview.add("📜 Nhật ký Giao dịch & ABC")
        self.tab_procure = self.tabview.add("🛒 Trình tạo PO")

        self.setup_inventory_tab()
        self.setup_recipe_tab()
        self.setup_suppliers_tab()
        self.setup_ledger_tab()
        self.setup_procure_tab()

    def setup_inventory_tab(self):
        lang = LANGUAGES[self.current_lang]
        
        left_frame = ctk.CTkFrame(self.tab_inventory, width=320, corner_radius=12, fg_color="#2c3e50")
        left_frame.pack(side="left", fill="y", padx=5, pady=5)
        left_frame.pack_propagate(False)
        
        self.form_header = ctk.CTkLabel(left_frame, text=lang["form_header"], font=ctk.CTkFont(size=14, weight="bold"), text_color="#f39c12")
        self.form_header.pack(pady=8)
        
        self.entry_id = self.create_input(left_frame, lang["p_id"])
        self.entry_name = self.create_input(left_frame, lang["p_name"])
        
        self.combo_category = ctk.CTkComboBox(left_frame, values=["Khô", "Tươi lạnh", "Đóng hộp", "Bao bì", "Khác"], width=280, height=26, state="readonly")
        self.combo_category.pack(pady=2, padx=15)
        
        self.entry_qty = self.create_input(left_frame, lang["p_qty"])
        self.entry_price = self.create_input(left_frame, lang["p_price"])
        self.entry_price.bind("<KeyRelease>", self.on_price_changed)
        
        self.lbl_ai_price = ctk.CTkLabel(left_frame, text="💡 Giá bán đề xuất (AI): -- VNĐ", font=ctk.CTkFont(size=11, slant="italic"), text_color="#1abc9c")
        self.lbl_ai_price.pack(anchor="w", padx=18, pady=1)
        
        self.entry_expiry = self.create_input(left_frame, lang["p_expiry"])
        self.entry_shelf = self.create_input(left_frame, lang["p_shelf"])
        self.entry_min = self.create_input(left_frame, lang["p_min"])
        self.entry_supplier = self.create_input(left_frame, lang["p_supplier"])
        
        self.btn_add = self.create_btn(left_frame, lang["btn_add"], "#2ecc71", self.add_or_update_product)
        self.btn_delete = self.create_btn(left_frame, lang["btn_delete"], "#e74c3c", self.delete_product)
        self.btn_clear = self.create_btn(left_frame, lang["btn_clear"], "#7f8c8d", self.clear_entries)
        
        self.btn_waste = self.create_btn(left_frame, lang["btn_waste"], "#e67e22", self.report_wastage)
        self.btn_auto_order = self.create_btn(left_frame, lang["btn_auto_order"], "#9b59b6", self.trigger_auto_ordering)
        
        # New functions 7: DB Backup and Restore
        self.btn_backup = self.create_btn(left_frame, "💾 Sao Lưu Dữ Liệu", "#1abc9c", self.backup_database)
        self.btn_restore = self.create_btn(left_frame, "🔄 Khôi Phục Dữ Liệu", "#95a5a6", self.restore_database)
        
        self.btn_import = self.create_btn(left_frame, lang["btn_import"], "#f39c12", self.import_from_excel)
        self.btn_excel = self.create_btn(left_frame, lang["btn_excel"], "#2980b9", self.export_to_excel)

        self.widget_summary = ctk.CTkFrame(left_frame, fg_color="#1e272e", height=110, corner_radius=10)
        self.widget_summary.pack(fill="x", padx=15, pady=(5, 5))
        self.widget_summary.pack_propagate(False)
        
        self.lbl_summary_title = ctk.CTkLabel(self.widget_summary, text=lang["summary_title"], font=ctk.CTkFont(size=11, weight="bold"), text_color="#3498db")
        self.lbl_summary_title.pack(anchor="w", padx=12, pady=(8, 2))
        self.lbl_summary_health = ctk.CTkLabel(self.widget_summary, text="", font=ctk.CTkFont(size=11), text_color="#2ecc71")
        self.lbl_summary_health.pack(anchor="w", padx=12)
        self.lbl_summary_details = ctk.CTkLabel(self.widget_summary, text="", font=ctk.CTkFont(size=10), text_color="#bdc3c7", justify="left")
        self.lbl_summary_details.pack(anchor="w", padx=12, pady=2)

        right_frame = ctk.CTkFrame(self.tab_inventory, fg_color="transparent")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        search_frame = ctk.CTkFrame(right_frame, height=45, corner_radius=8)
        search_frame.pack(fill="x", pady=(0, 5))
        
        self.search_lbl = ctk.CTkLabel(search_frame, text=lang["search_lbl"], font=ctk.CTkFont(size=11, weight="bold"))
        self.search_lbl.pack(side="left", padx=10)
        
        self.entry_search = ctk.CTkEntry(search_frame, placeholder_text=lang["search_holder"], width=180, height=28)
        self.entry_search.pack(side="left", padx=5, pady=8)
        self.entry_search.bind("<KeyRelease>", lambda e: self.update_table())
        
        self.btn_all = ctk.CTkButton(search_frame, text=lang["btn_all"], width=60, height=28, command=lambda: self.set_filter("all"), fg_color="#34495e")
        self.btn_all.pack(side="left", padx=2)
        self.btn_filter_low = ctk.CTkButton(search_frame, text=lang["filter_low"], width=100, height=28, command=lambda: self.set_filter("low"), fg_color="#c0392b")
        self.btn_filter_low.pack(side="left", padx=2)
        self.btn_filter_ok = ctk.CTkButton(search_frame, text=lang["filter_available"], width=80, height=28, command=lambda: self.set_filter("available"), fg_color="#27ae60")
        self.btn_filter_ok.pack(side="left", padx=2)
        self.btn_filter_exp = ctk.CTkButton(search_frame, text=lang["filter_expired"], width=80, height=28, command=lambda: self.set_filter("expired"), fg_color="#d35400")
        self.btn_filter_exp.pack(side="left", padx=2)
        self.btn_filter_high = ctk.CTkButton(search_frame, text=lang["filter_high_val"], width=100, height=28, command=lambda: self.set_filter("high_val"), fg_color="#8e44ad")
        self.btn_filter_high.pack(side="left", padx=2)
        
        # Chức năng 4: Nút lọc cảnh báo sớm hạn dùng (Pre-expiry filter in 3 days)
        self.btn_filter_soon_exp = ctk.CTkButton(search_frame, text="⏳ Sắp Hết Hạn (≤3 ngày)", width=130, height=28, command=lambda: self.set_filter("soon_expired"), fg_color="#d35400")
        self.btn_filter_soon_exp.pack(side="left", padx=2)

        # Chức năng 9: Kiểm Kê Kho Thực Tế
        self.btn_audit = ctk.CTkButton(search_frame, text="🔍 Kiểm Kho", width=90, height=28, command=self.open_audit_dialog, fg_color="#2980b9")
        self.btn_audit.pack(side="right", padx=5)

        # Chức năng 10: Chuyển Kho Nội Bộ
        self.btn_transfer = ctk.CTkButton(search_frame, text="🚚 Chuyển Kho", width=95, height=28, command=self.open_transfer_dialog, fg_color="#e67e22")
        self.btn_transfer.pack(side="right", padx=5)
        
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview", rowheight=26, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#2c3e50", foreground="white")
        
        self.tree = ttk.Treeview(right_frame, columns=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8", "col9"), show="headings")
        widths = {"col1": 60, "col2": 160, "col3": 85, "col4": 65, "col5": 90, "col6": 80, "col7": 95, "col8": 65, "col9": 120}
        for col in self.tree["columns"]:
            self.tree.column(col, width=widths[col], anchor="center" if col not in ["col2", "col3", "col9"] else "w")
            
        self.tree.pack(fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_product_select)
        
        self.lbl_table_counter = ctk.CTkLabel(right_frame, text="", font=ctk.CTkFont(size=11, slant="italic"), text_color="#bdc3c7")
        self.lbl_table_counter.pack(anchor="w", padx=5, pady=2)
        
        log_panel = ctk.CTkFrame(right_frame, height=100, corner_radius=8)
        log_panel.pack(fill="x", pady=5)
        log_panel.pack_propagate(False)
        
        self.log_panel_header = ctk.CTkLabel(log_panel, text=lang["log_header"], font=ctk.CTkFont(size=11, weight="bold"), text_color="#3498db")
        self.log_panel_header.pack(anchor="w", padx=10, pady=2)
        
        self.log_tree = ttk.Treeview(log_panel, columns=("Time", "Action"), show="headings")
        self.log_tree.heading("Time", text=lang["log_time"])
        self.log_tree.heading("Action", text=lang["log_action"])
        self.log_tree.column("Time", width=90, anchor="center")
        self.log_tree.column("Action", width=750, anchor="w")
        self.log_tree.pack(fill="both", expand=True, padx=5, pady=2)

        self.charts_container = ctk.CTkFrame(right_frame, height=180, fg_color="transparent")
        self.charts_container.pack(fill="x", pady=(2, 0))
        self.chart_frame1 = ctk.CTkFrame(self.charts_container, fg_color="white", corner_radius=8)
        self.chart_frame1.pack(side="left", fill="both", expand=True, padx=(0, 2))
        self.chart_frame2 = ctk.CTkFrame(self.charts_container, fg_color="white", corner_radius=8)
        self.chart_frame2.pack(side="right", fill="both", expand=True, padx=(2, 0))

    # Chức năng 2: Định mức Pizza & COGS
    def setup_recipe_tab(self):
        self.recipe_left = ctk.CTkFrame(self.tab_recipe, width=400, fg_color="#2c3e50")
        self.recipe_left.pack(side="left", fill="y", padx=10, pady=10)
        
        ctk.CTkLabel(self.recipe_left, text="🍕 CHỌN PIZZA KIỂM TRA ĐỊNH MỨC", font=ctk.CTkFont(size=14, weight="bold"), text_color="#f1c40f").pack(pady=15)
        
        self.combo_recipe_select = ctk.CTkComboBox(self.recipe_left, values=list(RECIPES.keys()), width=280, command=self.calculate_recipe_cogs)
        self.combo_recipe_select.pack(pady=10)
        self.combo_recipe_select.set("Pizza Hải Sản (Seafood)")
        
        self.lbl_recipe_cogs = ctk.CTkLabel(self.recipe_left, text="Tổng giá vốn COGS: 0 VND", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_recipe_cogs.pack(pady=10)
        
        self.lbl_recipe_capacity = ctk.CTkLabel(self.recipe_left, text="Khả năng làm tối đa: 0 cái", font=ctk.CTkFont(size=13, weight="bold"), text_color="#2ecc71")
        self.lbl_recipe_capacity.pack(pady=5)

        # Chức năng 8: Dự báo Tiêu thụ AI giả lập (7 ngày)
        ctk.CTkButton(self.recipe_left, text="🔮 Đề Xuất Tối Ưu Tồn Kho AI (7 Ngày)", fg_color="#9b59b6", command=self.forecast_inventory_ai).pack(pady=20)
        
        self.recipe_right = ctk.CTkFrame(self.tab_recipe, fg_color="transparent")
        self.recipe_right.pack(side="right", fill="both", expand=True, padx=10, pady=10)
        
        self.recipe_tree = ttk.Treeview(self.recipe_right, columns=("ID", "Name", "Needed", "Price", "Subtotal"), show="headings")
        self.recipe_tree.heading("ID", text="Mã NL")
        self.recipe_tree.heading("Name", text="Tên Nguyên Liệu")
        self.recipe_tree.heading("Needed", text="Lượng Cần/Bánh")
        self.recipe_tree.heading("Price", text="Đơn Giá Kho")
        self.recipe_tree.heading("Subtotal", text="Thành Tiền")
        self.recipe_tree.pack(fill="both", expand=True)

    # Chức năng 3: Tab danh sách Nhà cung cấp chi tiết
    def setup_suppliers_tab(self):
        sup_frame = ctk.CTkFrame(self.tab_suppliers, fg_color="transparent")
        sup_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        sup_left = ctk.CTkFrame(sup_frame, width=320, fg_color="#2c3e50")
        sup_left.pack(side="left", fill="y", padx=5)
        
        ctk.CTkLabel(sup_left, text="👤 THÔNG TIN NHÀ CUNG CẤP", font=ctk.CTkFont(size=13, weight="bold"), text_color="#3498db").pack(pady=10)
        self.entry_sup_name = ctk.CTkEntry(sup_left, placeholder_text="Tên nhà cung cấp", width=250)
        self.entry_sup_name.pack(pady=5)
        self.entry_sup_phone = ctk.CTkEntry(sup_left, placeholder_text="Số điện thoại", width=250)
        self.entry_sup_phone.pack(pady=5)
        self.entry_sup_email = ctk.CTkEntry(sup_left, placeholder_text="Email liên hệ", width=250)
        self.entry_sup_email.pack(pady=5)
        self.entry_sup_address = ctk.CTkEntry(sup_left, placeholder_text="Địa chỉ", width=250)
        self.entry_sup_address.pack(pady=5)
        
        ctk.CTkButton(sup_left, text="💾 Lưu Nhà Cung Cấp", fg_color="#2ecc71", command=self.save_new_supplier).pack(pady=10)
        ctk.CTkButton(sup_left, text="🗑️ Xóa Đã Chọn", fg_color="#e74c3c", command=self.delete_supplier).pack(pady=5)
        
        sup_right = ctk.CTkFrame(sup_frame, fg_color="transparent")
        sup_right.pack(side="right", fill="both", expand=True, padx=5)
        
        self.sup_tree = ttk.Treeview(sup_right, columns=("Name", "Phone", "Email", "Address"), show="headings")
        self.sup_tree.heading("Name", text="Tên NCC")
        self.sup_tree.heading("Phone", text="Số điện thoại")
        self.sup_tree.heading("Email", text="Email")
        self.sup_tree.heading("Address", text="Địa chỉ")
        self.sup_tree.pack(fill="both", expand=True)
        self.sup_tree.bind("<<TreeviewSelect>>", self.on_supplier_select)
        
        self.update_suppliers_table()

    # Chức năng 4: Tab Nhật ký Giao dịch (Ledger) & Phân tích ABC
    def setup_ledger_tab(self):
        ledger_frame = ctk.CTkFrame(self.tab_ledger, fg_color="transparent")
        ledger_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        left_abc = ctk.CTkFrame(ledger_frame, width=380, fg_color="#2c3e50")
        left_abc.pack(side="left", fill="y", padx=5)
        
        # Chức năng 1: Phân Tích ABC Phân Loại Tồn Kho
        ctk.CTkLabel(left_abc, text="💎 PHÂN TÍCH PHÂN LOẠI ABC", font=ctk.CTkFont(size=14, weight="bold"), text_color="#1abc9c").pack(pady=15)
        self.lbl_abc_analysis = ctk.CTkLabel(left_abc, text="Nhóm A (Vốn cao >70%):\nNhóm B (Vốn vừa 20%):\nNhóm C (Vốn thấp 10%):", justify="left", font=ctk.CTkFont(family="Courier", size=11))
        self.lbl_abc_analysis.pack(pady=10, padx=15)
        
        ctk.CTkButton(left_abc, text="📊 Chạy Phân Tích ABC", fg_color="#16a085", command=self.run_abc_classification).pack(pady=15)
        
        right_led = ctk.CTkFrame(ledger_frame, fg_color="transparent")
        right_led.pack(side="right", fill="both", expand=True, padx=5)
        
        ctk.CTkLabel(right_led, text="📜 LỊCH SỬ GIAO DỊCH KHO CHI TIẾT", font=ctk.CTkFont(size=12, weight="bold")).pack(pady=5)
        self.ledger_tree = ttk.Treeview(right_led, columns=("Timestamp", "User", "Action", "Type"), show="headings")
        self.ledger_tree.heading("Timestamp", text="Thời gian")
        self.ledger_tree.heading("User", text="Thực hiện")
        self.ledger_tree.heading("Action", text="Nội dung hoạt động")
        self.ledger_tree.heading("Type", text="Phân loại")
        self.ledger_tree.pack(fill="both", expand=True)
        self.update_ledger_table()

    # Chức năng 5: Tab Trình tạo Đơn mua hàng (Purchase Order Builder)
    def setup_procure_tab(self):
        proc_frame = ctk.CTkFrame(self.tab_procure, fg_color="transparent")
        proc_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        left_proc = ctk.CTkFrame(proc_frame, width=420, fg_color="#2c3e50")
        left_proc.pack(side="left", fill="y", padx=5)
        
        ctk.CTkLabel(left_proc, text="🛒 THIẾT LẬP PO ĐẶT HÀNG", font=ctk.CTkFont(size=14, weight="bold"), text_color="#e67e22").pack(pady=15)
        
        self.combo_po_supplier = ctk.CTkComboBox(left_proc, values=[], width=280)
        self.combo_po_supplier.pack(pady=10)
        
        ctk.CTkButton(left_proc, text="🔄 Tải Danh Sách Nhà Cung Cấp", fg_color="#34495e", command=self.load_procure_suppliers).pack(pady=5)
        ctk.CTkButton(left_proc, text="📋 Thêm Hàng Dưới Mức Min Vào PO", fg_color="#f39c12", command=self.add_low_stock_to_po).pack(pady=10)
        ctk.CTkButton(left_proc, text="📝 Xuất Nháp PO Gửi Email", fg_color="#2ecc71", command=self.export_po_draft_text).pack(pady=15)
        
        right_proc = ctk.CTkFrame(proc_frame, fg_color="transparent")
        right_proc.pack(side="right", fill="both", expand=True, padx=5)
        
        self.po_tree = ttk.Treeview(right_proc, columns=("ID", "Name", "CurrentQty", "MinLevel", "OrderQty", "Supplier"), show="headings")
        self.po_tree.heading("ID", text="Mã NL")
        self.po_tree.heading("Name", text="Nguyên Liệu")
        self.po_tree.heading("CurrentQty", text="Hiện Có")
        self.po_tree.heading("MinLevel", text="Định Mức")
        self.po_tree.heading("OrderQty", text="Đặt Thêm")
        self.po_tree.heading("Supplier", text="Nhà Cung Cấp")
        self.po_tree.pack(fill="both", expand=True)

    # Chức năng 1: Logic ABC
    def run_abc_classification(self):
        if not self.inventory: return
        total_val = sum(p['quantity'] * p['price'] for p in self.inventory)
        if total_val == 0: return
        
        sorted_p = sorted(self.inventory, key=lambda x: x['quantity'] * x['price'], reverse=True)
        acc_val = 0
        group_a, group_b, group_c = [], [], []
        
        for p in sorted_p:
            val = p['quantity'] * p['price']
            acc_val += val
            pct = (acc_val / total_val) * 100
            
            if pct <= 70:
                group_a.append(f"{p['name']} ({val:,}đ)")
            elif pct <= 90:
                group_b.append(f"{p['name']} ({val:,}đ)")
            else:
                group_c.append(f"{p['name']} ({val:,}đ)")
                
        text = f"💎 PHÂN TÍCH VỐN ABC TRONG KHO:\n\n"
        text += f"🔴 Nhóm A (70% Vốn Cao - Cần Kiểm Soát Sát Sao):\n" + ("\n • ".join(group_a) if group_a else " Trống") + "\n\n"
        text += f"🟡 Nhóm B (20% Vốn Trung Bình):\n" + ("\n • ".join(group_b) if group_b else " Trống") + "\n\n"
        text += f"🟢 Nhóm C (10% Vốn Thấp - Nới Lỏng Thủ Tục):\n" + ("\n • ".join(group_c) if group_c else " Trống")
        
        self.lbl_abc_analysis.configure(text=text)
        self.log_message("Chạy phân tích cơ cấu ABC-XYZ cho dòng tài sản vốn tồn kho.", "ANALYSIS")

    # Chức năng 2: Logic COGS & Định mức Pizza
    def calculate_recipe_cogs(self, selection=None):
        recipe_name = self.combo_recipe_select.get()
        if recipe_name not in RECIPES: return
        
        recipe = RECIPES[recipe_name]
        total_cogs = 0
        max_capacity = 9999
        
        for item in self.recipe_tree.get_children():
            self.recipe_tree.delete(item)
            
        for p_id, qty_needed in recipe.items():
            db_item = next((p for p in self.inventory if p['id'] == p_id), None)
            if db_item:
                subtotal = db_item['price'] * qty_needed
                total_cogs += subtotal
                self.recipe_tree.insert("", "end", values=(p_id, db_item['name'], qty_needed, f"{db_item['price']:,}", f"{int(subtotal):,}"))
                
                capacity = int(db_item['quantity'] / qty_needed)
                if capacity < max_capacity:
                    max_capacity = capacity
            else:
                self.recipe_tree.insert("", "end", values=(p_id, "THIẾU TRONG KHO!", qty_needed, 0, 0))
                max_capacity = 0
                
        self.lbl_recipe_cogs.configure(text=f"Tổng chi phí giá vốn (COGS): {int(total_cogs):,} VNĐ/bánh")
        self.lbl_recipe_capacity.configure(text=f"Năng lực làm bánh hiện tại trong kho: {max_capacity} cái")

    # Chức năng 3: Quản lý Nhà cung cấp
    def save_new_supplier(self):
        name = self.entry_sup_name.get().strip()
        phone = self.entry_sup_phone.get().strip()
        email = self.entry_sup_email.get().strip()
        address = self.entry_sup_address.get().strip()
        
        if not name: return
        self.suppliers_list = [s for s in self.suppliers_list if s['name'] != name]
        self.suppliers_list.append({"name": name, "phone": phone, "email": email, "address": address})
        self.save_suppliers()
        self.update_suppliers_table()
        self.log_message(f"Đã cập nhật/thêm nhà cung cấp '{name}' vào hệ thống.", "SUPPLIER")

    def delete_supplier(self):
        selected = self.sup_tree.selection()
        if not selected: return
        name = self.sup_tree.item(selected)['values'][0]
        self.suppliers_list = [s for s in self.suppliers_list if s['name'] != name]
        self.save_suppliers()
        self.update_suppliers_table()

    def update_suppliers_table(self):
        for item in self.sup_tree.get_children():
            self.sup_tree.delete(item)
        for s in self.suppliers_list:
            self.sup_tree.insert("", "end", values=(s['name'], s['phone'], s['email'], s['address']))

    def on_supplier_select(self, event):
        selected = self.sup_tree.selection()
        if not selected: return
        v = self.sup_tree.item(selected)['values']
        self.entry_sup_name.delete(0, 'end'); self.entry_sup_name.insert(0, v[0])
        self.entry_sup_phone.delete(0, 'end'); self.entry_sup_phone.insert(0, v[1])
        self.entry_sup_email.delete(0, 'end'); self.entry_sup_email.insert(0, v[2])
        self.entry_sup_address.delete(0, 'end'); self.entry_sup_address.insert(0, v[3])

    # Chức năng 4: Lịch sử Giao dịch
    def update_ledger_table(self):
        if not hasattr(self, 'ledger_tree'): return
        for item in self.ledger_tree.get_children():
            self.ledger_tree.delete(item)
        for t in self.transactions[-50:]: # hiển thị 50 giao dịch gần nhất
            self.ledger_tree.insert("", "end", values=(t['timestamp'], t['user'], t['action'], t['type']))

    # Chức năng 5: Logic Purchase Order (PO) Builder
    def load_procure_suppliers(self):
        names = [s['name'] for s in self.suppliers_list]
        self.combo_po_supplier.configure(values=names)
        if names: self.combo_po_supplier.set(names[0])

    def add_low_stock_to_po(self):
        target_supplier = self.combo_po_supplier.get()
        if not target_supplier: return
        
        for item in self.po_tree.get_children():
            self.po_tree.delete(item)
            
        for p in self.inventory:
            min_l = p.get('min_level', 5)
            if p['quantity'] < min_l and p.get('supplier', '') == target_supplier:
                qty_to_order = min_l * 2 - p['quantity']
                self.po_tree.insert("", "end", values=(p['id'], p['name'], p['quantity'], min_l, qty_to_order, target_supplier))

    def export_po_draft_text(self):
        target_supplier = self.combo_po_supplier.get()
        if not target_supplier: return
        
        po_content = f"======= PHIẾU ĐƠN ĐẶT HÀNG NHÁP (PO DRAFT) =======\n"
        po_content += f"Ngày đặt hàng: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        po_content += f"Nhà cung cấp đối tác: {target_supplier}\n"
        po_content += f"Người lập phiếu: {self.current_user} ({self.current_role})\n"
        po_content += f"----------------------------------------------------\n"
        po_content += f"Mã NL | Tên Nguyên Liệu | Số Lượng Cần Giao\n"
        po_content += f"----------------------------------------------------\n"
        
        items_count = 0
        for item in self.po_tree.get_children():
            v = self.po_tree.item(item)['values']
            po_content += f"{v[0]} | {v[1]} | {v[4]} đơn vị\n"
            items_count += 1
            
        if items_count == 0:
            messagebox.showwarning("Dự Thảo PO", "Không có nguyên liệu nào trong bảng để lập PO!")
            return
            
        po_content += f"----------------------------------------------------\n"
        po_content += f"Vui lòng báo giá & xác nhận giao hàng sớm nhất có thể.\n"
        
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(po_content)
            messagebox.showinfo("PO Draft Exported", "Xuất file nháp PO gửi nhà cung cấp thành công!")
            self.log_message(f"Xuất nháp PO gửi NCC {target_supplier}", "PO")

    # Chức năng 7: Backup và Restore Database
    def backup_database(self):
        if self.current_role != "Admin": return
        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("Backup Files", "*.json")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.inventory, f, ensure_ascii=False, indent=4)
            messagebox.showinfo("Success", "Đã sao lưu thành công cơ sở dữ liệu kho!")
            self.log_message("Sao lưu cơ sở dữ liệu kho.", "BACKUP")

    def restore_database(self):
        if self.current_role != "Admin": return
        file_path = filedialog.askopenfilename(filetypes=[("Backup Files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    self.inventory = json.load(f)
                self.save_data()
                self.update_table()
                messagebox.showinfo("Success", "Khôi phục dữ liệu hệ thống thành công!")
                self.log_message("Khôi phục toàn bộ dữ liệu từ file backup.", "RESTORE")
            except Exception as e:
                messagebox.showerror("Error", f"Lỗi đọc file phục hồi: {str(e)}")

    # Chức năng 8: AI Demand Forecasting
    def forecast_inventory_ai(self):
        forecast_text = "🔮 ĐỀ XUẤT TỒN KHO AN TOÀN (DỰ BÁO NHU CẦU 7 NGÀY)\n\n"
        for p in self.inventory:
            # Mô hình dự báo AI giả lập dựa trên mức độ bán hàng và lượng tồn tối thiểu
            suggested_safety = int(p.get('min_level', 5) * 1.5)
            order_decision = suggested_safety - p['quantity']
            if order_decision < 0: order_decision = 0
            
            forecast_text += f"• {p['name']}:\n"
            forecast_text += f"  - Lượng tiêu thụ dự báo (7 ngày): {suggested_safety} đơn vị\n"
            forecast_text += f"  - Đề xuất bổ sung gấp: {order_decision} đơn vị\n\n"
            
        messagebox.showinfo("AI Predictive Modeling", forecast_text)
        self.log_message("Chạy mô hình AI dự báo nhu cầu hàng hóa tuần kế tiếp.", "AI_DEMAND")

    # Chức năng 9: Kiểm Kho Thực Tế
    def open_audit_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Kiểm kho", "Vui lòng chọn 1 nguyên liệu cần kiểm trong bảng!")
            return
        vals = self.tree.item(selected)['values']
        p_id = vals[0]
        p_name = vals[1]
        p_sys_qty = int(vals[3])
        
        audit_window = ctk.CTkToplevel(self)
        audit_window.title("Phiếu Kiểm Kê Kho Thực Tế")
        audit_window.geometry("350x220")
        audit_window.grab_set()
        
        ctk.CTkLabel(audit_window, text=f"Kiểm kho: {p_name}", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        ctk.CTkLabel(audit_window, text=f"Số lượng trên hệ thống: {p_sys_qty}").pack(pady=5)
        
        entry_actual = ctk.CTkEntry(audit_window, placeholder_text="Nhập lượng thực tế đếm được", width=200)
        entry_actual.pack(pady=5)
        
        def save_audit():
            try:
                actual_qty = int(entry_actual.get())
                diff = actual_qty - p_sys_qty
                for p in self.inventory:
                    if p['id'] == p_id:
                        p['quantity'] = actual_qty
                        break
                self.save_data()
                self.update_table()
                self.log_message(f"Cân đối kiểm kho mã {p_id}. Chênh lệch: {diff} đơn vị.", "STOCK_AUDIT")
                audit_window.destroy()
                messagebox.showinfo("Thành công", f"Đã cân đối lượng thực tế cho nguyên liệu {p_name}.")
            except ValueError:
                messagebox.showerror("Lỗi", "Số lượng thực tế phải là một số hợp lệ!")
                
        ctk.CTkButton(audit_window, text="Xác nhận Cân Đối Kho", fg_color="#2ecc71", command=save_audit).pack(pady=10)

    # Chức năng 10: Chuyển Kho Nội Bộ
    def open_transfer_dialog(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Chuyển kho", "Vui lòng chọn 1 nguyên liệu cần chuyển trong bảng!")
            return
        vals = self.tree.item(selected)['values']
        p_id = vals[0]
        p_qty = int(vals[3])
        
        tf_window = ctk.CTkToplevel(self)
        tf_window.title("Điều Chuyển Kho Nội Bộ")
        tf_window.geometry("380x260")
        tf_window.grab_set()
        
        ctk.CTkLabel(tf_window, text=f"Chuyển nguyên liệu: {vals[1]}", font=ctk.CTkFont(weight="bold")).pack(pady=10)
        
        combo_branch = ctk.CTkComboBox(tf_window, values=["Chi nhánh Quận 1", "Chi nhánh Quận 3", "Chi nhánh Gò Vấp"], width=220)
        combo_branch.pack(pady=5)
        combo_branch.set("Chi nhánh Quận 1")
        
        entry_tf_qty = ctk.CTkEntry(tf_window, placeholder_text="Nhập số lượng cần chuyển", width=220)
        entry_tf_qty.pack(pady=5)
        
        def process_transfer():
            try:
                tf_qty = int(entry_tf_qty.get())
                if tf_qty <= 0 or tf_qty > p_qty:
                    messagebox.showerror("Lỗi", "Số lượng chuyển đi không hợp lệ!")
                    return
                for p in self.inventory:
                    if p['id'] == p_id:
                        p['quantity'] -= tf_qty
                        break
                self.save_data()
                self.update_table()
                self.log_message(f"Xuất chuyển {tf_qty} đơn vị của mã {p_id} sang {combo_branch.get()}.", "TRANSFER")
                tf_window.destroy()
                messagebox.showinfo("Thành công", "Lập vận đơn điều phối hàng sang chi nhánh thành công!")
            except ValueError:
                messagebox.showerror("Lỗi", "Vui lòng nhập số lượng hợp lệ!")
                
        ctk.CTkButton(tf_window, text="Tạo Vận Đơn Xuất Kho", fg_color="#e67e22", command=process_transfer).pack(pady=15)

    # ==================== PHẦN XỬ LÝ CŨ ĐƯỢC GIỮ NGUYÊN ====================
    def report_wastage(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Wastage", "Vui lòng chọn một mặt hàng trong bảng để báo hủy!")
            return
        p_id = self.tree.item(selected)['values'][0]
        for p in self.inventory:
            if p['id'] == p_id:
                if p['quantity'] > 0:
                    p['quantity'] -= 1
                    self.log_message(f"🚨 HỦY HAO HỤT: Đã hủy 1 đơn vị của mã {p_id} (Hao hụt bếp).", "WASTAGE")
                    self.save_data()
                    self.update_table()
                    return
                
    def trigger_auto_ordering(self):
        if self.current_role != "Admin": return
        needed_orders = []
        for p in self.inventory:
            if p['quantity'] < p.get('min_level', 5):
                needed_orders.append(f"{p['name']} (NCC: {p.get('supplier','Chưa rõ')})")
        
        if needed_orders:
            info = "\n• ".join(needed_orders)
            messagebox.showinfo("Auto procurement", f"🛒 ĐÃ KHỞI TẠO ĐƠN ĐẶT HÀNG TỰ ĐỘNG ĐẾN NCC CHO:\n• {info}")
            self.log_message("🛒 AI Procurement: Tự động kết nối và gửi bản thảo PO đến Nhà cung cấp liên kết.", "PO")
        else:
            messagebox.showinfo("Auto procurement", "✅ Hiện tại không có mặt hàng nào dưới mức an toàn cần đặt.")

    def on_price_changed(self, event):
        try:
            val = float(self.entry_price.get().strip())
            suggested = int(val * 1.5)
            self.lbl_ai_price.configure(text=LANGUAGES[self.current_lang]["ai_price_lbl"].format(f"{suggested:,}"))
        except:
            self.lbl_ai_price.configure(text="💡 Giá bán đề xuất (AI): -- VNĐ")

    def create_kpi_card(self, parent, color):
        card = ctk.CTkFrame(parent, fg_color=color, height=85, width=220, corner_radius=12)
        card.pack(side="left", expand=True, padx=4)
        card.pack_propagate(False)
        lbl_t = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=11, weight="bold"), text_color="#ecf0f1")
        lbl_t.pack(anchor="w", padx=12, pady=(10, 2))
        lbl_v = ctk.CTkLabel(card, text="", font=ctk.CTkFont(size=18, weight="bold"), text_color="white")
        lbl_v.pack(anchor="w", padx=12)
        return lbl_t, lbl_v

    def create_input(self, parent, placeholder):
        entry = ctk.CTkEntry(parent, placeholder_text=placeholder, width=280, height=26)
        entry.pack(pady=2, padx=15)
        return entry

    def create_btn(self, parent, text, color, command):
        btn = ctk.CTkButton(parent, text=text, command=command, fg_color=color, font=ctk.CTkFont(weight="bold", size=11), height=26)
        btn.pack(fill="x", padx=15, pady=2)
        return btn

    def toggle_theme(self):
        ctk.set_appearance_mode("Dark" if self.switch_theme.get() == 1 else "Light")
        self.update_ui_strings()

    def set_filter(self, filter_type):
        self.current_filter = filter_type
        self.update_table()

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        lang = LANGUAGES[self.current_lang]
        search_keyword = self.entry_search.get().lower().strip()
        
        self.tree.tag_configure('expired', background='#fadbd8', foreground='#78281f')
        self.tree.tag_configure('soon_expired', background='#fdebd0', foreground='#b9770e') # Sắp hết hạn (Chức năng 4)
        self.tree.tag_configure('low_stock', background='#fbeee6', foreground='#a04000') 
        self.tree.tag_configure('normal', background='#ffffff', foreground='black')
        
        total_items = len(self.inventory)
        total_qty = sum(p['quantity'] for p in self.inventory)
        total_value = sum(p['quantity'] * p['price'] for p in self.inventory)
        
        self.card_lbl1.configure(text=lang["card_items_title"])
        self.card_val1.configure(text=lang["card_items_val"].format(total_items))
        self.card_lbl2.configure(text=lang["card_qty_title"])
        self.card_val2.configure(text=lang["card_qty_val"].format(total_qty))
        self.card_lbl3.configure(text=lang["card_value_title"])
        self.card_val3.configure(text=lang["card_value_val"].format(total_value))
        
        critical_alerts = []
        low_count = 0
        displayed_count = 0
        
        for p in self.inventory:
            name = p['name']
            cat = p.get('category', 'Khác')
            exp = p.get('expiry', 0)
            min_l = p.get('min_level', 5)
            shelf = p.get('shelf', "Chưa rõ")
            supplier = p.get('supplier', "Chưa rõ")
            item_total_val = p['quantity'] * p['price']
            
            if search_keyword and (search_keyword not in name.lower() and search_keyword not in p['id'].lower() and search_keyword not in shelf.lower() and search_keyword not in cat.lower()):
                continue
                
            if self.current_filter == "low" and p['quantity'] >= min_l:
                continue
            if self.current_filter == "available" and p['quantity'] < min_l:
                continue
            if self.current_filter == "expired" and exp > 0:
                continue
            if self.current_filter == "soon_expired" and (exp <= 0 or exp > 3):
                continue
            if self.current_filter == "high_val" and item_total_val <= 1000000:
                continue
                
            if exp == 0:
                tag = 'expired'
                critical_alerts.append(f"{name}")
            elif 0 < exp <= 3:
                tag = 'soon_expired'
            elif p['quantity'] < min_l:
                tag = 'low_stock'
                critical_alerts.append(f"{name}")
                low_count += 1
            else:
                tag = 'normal'
                
            self.tree.insert("", "end", values=(p['id'], name, cat, p['quantity'], f"{p['price']:,}", f"{exp} {lang['day_unit']}", shelf, min_l, supplier), tags=(tag,))
            displayed_count += 1
        
        self.lbl_table_counter.configure(text=lang["table_counter"].format(displayed_count, total_items))
        
        if low_count > 0:
            self.lbl_summary_health.configure(text=lang["summary_risk"], text_color="#e74c3c")
        else:
            self.lbl_summary_health.configure(text=lang["summary_health"], text_color="#2ecc71")
        self.lbl_summary_details.configure(text=f"• {lang['filter_low']}: {low_count}\n• Out of stock: {len(critical_alerts) - low_count}\n• Asset: {total_value:,} VND")

        if critical_alerts:
            self.card_alert.configure(fg_color="#78281f")
            self.lbl_alert_content.configure(text=lang["alert_msg"].format(", ".join(critical_alerts[:2])), text_color="#ff7675")
        else:
            self.card_alert.configure(fg_color="#1e272c")
            self.lbl_alert_content.configure(text=lang["alert_empty"], text_color="#2ecc71")
            
        self.show_charts()

    def add_or_update_product(self):
        lang = LANGUAGES[self.current_lang]
        p_id = self.entry_id.get().strip().upper()
        name = self.entry_name.get().strip()
        cat = self.combo_category.get()
        if not p_id or not name or cat == lang["p_category"]: return
        
        try:
            qty = int(self.entry_qty.get().strip())
            price = int(self.entry_price.get().strip())
            expiry = int(self.entry_expiry.get().strip())
            min_l = int(self.entry_min.get().strip())
        except:
            messagebox.showerror("Error", lang["msg_err_num"])
            return

        shelf = self.entry_shelf.get().strip() or "Kệ chung"
        supplier = self.entry_supplier.get().strip() or "Vãng lai"
        
        for p in self.inventory:
            if p['id'] == p_id:
                p.update({"name": name, "category": cat, "quantity": qty, "price": price, "expiry": expiry, "shelf": shelf, "min_level": min_l, "supplier": supplier})
                self.log_message(lang["log_up"].format(p_id), "UPDATE")
                self.save_data()
                self.update_table()
                return
                
        self.inventory.append({"id": p_id, "name": name, "category": cat, "quantity": qty, "price": price, "expiry": expiry, "shelf": shelf, "min_level": min_l, "supplier": supplier})
        self.log_message(lang["log_add"].format(p_id), "ADD")
        self.save_data()
        self.update_table()

    def delete_product(self):
        selected = self.tree.selection()
        if not selected: return
        p_id = self.tree.item(selected)['values'][0]
        self.inventory = [p for p in self.inventory if p['id'] != p_id]
        self.log_message(LANGUAGES[self.current_lang]["log_del"].format(p_id), "DELETE")
        self.save_data()
        self.update_table()

    def import_from_excel(self):
        if self.current_role != "Admin": return
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            try:
                df = pd.read_excel(file_path)
                for _, row in df.iterrows():
                    self.inventory.append({
                        "id": str(row.get('Mã NL', 'NL_NEW')), "name": str(row.get('Tên Nguyên Liệu', 'Chưa rõ')),
                        "category": str(row.get('Phân Loại', 'Khác')),
                        "quantity": int(row.get('Số Lượng', 0)), "price": int(row.get('Giá Nhập', 0)),
                        "expiry": int(row.get('Hạn Dùng', 30)), "shelf": str(row.get('Vị Trí Kệ', 'Kệ chung')),
                        "min_level": 5, "supplier": "Imported"
                    })
                self.save_data()
                self.update_table()
                self.log_message(LANGUAGES[self.current_lang]["log_import"], "IMPORT")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def export_to_excel(self):
        if self.current_role != "Admin": return
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            pd.DataFrame(self.inventory).to_excel(file_path, index=False)
            messagebox.showinfo("Success", "Exported!")

    def on_product_select(self, event):
        selected = self.tree.selection()
        if not selected: return
        vals = self.tree.item(selected)['values']
        self.clear_entries()
        self.entry_id.insert(0, vals[0])
        self.entry_name.insert(0, vals[1])
        self.combo_category.set(vals[2])
        self.entry_qty.insert(0, vals[3])
        self.entry_price.insert(0, vals[4].replace(",", ""))
        self.on_price_changed(None)
        
        for p in self.inventory:
            if p['id'] == vals[0]:
                self.entry_expiry.insert(0, str(p.get('expiry', 0)))
                self.entry_shelf.insert(0, str(p.get('shelf', '')))
                self.entry_min.insert(0, str(p.get('min_level', 5)))
                self.entry_supplier.insert(0, str(p.get('supplier', '')))

    def clear_entries(self):
        for e in [self.entry_id, self.entry_name, self.entry_qty, self.entry_price, self.entry_expiry, self.entry_shelf, self.entry_min, self.entry_supplier]:
            e.delete(0, 'end')
        self.combo_category.set(LANGUAGES[self.current_lang]["p_category"])
        self.lbl_ai_price.configure(text="💡 Giá bán đề xuất (AI): -- VNĐ")

    def show_charts(self):
        for f in [self.chart_frame1, self.chart_frame2]:
            for w in f.winfo_children(): w.destroy()
        if not self.inventory: return
        
        names = [p['name'][:10] for p in self.inventory]
        quantities = [p['quantity'] for p in self.inventory]
        values = [p['quantity'] * p['price'] for p in self.inventory]
        
        is_dark = self.switch_theme.get() == 1
        bg_color = '#2c3e50' if is_dark else '#ffffff'
        text_color = '#ffffff' if is_dark else '#2c3e50'
        
        fig1, ax1 = plt.subplots(figsize=(4.5, 1.8), dpi=95, facecolor=bg_color)
        ax1.set_facecolor(bg_color)
        ax1.bar(names, quantities, color='#3498db', width=0.35)
        ax1.set_title(LANGUAGES[self.current_lang]["chart1_title"], fontsize=8, color=text_color, fontweight='bold')
        ax1.tick_params(colors=text_color, labelsize=7)
        plt.setp(ax1.get_xticklabels(), rotation=10, ha="right")
        fig1.tight_layout()
        canvas1 = FigureCanvasTkAgg(fig1, master=self.chart_frame1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True)

        fig2, ax2 = plt.subplots(figsize=(4.5, 1.8), dpi=95, facecolor=bg_color)
        if sum(values) > 0:
            ax2.pie(values, labels=names, autopct='%1.1f%%', colors=['#2ecc71','#e67e22','#9b59b6','#f1c40f','#34495e'], textprops={'color': text_color, 'size': 6})
        ax2.set_title(LANGUAGES[self.current_lang]["chart2_title"], fontsize=8, color=text_color, fontweight='bold')
        fig2.tight_layout()
        canvas2 = FigureCanvasTkAgg(fig2, master=self.chart_frame2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True)
        plt.close('all')


# ==================== KÍCH HOẠT HỆ THỐNG PHẦN MỀM ====================
def run_main_app(username, role, selected_lang):
    main_app = EnterprisePizzaWarehouseApp(username, role, selected_lang)
    main_app.mainloop()

if __name__ == "__main__":
    auth_window = AuthWindow(on_auth_success=None)
    auth_window.mainloop()