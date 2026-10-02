class WebsiteSrapperErrorHandeler(Exception):
    """
    Custom exception class for handling errors related to website scraping.
    Inherits from the built-in Exception class.
    """

    def __init__(self, messages):
        super().__init__(messages)
