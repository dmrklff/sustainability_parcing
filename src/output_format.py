import openpyxl
from openpyxl.styles import Font

from settings import OUTPUT_DATA_PATH, FUND_NAME


def make_file(
        article: str,
        article_source: dict,
        summary: str,
        sust_results: list[dict],
        fund_name: str = FUND_NAME
) -> None:
    """
    Make Excel file with classified article,
    key sustainability data and its sources

    Parameters:
    -----------
    article: str
        Classified article
    article_source: dict
        Dictionary with source of classified article
    summary: str
        Summary of sustainability data
    sust_results: list[dict]
        List of sustainability data sources
    fund_name: str
        Name of fund

    Returns:
    --------
    None
    """
    wb = openpyxl.Workbook()
    ws1 = wb.active
    ws1.title = "General Info"
    ws2 = wb.create_sheet("Sources")
    ws1['A1'] = fund_name
    ws1['A1'].font = Font(bold=True)
    ws1["A2"] = "Article 8"
    ws1["A2"].font = Font(bold=True)
    ws1["A3"] = "Article 9"
    ws1["A3"].font = Font(bold=True)
    ws1["B2"] = "Yes" if article == 8 else "No"
    ws1["B2"].font = Font(bold=True)
    ws1["B3"] = "Yes" if article == 9 else "No"
    ws1["B3"].font = Font(bold=True)
    article_src_text = f"Source: page {article_source['page']}: " \
                       f"{article_source['sentence'][0]}"
    if ws1["B2"].value == "Yes":
        ws1["C2"] = article_src_text
    elif ws1["B3"].value == "Yes":
        ws1["C3"] = article_src_text
    ws1["A5"] = "Other sustainability data"
    ws1["A5"].font = Font(bold=True)
    for i in range(len(summary)):
        ws1[f"A{i + 6}"] = summary[i]
    ws2["A1"] = f"Article {article}"
    ws2["A1"].font = Font(bold=True)
    ws2["A2"] = article_src_text
    ws2["A3"] = "Other sustainability data"
    ws2["A3"].font = Font(bold=True)
    for i in range(len(sust_results)):
        ws2[f"A{i + 4}"] = sust_results[i]
    OUTPUT_DATA_PATH.mkdir(exist_ok=True)
    wb.save(OUTPUT_DATA_PATH / f"{fund_name}.xlsx")
