def rpc(
        pb,
        required_fields=None,
        is_atomic=False,
):
    if required_fields is None:
        required_fields = []

    def func_wrapper(func):
        async def arg_wrapper(self, stream):
            if is_atomic:
                async with db.transaction() as tx:
                    is_success = True
                    response = dict()
                    try:
                        request = await get_request(stream, required_fields)
                        response = await func(self, request)
                        response["code"] = response.get("code", 0)
                    except ValidationException as e:
                        is_success = False
                        response["errors"] = validation_error_handler(e.detail)
                        response["code"] = 3
                    except Exception as e:
                        is_success = False
                        traceback.print_exc()
                        if conf.ENV != "testing":
                            pass
                        response["errors"] = system_error_handler(str(e))
                        response["code"] = 3
                    try:
                        await stream.send_message(convert(response, pb))
                    except Exception as e:
                        is_success = False
                        traceback.print_exc()
                        if conf.ENV != "testing":
                            pass
                        response = dict()
                        response["errors"] = system_error_handler(str(e))
                        response["code"] = 3
                        await stream.send_message(convert(response, pb))
                    if not is_success:
                        await tx.raise_rollback()
            else:
                response = dict()
                try:
                    request = await get_request(stream, required_fields)
                    response = await func(self, request)
                    response["code"] = response.get("code", 0)
                except ValidationException as e:
                    response["errors"] = validation_error_handler(e.detail)
                    response["code"] = 3
                except ValidationError as e:
                    response["errors"] = marshmallow_err_handler(
                        e.normalized_messages()
                    )
                    response["code"] = 3
                except Exception as e:
                    traceback.print_exc()
                    if conf.ENV != "testing":
                        capture_exception(e)
                    response["errors"] = system_error_handler(str(e))
                    response["code"] = 3
                try:
                    await stream.send_message(convert(response, pb))
                except Exception as e:
                    traceback.print_exc()
                    if conf.ENV != "testing":
                        capture_exception(e)
                    response = dict()
                    response["errors"] = system_error_handler(str(e))
                    response["code"] = 3
                    await stream.send_message(convert(response, pb))

        return arg_wrapper

    return func_wrapper
