import openai
import tiktoken

from settings import OPENAI_TOKEN, MODEL_NAME


openai.api_key = OPENAI_TOKEN


def find_sustainability(
        page: str
) -> str:
    """
    Find sustainability information on the page

    Parameters:
    -----------
    page: str
        Page text

    Returns:
    --------
    str
        Sustainability information if it's present
    """
    prompt_text = f"""Given the information {page}, is there 
    information about sustainability?
    text: """
    message_type = openai.Completion.create(
        model=MODEL_NAME,
        prompt=prompt_text,
        max_tokens=2,
        temperature=0,
    )

    ans = message_type['choices'][0]['text']

    if "yes" in ans.lower():
        return get_sustainability(
            page=page
        )
    else:
        return None


def get_sustainability(
        page: str
) -> str:
    """
    Get sustainability information from the page

    Parameters:
    -----------
    page: str
        Page text

    Returns:
    --------
    str
        Sustainability information found on the page
    """
    prompt_text = f"""Given the information {page}, find exact 
    sentence which contains information about sustainability.
    text: """

    message_type = openai.Completion.create(
        model=MODEL_NAME,
        prompt=prompt_text,
        max_tokens=100,
        temperature=0,
    )

    sust_info = message_type['choices'][0]['text']
    return sust_info


def tokens_cnt(
        sentence: str
) -> int:
    """Get number of tokens in sentence"""
    encoding = tiktoken.encoding_for_model(MODEL_NAME)
    tokens = encoding.encode(sentence)
    n_tokens = len(tokens)
    return n_tokens


def nex_part(
        text: str,
        token_limit: int = 1024
) -> str:
    """Split text into chunks of 1024 tokens"""
    chunk = ""
    cur_tkn_cnt = 0
    for sentence in text:
        if cur_tkn_cnt + tokens_cnt(sentence) < token_limit:
            chunk += str(sentence)
            cur_tkn_cnt += tokens_cnt(sentence)
        else:
            yield chunk
            chunk = ""
            cur_tkn_cnt = 0
    if chunk:
        yield chunk


def get_sust_summary(
        sust_info: str
) -> str:
    """Get summary of all collected sustainability information"""
    summaries = []
    for chunk in nex_part(sust_info):
        prompt_text = f"""Given the information {chunk}, write 
        a brief summary.
        text: """

        message_type = openai.Completion.create(
            model=MODEL_NAME,
            prompt=prompt_text,
            max_tokens=1000,
            temperature=0,
        )

        summaries.append(message_type['choices'][0]['text'])
    summary = " ".join(summaries)
    summary = summary.split(". ")
    return summary
