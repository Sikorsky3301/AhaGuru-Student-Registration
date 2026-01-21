# MySQL Setup Instructions for Django Project

## Step 1: Install MySQL Python Client

You need to install a MySQL adapter for Python. Choose one of these options:

### Option A: Using mysqlclient (Recommended, but requires MySQL development libraries)
```bash
pip install mysqlclient
```

### Option B: Using PyMySQL (Easier, no additional dependencies)
```bash
pip install PyMySQL
```

If using PyMySQL, you also need to add this to your `core/core/__init__.py`:
```python
import pymysql
pymysql.install_as_MySQLdb()
```

## Step 2: Create the MySQL Database

1. Open MySQL Command Line or MySQL Workbench
2. Connect to your MySQL server
3. Run this command to create the database:
```sql
CREATE DATABASE edtech_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

## Step 3: Update Django Settings with Your MySQL Credentials

Edit `core/core/settings.py` and update the DATABASES section:
- Replace `"USER": "root"` with your MySQL username
- Replace `"PASSWORD": ""` with your MySQL password

## Step 4: Run the SQL Script to Create the Table

### Option A: Using MySQL Command Line
```bash
mysql -u root -p edtech_db < sql_scripts/student_table.sql
```

### Option B: Using MySQL Workbench
1. Open MySQL Workbench
2. Connect to your MySQL server
3. Select the `edtech_db` database
4. Open the file `sql_scripts/student_table.sql`
5. Execute the script (Ctrl+Shift+Enter or click Execute)

### Option C: Copy-paste in MySQL Command Line
1. Open MySQL Command Line
2. Connect: `mysql -u root -p`
3. Use the database: `USE edtech_db;`
4. Copy and paste the contents of `sql_scripts/student_table.sql`
5. Press Enter to execute

## Step 5: Test Django Connection

Run this command to test if Django can connect to MySQL:
```bash
cd core
python manage.py check --database default
```

If successful, you should see "System check identified no issues".

## Troubleshooting

- **Error: "No module named 'MySQLdb'"**: Install mysqlclient or PyMySQL (see Step 1)
- **Error: "Access denied"**: Check your MySQL username and password in settings.py
- **Error: "Unknown database"**: Make sure you created the `edtech_db` database (Step 2)
- **Error: "Table already exists"**: The table was already created. You can drop it first with `DROP TABLE student;` if needed

