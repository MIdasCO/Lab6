from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

# 1. Таблица client_type
class ClientType(Base):
    __tablename__ = "client_type"
    client_type_id = Column(Integer, primary_key=True)
    type_name = Column(String(45), nullable=False)


# 2. Таблица contact_type
class ContactType(Base):
    __tablename__ = "contact_type"
    contact_type_id = Column(Integer, primary_key=True)
    type_name = Column(String(45), nullable=False)


# 3. Таблица contact
class Contact(Base):
    __tablename__ = "contact"
    contact_id = Column(Integer, primary_key=True)
    contact_value = Column(String(45))
    contact_type_id = Column(Integer, ForeignKey("contact_type.contact_type_id"), nullable=False)
    
    # Связь с contact_type
    contact_type = relationship("ContactType")


# 4. Таблица district
class District(Base):
    __tablename__ = "district"
    district_id = Column(Integer, primary_key=True)
    # Можно добавить дополнительные поля по необходимости


# 5. Таблица client
class Client(Base):
    __tablename__ = "client"
    client_id = Column(Integer, primary_key=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    client_type_id = Column(Integer, ForeignKey("client_type.client_type_id"), nullable=False)
    contact_id = Column(Integer, ForeignKey("contact.contact_id"), nullable=False)
    district_id = Column(Integer, ForeignKey("district.district_id"), nullable=False)
    discount = Column(Integer)
    registration_date = Column(String(45))  # Если нужно, можно использовать DateTime
    workplace = Column(String(45))
    position = Column(String(45))
    passport_number = Column(String(45))
    login = Column(String(45))
    password = Column(String(100))
    
    # Связи
    client_type = relationship("ClientType")
    contact = relationship("Contact")
    district = relationship("District")


# 6. Таблица order_type
class OrderType(Base):
    __tablename__ = "order_type"
    order_type_id = Column(Integer, primary_key=True)
    wholesale = Column(String(100), nullable=False)
    retail = Column(String(100), nullable=False)


# 7. Таблица discount_type
class DiscountType(Base):
    __tablename__ = "discount_type"
    discount_type_id = Column(Integer, primary_key=True)
    event_name = Column(String(45), nullable=False)


# 8. Таблица event_type
class EventType(Base):
    __tablename__ = "event_type"
    event_type_id = Column(Integer, primary_key=True)
    type_name = Column(String(100))


# 9. Таблица event
class Event(Base):
    __tablename__ = "event"
    event_id = Column(Integer, primary_key=True)
    event_name = Column(String(100))
    event_type_id = Column(Integer, ForeignKey("event_type.event_type_id"), nullable=False)
    comment = Column(String(45))
    
    event_type = relationship("EventType")


# 10. Таблица discount
class Discount(Base):
    __tablename__ = "discount"
    discount_id = Column(Integer, primary_key=True)
    discount_value = Column(String(45), nullable=False)
    discount_type_id = Column(Integer, ForeignKey("discount_type.discount_type_id"), nullable=False)
    event_id = Column(Integer, ForeignKey("event.event_id"), nullable=False)
    
    discount_type = relationship("DiscountType")
    event = relationship("Event")


# 11. Таблица order_status
class OrderStatus(Base):
    __tablename__ = "order_status"
    order_status_id = Column(Integer, primary_key=True)
    in_progress = Column(String(45), nullable=False)
    completed = Column(String(45), nullable=False)


# 12. Таблица position
class Position(Base):
    __tablename__ = "position"
    position_id = Column(Integer, primary_key=True)
    position_name = Column(String(45), nullable=False)


# 13. Таблица employee
class Employee(Base):
    __tablename__ = "employee"
    employee_id = Column(Integer, primary_key=True)
    first_name = Column(String(45), nullable=False)
    last_name = Column(String(45), nullable=False)
    salary = Column(String(45))
    registration_date = Column(String(45))  # Можно использовать DateTime
    phone = Column(Integer)
    login = Column(String(45))
    password = Column(String(45))
    position_id = Column(Integer, ForeignKey("position.position_id"), nullable=False)
    
    position = relationship("Position")


# 14. Таблица order_table
class OrderTable(Base):
    __tablename__ = "order_table"
    order_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.client_id"), nullable=False)
    order_type_id = Column(Integer, ForeignKey("order_type.order_type_id"), nullable=False)
    discount_id = Column(Integer, ForeignKey("discount.discount_id"), nullable=False)
    order_status_id = Column(Integer, ForeignKey("order_status.order_status_id"), nullable=False)
    order_date = Column(Date)
    invoice_number = Column(String(45))
    comment = Column(String(45))
    employee_id = Column(Integer, ForeignKey("employee.employee_id"), nullable=False)
    
    client = relationship("Client")
    order_type = relationship("OrderType")
    discount = relationship("Discount")
    order_status = relationship("OrderStatus")
    employee = relationship("Employee")


# 15. Таблица payment_type
class PaymentType(Base):
    __tablename__ = "payment_type"
    payment_type_id = Column(Integer, primary_key=True)
    cash = Column(String(45), nullable=False)
    card = Column(String(45), nullable=False)


# 16. Таблица payment
class Payment(Base):
    __tablename__ = "payment"
    payment_id = Column(Integer, primary_key=True)
    payment_type_id = Column(Integer, ForeignKey("payment_type.payment_type_id"), nullable=False)
    amount = Column(Integer)
    payment_date = Column(String(45))
    comment = Column(String(45))
    order_id = Column(Integer, ForeignKey("order_table.order_id"), nullable=False)
    
    payment_type = relationship("PaymentType")
    order = relationship("OrderTable")


# 17. Таблица category
class Category(Base):
    __tablename__ = "category"
    category_id = Column(Integer, primary_key=True)
    category_name = Column(String(100), nullable=False)


# 18. Таблица product
class Product(Base):
    __tablename__ = "product"
    product_id = Column(Integer, primary_key=True)
    product_name = Column(String(45), nullable=False)
    description = Column(String(45), nullable=False)
    registration_date = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey("category.category_id"), nullable=False)
    photo = Column(String(45))
    
    category = relationship("Category")


