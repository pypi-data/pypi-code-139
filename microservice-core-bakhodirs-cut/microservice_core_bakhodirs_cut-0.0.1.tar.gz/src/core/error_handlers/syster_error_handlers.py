def system_error_handler(error):
    return [dict(field="non_field_errors", messages=[str(error)])]
