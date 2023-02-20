# Data Warehousing

Hi. This is the repository for a data warehousing project I completed at NYU. The project consisted of taking a CSV file and transferring it into a data warehouse.

---

**Project Title:** Simple ETL Transfer to Data Warehouse

**Project Description:** In this project I used Oracle SQL Developer to take a CSV file and import it into a stage table. Then I used Oracle SQL Data Modeler to create a data model for my data warehouse (OLAP). The data warehouse included a central fact/data table and three additional tables. I then used SQL to transfer the data from the stage table into the data warehouse, where the intent was to increase redundancy (opposed to OLTP systems). The second part of the project consisted of creating views in Oracle for different queries such as Top-N queries and aggregate functions.