from enum import StrEnum


class NotionBlockType(StrEnum):
    HEADING1 = "heading_1"
    HEADING2 = "heading_2"
    HEADING3 = "heading_3"
    PARAGRAPH = "paragraph"
    BULLETED_LIST_ITEM = "bulleted_list_item"
    NUMBERED_LIST_ITEM = "numbered_list_item"
    TO_DO = "to_do"
    TOGGLE = "toggle"
    CODE = "code"
    QUOTE = "quote"
    CALLOUT = "callout"
    DIVIDER = "divider"
