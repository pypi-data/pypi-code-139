import os
import pkgutil


def walk_modules(module, prefix=None, module_dir=None, include_self=True, to_dict=False):
    result = []

    if module is not None:
        module_name = module.__name__
        if include_self:
            if to_dict:
                result.append(dict(
                    endpoint=module_name,
                    is_pkg='__init__' in os.path.basename(module.__file__),
                ))
            else:
                result.append(module_name)
        if prefix is None:
            prefix = module_name

        if module_dir is None:
            # Walk package only.
            if not getattr(module, '__file__', None) or '__init__' not in os.path.basename(module.__file__):
                return result
            module_dir = os.path.dirname(module.__file__)
    elif prefix is None or module_dir is None:
        raise Exception('Must provide prefix and module_dir.')

    for module_info in pkgutil.iter_modules([module_dir]):
        module_info: pkgutil.ModuleInfo
        module_endpoint = '%s.%s' % (prefix, module_info.name)
        if to_dict:
            result.append(dict(
                endpoint=module_endpoint,
                is_pkg=module_info.ispkg,
            ))
        else:
            result.append(module_endpoint)
        if module_info.ispkg:
            result += walk_modules(
                module=None,
                prefix=module_endpoint,
                module_dir=os.path.join(module_dir, module_info.name),
                to_dict=to_dict,
            )

    return result


def walk_files(dir_, *filters):
    result = []
    for d, ds, fs in os.walk(dir_):
        for f in fs:
            p = os.path.join(d, f)
            if filters:
                drop = False
                for filter_ in filters:
                    if not filter_(d, f, p):
                        drop = True
                        break
                if drop:
                    continue
            result.append(p)

    return result
