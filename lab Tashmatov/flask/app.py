from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "secret_key_for_session"  # Для продакшена храните секретный ключ в переменных окружения

# ============================
# Глобальные данные (имитация базы)
# ============================

users = {
    "client1": {
        "password": "pass1",
        "role": "Клиент",
        "first_name": "Иван",
        "last_name": "Иванов"
    },
    "accountant1": {
        "password": "accpass",
        "role": "Бухгалтер",
        "first_name": "Ольга",
        "last_name": "Смирнова"
    },
    "admin": {
        "password": "admin123",
        "role": "Администратор",
        "first_name": "Super",
        "last_name": "Admin"
    }
}

flowers = [
    {"id": 1, "category": "Цветы", "name": "Роза",       "price": 200},
    {"id": 2, "category": "Цветы", "name": "Лилия",      "price": 250},
    {"id": 3, "category": "Цветы", "name": "Тюльпан",    "price": 150},
    {"id": 4, "category": "Цветы", "name": "Гербера",    "price": 180},
    {"id": 5, "category": "Цветы", "name": "Орхидея",    "price": 300},
    {"id": 6, "category": "Цветы", "name": "Ромашка",    "price": 100},
    {"id": 7, "category": "Цветы", "name": "Ирис",       "price": 220},
    {"id": 8, "category": "Цветы", "name": "Нарцисс",    "price": 170},
    {"id": 9, "category": "Цветы", "name": "Пионы",      "price": 280},
    {"id": 10, "category": "Цветы", "name": "Фиалка",    "price": 130}
]

orders = []
order_id_counter = 1

payments = []
payment_id_counter = 1

order_contacts = {}
contacts = {}

discounts = [
    {"id": 1, "event_name": "Весенняя акция", "discount": 10, "start_date": "2025-04-01", "end_date": "2025-04-30"}
]

# ============================
# Вспомогательная функция для бухгалтера
# ============================
def accountant_required():
    return "user_login" in session and session.get("user_role") == "Бухгалтер"

def get_db():
    db = sqlite3.connect('test.db')
    db.row_factory = sqlite3.Row
    return db