# 19. Таблица delivery_type
class DeliveryType(Base):
    __tablename__ = "delivery_type"
    delivery_type_id = Column(Integer, primary_key=True)
    urgent = Column(String(45), nullable=False)
    contract = Column(String(45), nullable=False)


# 20. Таблица supplier
class Supplier(Base):
    __tablename__ = "supplier"
    supplier_id = Column(Integer, primary_key=True)
    company_name = Column(String(45))
    registration_date = Column(DateTime)
    comment = Column(String(45))


# 21. Таблица delivery
class Delivery(Base):
    __tablename__ = "delivery"
    delivery_id = Column(Integer, primary_key=True)
    company_name = Column(String(45), nullable=False)
    delivery_date = Column(Date, nullable=False)
    supplier_name = Column(String(45), nullable=False)
    comment = Column(String(45), nullable=False)
    delivery_type_id = Column(Integer, ForeignKey("delivery_type.delivery_type_id"), nullable=False)
    invoice_number = Column(Integer)
    supplier_id = Column(Integer, ForeignKey("supplier.supplier_id"), nullable=False)
    
    delivery_type = relationship("DeliveryType")
    supplier = relationship("Supplier")


# 22. Таблица warehouse
class Warehouse(Base):
    __tablename__ = "warehouse"
    warehouse_id = Column(Integer, primary_key=True)
    warehouse_name = Column(String(45))


# 23. Таблица delivery_list
class DeliveryList(Base):
    __tablename__ = "delivery_list"
    delivery_list_id = Column(Integer, primary_key=True)
    quantity = Column(String(45), nullable=False)
    price = Column(String(45), nullable=False)
    delivery_id = Column(Integer, ForeignKey("delivery.delivery_id"), nullable=False)
    warehouse_id = Column(Integer, ForeignKey("warehouse.warehouse_id"), nullable=False)
    comment = Column(String(45))
    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)
    
    delivery = relationship("Delivery")
    warehouse = relationship("Warehouse")
    product = relationship("Product")


# 24. Таблица payout_type
class PayoutType(Base):
    __tablename__ = "payout_type"
    payout_type_id = Column(Integer, primary_key=True)
    payout_name = Column(String(45))


# 25. Таблица salary
class Salary(Base):
    __tablename__ = "salary"
    salary_id = Column(Integer, primary_key=True)
    amount = Column(Integer, nullable=False)
    date_paid = Column(String(45))
    comment = Column(String(45))
    bonus = Column(String(45))
    payout_type_id = Column(Integer, ForeignKey("payout_type.payout_type_id"), nullable=False)
    employee_id = Column(Integer, ForeignKey("employee.employee_id"), nullable=False)
    
    payout_type = relationship("PayoutType")
    employee = relationship("Employee")


# 26. Таблица order_item
class OrderItem(Base):
    __tablename__ = "order_item"
    order_item_id = Column(Integer, primary_key=True, autoincrement=True)
    delivery_list_id = Column(Integer, ForeignKey("delivery_list.delivery_list_id"), nullable=False)
    order_id = Column(Integer, ForeignKey("order_table.order_id"), nullable=False)
    quantity = Column(String(45))
    discounted_price = Column(Integer)
    
    delivery_list = relationship("DeliveryList")
    order = relationship("OrderTable")


# 27. Таблица price_list
class PriceList(Base):
    __tablename__ = "price_list"
    price_list_id = Column(Integer, primary_key=True)
    comment = Column(String(45), nullable=False)
    price = Column(Integer, nullable=False)
    last_updated = Column(DateTime)
    product_id = Column(Integer, ForeignKey("product.product_id"), nullable=False)
    
    product = relationship("Product")


# 28. Таблица report
class Report(Base):
    __tablename__ = "report"
    report_id = Column(Integer, primary_key=True)
    report_datetime = Column(DateTime, nullable=False)
    form_name = Column(String(45))
    report_name = Column(String(45))


# 29. Таблица tax
class Tax(Base):
    __tablename__ = "tax"
    tax_id = Column(Integer, primary_key=True)
    rate = Column(Integer)
    tax_name = Column(String(45))
    comment = Column(String(45))


# 30. Таблица delivery_payment
class DeliveryPayment(Base):
    __tablename__ = "delivery_payment"
    delivery_payment_id = Column(Integer, primary_key=True)
    amount = Column(Integer)
    payment_type_id = Column(Integer, ForeignKey("payment_type.payment_type_id"), nullable=False)
    delivery_id = Column(Integer, ForeignKey("delivery.delivery_id"), nullable=False)
    payment_date = Column(DateTime)
    comment = Column(String(145))
    
    payment_type = relationship("PaymentType")
    delivery = relationship("Delivery")


# 31. Таблица product_writeoff
class ProductWriteoff(Base):
    __tablename__ = "product_writeoff"
    writeoff_id = Column(Integer, primary_key=True)
    comment = Column(String(45))
    date = Column(String(45))
    quantity = Column(Integer)
