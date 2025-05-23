import os
import random
import time
from datetime import datetime

from playwright.async_api import async_playwright

from config import loadEnv

loadEnv()
url = os.getenv("URL")
print(url)


# Human-like delay function
def delay(minSeconds=1.5, maxSeconds=2.5):
    time.sleep(random.uniform(minSeconds, maxSeconds))


async def SecEdgerAsync(companyName: str):
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(java_script_enabled=True, viewport=None)
        page = await context.new_page()

        # Navigate to SEC EDGAR
        await page.goto(url, wait_until="domcontentloaded")
        print(f"✅ {companyName} - Page loaded")

        # Click on "Show Full Search Form"
        await page.locator("a#show-full-search-form").click()
        print(f"✅ {companyName} - Show Full Search clicked")
        delay()

        # Fill in company name
        await page.locator("input#entity-full-form").fill(companyName)
        print(f"✅ {companyName} - Company name entered")
        delay()

        # Press Enter
        await page.locator("input#entity-full-form").press("Enter")
        print(f"✅ {companyName} - Enter pressed")
        await page.wait_for_timeout(2000)

        # Select Date Range
        await page.locator("select#date-range-select").select_option(value="1y")
        print(f"✅ {companyName} - Date range set to 'All'")
        delay()

        # Wait for results table to load
        await page.wait_for_selector(
            "table.table tbody tr td.filetype a", timeout=20000
        )

        # List of filing types we care about
        targetFilings = {
            "10-K": "Annual Report",
            "10-Q": "Quarterly Report",
            "8-K": "Current Report",
            "DEF 14A": "Proxy Statement",
            "SC 13D": "Schedule 13D",
            "SC 13G": "Schedule 13G",
            "ARS": "Annual Report",
            "4": "Insider trading report",
            "F-4": "Registration Statement",
            "S-1": "Registration Statement",
            "424B5": "Prospectus",
            "144": "Securities Offered Pursuant to Rule 144",
            "PRE 14A": "Preliminary Proxy Statement",
        }

        # Scrape filing data
        filingRows = await page.locator("table.table tbody tr").all()

        latestFilings = {}  # To store latest filing per type

        for row in filingRows:
            link_elem = row.locator("td.filetype a").first
            if await link_elem.count() == 0:
                continue
            link = await link_elem.get_attribute("href")
            text = await link_elem.inner_text()
            dateStr = await row.locator("td.filed").inner_text()
            print("DateFiled:", dateStr)
            # Try parsing date
            try:
                dateObject = datetime.strptime(dateStr, "%Y-%m-%d")
            except ValueError:
                dateObject = datetime.min

            # Try to extract base filing tag
            filingTag = text.split()[0]

            # If it's one of our target filings
            if filingTag in targetFilings:
                if (
                    filingTag not in latestFilings
                    or dateObject > latestFilings[filingTag]["date"]
                ):
                    latestFilings[filingTag] = {
                        "full_text": text,
                        "link": link,
                        "date": dateObject,
                    }

        print(f"📄 Found {len(latestFilings)} matching filings.")

        # Create download directory
        downloadDirectory = os.path.join("downloads", companyName)
        os.makedirs(downloadDirectory, exist_ok=True)

        # Download each latest filing
        for _, filing in latestFilings.items():
            print(f"🖨️ Opening: {filing['full_text']} ({filing['date']})")

            new_page = await context.new_page()
            await new_page.goto(filing["link"], wait_until="networkidle")

            safe_title = filing["full_text"].replace("/", "_").replace(" ", "_")
            pdf_path = os.path.join(
                downloadDirectory,
                f"{safe_title}_{filing['date'].strftime('%Y%m%d')}.pdf",
            )

            await new_page.pdf(path=pdf_path, format="Letter", print_background=True)
            print(f"💾 Saved PDF: {pdf_path}")

            await new_page.close()
            delay(1, 2)

        await context.close()
        await browser.close()
        print(f"✅ {companyName} - Browser closed")


#  10-K (Annual Reporting)
#  10-Q, (Quarterly Reporting)
#  8-K (Recent Filings)
#  Form-4 (Insider Buying)
#  DEF 14A (Proxy Statements),
#  13F (Institutional Holdings)
#  13D/13G   (Activist Ownership)
#  S-1 (IPO Stock)
#  S-1 (IPO Stock)