# ============================
# Маршруты для клиентов (шаблоны из templates/customer/)
# ============================

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_type = request.form.get("user_type")
        login_name = request.form.get("login_name")
        password = request.form.get("password")
        user_data = users.get(login_name)
        if user_data and user_data["password"] == password and user_data["role"] == user_type:
            session["user_login"] = login_name
            session["user_role"] = user_type
            if "current_order" not in session:
                session["current_order"] = []
            return redirect(url_for("dashboard"))
        else:
            return render_template("customer/login.html", error="Неверный логин, пароль или тип пользователя")
    return render_template("customer/login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        login_name = request.form.get("login_name")
        password = request.form.get("password")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        if not login_name or not password:
            return render_template("customer/register.html", error="Логин и пароль обязательны")
        if login_name in users:
            return render_template("customer/register.html", error="Пользователь с таким логином уже существует")
        users[login_name] = {
            "password": password,
            "role": "Клиент",
            "first_name": first_name,
            "last_name": last_name
        }
        return redirect(url_for("login"))
    return render_template("customer/register.html")

@app.route("/dashboard")
def dashboard():
    if "user_login" not in session:
        return redirect(url_for("login"))
    role = session.get("user_role")
    if role == "Бухгалтер":
        return redirect(url_for("accountant_dashboard"))
    return render_template("customer/dashboard.html", user=session["user_login"], role=role)

@app.route("/price_list")
def price_list():
    return render_template("customer/price_list.html", flowers=flowers)

@app.route("/order_composition", methods=["GET", "POST"])
def order_composition():
    if "user_login" not in session:
        return redirect(url_for("login"))
    if "current_order" not in session:
        session["current_order"] = []
    if request.method == "POST":
        action = request.form.get("action")
        if action == "add_item":
            flower_id = int(request.form.get("flower_id"))
            quantity = int(request.form.get("quantity"))
            flower = next((f for f in flowers if f["id"] == flower_id), None)
            if flower:
                current_order = session.get("current_order", [])
                current_order.append({
                    "flower_id": flower_id,
                    "flower_name": flower["name"],
                    "price": flower["price"],
                    "quantity": quantity
                })
                session["current_order"] = current_order
        elif action == "place_order":
            global order_id_counter
            current_order = session.get("current_order", [])
            if not current_order:
                return render_template("customer/order_composition.html", error="Нет товаров в заказе", items=[], total=0, flowers=flowers)
            total = sum(item["price"] * item["quantity"] for item in current_order)
            new_order = {
                "order_id": order_id_counter,
                "client": session["user_login"],
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "items": current_order,
                "total": total,
                "status": "В работе",
                "invoice_number": f"INV{order_id_counter:03d}"
            }
            orders.append(new_order)
            order_id_counter += 1
            session["current_order"] = []
            return redirect(url_for("client_orders"))
    current_order = session.get("current_order", [])
    total = sum(item["price"] * item["quantity"] for item in current_order)
    return render_template("customer/order_composition.html", items=current_order, total=total, flowers=flowers)

@app.route("/client_orders")
def client_orders():
    if "user_login" not in session:
        return redirect(url_for("login"))
    client = session["user_login"]
    client_orders = [o for o in orders if o["client"] == client]
    return render_template("customer/client_orders.html", orders=client_orders)

@app.route("/order_cancellation", methods=["GET", "POST"])
def order_cancellation():
    if "user_login" not in session:
        return redirect(url_for("login"))
    message = ""
    client = session["user_login"]
    client_orders = [o for o in orders if o["client"] == client and o["status"] == "В работе"]
    if request.method == "POST":
        order_id = int(request.form.get("order_id"))
        order = next((o for o in orders if o["order_id"] == order_id and o["client"] == client and o["status"] == "В работе"), None)
        if order:
            order["status"] = "Отменён"
            message = f"Заказ {order_id} отменён."
        else:
            message = "Заказ не найден или уже отменён."
    return render_template("customer/order_cancellation.html", message=message, orders=client_orders)

@app.route("/orders_payment_period", methods=["GET", "POST"])
def orders_payment_period():
    filtered_orders = []
    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        client = session.get("user_login")
        for order in orders:
            if order["client"] == client:
                order_date = order["date"][:10]
                if start_date <= order_date <= end_date:
                    filtered_orders.append(order)
    return render_template("customer/orders_payment_period.html", orders=filtered_orders)

@app.route("/client_contact_registration", methods=["GET", "POST"])
def client_contact_registration():
    if "user_login" not in session:
        return redirect(url_for("login"))
    message = ""
    client = session["user_login"]
    if request.method == "POST":
        contact_type = request.form.get("contact_type")
        contact_value = request.form.get("contact_value")
        if client not in contacts:
            contacts[client] = []
        contacts[client].append({"type": contact_type, "value": contact_value})
        message = "Контакт клиента зарегистрирован."
    client_contacts = contacts.get(client, [])
    return render_template("customer/client_contact_registration.html", message=message, contacts=client_contacts)

@app.route("/order_contact_registration", methods=["GET", "POST"])
def order_contact_registration():
    if "user_login" not in session:
        return redirect(url_for("login"))
    message = ""
    if request.method == "POST":
        try:
            order_id = int(request.form.get("order_id"))
        except (TypeError, ValueError):
            order_id = None
        contact_type = request.form.get("contact_type")
        contact_value = request.form.get("contact_value")
        employee_name = request.form.get("employee_name", "")
        if order_id is None:
            message = "Укажите корректный номер заказа."
        else:
            if order_id not in order_contacts:
                order_contacts[order_id] = []
            order_contacts[order_id].append({
                "contact_type": contact_type,
                "contact_value": contact_value,
                "employee_name": employee_name
            })
            message = f"Контакт для заказа {order_id} зарегистрирован."
    return render_template("customer/order_contact_registration.html", message=message)

@app.route("/order_edit", methods=["GET", "POST"])
def order_edit():
    if "user_login" not in session:
        return redirect(url_for("login"))
    message = ""
    order_data = None
    client = session["user_login"]
    if request.method == "POST":
        action = request.form.get("action")
        if action == "load":
            try:
                order_id = int(request.form.get("order_id"))
            except (TypeError, ValueError):
                message = "Введите корректный номер заказа."
                return render_template("customer/order_edit.html", message=message, order_data=None)
            order_data = next((o for o in orders if o["order_id"] == order_id and o["client"] == client), None)
            if not order_data:
                message = "Заказ не найден."
        elif action == "update":
            try:
                order_id = int(request.form.get("order_id"))
            except (TypeError, ValueError):
                message = "Введите корректный номер заказа."
                return render_template("customer/order_edit.html", message=message, order_data=None)
            order_data = next((o for o in orders if o["order_id"] == order_id and o["client"] == client), None)
            if order_data:
                new_items = []
                total = 0
                for i, item in enumerate(order_data["items"]):
                    qty_str = request.form.get(f"quantity_{i}")
                    try:
                        new_qty = int(qty_str)
                    except (TypeError, ValueError):
                        new_qty = item["quantity"]
                    new_items.append({
                        "flower_id": item["flower_id"],
                        "flower_name": item["flower_name"],
                        "price": item["price"],
                        "quantity": new_qty
                    })
                    total += item["price"] * new_qty
                order_data["items"] = new_items
                order_data["total"] = total
                message = "Заказ успешно обновлён."
            else:
                message = "Заказ не найден."
    return render_template("customer/order_edit.html", message=message, order_data=order_data)

@app.route("/order_payment", methods=["GET", "POST"])
def order_payment():
    if "user_login" not in session:
        return redirect(url_for("login"))
    global payment_id_counter
    message = ""
    client = session["user_login"]
    client_orders = [o for o in orders if o["client"] == client and o["status"] != "Отменён"]
    if request.method == "POST":
        try:
            order_id = int(request.form.get("order_id"))
        except (TypeError, ValueError):
            order_id = None
        amount = float(request.form.get("amount") or 0)
        payment_method = request.form.get("payment_method")
        order = next((o for o in client_orders if o["order_id"] == order_id), None)
        if order:
            payment = {
                "payment_id": payment_id_counter,
                "order_id": order_id,
                "amount": amount,
                "method": payment_method,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            payments.append(payment)
            payment_id_counter += 1
            message = f"Оплата {amount} руб. для заказа {order_id} принята."
        else:
            message = "Заказ не найден или отменён."
    return render_template("customer/order_payment.html", message=message, orders=client_orders)

@app.route("/client_debts", methods=["GET", "POST"])
def client_debts():
    if "user_login" not in session:
        return redirect(url_for("login"))
    client = session["user_login"]
    client_orders = [o for o in orders if o["client"] == client and o["status"] != "Отменён"]
    debts = []
    if request.method == "POST":
        try:
            order_id = int(request.form.get("order_id"))
        except (TypeError, ValueError):
            order_id = None
        pay_amount = float(request.form.get("pay_amount") or 0)
        order = next((o for o in client_orders if o["order_id"] == order_id), None)
        if order:
            global payment_id_counter
            payment = {
                "payment_id": payment_id_counter,
                "order_id": order_id,
                "amount": pay_amount,
                "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            payments.append(payment)
            payment_id_counter += 1
    for o in client_orders:
        paid = sum(p["amount"] for p in payments if p["order_id"] == o["order_id"])
        if paid < o["total"]:
            debts.append({
                "order_id": o["order_id"],
                "total": o["total"],
                "paid": paid,
                "due": o["total"] - paid
            })
    return render_template("customer/client_debts.html", debts=debts)

@app.route("/cancelled_orders")
def cancelled_orders():
    if "user_login" not in session:
        return redirect(url_for("login"))
    client = session["user_login"]
    cancelled = [o for o in orders if o["client"] == client and o["status"] == "Отменён"]
    return render_template("customer/cancelled_orders.html", orders=cancelled)

@app.route("/current_discounts")
def current_discounts():
    if "user_login" not in session:
        return redirect(url_for("login"))
    return render_template("customer/current_discounts.html", discounts=discounts)

@app.route("/authorization_form")
def authorization_form():
    if "user_login" not in session:
        return redirect(url_for("login"))
    return render_template("customer/authorization_form.html")

# ============================
# Маршруты для бухгалтера (шаблоны из templates/accountant/)
# ============================

@app.route("/accountant/dashboard")
def accountant_dashboard():
    if not accountant_required():
        return redirect(url_for("login"))
    return render_template("accountant/accountant_dashboard.html")

@app.route("/accountant/turnover/warehouse")
def accountant_turnover_warehouse():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "product_type": "Цветы", "product": "Роза", "supply_qty": 100, "sales_qty": 80, "remaining": 20, "revenue": 16000, "profit_loss": 2000, "taxes": 500, "net_profit": 1500}
    ]
    return render_template("accountant/accountant_turnover_warehouse.html", data=data)

@app.route("/accountant/turnover/branch")
def accountant_turnover_branch():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "branch": "Филиал 1", "revenue": 20000}
    ]
    return render_template("accountant/accountant_turnover_branch.html", data=data)

