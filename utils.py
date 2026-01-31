from bs4 import BeautifulSoup
import re


def detect_jobs_per_page_and_total_items(html):
    matche = re.search(r'(?P<item_min>\d+)-(?P<item_max>\d+)\s+of\s+(?P<item_max_total>\d+)', html, flags=re.DOTALL|re.IGNORECASE)
    if not matche:

        matches = re.findall(r'href="[^"]+\/JobDetail\/[^"]+', html, flags=re.DOTALL|re.IGNORECASE)
        if not matches:
            return 0, 0, []
        jobs_per_page = len(matches)
        total_items = 10_000
    else:    
        jobs_per_page = int(matche.group('item_max')) - int(matche.group('item_min'))
        jobs_per_page += 1
        total_items = int(matche.group('item_max_total'))


    pages_offset = [page for page in range(0, total_items, jobs_per_page)]
    
    return jobs_per_page, total_items, pages_offset



def parse_avature_description_html(soup: BeautifulSoup) -> str:

    article = soup.select("article.article--details")[-1]
    blocks = article.select(".field--rich-text .article__content__view__field__value")

    html_blocks = [str(b) for b in blocks]
    return "\n".join(html_blocks)


def parse_avature_description_text(soup: BeautifulSoup) -> str:

    article = soup.select("article.article--details")[-1]
    blocks = article.select(".field--rich-text .article__content__view__field__value")

    text_blocks = [b.get_text(" ", strip=True) for b in blocks]
    return "\n\n".join(text_blocks)

def parse_avature_metadata(soup: BeautifulSoup) -> dict:
    metadata = {}

    for p in soup.select("article.article--details p.paragraph"):
        strong = p.find("strong")
        if not strong:
            continue

        key = strong.get_text(strip=True).rstrip(":")
        strong.extract()  # remove label do DOM
        value = p.get_text(strip=True)

        if value:
            metadata[key] = value

    
    # ----------------------
    # Metadata (label/value)
    # ----------------------
    for field in soup.select(
        "article.article--details.regular-fields--cols-2Z "
        ".article__content__view__field"
        ".article--details"
    ):
        label = field.select_one(
            ".article__content__view__field__label"
        )
        value = field.select_one(
            ".article__content__view__field__value"
        )

        if label and value:
            key = label.get_text(strip=True)
            val = value.get_text(strip=True)
            metadata[key] = val


    rows = soup.select("div.job_details_table div.row, .job_details_table div.row")

    for row in rows:
        cols = row.select("div.col-sm-6")
        if len(cols) != 2:
            continue

        key = cols[0].get_text(" ", strip=True)
        value = cols[1].get_text(" ", strip=True)

        key = key.replace(":", "").strip()
        metadata[key] = value


    for field in soup.select("article.article--details .article__content__view__field"):
        label = field.select_one(".article__content__view__field__label")
        value = field.select_one(".article__content__view__field__value")

        if not label or not value:
            continue

        key = label.get_text(" ", strip=True)
        val = value.get_text(" ", strip=True)

        metadata[key] = val

    return metadata


def parse_avature_job_detail(html: str) -> dict:
    soup = BeautifulSoup(html, "html.parser")

    data = {
        "title": None,
        "description_html": None,
        "description_text": None,
        "application_url": None
    }

    # ----------------------
    # Job Title
    # ----------------------
    title_tag = soup.select_one(".banner__text__title, h2.text1_5, .pageTitle1, h2.title")
    if title_tag:
        data["title"] = title_tag.get_text(strip=True)

    # ----------------------
    # Job Description
    # ----------------------
    desc_block = soup.select_one(
        "article.article--details .tf_replaceFieldVideoTokens .article__content__view__field__value"
    )
    desc_block_2 = soup.select_one(
        ".main__content, .article__content__view, .jobDetail "
    )
    if desc_block:
        data["description_html"] = str(desc_block)
        data["description_text"] = desc_block.get_text(
            separator="\n",
            strip=True
        )
    elif desc_block_2:
        #data["description_html"] = str(desc_block_2)
        data["description_text"] = desc_block_2.get_text(
            separator="\n",
            strip=True
        )

    # ----------------------
    # Application URL
    # ----------------------
    apply_btn = soup.select_one("a.button--primary[href], a.buttonLike")
    if apply_btn:
        data["application_url"] = apply_btn["href"]
    else:
        apply_btn = soup.select_one("a.button--default[href]")
        if apply_btn:
            data["application_url"] = apply_btn["href"]
    

    if data['description_text'] is None:
        data["description_html"] = parse_avature_description_html(soup)
        data["description_text"] = parse_avature_description_text(soup)

    data['metadata'] = parse_avature_metadata(soup)

    return data



def get_links_jobs(page_html):
    
    soup = BeautifulSoup(page_html, "html.parser")

    links = []

    for header in soup.select("div.article__header__text, .jobResultItem, h3.article__header__text__title"):
        a = header.find("a", href=True)
        if a:
            if a['href'].startswith('https://'):
                links.append(a["href"])

    return links