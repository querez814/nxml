from sec_edgar_downloader import Downloader



dl = Downloader("MyCompanyName", "myemail@gmail.com", "C:/Users/quere/DEV/Projects/svfin/backend/sec/filings/notables/nvda")
def dl_file():
    return dl.get("10-Q", "NVDA", limit=20, download_details=False)



if __name__ == "__main__":
    dl_file()