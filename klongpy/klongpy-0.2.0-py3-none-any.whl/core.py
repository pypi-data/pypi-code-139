from collections import deque
import numpy as np
import re
from util import *


np.seterr(divide='ignore')

# TOOO:
# read sym is broken (f0 reads as f)
# add fn projections (e.g. {x-y}:(1;)@2 )
# cycle through params for take, split
# add dictionary support
# add shifted operators (e.g. :@)
# add seperate char vs string support
# add split op
# add amend support
# add conditionals
# add dyad adverb support
# add each family support
# add over family support
# add scan family support
# add iterator family support
# add channel family support
# add system commands
# add debug support


class KGSym(str):
    def __repr__(self):
        return f":{super(KGSym,self).__str__()}"
    def __eq__(self, o):
        return isinstance(o,KGSym) and self.__str__() == o.__str__()
    def __hash__(self):
        return super(KGSym,self).__hash__()


# TODO: is it actually helpful for this to be a list?
class KGFn(list):
    pass


kg_global_vars = dict()
kg_context = deque([kg_global_vars])


def kg_context_clear():
    kg_global_vars.clear()
    while kg_context_pop():
        pass


def kg_context_push(d=None):
    kg_context.insert(0,d or {})


def kg_context_pop():
    return kg_context.popleft() if len(kg_context) > 1 else None


def def_var(k,v):
    assert isinstance(k, KGSym)
    kg_context[0][k] = v


def is_sym(k): # TODO: use next/filter?
    if not isinstance(k, KGSym):
        return False
    for d in kg_context:
        if in_map(k, d):
            return True
    return False


# TODO: use next/filter?
# TODO: do we need to differentiate sym vs var? sym: => sym
def find_var(k):
    if not isinstance(k, KGSym):
        return False
    for d in kg_context:
        if in_map(k, d):
            return d[k]
    return None


# TODO: does this need to be override safe?
def mk_var(k,v=None):
    if not is_sym(k):
        def_var(k, v or k)
    return k


def rec_flatten(a):
    if not is_list(a) or len(a) == 0:
        return a
    if is_list(a[0]):
        p = rec_flatten(a[0])
        q = rec_flatten(a[1:])
        return np.concatenate([p,q])
    return np.concatenate([a[:1], rec_flatten(a[1:])])


def rec_fn(a,f):
    return np.asarray([rec_fn(x, f) for x in a], dtype=object) if is_list(a) else f(a)


def vec_fn(a, f):
    if isinstance(a, np.ndarray) and a.dtype == 'O':
        return np.asarray([((vec_fn(x, f) if len(x) > 1 else f(x)) if is_list(x) else f(x)) for x in a] if is_list(a) else f(a), dtype=object)
    return f(a)


def rec_fn2(a,b,f):
    return np.asarray([rec_fn2(x, y, f) for x,y in zip(a,b)], dtype=object) if is_list(a) and is_list(b) else f(a,b)

# 1 vec[A],vec[B]
# 2 vec[A],obj_vec[B]
# 3 vec[A],scalar[B]
# 4 obj_vec[A],vec[B] (may either be vec[B] or obj_vec[B])
# 5 obj_vec[A],scalar[B]
# 6 scalar[A],vec[B]
# 7 scalar[A],obj_vec[B]
# 8 scalar[A],scalar[B]
def vec_fn2(a, b, f):
    if isinstance(a,np.ndarray):
        if a.dtype != 'O':
            if isinstance(b,np.ndarray):
                if b.dtype != 'O':
                    # 1
                    return f(a,b)
                else:
                    # 2
                    assert len(a) == len(b)
                    return np.asarray([vec_fn2(x, y, f) for x,y in zip(a,b)], dtype=object)
            else:
                # 3
                return f(a,b)
        else:
            if isinstance(b,np.ndarray):
                # 4
                assert len(a) == len(b)
                return np.asarray([vec_fn2(x, y, f) for x,y in zip(a,b)], dtype=object)
            else:
                # 5
                return np.asarray([vec_fn2(x,b,f) for x in a], dtype=object)
    else:
        if isinstance(b,np.ndarray):
            if b.dtype != 'O':
                # 6
                return f(a,b)
            else:
                # 7
                return np.asarray([vec_fn2(a,x,f) for x in b], dtype=object)
        else:
            # 8
            return f(a,b)

    return np.asarray([vec_fn2(x,q,f) for x in p], dtype=object)



def is_atom(x):
    return is_empty(x) if is_iterable(x) and not is_sym(x) else True


