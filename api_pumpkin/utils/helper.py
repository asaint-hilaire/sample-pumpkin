def response(error=None, payload=None):
    return {
        'error': error,
        'body': payload
    }
