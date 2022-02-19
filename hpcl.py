from http import cookies
from time import sleep
from turtle import color
import requests
from bs4 import BeautifulSoup
from os import path, remove
import pickle
from rich import print
import sys
from rich.console import Console


login_url =  'https://sales.hpcl.co.in/bportal/login/cust_login_ads.jsp' 
balcheck_url = 'https://sales.hpcl.co.in/bportal/retail/account_bal.jsp'
login_header = {
  'Content-Type': 'application/x-www-form-urlencoded' ,
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36' ,
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9' }
login_file = "hpcl.session"

r = requests.Session()
if path.isfile(login_file) == False:
    print("no login file found, creating one .....")
    username = input("Enter dealer id : ")
    password = input("Enter password : ")
    login_creds = f'cust_id={username}&pwd={password}' 
    st = r.post(login_url, data=login_creds, headers=login_header)
    if 'open("../login/invalid.html", "_self");' in st.text:
        print("[red]Incorrect Credentials[/red]")
        exit(0)
    with open(login_file, 'wb') as f:
        pickle.dump(r.cookies, f)
else:
    try:
        with open(login_file, 'rb') as f:
            r.cookies.update(pickle.load(f))
    except Exception as e:
        print("got error, removing session file")
        remove(login_file)
        exit(0)

console = Console()
with console.status("Checking balance....", spinner="aesthetic") as status:
    for i in range(0, int(sys.argv[1])):
        bal = r.get(balcheck_url, cookies=r.cookies)
        s = BeautifulSoup(bal.content, 'html.parser')
        last_update = s.table.tbody.find_all("tr")[2].find_all("td")[1].text
        balance = s.table.tbody.find_all("tr")[1].find_all("td")[1].text
        color = "red"
        if float(balance) > 0:
            color = "red"
        else:
            color = "blue"
        console.print(f'[bold {color}]{balance}[/bold {color}]')
        console.print(f'[bold]Last updated on[/bold] {last_update}')
        sleep(int(sys.argv[2]))