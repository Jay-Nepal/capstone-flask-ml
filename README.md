## Code repo for Capstone LightXpense project

### What it accomplishes
- A smart and efficient solution to classifying and extracting live data for employee expense re-imbursement
- Utilizing OCR and ML, enables SME companies to quickly deploy a solution to make expense re-imbursement efficient whilst also,
- Providing a smart and live data view of expense re-imbursement

### Where it is deployed:
- Currently we maintain it at http://lightxpense.fast-page.org/

### How to deploy:
- Change the mySQL DB connection in db_connection.php file to your SQL table, and you should be good to go!
- For specific database table schema, you could reverse engineer it from the HTML files or reach out to one of the team members.
- For local testing purposes, remove db_connection.php and all other php linkage to that file.
    - Note that this will remove functionalities related to database (login, register and personalization)
    - But you can test ML, OCR and other flow locally
  
### Meet the team:
- Tai Yong Xin
- Low Kah Kheng
- Aarogya Banepali
- Siow Zi Ting
- Yoon Yen Wei
