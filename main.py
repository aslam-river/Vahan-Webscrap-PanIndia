import csv
import datetime

from playwright.sync_api import sync_playwright

state_list = ['Rajasthan(59)', 'Tamil Nadu(148)']
dummy_sates_list = [
    'Andaman & Nicobar Island(5)',
    'Andhra Pradesh(84)',
    'Arunachal Pradesh(29)',
    'Assam(35)',
    'Bihar(48)',
    'Chhattisgarh(31)',
    'Chandigarh(1)',
    'UT of DNH and DD(3)',
    'Delhi(16)',
    'Goa(13)',
    'Gujarat(37)',
    'Himachal Pradesh(98)',
    'Haryana(104)',
    'Jharkhand(25)',
    'Jammu and Kashmir(21)',
    'Karnataka(68)',
    'Kerala(87)',
    'Ladakh(3)',
    'Lakshadweep(9)',
    'Maharashtra(59)',
    'Meghalaya(14)',
    'Manipur(17)',
    'Madhya Pradesh(53)',
    'Mizoram(12)',
    'Nagaland(9)',
    'Odisha(39)',
    'Punjab(96)',
    'Puducherry(8)',
    'Rajasthan(60)',
    'Sikkim(9)',
    'Tamil Nadu(148)',
    'Telangana(57)',
    'Tripura(9)',
    'Uttarakhand(21)',
    'Uttar Pradesh(77)',
    'West Bengal(59)'
]
current_time = datetime.datetime.now()
timestamp_string = current_time.strftime("%Y-%m-%d_%H-%M-%S")
file_name = f"Panindia_{timestamp_string}.csv"

