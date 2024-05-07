from robocorp.tasks import task
from robocorp import browser
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from RPA.PDF import PDF
from RPA.Browser.Selenium import Selenium
from RPA.Archive import Archive
import time





@task
def order_robots_from_RobotSpareBin():
    """
    Orders robots from RobotSpareBin Industries Inc.
    Saves the order HTML receipt as a PDF file.
    Saves the screenshot of the ordered robot.
    Embeds the screenshot of the robot to the PDF receipt.
    Creates ZIP archive of the receipts and the images.
    """
    url="https://robotsparebinindustries.com/#/robot-order"
    open_robot_order_website(url)
    close_annoying_modal()
    
    orders = get_orders("orders.csv")
    

def get_orders(filename):
    http = HTTP()
    http.download(url="https://robotsparebinindustries.com/orders.csv", overwrite=True)
    table = Tables()
    csv = table.read_table_from_csv(filename, header=True)

    for row in csv :
              
        try:
            fill_the_form(row)
            page = browser.page()
            page.focus("#order-another")
        except:
            page.reload
            fill_the_form(row)
            page = browser.page()
            
            
        store_receipt_as_pdf(row["Order number"])
        page.click("#order-another")
        close_annoying_modal()
        
    archive_receipts()
    return csv

def fill_the_form(row):
    page = browser.page()
   
    page.select_option("#head", str(row["Head"]))
    page.click("#id-body-"+str(row["Body"]))
    page.fill("xpath=/html/body/div[1]/div/div[1]/div/div[1]/form/div[3]/input", str(row["Legs"]))
    page.fill("#address", row["Address"])
    
    page.click("#order")

def close_annoying_modal():
    page = browser.page()
    page.click("text=OK")

def open_robot_order_website(url):
    browser.configure(
        slowmo=100,
    )
    browser.goto(url)

def store_receipt_as_pdf(order_number):
    page = browser.page()
    receipt = page.locator("#receipt").inner_html()
    pdf = PDF()
    pdf.html_to_pdf(receipt, "output/receipts/"+str(order_number)+".pdf")

def archive_receipts():
    lib = Archive()
    lib.archive_folder_with_zip("./output/receipts","./output/receipts.zip", recursive=True)