-- ================================================
-- 1. Создание базы данных RA_v1 (если не существует)
-- ================================================
IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'RA_v1')
BEGIN
    CREATE DATABASE [RA_v1];
END
GO

USE [RA_v1];
GO

--------------------------------------------------
-- Table: Branch
--------------------------------------------------
IF OBJECT_ID('dbo.Branch', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Branch] (
        [BranchID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: Suppliers
--------------------------------------------------
IF OBJECT_ID('dbo.Suppliers', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Suppliers] (
        [SupplierID] INT NOT NULL PRIMARY KEY,
        [BranchID] INT NOT NULL,
        [Name] VARCHAR(45) NULL,
        CONSTRAINT [FK_Suppliers_Branch] FOREIGN KEY ([BranchID])
            REFERENCES [dbo].[Branch] ([BranchID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: SupplyStatus
--------------------------------------------------
IF OBJECT_ID('dbo.SupplyStatus', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[SupplyStatus] (
        [SupplyStatusID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: SupplierContacts
--------------------------------------------------
IF OBJECT_ID('dbo.SupplierContacts', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[SupplierContacts] (
        [SupplierContactID] INT NOT NULL PRIMARY KEY,
        [SupplierID] INT NOT NULL,
        CONSTRAINT [FK_SupplierContacts_Suppliers] FOREIGN KEY ([SupplierID])
            REFERENCES [dbo].[Suppliers] ([SupplierID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: SupplyType
--------------------------------------------------
IF OBJECT_ID('dbo.SupplyType', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[SupplyType] (
        [SupplyTypeID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: SupplyPaymentType
--------------------------------------------------
IF OBJECT_ID('dbo.SupplyPaymentType', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[SupplyPaymentType] (
        [SupplyPaymentTypeID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: SupplyPayment
--------------------------------------------------
IF OBJECT_ID('dbo.SupplyPayment', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[SupplyPayment] (
        [SupplyPaymentID] INT NOT NULL PRIMARY KEY,
        [SupplyPaymentTypeID] INT NOT NULL,
        CONSTRAINT [FK_SupplyPayment_SupplyPaymentType] FOREIGN KEY ([SupplyPaymentTypeID])
            REFERENCES [dbo].[SupplyPaymentType] ([SupplyPaymentTypeID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: Position
--------------------------------------------------
IF OBJECT_ID('dbo.Position', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Position] (
        [PositionID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: Employee
-- Добавлен столбец [Role] для хранения роли сотрудника (по умолчанию 'Employee')
--------------------------------------------------
IF OBJECT_ID('dbo.Employee', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Employee] (
        [EmployeeID] INT NOT NULL PRIMARY KEY,
        [BranchID] INT NOT NULL,
        [PositionID] INT NOT NULL,
        [FirstName] VARCHAR(45) NULL,
        [LastName] VARCHAR(45) NULL,
        [INN] VARCHAR(45) NULL,
        [Password] VARCHAR(45) NULL,
        [Login] VARCHAR(45) NULL,
        [Salary] VARCHAR(45) NULL,
        [Role] VARCHAR(20) NOT NULL DEFAULT('Employee'),
        CONSTRAINT [FK_Employee_Branch] FOREIGN KEY ([BranchID])
            REFERENCES [dbo].[Branch] ([BranchID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Employee_Position] FOREIGN KEY ([PositionID])
            REFERENCES [dbo].[Position] ([PositionID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: Warehouse
--------------------------------------------------
IF OBJECT_ID('dbo.Warehouse', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Warehouse] (
        [WarehouseID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: Supplies
--------------------------------------------------
IF OBJECT_ID('dbo.Supplies', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Supplies] (
        [SupplyID] INT NOT NULL PRIMARY KEY,
        [SupplierID] INT NOT NULL,
        [SupplyStatusID] INT NOT NULL,
        [SupplyTypeID] INT NOT NULL,
        [SupplyPaymentID] INT NOT NULL,
        [EmployeeID] INT NOT NULL,
        [WarehouseID] INT NOT NULL,
        [Date] VARCHAR(45) NULL,
        [Price] VARCHAR(45) NULL,
        [InvoiceNumber] VARCHAR(45) NULL,
        [Comments] VARCHAR(45) NULL,
        CONSTRAINT [FK_Supplies_Suppliers] FOREIGN KEY ([SupplierID])
            REFERENCES [dbo].[Suppliers] ([SupplierID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Supplies_SupplyStatus] FOREIGN KEY ([SupplyStatusID])
            REFERENCES [dbo].[SupplyStatus] ([SupplyStatusID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Supplies_SupplyType] FOREIGN KEY ([SupplyTypeID])
            REFERENCES [dbo].[SupplyType] ([SupplyTypeID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Supplies_SupplyPayment] FOREIGN KEY ([SupplyPaymentID])
            REFERENCES [dbo].[SupplyPayment] ([SupplyPaymentID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Supplies_Employee] FOREIGN KEY ([EmployeeID])
            REFERENCES [dbo].[Employee] ([EmployeeID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Supplies_Warehouse] FOREIGN KEY ([WarehouseID])
            REFERENCES [dbo].[Warehouse] ([WarehouseID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: ClientType
--------------------------------------------------
IF OBJECT_ID('dbo.ClientType', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[ClientType] (
        [ClientTypeID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: Clients
-- Обновленная таблица клиентов с требуемыми полями
--------------------------------------------------
IF OBJECT_ID('dbo.Clients', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Clients] (
        [ClientID] INT NOT NULL PRIMARY KEY,
        [ClientTypeID] INT NOT NULL,
        [District] VARCHAR(45) NULL,
        [Activity] VARCHAR(45) NULL,
        [LastName] VARCHAR(45) NULL,
        [FirstName] VARCHAR(45) NULL,
        [MiddleName] VARCHAR(45) NULL,
        [BirthDate] DATE NULL,
        [RegistrationDate] VARCHAR(45) NULL,
        [Login] VARCHAR(45) NULL,
        [Password] VARCHAR(45) NULL,
        CONSTRAINT [FK_Clients_ClientType] FOREIGN KEY ([ClientTypeID])
            REFERENCES [dbo].[ClientType] ([ClientTypeID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: ClientContactType
--------------------------------------------------
IF OBJECT_ID('dbo.ClientContactType', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[ClientContactType] (
        [ClientContactTypeID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: ClientContacts
--------------------------------------------------
IF OBJECT_ID('dbo.ClientContacts', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[ClientContacts] (
        [ClientContactID] INT NOT NULL PRIMARY KEY,
        [ClientID] INT NOT NULL,
        [ClientContactTypeID] INT NOT NULL,
        CONSTRAINT [FK_ClientContacts_Clients] FOREIGN KEY ([ClientID])
            REFERENCES [dbo].[Clients] ([ClientID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_ClientContacts_ClientContactType] FOREIGN KEY ([ClientContactTypeID])
            REFERENCES [dbo].[ClientContactType] ([ClientContactTypeID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: PaymentType
--------------------------------------------------
IF OBJECT_ID('dbo.PaymentType', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[PaymentType] (
        [PaymentTypeID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: PaymentStatus
--------------------------------------------------
IF OBJECT_ID('dbo.PaymentStatus', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[PaymentStatus] (
        [PaymentStatusID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: OrderStatus
--------------------------------------------------
IF OBJECT_ID('dbo.OrderStatus', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[OrderStatus] (
        [OrderStatusID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: OrderType
--------------------------------------------------
IF OBJECT_ID('dbo.OrderType', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[OrderType] (
        [OrderTypeID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: DeliveryType
--------------------------------------------------
IF OBJECT_ID('dbo.DeliveryType', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[DeliveryType] (
        [DeliveryTypeID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: Delivery
--------------------------------------------------
IF OBJECT_ID('dbo.Delivery', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Delivery] (
        [DeliveryID] INT NOT NULL PRIMARY KEY,
        [DeliveryTypeID] INT NOT NULL,
        CONSTRAINT [FK_Delivery_DeliveryType] FOREIGN KEY ([DeliveryTypeID])
            REFERENCES [dbo].[DeliveryType] ([DeliveryTypeID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: Debt
--------------------------------------------------
IF OBJECT_ID('dbo.Debt', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Debt] (
        [DebtID] INT NOT NULL PRIMARY KEY,
        [DebtDescription] VARCHAR(45) NOT NULL
    );
END
GO

--------------------------------------------------
-- Table: PromotionType
--------------------------------------------------
IF OBJECT_ID('dbo.PromotionType', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[PromotionType] (
        [PromotionTypeID] INT NOT NULL PRIMARY KEY
    );
END
GO

--------------------------------------------------
-- Table: Promotions
--------------------------------------------------
IF OBJECT_ID('dbo.Promotions', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Promotions] (
        [PromotionID] INT NOT NULL PRIMARY KEY,
        [PromotionTypeID] INT NOT NULL,
        [Name] VARCHAR(45) NULL,
        [Discount] VARCHAR(45) NULL,
        CONSTRAINT [FK_Promotions_PromotionType] FOREIGN KEY ([PromotionTypeID])
            REFERENCES [dbo].[PromotionType] ([PromotionTypeID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: Orders
--------------------------------------------------
IF OBJECT_ID('dbo.Orders', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Orders] (
        [OrderID] INT NOT NULL PRIMARY KEY,
        [OrderStatusID] INT NOT NULL,
        [OrderTypeID] INT NOT NULL,
        [DeliveryID] INT NOT NULL,
        [ClientID] INT NOT NULL,
        [DebtID] INT NOT NULL,
        [PromotionID] INT NOT NULL,
        [EmployeeID] INT NOT NULL,
        [BranchID] INT NOT NULL,
        [OrderDate] VARCHAR(45) NULL,
        [Comments] VARCHAR(45) NULL,
        [InvoiceNumber] VARCHAR(45) NULL,
        CONSTRAINT [FK_Orders_OrderStatus] FOREIGN KEY ([OrderStatusID])
            REFERENCES [dbo].[OrderStatus] ([OrderStatusID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Orders_OrderType] FOREIGN KEY ([OrderTypeID])
            REFERENCES [dbo].[OrderType] ([OrderTypeID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Orders_Delivery] FOREIGN KEY ([DeliveryID])
            REFERENCES [dbo].[Delivery] ([DeliveryID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Orders_Clients] FOREIGN KEY ([ClientID])
            REFERENCES [dbo].[Clients] ([ClientID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Orders_Debt] FOREIGN KEY ([DebtID])
            REFERENCES [dbo].[Debt] ([DebtID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Orders_Promotions] FOREIGN KEY ([PromotionID])
            REFERENCES [dbo].[Promotions] ([PromotionID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Orders_Employee] FOREIGN KEY ([EmployeeID])
            REFERENCES [dbo].[Employee] ([EmployeeID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Orders_Branch] FOREIGN KEY ([BranchID])
            REFERENCES [dbo].[Branch] ([BranchID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: Payment
--------------------------------------------------
IF OBJECT_ID('dbo.Payment', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Payment] (
        [PaymentID] INT NOT NULL PRIMARY KEY,
        [PaymentTypeID] INT NOT NULL,
        [PaymentStatusID] INT NOT NULL,
        [OrderID] INT NOT NULL,
        CONSTRAINT [FK_Payment_PaymentType] FOREIGN KEY ([PaymentTypeID])
            REFERENCES [dbo].[PaymentType] ([PaymentTypeID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Payment_PaymentStatus] FOREIGN KEY ([PaymentStatusID])
            REFERENCES [dbo].[PaymentStatus] ([PaymentStatusID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_Payment_Orders] FOREIGN KEY ([OrderID])
            REFERENCES [dbo].[Orders] ([OrderID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: ProductCategory
--------------------------------------------------
IF OBJECT_ID('dbo.ProductCategory', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[ProductCategory] (
        [ProductCategoryID] INT NOT NULL PRIMARY KEY,
        [CategoryDescription] VARCHAR(45) NOT NULL
    );
END
GO

--------------------------------------------------
-- Table: Product
--------------------------------------------------
IF OBJECT_ID('dbo.Product', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Product] (
        [ProductID] INT NOT NULL PRIMARY KEY,
        [ProductStatusID] INT NOT NULL,
        [ProductCategoryID] INT NOT NULL,
        CONSTRAINT [FK_Product_ProductCategory] FOREIGN KEY ([ProductCategoryID])
            REFERENCES [dbo].[ProductCategory] ([ProductCategoryID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: SupplyComposition
--------------------------------------------------
IF OBJECT_ID('dbo.SupplyComposition', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[SupplyComposition] (
        [SupplyCompositionID] INT NOT NULL PRIMARY KEY,
        [SupplyID] INT NOT NULL,
        [ProductID] INT NOT NULL,
        [Price] VARCHAR(45) NULL,
        [Quantity] VARCHAR(45) NULL,
        CONSTRAINT [FK_SupplyComposition_Supplies] FOREIGN KEY ([SupplyID])
            REFERENCES [dbo].[Supplies] ([SupplyID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_SupplyComposition_Product] FOREIGN KEY ([ProductID])
            REFERENCES [dbo].[Product] ([ProductID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: DebtCopy1
--------------------------------------------------
IF OBJECT_ID('dbo.DebtCopy1', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[DebtCopy1] (
        [DebtID] INT NOT NULL PRIMARY KEY,
        [DebtDescription] VARCHAR(45) NOT NULL
    );
END
GO

--------------------------------------------------
-- Table: ProductWriteOff
--------------------------------------------------
IF OBJECT_ID('dbo.ProductWriteOff', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[ProductWriteOff] (
        [WriteOffID] INT NOT NULL PRIMARY KEY,
        [SupplyCompositionID] INT NOT NULL,
        [EmployeeID] INT NOT NULL,
        CONSTRAINT [FK_ProductWriteOff_SupplyComposition] FOREIGN KEY ([SupplyCompositionID])
            REFERENCES [dbo].[SupplyComposition] ([SupplyCompositionID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_ProductWriteOff_Employee] FOREIGN KEY ([EmployeeID])
            REFERENCES [dbo].[Employee] ([EmployeeID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: Salary
--------------------------------------------------
IF OBJECT_ID('dbo.Salary', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[Salary] (
        [SalaryID] INT NOT NULL PRIMARY KEY,
        [SalaryDescription] VARCHAR(45) NOT NULL,
        [EmployeeID] INT NOT NULL,
        CONSTRAINT [FK_Salary_Employee] FOREIGN KEY ([EmployeeID])
            REFERENCES [dbo].[Employee] ([EmployeeID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: OrderComposition
--------------------------------------------------
IF OBJECT_ID('dbo.OrderComposition', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[OrderComposition] (
        [OrderCompositionID] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
        [OrderCompositionDescription] VARCHAR(45) NULL,
        [OrderID] INT NOT NULL,
        [SupplyCompositionID] INT NOT NULL,
        [OrderCompound] VARCHAR(45) NULL,
        [Quantity] VARCHAR(45) NULL,
        CONSTRAINT [FK_OrderComposition_Orders] FOREIGN KEY ([OrderID])
            REFERENCES [dbo].[Orders] ([OrderID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION,
        CONSTRAINT [FK_OrderComposition_SupplyComposition] FOREIGN KEY ([SupplyCompositionID])
            REFERENCES [dbo].[SupplyComposition] ([SupplyCompositionID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- Table: PriceList
--------------------------------------------------
IF OBJECT_ID('dbo.PriceList', 'U') IS NULL
BEGIN
    CREATE TABLE [dbo].[PriceList] (
        [OrderID] INT NOT NULL,
        [Price] VARCHAR(45) NULL,
        [Date] VARCHAR(45) NULL,
        [PriceReason] VARCHAR(45) NULL,
        CONSTRAINT [FK_PriceList_Orders] FOREIGN KEY ([OrderID])
            REFERENCES [dbo].[Orders] ([OrderID])
            ON DELETE NO ACTION
            ON UPDATE NO ACTION
    );
END
GO

--------------------------------------------------
-- 2. Вставка тестовых данных
--------------------------------------------------

-- Insert one Branch record
IF NOT EXISTS (SELECT 1 FROM [dbo].[Branch] WHERE [BranchID] = 1)
BEGIN
    INSERT INTO [dbo].[Branch] ([BranchID])
    VALUES (1);
END
GO

-- Insert one Position record
IF NOT EXISTS (SELECT 1 FROM [dbo].[Position] WHERE [PositionID] = 1)
BEGIN
    INSERT INTO [dbo].[Position] ([PositionID])
    VALUES (1);
END
GO

-- Insert one ClientType record
IF NOT EXISTS (SELECT 1 FROM [dbo].[ClientType] WHERE [ClientTypeID] = 1)
BEGIN
    INSERT INTO [dbo].[ClientType] ([ClientTypeID])
    VALUES (1);
END
GO

--------------------------------------------------
-- Insert 3 Employees
--------------------------------------------------
INSERT INTO [dbo].[Employee] ([EmployeeID], [BranchID], [PositionID], [FirstName], [LastName], [INN], [Password], [Login], [Salary], [Role])
VALUES 
(1, 1, 1, 'John', 'Doe', '123456789', 'pass1', 'jdoe', '50000', 'Employee'),
(2, 1, 1, 'Alice', 'Smith', '987654321', 'pass2', 'asmith', '55000', 'Employee'),
(3, 1, 1, 'Bob', 'Brown', '555666777', 'pass3', 'bbrown', '60000', 'Employee');
GO

--------------------------------------------------
-- Insert Administrator record (для регистрации сотрудников)
--------------------------------------------------
IF NOT EXISTS (SELECT 1 FROM [dbo].[Employee] WHERE [Login] = 'admin')
BEGIN
    INSERT INTO [dbo].[Employee] ([EmployeeID], [BranchID], [PositionID], [FirstName], [LastName], [INN], [Password], [Login], [Salary], [Role])
    VALUES (999, 1, 1, 'Admin', 'User', '000000000', 'admin123', 'admin', '0', 'Administrator');
END
GO

--------------------------------------------------
-- Insert 5 Clients
--------------------------------------------------
INSERT INTO [dbo].[Clients] ([ClientID], [ClientTypeID], [District], [Activity], [LastName], [FirstName], [MiddleName], [BirthDate], [RegistrationDate], [Login], [Password])
VALUES
(1, 1, 'District A', 'Retail', 'Johnson', 'Michael', 'A.', '1980-01-15', CONVERT(VARCHAR(45), GETDATE(), 120), 'mjohnson', 'pass1'),
(2, 1, 'District B', 'IT', 'Connor', 'Sarah', 'B.', '1985-05-20', CONVERT(VARCHAR(45), GETDATE(), 120), 'sconnor', 'pass2'),
(3, 1, 'District C', 'Manufacturing', 'Lee', 'David', 'C.', '1978-09-10', CONVERT(VARCHAR(45), GETDATE(), 120), 'dlee', 'pass3'),
(4, 1, 'District D', 'Design', 'Watson', 'Emma', 'D.', '1990-12-05', CONVERT(VARCHAR(45), GETDATE(), 120), 'ewatson', 'pass4'),
(5, 1, 'District E', 'Finance', 'Twist', 'Oliver', 'E.', '1982-03-25', CONVERT(VARCHAR(45), GETDATE(), 120), 'otwist', 'pass5');
GO

--------------------------------------------------
-- 3. Создание хранимых процедур
--------------------------------------------------

-- Процедура для регистрации нового клиента (с требуемыми полями)
IF OBJECT_ID('dbo.spRegisterClient', 'P') IS NOT NULL
    DROP PROCEDURE dbo.spRegisterClient;
GO

CREATE PROCEDURE [dbo].[spRegisterClient]
    @ClientID INT,
    @ClientTypeID INT,
    @District VARCHAR(45),
    @Activity VARCHAR(45),
    @LastName VARCHAR(45),
    @FirstName VARCHAR(45),
    @MiddleName VARCHAR(45),
    @BirthDate DATE,
    @Login VARCHAR(45),
    @Password VARCHAR(45)
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRY
        INSERT INTO [dbo].[Clients] (
            [ClientID],
            [ClientTypeID],
            [District],
            [Activity],
            [LastName],
            [FirstName],
            [MiddleName],
            [BirthDate],
            [RegistrationDate],
            [Login],
            [Password]
        )
        VALUES (
            @ClientID,
            @ClientTypeID,
            @District,
            @Activity,
            @LastName,
            @FirstName,
            @MiddleName,
            @BirthDate,
            CONVERT(VARCHAR(45), GETDATE(), 120), -- Текущая дата регистрации
            @Login,
            @Password
        );

        SELECT 'Client registered successfully' AS Result;
    END TRY
    BEGIN CATCH
        SELECT ERROR_MESSAGE() AS ErrorMessage;
    END CATCH
END
GO

-- Процедура для регистрации нового сотрудника (требует, чтобы вызывающий был администратором)
IF OBJECT_ID('dbo.spRegisterEmployee', 'P') IS NOT NULL
    DROP PROCEDURE dbo.spRegisterEmployee;
GO

CREATE PROCEDURE [dbo].[spRegisterEmployee]
    @CallerLogin VARCHAR(45),  -- логин администратора, вызывающего процедуру
    @EmployeeID INT,
    @BranchID INT,
    @PositionID INT,
    @FirstName VARCHAR(45),
    @LastName VARCHAR(45),
    @INN VARCHAR(45),
    @Password VARCHAR(45),
    @Login VARCHAR(45),
    @Salary VARCHAR(45)
AS
BEGIN
    SET NOCOUNT ON;
    DECLARE @CallerRole VARCHAR(20);

    -- Проверка роли вызывающего (должна быть Administrator)
    SELECT @CallerRole = [Role]
    FROM [dbo].[Employee]
    WHERE [Login] = @CallerLogin;

    IF (@CallerRole <> 'Administrator')
    BEGIN
        SELECT 'Access denied: Only administrators can register employees.' AS Result;
        RETURN;
    END

    BEGIN TRY
        INSERT INTO [dbo].[Employee] (
            [EmployeeID],
            [BranchID],
            [PositionID],
            [FirstName],
            [LastName],
            [INN],
            [Password],
            [Login],
            [Salary],
            [Role]
        )
        VALUES (
            @EmployeeID,
            @BranchID,
            @PositionID,
            @FirstName,
            @LastName,
            @INN,
            @Password,
            @Login,
            @Salary,
            'Employee'
        );

        SELECT 'Employee registered successfully' AS Result;
    END TRY
    BEGIN CATCH
        SELECT ERROR_MESSAGE() AS ErrorMessage;
    END CATCH
END
GO

-- Процедура авторизации пользователя (Client или Employee)
IF OBJECT_ID('dbo.spAuthorizeUser', 'P') IS NOT NULL
    DROP PROCEDURE dbo.spAuthorizeUser;
GO

CREATE PROCEDURE [dbo].[spAuthorizeUser]
    @UserType VARCHAR(10),   -- 'Client' или 'Employee'
    @Login VARCHAR(45),
    @Password VARCHAR(45)
AS
BEGIN
    SET NOCOUNT ON;

    IF (@UserType = 'Client')
    BEGIN
        SELECT COUNT(*) AS UserCount
        FROM [dbo].[Clients]
        WHERE [Login] = @Login
          AND [Password] = @Password;
    END
    ELSE IF (@UserType = 'Employee')
    BEGIN
        SELECT COUNT(*) AS UserCount
        FROM [dbo].[Employee]
        WHERE [Login] = @Login
          AND [Password] = @Password;
    END
    ELSE
    BEGIN
        SELECT -1 AS UserCount;  -- Неверный тип пользователя
    END
END
GO
