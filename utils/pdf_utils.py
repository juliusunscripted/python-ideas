from pypdf import PdfReader
from io import BytesIO
import structlog

log = structlog.stdlib.get_logger()


class PdfBytes:
    def __init__(self, pdf_bytes: bytes):
        self.reader = PdfReader(BytesIO(pdf_bytes))

    @property
    def number_of_pages(self):
        number_of_pages = self.reader.get_num_pages()
        log.debug("pdf reader", number_of_pages=number_of_pages)
        return number_of_pages

    def get_text_of_page(self, page_index_number: int):
        if page_index_number >= self.number_of_pages:
            raise ValueError("page_index_number must be smaller than number of pages")

        page = self.reader.pages[page_index_number]
        page_extracted_text = page.extract_text()
        return page_extracted_text