with sync_playwright() as p:
    # Launches browser (Firefox to match your original preference, headed mode)
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # Open the Dashboard URL
    page.goto("https://vahan.parivahan.gov.in/vahan4dashboard/vahan/vahan/view/reportview.xhtml")

    # Open the CSV file for appending
    with open(file_name, 'a', newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)

        for i in dummy_sates_list:
            print(datetime.datetime.now())
        #     if i != 'Tamil Nadu(148)':
        #         page.reload()
        #         page.wait_for_load_state("networkidle")

            # Select state dropdown
            page.locator("(//span[@class='ui-icon ui-icon-triangle-1-s ui-c'])[2]").click()

            print(i)
            state_element = page.locator(f"//li[@data-label='{i}']")

            # Dynamic wait until the option is visible
            state_element.wait_for(state="visible")
            state_name = state_element.inner_text()
            print("extracted",state_name)
            page.wait_for_timeout(1000)
            # Click state option using execute_script equivalent
            state_element.click()
            page.wait_for_load_state("networkidle")
            print("clicked")
            page.wait_for_timeout(1000)

            # Y axis code
            page.locator("#yaxisVar_label").click()
            page.wait_for_selector("#yaxisVar_4", state="visible", timeout=5000)
            print("Found item text:", page.locator("#yaxisVar_4").inner_text())
            page.wait_for_timeout(1000)
            page.locator("#yaxisVar_4").click()
            page.wait_for_timeout(1000)
            print("Maker successfully clicked!")

            # X axis code
            page.locator("xpath=//*[@id='xaxisVar']/div[3]/span").click()
            page.wait_for_timeout(1000)
            page.locator("xpath=//*[@id='xaxisVar_7']").click()
            page.wait_for_timeout(1000)

            # Main refresh
            page.locator("xpath=//span[text()='Refresh']").first.click()
            # page.wait_for_load_state("networkidle")
            page.wait_for_selector("#j_idt124", state='hidden')
            page.wait_for_selector("#j_idt123",state='hidden')

            # Open filter toggler
            zz = page.locator("//*[@id='filterLayout-toggler']/span/a/span")
            zz.click()
            page.wait_for_timeout(1000)

            # Apply filters for two wheeler level
            classes = page.locator(
                "//label[text()='TWO WHEELER (Invalid Carriage)']/preceding-sibling::div/div[2]").get_attribute("class")

            if "ui-state-active" not in classes:
                page.locator("//label[text()='TWO WHEELER (Invalid Carriage)']").click()
            # page.locator("//label[text()='TWO WHEELER (Invalid Carriage)']").click()
            page.locator("//label[text()='TWO WHEELER(NT)']").click()
            page.locator("//label[text()='TWO WHEELER(T)']").click()

            view = page.locator("//label[text()='ELECTRIC(BOV)']")
            view.scroll_into_view_if_needed()
            view.click()

            dd = page.locator("//label[text()='PLUG-IN HYBRID EV']")
            dd.evaluate("el => el.click()")

            ee = page.locator("//label[text()='PURE EV']")
            ee.evaluate("el => el.click()")

            ff = page.locator("//label[text()='STRONG HYBRID EV']")
            ff.evaluate("el => el.click()")

            # Click left-side refresh
            page.locator("(//span[text()='Refresh'])[2]").click()
            page.wait_for_selector("#j_idt124", state='hidden')
            page.wait_for_selector("#j_idt123", state='hidden')
            page.wait_for_timeout(2000)

            # Find number of month columns dynamically
            month_columns = page.locator("//table/thead/tr[3]/th").count() // 2

            table_cells = page.locator("//table[@style='table-layout:auto;']//tbody//tr//td")
            page_links = page.locator("//a[contains(@aria-label,'Page ')]")

            has_table_data = table_cells.count() > 1
            pages_count = page_links.count()

            # Single Page Scraping
            if has_table_data and pages_count == 1:
                tr_count = page.locator("//table[@style='table-layout:auto;']//tbody//tr").count()
                for k in range(1, tr_count + 1):
                    sno = page.locator(f"//table[@style='table-layout:auto;']//tbody//tr[{k}]//td[1]").inner_text()
                    maker = page.locator(f"//table[@style='table-layout:auto;']//tbody//tr[{k}]//td[2]").inner_text()

                    months_data = []
                    for m in range(3, 3 + month_columns):
                        month_value = page.locator(
                            f"//table[@style='table-layout:auto;']//tbody//tr[{k}]//td[{m}]").inner_text()
                        months_data.append(month_value)

                    total = page.locator(
                        f"//table[@style='table-layout:auto;']//tbody//tr[{k}]//td[{3 + month_columns}]").inner_text()

                    row_data = [state_name, sno, maker] + months_data + [total]
                    csvwriter.writerow(row_data)
                    print(row_data)

            # Multipage Scraping
            elif has_table_data and pages_count > 1:
                for l in range(pages_count):
                    if l > 0:
                        # Go to next page
                        page.locator("//*[@id='groupingTable_paginator_bottom']/a[3]").click()
                        # Short transition buffer during dynamic page changes
                        page.wait_for_timeout(1000)

                    tr_count = page.locator("//table[@style='table-layout:auto;']//tbody//tr").count()
                    for k in range(1, tr_count + 1):
                        sno = page.locator(f"//table[@style='table-layout:auto;']//tbody//tr[{k}]//td[1]").inner_text()
                        maker = page.locator(
                            f"//table[@style='table-layout:auto;']//tbody//tr[{k}]//td[2]").inner_text()

                        months_data = []
                        for m in range(3, 3 + month_columns):
                            month_value = page.locator(
                                f"//table[@style='table-layout:auto;']//tbody//tr[{k}]//td[{m}]").inner_text()
                            months_data.append(month_value)

                        total = page.locator(
                            f"//table[@style='table-layout:auto;']//tbody//tr[{k}]//td[{3 + month_columns}]").inner_text()

                        row_data = [state_name, sno, maker] + months_data + [total]
                        csvwriter.writerow(row_data)
                        print(row_data)
            else:
                print('No data', state_name)

            # Scroll and Click dynamic refresh
            refresh_btn = page.locator("(//span[text()='Refresh'])[2]")
            try:
                refresh_btn.wait_for(state="visible", timeout=2000)
                refresh_btn.scroll_into_view_if_needed()
                refresh_btn.click()
            except Exception:
                page.locator("//*[@id='filterLayout-toggler']/span/a/span").click()
                refresh_btn.wait_for(state="visible", timeout=2000)
                refresh_btn.scroll_into_view_if_needed()
                refresh_btn.click()

            zz = page.locator("//*[@id='filterLayout-toggler']/span/a/span")
            zz.evaluate("el => el.click()")
    #
    print(datetime.datetime.now())
    # Close browser session safely
    browser.close()