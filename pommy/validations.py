from click import BadParameter


def validate_positive_int(msg, min=1):
    """
    Returns a clik.option callback to validate that the value of
    an option is a positive integer. If it is not, it uses the
    received message.
    """

    def callback(ctx, param, value):
        if value < min:
            raise BadParameter(msg)

        return value

    return callback