@app.route("/accountant/turnover/overall")
def accountant_turnover_overall():
    if not accountant_required():
        return redirect(url_for("login"))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT SUM(revenue) as total_revenue, 
               SUM(profit) as total_profit 
        FROM turnover_overall
    """)
    data = [dict(row) for row in cursor.fetchall()]
    if not data:
        # If no data, insert test data
        cursor.execute("""
            INSERT INTO turnover_overall (total_revenue, total_profit)
            VALUES (50000, 7000)
        """)
        db.commit()
        data = [{"total_revenue": 50000, "total_profit": 7000}]
    db.close()
    return render_template("accountant/accountant_turnover_overall.html", data=data)

@app.route("/accountant/turnover/product")
def accountant_turnover_product():
    if not accountant_required():
        return redirect(url_for("login"))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT * FROM turnover_product
    """)
    data = [dict(row) for row in cursor.fetchall()]
    if not data:
        cursor.execute("""
            INSERT INTO turnover_product 
            (product, supply_qty, sales_qty, remaining, revenue, profit_loss, taxes, net_profit)
            VALUES 
            ('Роза', 100, 80, 20, 16000, 2000, 500, 1500)
        """)
        db.commit()
        data = [{"product": "Роза", "supply_qty": 100, "sales_qty": 80, 
                 "remaining": 20, "revenue": 16000, "profit_loss": 2000, 
                 "taxes": 500, "net_profit": 1500}]
    db.close()
    return render_template("accountant/accountant_turnover_product.html", data=data)

