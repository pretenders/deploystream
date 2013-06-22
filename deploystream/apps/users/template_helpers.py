from deploystream import app


@app.template_filter('humanize_time')
def humanize_time(datetime):
    return datetime.strftime("%B %d, %Y")