def is_symbolic(c):
	return is_alpha(c) or is_number(c) or c == '.'


def is_special(c):
	return (is_char(c)) and (not is_number(c)) and (isinstance(c, str) and len(c) == 1 and ord(c) >= ord(' '))


def is_operator(x):
    return (in_map(x, vm) or in_map(x, vd)) and is_special(x[0])


def kg_truth(x):
    return x*1


def read_num(t, i=0):
    p = i
    use_float = False
    if t[i] == '-':
        i += 1
    while i < len(t):
        if t[i] == '.' or t[i] == 'e':
            assert use_float == False
            use_float = True
        elif not t[i].isnumeric():
            break
        i += 1
    return i, float(t[p:i]) if use_float else int(t[p:i])


def read_alpha(t, i=0):
    p = i
    while i < len(t) and t[i].isalpha():
        i += 1
    return i, str(t[p:i])


def read_sym(t, i=0):
    p = i
    while i < len(t) and is_symbolic(t[i]):
        i += 1
    return i, KGSym(str(t[p:i]))


def read_comment(t, i=0):
    while not cmatch(t, i, '"'):
        i += 1
    return i


def skip_space(t, i=0):
    while i < len(t) and t[i].isspace():
        i += 1
    return i


def skip(t, i=0):
    i = skip_space(t,i)
    if cmatch(t, i, ':') and cpeek(t,i,'"'):
        i = read_comment(t,i)
    return i


def read_list(t, delim, i=0):
    arr = []
    obj_arr = False
    while not cmatch(t,i,delim):
        # TODO: make cleaner: kind of a hack to pass in read_neg but
        #       we can knowling read neg numbers in list context
        i, q = kg_token(t, i, read_neg=True)
        obj_arr = obj_arr or isinstance(q, (np.ndarray, str))
        arr.append(q)
    if cmatch(t,i,delim):
        i += 1
    return i, np.asarray(arr,dtype=object) if obj_arr else np.asarray(arr)


def read_string(t, i=0):
    p = i
    while not cmatch(t,i,'"'):
        i += 1
    return i+1, t[p:i]


def kg_shifted(t, i=0):
    if t[i].isalpha() or t[i] == '.':
        return read_sym(t,i)
    elif t[i].isnumeric() or t[i] == '"':
        return kg_token(t, i)
    elif t[i] == '{':
        raise RuntimeError("dict unsupported")
    return i+1, f":{t[i]}"


def kg_token(t, i=0, read_neg=False):
    i = skip(t, i)
    if i >= len(t):
        return i, None
    if t[i] == '"':
        return read_string(t, i+1)
    elif t[i] == ':':
        return kg_shifted(t, i+1)
    elif t[i] == '[':
        return read_list(t, ']', i+1)
    elif t[i].isnumeric() or (read_neg and (t[i] == '-' and (i+1) < len(t) and t[i+1].isnumeric())):
        return read_num(t, i)
    elif is_symbolic(t[i]):
        return read_sym(t, i)
    return i+1, t[i] # symbol


def safe_eq(a,b):
    return isinstance(a,type(b)) and a == b


def read_fn_args(t, i=0):
    i = cexpect(t,i,'(')
    arr = []
    if cpeek(t, i, ')'):
        # nilad application
        return i,arr
    i,a = kg_expr(t,i)
    arr.append(a)
    while cmatch(t,i,';'):
        i,_ = kg_token(t,i)
        i,a = kg_expr(t,i)
        arr.append(a)
    i = cexpect(t,i,')')
    return i,arr


def kg_factor(t, i=0):
    i,a = kg_token(t, i)
    if safe_eq(a, '('):
        i,a = kg_expr(t, i)
        i = cexpect(t, i, ')')
    elif safe_eq(a, '{'):
        i,a = kg_prog(t, i)
        a = a[0] if len(a) > 0 else a
        i = cexpect(t, i, '}')
        if cmatch(t, i, '('):
            i,fa = read_fn_args(t,i)
            a = KGFn([a, fa])
        else:
            a = KGFn([a])
    elif safe_eq(a, ':['):
        die("conditional unsupported")
    elif in_map(a, vm): # need is_operator?
        ii, aa = kg_token(t, i)
        a = [a]
        if in_map(aa, vma):
            a.append(aa)
            i = ii
        i, aa = kg_expr(t, i)
        a.append(aa)
    return i, a


