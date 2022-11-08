from __future__ import annotations
import sys, logging, subprocess, re
from argparse import ArgumentParser
from pathlib import Path
import sys

logger = logging.getLogger(__name__)

class Dist:
    def __init__(self, path: Path):
        self.path = path
        self.name = path.name
    
        m = re.match(r"^(?P<package>.+)\-(?P<version>[^\-]+)\-(?P<python_tag>[^\-]+)\-(?P<abi_tag>[^\-]+)\-(?P<platform_tag>[^\-]+).whl$", path.name)
        if not m:
            self.package = None
            self.version = None
            self.python_tag = None
            self.abi_tag = None
            self.platform_tag = None
        
        else:
            self.package = m.group("package")
            self.version = m.group("version")
            self.python_tag = m.group("python_tag")
            self.abi_tag = m.group("abi_tag")
            self.platform_tag = m.group("platform_tag")

    @property
    def tag(self):
        if self.python_tag is None or self.abi_tag is None or self.platform_tag is None:
            return None
        return f"{self.python_tag}-{self.abi_tag}-{self.platform_tag}"

    def __str__(self):
        return self.path.as_posix()


class BuildMixin:
    upload_repository: str
    checkbuild_package: str
    checkbuild_version = re.compile(r"^\d+\.\d+\.\d+$")
    checkbuild_python_tag = "py3"
    checkbuild_abi_tag = "none"
    checkbuild_platform_tag = "any"

    def _get_dists(self) -> list[Dist]:
        return [Dist(path) for path in Path.cwd().joinpath("dist").iterdir()]


    def checkbuild(self):
        # check generated wheel
        dists = self._get_dists()
        if len(dists) == 0:
            logger.error(f"no file generated in dist")
            return False

        ok = True
        for dist in dists:
            if not dist.package:
                logger.error(f"invalid file name format: {dist.name}")
                ok = False
                continue

            if hasattr(self, "checkbuild_package") and dist.package != self.checkbuild_package:
                logger.error(f"invalid wheel package \"{dist.package}\" for {dist.name} (expected \"{self.checkbuild_package}\")")
                ok = False
            elif not self.checkbuild_version.match(dist.version):
                logger.error(f"invalid wheel version \"{dist.version}\" for {dist.name} (expected pattern {self.checkbuild_version.pattern})")
                ok = False
            elif dist.python_tag != self.checkbuild_python_tag or dist.abi_tag != self.checkbuild_abi_tag or dist.platform_tag != self.checkbuild_platform_tag:
                logger.error(f"invalid wheel tag \"{dist.tag}\" for {dist.name} (expected {self.checkbuild_python_tag}-{self.checkbuild_abi_tag}-{self.checkbuild_platform_tag})")
                ok = False

        if not ok:
            return False

        if len(dists) >= 2:
            logger.error(f"several files generated in dist: {dists}")
            return False

        # "twine check": checks whether your distribution's long description will render correctly on PyPI.
        command = [sys.executable, "-m", "twine", "check", "--strict"] + [dist.path for dist in dists]
        cp = subprocess.run(command, text=True, stdout=sys.stdout, stderr=sys.stderr)
        if cp.returncode != 0:
            logger.error(f"check returned code {cp.returncode}")
            return False
        else:
            return dists


    def upload_add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--repository", "-r", help="repository name, as declared in ~/.pypirc")


    def upload(self, repository=None, skip_check=False):
        if skip_check:
            dists = self._get_dists()
        else:
            logger.info("check build")
            dists = self.checkbuild()
            if not dists:
                logger.warning(f"upload cancelled")
                return

        package = dists[0].package
        if not repository:
            try:
                repository = self.upload_repository
            except AttributeError:
                repository = package

        command = [sys.executable, "-m", "twine", "upload", "--repository", repository] + [dist.path for dist in dists]

        logger.info(f"uploading to repository \"{repository}\": {', '.join(dist.name for dist in dists)}")
        cp = subprocess.run(command, text=True, stdout=sys.stdout, stderr=sys.stderr)
        if cp.returncode != 0:
            logger.error(f"twine upload returned code {cp.returncode}")


    def build_add_arguments(self, parser: ArgumentParser):
        parser.add_argument("--upload", "-u", action="store_true", help="upload to pypi after build")
        self.upload_add_arguments(parser)


    def build(self, upload = False, repository = None):
        # Clean before build
        if hasattr(self, "clean"):
            logger.info("clean before build")
            self.clean()

        # Build
        logger.info("build distribution")
        subprocess.run([sys.executable, "-m", "pip", "wheel", "--no-deps", "-w", "dist", "."], check=True, stdout=sys.stdout, stderr=sys.stderr)

        # Check
        ok = True

        logger.info("check build")
        ok = ok and self.checkbuild()

        # Upload if required
        if upload:
            if not ok:
                logger.warning(f"upload cancelled")
                return
        
            logger.info(f"upload distribution")
            self.upload(repository=repository, skip_check=True)
