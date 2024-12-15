How to run Flask Backend API server:
1. Create virtual environment:
- From VSCode, press Ctrl + P, type ">Python: Create Environment" and choose the selection
- Choose Venv, Python version and check the checkbox of requirements.txt
- Wait for VSCode create, active virtual environment and install essential library
2. Create database:
- Install MySQL
- Create user with username is "root" and password is "12345"
- Run MySQL Workbench, connect to localinstance using username and password created above
- Choose Data Import/Restore
- Choose Import from Self-Contained File and choose Dump.sql file from this folder
- Create a new Schema called "ShoppingAssistant"
- Click "Start Import"
3. Run server
- From VSCode terminal (virtual environment activated), type "flask run --cert=cert.pem --key=key.pem --debug"
- You can access the api from frontend or test api from Postman, ... now

Link github
