class RequestConfig:
    def __init__(self, use_pos_api: bool = False,
                 use_pos_token: bool = False,
                 ignore_request_body: bool = False,
                 follow_redirects: bool = True,
                 format_millisecond: bool = False,
                 debug_rate_limit: bool = False) -> None:
        self.use_pos_api = use_pos_api
        self.use_pos_token = use_pos_token
        self.ignore_request_body = ignore_request_body
        self.follow_redirects = follow_redirects
        self.format_millisecond = format_millisecond
        self.debug_rate_limit = debug_rate_limit
