📌 METHODS USED IN BILL PDF GENERATION
======================================

Categorized by Module with Purpose & Description
------------------------------------------------

1️⃣ **FPDF MODULE (from fpdf import FPDF)**
-------------------------------------------

This module is used to **programmatically create PDF documents** in Python.

### 🔹 FPDF()

**Module:** fpdf**Type:** Class constructor

**Why used:** Creates a new PDF document object in memory.

**What it does:** Initializes an empty PDF file that we can add pages, text, tables, and formatting to.

### 🔹 pdf.add\_page()

**Module:** fpdf

**Why used:** A PDF must have at least one page before adding content.

**What it does:** Adds a new blank page to the PDF.

### 🔹 pdf.set\_auto\_page\_break(auto=True, margin=15)

**Module:** fpdf

**Why used:** Prevents content from overflowing outside the page.

**What it does:** Automatically adds a new page when content reaches the bottom margin.

### 🔹 pdf.set\_font(family, style, size)

**Module:** fpdf

**Why used:** Controls text appearance (font type, bold/italic, size).

**What it does:** Sets the font for all text printed after this call.

Example:

```
pdf.set_font("Arial", "B", 20)
```
### 🔹 pdf.cell(width, height, text, border, ln, align)

**Module:** fpdf

**Why used:** This is the **core method** for printing text and tables.

**What it does:** Creates a rectangular cell and prints text inside it.

Used for:

*   Titles
    
*   Customer details
    
*   Table headers
    
*   Table rows
    
*   Totals
    

### 🔹 pdf.ln(height)

**Module:** fpdf

**Why used:** Controls vertical spacing.

**What it does:** Moves the cursor down by a specified height.

### 🔹 pdf.output(file\_name)

**Module:** fpdf

**Why used:** Saves the PDF to disk.

**What it does:** Writes the in-memory PDF content into a .pdf file.

2️⃣ **MYSQL.CONNECTOR MODULE (import mysql.connector)**
-------------------------------------------------------

Used for **database connectivity and data retrieval**.

### 🔹 mysql.connector.connect()

**Module:** mysql.connector

**Why used:** Establishes a connection between Python and MySQL.

**What it does:** Creates a live database session using host, username, password, and database name.

### 🔹 conn\_obj.cursor()

**Module:** mysql.connector

**Why used:** Required to execute SQL queries.

**What it does:** Creates a cursor object that sends SQL commands to MySQL.

### 🔹 cur\_obj.execute(query, params)

**Module:** mysql.connector

**Why used:** Executes SQL queries securely.

**What it does:** Runs parameterized SQL queries and prevents SQL injection.

### 🔹 cur\_obj.fetchone()

**Module:** mysql.connector

**Why used:** Fetches a single database record.

**What it does:** Returns one row as a tuple (used for bill summary).

### 🔹 cur\_obj.fetchall()

**Module:** mysql.connector

**Why used:** Fetches multiple records.

**What it does:** Returns all matching rows as a list of tuples (used for product items).

3️⃣ **OS MODULE (import os)**
-----------------------------

Used for **system-level file handling**.

### 🔹 os.startfile(file\_name)

**Module:** os

**Why used:** Automatically opens the generated PDF in Windows.

**What it does:** Opens the file using the system’s default PDF viewer.

4️⃣ **SYS MODULE (import sys)**
-------------------------------

Used for **platform detection**.

### 🔹 sys.platform

**Module:** sys

**Why used:** To detect the operating system.

**What it does:** Returns platform identifier like:

*   win32 → Windows
    
*   darwin → macOS
    
*   linux → Linux
    

5️⃣ **SUBPROCESS MODULE (import subprocess)**
---------------------------------------------

Used for **executing system commands**.

### 🔹 subprocess.call(command)

**Module:** subprocess

**Why used:** To open files on macOS and Linux.

**What it does:** Runs OS-level commands like:

```
open Bill.pdf
xdg-open Bill.pdf
```

6️⃣ **PYTHON BUILT-IN FEATURES**
--------------------------------

### 🔹 Tuple Unpacking

```
bill_id, cust_name, ph_no, total_amt, final_amt, bill_date = bill_summary

```
**Why used:** Improves readability and avoids index-based access.

**What it does:** Assigns each value from the database row tuple to a variable.

### 🔹 f-Strings

```
f"Bill No: {bill_id}"

```
**Why used:** Clean and readable string formatting.

**What it does:** Inserts variable values directly into strings.

### 🔹 Exception Handling

```
try:
    ...
except Exception as e:

```
**Why used:** Prevents program crash during auto-open.

**What it does:** Safely handles OS-level errors.
