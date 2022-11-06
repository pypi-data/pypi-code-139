import bs4, os, re, io, json
import hashlib, flask
from . import const
from . import exc

class Illumni:
    def __init__(self):
        self.app = flask.Flask(import_name="Illumni")
        self.app.config["TEMPLATE_AUTO_RELOAD"] = True
        self.compiler = RouteCompiler()
        self.renderer = RouteRenderer()
        
    def start(self, host: str = "0.0.0.0", port: int = 80):
        if not os.path.exists("routes"):
            raise exc.NoRoutesDir
        
        if len(os.listdir("routes")) == 0:
            print("no routes detected, exiting app.")
            os._exit(0)
        
        pages = {}

        self.app.add_url_rule(
            rule="/il-0.js",
            view_func=self.renderer.render_bytes(
                data=const.JS_0,
                mimetype="text/javascript"
            )
        )
        
        self.app.add_url_rule(
            rule="/il-1.js",
            view_func=self.renderer.render_bytes(
                data=const.JS_1,
                mimetype="text/javascript"
            )
        )
        
        self.app.add_url_rule(
            rule="/il-2.js",
            view_func=self.renderer.render_bytes(
                data=const.JS_2,
                mimetype="text/javascript"
            )
        )
        
        for root, dirs, _ in os.walk("routes"):
            for dir in dirs:
                path = os.path.join(root, dir)
                                
                pages[path.replace("routes\\", "")] = {
                    "html": os.path.exists(f"{path}\\page.html"),
                    "css": os.path.exists(f"{path}\\page.css"),
                    "js": os.path.exists(f"{path}\\page.js")
                }
                
        for path in pages:
            if pages[path]["html"]:
                self.app.add_url_rule(
                    rule=self.compiler.compile_whole(name=path),
                    view_func=self.renderer.render_page(path=path)
                )
            
            if pages[path]["css"]:
                self.app.add_url_rule(
                    rule=self.compiler.compile_whole(name=f"{path}\\page.css"),
                    view_func=self.renderer.render_source(path=path,type="css")
                )

            if pages[path]["js"]:
                self.app.add_url_rule(
                    rule=self.compiler.compile_whole(name=f"{path}\\page.js"),
                    view_func=self.renderer.render_source(path=path,type="js")
                )
        
        self.app.run(host, port)
        
class RouteRenderer:
    def __init__(self):
        self.compiler = RouteCompiler()
        
        self.js = {
            '{"css": true, "js": true}': "/il-2.js",
            '{"css": false, "js": true}': "/il-1.js",
            '{"css": true, "js": false}': "/il-0.js",
            '{"css": false, "js": false}': None,
        }
        
    def format(self, content: str, kwargs: dict):
        e = content
        
        for key in kwargs:            
            e = e.replace("{" + f"{{ {key} }}" + "}", kwargs[key])
        
        return e
    
    def view_func(self, name: str, content):
        f = lambda *args, **kwargs: self.format(content, kwargs)
        f.__name__ = hashlib.md5(name.encode()).hexdigest()
        return f
    
    def render_file(self, name: str, path: str):
        f = lambda *args, **kwargs: flask.send_file(f"{os.getcwd()}\\{path}")
        f.__name__ = hashlib.md5(name.encode()).hexdigest()
        return f
    
    def render_bytes(self, data: bytes, mimetype: str):
        f = lambda *args, **kwargs: flask.send_file(io.BytesIO(data), mimetype)
        f.__name__ = hashlib.md5(data).hexdigest()
        return f
    
    def render_source(self, path: str, type: str):
        if os.path.exists(f"routes\\{path}\\page.{type}"):
            return self.render_file(name=f"routes\\{path}\\page.{type}", path=f"routes\\{path}\\page.{type}")
        else:
            raise exc.FileNonexistant
    
    def render_page(self, path: str):
        if os.path.exists(f"routes\\{path}\\page.html"):
            with open(f"routes\\{path}\\page.html", "r") as f:
                soup = bs4.BeautifulSoup(f.read(), "html.parser")
                f.close()
                
            if not soup.head:
                soup.append(soup.new_tag("head"))
            
            combo = json.dumps({
                "css": os.path.exists(f"routes\\{path}\\page.css"), 
                "js": os.path.exists(f"routes\\{path}\\page.js")
            })
            
            if self.js[combo]:
                soup.head.append( # type: ignore
                    soup.new_tag(
                        "script",
                        src=self.js[combo]
                    )
                )
            
            return self.view_func(name=f"routes\\{path}\\page.html", content=str(soup))
        else:
            raise exc.FileNonexistant
            
class RouteCompiler:
    def __init__(self):
        self.slug = re.compile(r"(?:\[)[^\[\]]*?(?:\])")
        self.group = re.compile(r"(?:\()[^\(\)]*?(?:\))")
        
    def compile_whole(self, name: str):
        return "/" + "/".join([self.compile(i) for i in name.split("\\")])
    
    def compile(self, name: str) -> str:
        if " " in name:
            raise exc.RouteError("Routes cannot contain spaces.")
        else:
            guess, valid = self.guess(name)
            
            if not valid[0]:
                raise exc.RouteError(valid[1])
            else:
                if guess == "slug":
                    return self.slug.findall(name)[0].replace("[", "<").replace("]", ">")
                elif guess == "name":
                    return name
                else:
                    return ""
            
    def validate(self, name: str) -> tuple[bool, str | None]:
        if "[" in name or "]" in name:
            if "(" in name or ")" in name:
                return False, "Mismatched \"(\" or \")\" in slug defenition."
            else:
                if name.count("[") == 1 and name.count("]") == 1:
                    return True, None
                else:
                    return False, "Mismatched \"[\" or \"]\" brackets."
        else:
            return True, None
            
    def guess(self, name: str) -> tuple[str, tuple[bool, str | None]]:
        if "[" in name and "]" in name:
            return "slug", self.validate(name)
        elif "(" in name and ")" in name:
            return "group", self.validate(name)
        else:
            return "name", self.validate(name)