@app.route("/accountant/turnover/category")
def accountant_turnover_category():
    if not accountant_required():
        return redirect(url_for("login"))
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT * FROM turnover_category
    """)
    data = [dict(row) for row in cursor.fetchall()]
    if not data:
        cursor.execute("""
            INSERT INTO turnover_category 
            (category, supply_qty, sales_qty, remaining, revenue, profit_loss, taxes, net_profit)
            VALUES 
            ('Цветы', 500, 400, 100, 80000, 10000, 2000, 8000)
        """)
        db.commit()
        data = [{"category": "Цветы", "supply_qty": 500, "sales_qty": 400, 
                 "remaining": 100, "revenue": 80000, "profit_loss": 10000, 
                 "taxes": 2000, "net_profit": 8000}]
    db.close()
    return render_template("accountant/accountant_turnover_category.html", data=data)

@app.route("/accountant/sales/warehouse")
def accountant_sales_warehouse():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "warehouse": "Склад 1", "sales": 30000}
    ]
    return render_template("accountant/accountant_sales_warehouse.html", data=data)

@app.route("/accountant/sales/product_type")
def accountant_sales_product_type():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "product_type": "Цветы", "sales": 50000}
    ]
    return render_template("accountant/accountant_sales_product_type.html", data=data)

@app.route("/accountant/sales/product")
def accountant_sales_product():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "product": "Роза", "price": 200, "quantity": 80, "date": "2025-04-05", "client": "client1", "order_number": 1}
    ]
    return render_template("accountant/accountant_sales_product.html", data=data)

@app.route("/accountant/sales/branch")
def accountant_sales_branch():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "branch": "Филиал 1", "sales": 40000}
    ]
    return render_template("accountant/accountant_sales_branch.html", data=data)

@app.route("/accountant/sales/client")
def accountant_sales_client():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "client": "client1", "sales": 35000}
    ]
    return render_template("accountant/accountant_sales_client.html", data=data)

@app.route("/accountant/order_composition_customer")
def accountant_order_composition_customer():
    if not accountant_required():
        return redirect(url_for("login"))
    return render_template("accountant/accountant_order_composition_customer.html", orders=orders)

@app.route("/accountant/order_cancellation_customer")
def accountant_order_cancellation_customer():
    if not accountant_required():
        return redirect(url_for("login"))
    cancelled = [o for o in orders if o["status"] == "Отменён"]
    return render_template("accountant/accountant_order_cancellation_customer.html", orders=cancelled)

@app.route("/accountant/sales/employees")
def accountant_sales_employees():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "employee": "Сидоров", "sales": 45000}
    ]
    return render_template("accountant/accountant_sales_employees.html", data=data)

@app.route("/accountant/sales/payment_type")
def accountant_sales_payment_type():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "payment_type": "Карта", "sales": 30000},
        {"number": 2, "payment_type": "Наличные", "sales": 25000}
    ]
    return render_template("accountant/accountant_sales_payment_type.html", data=data)

@app.route("/accountant/deliveries/product_type")
def accountant_deliveries_product_type():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "product_type": "Цветы", "deliveries": 120}
    ]
    return render_template("accountant/accountant_deliveries_product_type.html", data=data)

@app.route("/accountant/deliveries/product")
def accountant_deliveries_product():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "product": "Роза", "deliveries": 100}
    ]
    return render_template("accountant/accountant_deliveries_product.html", data=data)

@app.route("/accountant/deliveries/warehouse")
def accountant_deliveries_warehouse():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "warehouse": "Склад 1", "deliveries": 80}
    ]
    return render_template("accountant/accountant_deliveries_warehouse.html", data=data)

@app.route("/accountant/deliveries/suppliers")
def accountant_deliveries_suppliers():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "date": "2025-04-03", "supplier": "Поставщик А", "product_type": "Цветы", "product": "Роза", "quantity": 100, "price": 150, "warehouse": "Склад 1"}
    ]
    return render_template("accountant/accountant_deliveries_suppliers.html", data=data)

@app.route("/accountant/debts/customers")
def accountant_debts_customers():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "order_id": 1, "client": "client1", "total": 500, "paid": 300, "debt": 200}
    ]
    return render_template("accountant/accountant_debts_customers.html", data=data)

@app.route("/accountant/debts/suppliers")
def accountant_debts_suppliers():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "delivery_number": 101, "supplier": "Поставщик А", "employee": "Сидоров", "deadline": "2025-05-01", "amount_due": 10000, "debt": 2500}
    ]
    return render_template("accountant/accountant_debts_suppliers.html", data=data)

@app.route("/accountant/debts/suppliers_detail")
def accountant_debts_suppliers_detail():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "delivery_number": 102, "supplier": "Поставщик Б", "employee": "Петров", "deadline": "2025-05-05", "amount_due": 15000, "debt": 3000}
    ]
    return render_template("accountant/accountant_debts_suppliers_detail.html", data=data)

@app.route("/accountant/profitability/supplies")
def accountant_profitability_supplies():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "product_type": "Цветы", "product": "Роза", "purchase_price": 150, "sale_price": 200, "delivery_number": 101, "profit": 5000}
    ]
    return render_template("accountant/accountant_profitability_supplies.html", data=data)

@app.route("/accountant/break_even")
def accountant_break_even():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "product_type": "Цветы", "product": "Лилия", "purchase_price": 200, "sale_price": 250, "profit": 5000}
    ]
    return render_template("accountant/accountant_break_even.html", data=data)

@app.route("/accountant/taxes")
def accountant_taxes():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "tax_name": "НДС", "amount": 5000, "start_date": "2025-04-01", "end_date": "2025-04-30"}
    ]
    return render_template("accountant/accountant_taxes.html", data=data)

@app.route("/accountant/salaries")
def accountant_salaries():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "date": "2025-04-30", "accrued": 20000, "paid": 15000, "employee": "Сидоров", "position": "Продавец"}
    ]
    return render_template("accountant/accountant_salaries.html", data=data)

@app.route("/accountant/sales/promotions")
def accountant_sales_promotions():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "promotion": "Весенняя акция", "order": 1, "date": "2025-04-05", "amount": 4500}
    ]
    return render_template("accountant/accountant_sales_promotions.html", data=data)

@app.route("/accountant/auth_form", methods=["GET", "POST"])
def accountant_auth_form():
    message = ""
    if request.method == "POST":
        login_name = request.form.get("login")
        password = request.form.get("password")
        user_data = users.get(login_name)
        if user_data and user_data["password"] == password:
            message = "Успешная авторизация."
        else:
            message = "Неверные данные."
    return render_template("accountant/accountant_auth_form.html", message=message)

@app.route("/accountant/profit_loss_report")
def accountant_profit_loss_report():
    if not accountant_required():
        return redirect(url_for("login"))
    data = [
        {"number": 1, "expenses": 30000, "income": 50000, "taxes": 5000, "profit": 15000}
    ]
    return render_template("accountant/accountant_profit_loss_report.html", data=data)

# ============================
# Конец блока маршрутов для бухгалтера
# ============================

if __name__ == "__main__":
    app.run(debug=True)