def kg_expr(t, i=0):
    i, a = kg_factor(t, i)
    arr = None
    ii, aa = kg_token(t, i)
    while ii < len(t) and (is_operator(aa) or safe_eq(aa, "{")):
        if safe_eq(aa, '}') or safe_eq(aa, ')') or safe_eq(aa, ';'):
            break
        if in_map(aa, vd):
            # TODO: check for adverb
            arr = [a, aa] if arr is None else arr
            ii, aa = kg_expr(t, ii)
            arr.append(aa)
    return (i, a) if arr is None else (ii, arr)


def kg_prog(t, i=0):
    arr = []
    while True:
        i, q = kg_expr(t,i)
        arr.append(q if isinstance(q, list) and not isinstance(q, KGFn) else [q])
        if not cmatch(t, i, ';'):
            break
        i += 1
    return i, arr


def eval_groupby(a):
    q = np.asarray([x for x in a] if isinstance(a, str) else a)
    a = q.argsort()
    return np.asarray(np.split(a, np.unique(q[a], return_index=True)[1][1:]), dtype=object)


def eval_at_index(a,b):
    if isinstance(a,str):
        return ''.join(a[x] for x in b)
    if isinstance(a, KGFn):
        return kg_eval([KGFn([a[0], b])])
    if not is_empty(b):
        return np.asarray(a)[tuple(b) if isinstance(b,list) else b]
    return b


def eval_match(a,b):
    r = vec_fn2(a, b, lambda x,y: (np.isclose(x,y) if (is_number(x) and is_number(y)) else np.all(np.asarray(x,dtype=object) == np.asarray(y,dtype=object))))
    return kg_truth(rec_flatten(r).all())


def create_verb_dyad_adverbs():
    d = {}
    return d


def create_verb_dyads():
    d = {}
    d['!'] = lambda a, b: vec_fn2(a, b, np.fmod)
    d['#'] = lambda a, b: b[a:] if a < 0 else b[:a]
    d['$'] = lambda a, b: die("$ unsupported")
    d['%'] = lambda a, b: vec_fn2(a, b, np.divide)
    d['&'] = lambda a, b: vec_fn2(a, b, np.minimum)
    d['*'] = lambda a, b: vec_fn2(a, b, np.multiply)
    d['+'] = lambda a, b: vec_fn2(a, b, np.add)
    d[','] = lambda a, b: a+b if (isinstance(a,str) and isinstance(b,str)) else np.array([*to_list(a), *to_list(b)])
    d['-'] = lambda a, b: vec_fn2(a, b, np.subtract)
    d['<'] = lambda a, b: kg_truth(vec_fn2(a, b, lambda x,y: x < y if (isinstance(x,str) and isinstance(y,str)) else np.less(x,y)))
    d['='] = lambda a, b: vec_fn2(a, b, lambda x, y: kg_truth(np.asarray(x,dtype=object) == np.asarray(y,dtype=object)))
    d['>'] = lambda a, b: kg_truth(vec_fn2(a, b, lambda x,y: x > y if (isinstance(x,str) and isinstance(y,str)) else np.greater(x,y)))
    d['?'] = lambda a, b: np.asarray([m.start() for m in re.finditer(f"(?={b})", a)]) if isinstance(a,str) else np.where(np.asarray(a) == b)[0]
    d['@'] = eval_at_index
    d['^'] = lambda a, b: vec_fn2(a, b, lambda x,y: np.power(float(x) if is_integer(x) else x, y))
    d['_'] = lambda a, b: b[a:] if a >= 0 else b[:a]
    d['|'] = lambda a, b: vec_fn2(a, b, np.maximum)
    d['~'] = eval_match #lambda a, b: kg_truth((np.isclose(a,b) if (is_number(a) and is_number(b)) else np.all(np.asarray(a,dtype=object) == np.asarray(b,dtype=object))))
    d[':@'] = lambda a, b: np.asarray(a)[tuple(b) if is_list(b) else b] if not is_empty(b) else b
    d[':#'] = lambda a, b: die(":# unsupported")
    d[':$'] = lambda a, b: die(":$ unsupported")
    d[':%'] = lambda a, b: vec_fn2(a, b, lambda x,y: np.trunc(np.divide(x, y)))
    d[':+'] = lambda a, b: die(":+ unsupported")
    d[':-'] = lambda a, b: die(":- unsupported")
    d['::'] = def_var
    d[':='] = lambda a, b: die(":= unsupported")
    d[':^'] = lambda a, b: die(":^ unsupported")
    d[':_'] = lambda a, b: die(":_ unsupported")
    return d


def create_verb_monad_adverbs():
    d = {}
    d['\''] = lambda f, a: np.asarray([f(x) for x in a] if (is_iterable(a) and not is_empty(a)) else a if is_empty(a) else f(a))
    return d


