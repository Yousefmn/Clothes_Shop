class Supplier:
    SupplierID: int
    SupplierName: str
    ContactName: str
    Phone: str
    Email: str

class Category:
    CategoryID: int
    CategoryName: str
    Description: str

class Customer:
    CustomerID: int
    CustomerName: str
    Phone: str
    Email: str
    Address: str

class Product:
    ProductID: int
    ProductName: str
    SupplierID: int
    CategoryID: int
    Price: float
    Quantity: int

class Order:
    OrderID: int
    CustomerID: int
    OrderDate: str
    TotalAmount: float

class OrderDetail:
    OrderDetailID: int
    OrderID: int
    ProductID: int
    Quantity: int
    Price: float

class Employee:
    EmployeeID: int
    EmployeeName: str
    Position: str
    Phone: str
    Email: str

class Inventory:
    InventoryID: int
    ProductID: int
    Quantity: int
    LastUpdated: str

class Payment:
    PaymentID: int
    OrderID: int
    PaymentDate: str
    Amount: float

class Shipper:
    ShipperID: int
    ShipperName: str
    Phone: str
