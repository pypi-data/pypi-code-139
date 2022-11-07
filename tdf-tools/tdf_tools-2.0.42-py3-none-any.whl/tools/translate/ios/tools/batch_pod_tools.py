import json
import os
from tdf_tools.tools.cmd import Cmd
from tdf_tools.tools.shell_dir import ShellDir
from tdf_tools.tools.cmd import Cmd
import json
import glob


class BatchPodModel:
    def __init__(self, name: str, branch: str, path: str):
        self.name = name
        self.branch = branch
        self.path = path
        self.source_files: set[str] = set()


class BatchPodTools:
    # 可以进行国际化的列表
    def batchPodList() -> list[BatchPodModel]:
        os.environ["FLUTTER_IS_LOCAL"] = "false"
        podfile_json_str: str = Cmd.run("pod ipc podfile-json Podfile")
        podfile_json = json.loads(podfile_json_str)
        batch_pod_local = podfile_json["batch_pod_local"]
        pod_models = []
        for pod in batch_pod_local:
            pod_dic = batch_pod_local[pod][0]
            pod_model = BatchPodModel(
                pod,
                pod_dic["branch"],
                pod_dic["path"],
            )
            pod_models.append(pod_model)
        return pod_models

    # 获取 pod 的source_files
    def generate_pod_source_files(root_path: str, pods: list[BatchPodModel]):
        for pod in pods:
            podspec_path = ShellDir.findPodspec(pod.path)
            podspec_json_str: str = Cmd.run("pod ipc spec " + podspec_path)
            podspec_json = json.loads(podspec_json_str)
            source_paths: list[str] = podspec_json["source_files"]
            if source_paths is str:
                source_paths = [source_paths]
            module_files = set()
            for source_path in source_paths:
                source_path = root_path + "/" + pod.path + "/" + source_path
                for file_path in glob.glob(source_path):
                    if os.path.isfile(file_path):
                        module_files.add(file_path)
            pod.source_files = module_files
