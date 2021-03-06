from . import tool

import datetime
import html
import re

def markdown(conn, data, title, main_num):
    curs = conn.cursor()

    data = '<div id="render_contect">' + re.sub('\r\n', '<br>', html.escape(data)) + '</div>'
    plus_data = '<script>render_markdown();</script>'
    backlink = []

    return [data, plus_data, backlink]