def eval_shape(a):
    def _a(x): # use numpy's natural shape by replacing all strings with arrays
        return np.asarray([np.empty(len(y)) if isinstance(y,str) else (_a(y) if is_list(y) else y) for y in x])
    return 0 if is_atom(a) else np.asarray([len(a)]) if isinstance(a,str) else np.asarray(_a(a).shape)


# https://stackoverflow.com/questions/3382352/equivalent-of-numpy-argsort-in-basic-python
def kg_argsort(a, reverse=False):
    return np.asarray(sorted(range(len(a)), key=lambda x: np.max(a[x]) if is_list(a[x]) else a[x], reverse=reverse))


def create_verb_monads():
    d = {}
    d['!'] = lambda a: np.arange(a)
    d['#'] = lambda a: np.abs(a) if is_number(a) else ord(a) if is_char(a) else len(a)
    d['$'] = lambda a: die("$ unsupported")
    d['%'] = lambda a: vec_fn(a, lambda x: np.reciprocal(np.asarray(x,dtype=float)))
    d['&'] = lambda a: np.concatenate([np.zeros(x, dtype=int) + i for i,x in enumerate(a if is_list(a) else [a])])
    d['*'] = lambda a: a if is_empty(a) or not is_iterable(a) else a[0]
    d['+'] = lambda a: np.transpose(np.asarray(a))
    d[','] = lambda a: np.asarray([a],dtype=object) # np interpets ':foo" as ':fo"
    d['-'] = lambda a: vec_fn(a, lambda x: np.negative(np.asarray(x, dtype=object)))
    d['<'] = lambda a: kg_argsort([x for x in a] if isinstance(a,str) else a, reverse=False)
    d['='] = lambda a: eval_groupby(a)
    d['>'] = lambda a: kg_argsort([x for x in a] if isinstance(a,str) else a, reverse=True)
    d['?'] = lambda a: ''.join(np.unique([x for x in a])) if isinstance(a, str) else np.unique(a)
    d['@'] = lambda a: kg_truth(is_atom(a))
    d['^'] = lambda a: eval_shape(a)
    d['_'] = lambda a: vec_fn(a, lambda x: np.floor(np.asarray(x, dtype=float)))
    d['|'] = lambda a: a[::-1]
    d['~'] = lambda a: vec_fn(a, lambda x: 1 if is_empty(x) else kg_truth(np.logical_not(np.asarray(x, dtype=object))))
    d[':#'] = lambda a: die(":# unsupported")
    d[':_'] = lambda a: kg_truth(a is None or (np.isinf(a) if is_number(a) else False))
    return d


vda = create_verb_dyad_adverbs()
vd = create_verb_dyads()
vma = create_verb_monad_adverbs()
vm = create_verb_monads()


def kg_eval(x, level=0):
    # print(" " * level, "eval", x)
    if isinstance(x, np.ndarray) or len(x) == 0:
        return x
    a = x[0]
    if len(x) > 1 and in_map(a, vm):
        fn = vm[a]
        if in_map(x[1], vma):
            o = x[2:] if len(x) > 3 else x[2] if isinstance(x[2], list) else x[2:]
            fn = lambda x,y=vma[x[1]],z=fn: y(z, x)
        else:
           o = x[1:] if len(x) > 2 else x[1] if isinstance(x[1], list) else x[1:]
        o = kg_eval(o, level+1)
        return fn(o)
    elif len(x) > 1 and in_map(x[1], vd):
        if isinstance(a, list) and not isinstance(a, KGFn):
            a = kg_eval(a, level+1)
        elif isinstance(a, KGSym): # TODO: better way to do this?
            a = kg_eval([a], level+1)
        o = x[2:] if len(x) > 3 else x[2] if isinstance(x[2], list) else x[2:]
        o = kg_eval(o, level+1)
        return vd[x[1]](a, o)
    elif isinstance(a, KGSym):
        return find_var(a) or mk_var(a)
    elif isinstance(a, KGFn): # TODO: KGFun implies application
        if len(a) == 2:
            ctx = {KGSym(p): kg_eval(q,level+1) if isinstance(q,list) else kg_eval([q],level+1) if isinstance(q,KGSym) else q for p,q in zip(['x','y','z'],a[1])}
            kg_context_push(ctx)
            try:
                return kg_eval(a[0], level+1)
            finally:
                kg_context_pop()
        else:
            return kg_eval(a[0], level+1)
    return a
