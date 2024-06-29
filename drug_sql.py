-- Create customer table
CREATE TABLE IF NOT EXISTS customer (
  uid TEXT NOT NULL PRIMARY KEY,
  pass TEXT DEFAULT NULL,
  fname TEXT DEFAULT NULL,
  lname TEXT DEFAULT NULL,
  email TEXT DEFAULT NULL,
  address TEXT DEFAULT NULL,
  phno INTEGER DEFAULT NULL
);

-- Create seller table
CREATE TABLE IF NOT EXISTS seller (
  sid TEXT NOT NULL PRIMARY KEY,
  sname TEXT DEFAULT NULL,
  pass TEXT DEFAULT NULL,
  address TEXT DEFAULT NULL,
  phno INTEGER DEFAULT NULL
);

-- Create product table
CREATE TABLE IF NOT EXISTS product (
  pid TEXT NOT NULL PRIMARY KEY,
  pname TEXT DEFAULT NULL UNIQUE,
  manufacturer TEXT DEFAULT NULL,
  mfg DATE DEFAULT NULL,
  exp DATE DEFAULT NULL,
  price INTEGER DEFAULT NULL
);

-- Create inventory table
CREATE TABLE IF NOT EXISTS inventory (
  pid TEXT NOT NULL,
  pname TEXT DEFAULT NULL,
  quantity INTEGER DEFAULT NULL,
  sid TEXT NOT NULL,
  PRIMARY KEY (pid, sid),
  FOREIGN KEY (pid) REFERENCES product (pid) ON DELETE CASCADE,
  FOREIGN KEY (pname) REFERENCES product (pname) ON DELETE CASCADE,
  FOREIGN KEY (sid) REFERENCES seller (sid) ON DELETE CASCADE
);

-- Create orders table
CREATE TABLE IF NOT EXISTS orders (
  oid INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  pid TEXT DEFAULT NULL,
  sid TEXT DEFAULT NULL,
  uid TEXT DEFAULT NULL,
  orderdatetime TEXT DEFAULT NULL,
  quantity INTEGER DEFAULT NULL,
  price INTEGER DEFAULT NULL,
  FOREIGN KEY (pid) REFERENCES product (pid) ON DELETE CASCADE,
  FOREIGN KEY (sid) REFERENCES seller (sid) ON DELETE CASCADE,
  FOREIGN KEY (uid) REFERENCES customer (uid) ON DELETE CASCADE
);

-- Trigger to update orderdatetime before inserting an order
CREATE TRIGGER IF NOT EXISTS updatetime BEFORE INSERT ON orders
FOR EACH ROW
BEGIN
  UPDATE orders SET orderdatetime = datetime('now') WHERE oid = NEW.oid;
END;

-- Trigger to update inventory after inserting an order
CREATE TRIGGER IF NOT EXISTS inventorytrigger AFTER INSERT ON orders
FOR EACH ROW
BEGIN
  UPDATE inventory
  SET quantity = quantity - NEW.quantity
  WHERE pid = NEW.pid;
END;
