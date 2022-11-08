BASE_URL: str = "https://filesamples.com/samples/"

SAMPLES: dict[str, dict[str, list[str]]] = {
    "code": {
        "c": ["sample1.c"],
        "cpp": ["sample1.cpp"],
        "h": ["sample1.h"],
        "html": ["sample1.html"],
        "js": ["sample1.js"],
        "json": ["sample1.json"],
        "py": ["sample1.py"],
        "sh": ["sample1.sh"],
        "yaml": ["sample.yaml"],
    },
    "document": {
        "doc": ["sample1.doc"],
        "docx": ["sample1.docx"],
        "pdf": ["sample1.pdf"],
        "ppt": ["sample1.ppt"],
        "txt": ["sample1.txt"],
        "xls": ["sample1.xls"],
        "xlsx": ["sample1.xlsx"],
    },
    "image": {
        "gif": ["sample_1920×1080.gif"],
        "heic": ["sample1.heic"],
        "jpg": ["sample_1920×1280.jpg"],
        "png": ["sample_1920×1280.png"],
        "svg": ["sample_1920×1280.svg"],
    },
    "video": {
        "mov": ["sample_1280x720_surfing_with_audio.mov"],
        "mp4": ["sample_1280x720_surfing_with_audio.mp4"],
    },
}
