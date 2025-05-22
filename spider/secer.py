import random
import time
from datetime import datetime

from playwright.async_api import async_playwright

URL: str = "https://www.sec.gov/edgar/search/#"


# def SecEdger(companyName: str):
#     with sync_playwright() as p:
#         browser = p.chromium.launch(headless=False)  # Remove if not needed)
#         context = browser.new_context(java_script_enabled=True, viewport=None)
#         page = context.new_page()
#         page.goto(URL, wait_until="domcontentloaded")
#         page.locator("a#show-full-search-form").click()
#         page.locator("input#entity-full-form").fill(companyName)
#         page.wait_for_timeout(1000)
#         page.locator("input#entity-full-form").press("Enter")

#         # Selecting Date
#         page.locator("select#date-range-select").select_option(value="1y")
#         page.locator("select#date-range-select").evaluate("el => el.value")

#         # Filing Types
#         page.locator("span#show-filing-types").click()
#         page.wait_for_timeout(1000)
#         page.locator(".custom-control-label").all_inner_texts()
#         filings: list[str] = [
#             "10-K",
#             "10-Q",
#             "8-K",
#             "DEF 14A",
#             "F-4",
#             "S-1",
#             "SC 13D",
#             "SC 13G",
#         ]
#         for label in filings:
#             try:
#                 page.check(f"label:has-text('{label}')")
#                 print(f"✅ Checked box: {label}")
#             except ValueError as e:
#                 print(f"❌ Could not find checkbox for: {label} | Error: {str(e)}")
#         page.click("#custom_forms_set")
#         print("✅ Filtered....")
#         page.pause()
#         browser.close()


# Human-like delay function
def delay(minSeconds: float = 0.5, maxSeconds: float = 1.5):
    ranDelay = random.uniform(minSeconds, maxSeconds)
    time.sleep(ranDelay)


async def SecEdgerAsync(companyName: str):
    async with async_playwright() as p:
        # Launch browser (set headless=True for production)
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context(java_script_enabled=True, viewport=None)
        page = await context.new_page()

        # Navigate to SEC EDGAR
        await page.goto(URL, wait_until="domcontentloaded")
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
        await page.wait_for_timeout(2000)  # Wait 2 seconds after typing

        # Select Date Range
        await page.locator("select#date-range-select").select_option(value="1y")
        print(f"✅ {companyName} - Date range set to 1 year")
        delay()

        # Click "Browse filing types"
        await page.locator("span#show-filing-types").click()
        print(f"✅ {companyName} - Show filing types clicked")
        delay()

        # Wait for modal checkboxes to appear
        await page.wait_for_selector("label.custom-control-label", timeout=10000)

        # List of filings you want to check
        filings = [
            "10-K",
            "10-Q",
            "8-K",
            "DEF 14A",
            "F-4",
            "S-1",
            "SC 13D",
            "SC 13G",
        ]

        # Check each checkbox with a small delay between them
        for label in filings:
            try:
                locator = f"label:has-text('{label}')"
                await page.wait_for_selector(locator, timeout=10000)
                await page.check(locator)
                print(f"✅ {companyName} - Checked box: {label}")
                delay(0.3, 0.8)  # Small delay between checkbox clicks
            except ValueError as e:
                print(
                    f"❌ {companyName} - Could not find checkbox for: {label} | Error: {str(e)}"
                )

        # Click Filter button
        await page.click("#custom_forms_set")
        print(f"✅ {companyName} - Filter button clicked")
        delay()

        # Wait for filing table to load
        await page.wait_for_selector("table.table tbody tr td.filetype a")

        # Scrape filing data
        filingRows = await page.locator("table.table tbody tr").all()

        filingData: list = []

        for row in filingRows:
            linkElem = row.locator("td.filetype a").first
            if await linkElem.count() == 0:
                continue
            link = await linkElem.get_attribute("href")
            text = await linkElem.inner_text()
            dateFiled = await row.locator("td.filed").inner_text()

            # Try parsing date
            try:
                dateObject = datetime.strptime(dateFiled.strip(), "%Y-%m-%d")
            except ValueError:
                dateObject = datetime.min

            filingData.append({"link": link, "text": text.strip(), "date": dateObject})

        # Filter only those that match desired filings
        matchedFilings = [
            f for f in filingData if any(ft in f["text"] for ft in filings)
        ]

        # Sort by most recent
        matchedFilings.sort(key=lambda x: x["date"], reverse=True)

        print(f"📄 Found {len(matchedFilings)} Matching filings. Starting download...")
        for filing in matchedFilings:
            print(f"🖨️ Opening: {filing['text']} ({filing['date']})")

            # Open in new tab
            newPage = await context.new_page()
            await newPage.goto(filing["link"], wait_until="networkidle")

            # Generate PDF file name
            safeTitle = filing["text"].replace("/", "_").replace(" ", "_")
            pdfPath = f"{safeTitle}_{filing['date'].strftime('%Y%m%d')}.pdf"

            # Print to PDF
            await newPage.pdf(path=pdfPath, format="Letter", print_background=True)
            print(f"💾 Saved PDF: {pdfPath}")

            # Close tab
            await newPage.close()
            delay(1, 2)

        # Optional: Keep page open for inspection
        await page.pause()

        # Cleanup
        await context.close()
        await browser.close()
        print(f"✅ {companyName} - Browser closed")


# GOAL, recent, quarterly and Yearly


#  10-K (Annual Reporting)
#  10-Q, (Quarterly Reporting)
#  8-K (Recent Filings)
#  Form-4 (Insider Buying)
#  DEF 14A (Proxy Statements),
#  13F (Institutional Holdings)
#  13D/13G   (Activist Ownership)
#  S-1 (IPO Stock)
#  S-1 (IPO Stock)
