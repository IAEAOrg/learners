from strictyaml import Bool, EmptyDict, EmptyList, NullNone, Int, Map, MapPattern, Optional, Seq, Str, Any

config_schema = Map(
    {
        Optional("learners", default={"landingpage": "documentation"}): EmptyDict()
        | Map(
            {
                Optional(
                    "theme",
                    default={
                        "primary": "#666666",
                        "secondary": "#009899",
                        "success": "#009899",
                    },
                ): EmptyDict()
                | Map(
                    {
                        Optional("primary", default="#666666"): Str(),
                        Optional("secondary", default="#666666"): Str(),
                        Optional("success", default="#666666"): Str(),
                        Optional("primary_color", default="#666666"): Str(),
                        Optional("sidebar_background_color", default="#666666"): Str(),
                        Optional("menu_active_color", default="#ffffff"): Str(),
                        Optional("menu_inactive_color", default="#a3a3a3"): Str(),
                        Optional("main_background_color", default="#f6f6f6"): Str(),
                        Optional("main_text_color", default="#191b23"): Str(),
                        Optional("success_color", default="#4a8864"): Str(),
                        Optional("success_color_light", default="#6cbd8e"): Str(),
                        Optional("fail_color", default="#da1e55"): Str(),
                        Optional("fail_color_light", default="#d34a5d"): Str(),
                        Optional("info_color", default="#619dc7"): Str(),
                        Optional("info_color_light", default="#87b6d8"): Str(),
                        Optional("light_grey_color", default="#dedfe4"): Str(),
                        Optional("mid_grey_color", default="#c0c0c0"): Str(),
                        Optional("dark_grey_color", default="#8c8c8c"): Str(),
                        Optional("input_placeholder_color", default="#bfbfbf"): Str(),
                        Optional("input_background_color", default="#dedfe4"): Str(),
                        Optional("input_text_color", default="#191b23"): Str(),
                        Optional("nav_width", default="60px"): Str(),
                    }
                ),
                Optional(
                    "logo",
                    default='<?xml version="1.0" encoding="UTF-8"?><svg id="b" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 202.44 130.4"><g id="c"><g id="d"><g id="e"><path d="m120.33,100l-1.13,1.67c-20.13,29.84-60.63,37.71-90.47,17.58C9.96,106.59-.89,85.11.06,62.49,1.4,29.33,28.4,1.92,61.51.1c18.75-1.04,37.04,6.05,50.2,19.44.82.84.98,2.11.4,3.13l-13,22.43c-.36.62-1.01,1-1.72,1-.72.04-1.4-.31-1.79-.92-11.09-16.79-33.68-21.41-50.47-10.33-10.89,7.19-17.1,19.66-16.29,32.68,1.28,20.07,18.6,35.31,38.67,34.02,10.68-.68,20.52-6.03,26.9-14.61l1-1.35,24.92,14.41ZM202.09,5.67c-.47-.81-1.34-1.32-2.28-1.32h-54.51c-1.78,0-3.42.95-4.31,2.49l-39.22,67.93,24.9,14.39,32.36-56h27.21c.95-.02,1.81-.53,2.27-1.36l13.58-23.5c.47-.81.47-1.82,0-2.63Z" style="fill:#fff; stroke-width:0px;"/></g></g></g></svg>',
                ): Str(),
                Optional("headline", default="Welcome to Learners"): Str(),
                Optional(
                    "welcomeText",
                    default="Please log in with your assigned credentials:",
                ): Str(),
                Optional("landingpage", default="documentation"): Str(),
                Optional("language_code", default="en"): Str(),
                Optional("upload_folder", default="backend/statics/uploads"): Str(),
                Optional("upload_extensions", default=["txt", "pdf", "png", "jpg", "jpeg", "gif", "json", "svg"]): Seq(Str()),
            }
        ),
        Optional("jwt", default={"jwt_secret_key": "3668da1b-cef1-5085-ae20-443409c9cc73"},): Map(
            {
                Optional("jwt_secret_key", default="3668da1b-cef1-5085-ae20-443409c9cc73"): Str(),
                Optional("jwt_access_token_duration", default=720): Int(),
                Optional("jwt_for_vnc_access", default=True): Bool(),
            }
        ),
        Optional("database", default={"db_uri": "sqlite:///data.db"}): Map(
            {
                Optional("db_uri", default="sqlite:///data.db"): Str(),
            }
        ),
        "users": MapPattern(
            Str(),
            Map(
                {
                    "password": Str(),
                    Optional("role", default="participant"): Str(),
                    Optional("vnc_clients"): MapPattern(
                        Str(),
                        Map(
                            {
                                "target": Str(),
                                Optional("tooltip", default="Access client"): Str(),
                                Optional("server", default="DEFAULT-VNC-SERVER"): Str(),
                                Optional("username"): Str(),
                                Optional("password"): Str(),
                            }
                        ),
                    ),
                    Optional("meta"): Any(),
                }
            ),
        ),
        Optional("tabs", default={"documentation": {"show": ["all"]}, "exercises": {"show": []}, "presentations": {"show": []}}): MapPattern(
            Str(),
            EmptyDict()
            | Map(
                {
                    Optional("show", default=["all"]): NullNone() | EmptyList() | Seq(Str()),
                    Optional("tooltip"): Str(),
                    Optional("icon"): Str(),
                    Optional("url"): Str(),
                    Optional("proxy"): Bool(),
                }
            ),
        ),
        Optional("venjix", default={"auth_secret": "", "url": ""}): Map(
            {
                Optional("auth_secret", default=""): Str(),
                Optional("url", default=""): Str(),
            }
        ),
        Optional("novnc", default={"server": ""}): Map(
            {
                Optional("server", default=""): Str(),
            }
        ),
        Optional("statics", default={"directory": "statics", "serve_mode": "role"}): Map(
            {
                Optional("directory", default="statics"): Str(),
                Optional("serve_mode", default="role"): Str(),
            }
        ),
        Optional("init_notifications"): EmptyList()
        | Seq(
            Map(
                {
                    "title": Str(),
                    "msg": Str(),
                }
            )
        ),
    }
)
