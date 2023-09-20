import pdfplumber
from pathlib import Path
import logging

from tqdm import tqdm

from settings import INPUT_DATA_PATH, ARTICLE_NUMS
from gpt_utils import find_sustainability, get_sust_summary
from output_format import make_file


LOGGER = logging.getLogger("__main__")
logging.basicConfig(level=logging.INFO)


def find_article(
        page: str,
        page_num: int
) -> dict | None:
    """
    Find article in page

    Parameters:
    -----------
    page: str
        Page text
    page_num: int
        Page number

    Returns:
    --------
    dict | None
        Info about article
    """
    for article_num in ARTICLE_NUMS:
        if f"article {article_num}" in page.lower():
            sentence = [sent for sent in page.split(".")
                        if f"classified under article {article_num}"
                        in sent.lower()]
            if len(sentence) == 0:
                continue
            result = {
                "page": page_num,
                "n_article": article_num,
                "sentence": sentence
            }
            return result
        else:
            continue
    return None


def get_texts(
        path: Path
) -> list[str]:
    """
    Get all texts from pdf

    Parameters:
    -----------
    path: Path
        Path to pdf

    Returns:
    --------
    all_texts: list[str]
        List of texts from all pages
    """
    LOGGER.info("Parsing file %s...", path.stem)
    pdf = pdfplumber.open(path)
    all_texts = []

    for page in pdf.pages:
        content = page.extract_text()
        sentences = " ".join(content.split("\n"))
        all_texts.append(sentences)
    LOGGER.info("File parsed successfully. Number of pages: %s",
                len(all_texts))
    return all_texts


def collect_data(
        all_texts: list[str]
) -> tuple[list[dict], list[dict], set[int]]:
    """
    Collect data from all pages

    Parameters:
    -----------
    all_texts: list[str]
        List of texts from all pages

    Returns:
    --------
    data: tuple[list[dict], list[dict], set[int]]
        Data from all pages
    """
    LOGGER.info("Collecting data from all pages...")
    article_results, sust_results = [], []
    for page_num in tqdm(range(len(all_texts))):
        sust_info = find_sustainability(
            page=all_texts[page_num]
        )
        article_info = find_article(
            page=all_texts[page_num],
            page_num=page_num
        )
        if article_info:
            article_results.append(article_info)
        if sust_info:
            sust_results.append(sust_info)

    # Check if pattern for article classification is correct
    unique_articles = set([i.get("n_article") for i in article_results])
    if len(unique_articles) > 1:
        LOGGER.warning("Several article numbers fit into used pattern.")
        assert "Several article numbers fit into used pattern."

    LOGGER.info("Data collected successfully.")
    data = (article_results, sust_results, unique_articles)
    return data


def main(path):

    # Retrieve text from PDF file
    all_texts = get_texts(path=path)

    # Collect the necessary data
    article_results, sust_results, unique_articles = collect_data(all_texts=all_texts)

    # Organise data for an output file
    article = list(unique_articles)[0]
    article_source = article_results[0]
    summary = get_sust_summary(
        sust_info=sust_results
    )
    LOGGER.info("Summary of sustainability data collected successfully.")

    # Create an output file
    make_file(
        article=article,
        article_source=article_source,
        summary=summary,
        sust_results=sust_results,
        fund_name=path.stem
    )
    LOGGER.info(f"File {path.stem}.xlsx created successfully.")


if __name__ == '__main__':
    for path in INPUT_DATA_PATH.glob("*.pdf"):
        main(path)
