from kfp.v2.dsl import component, Input, Output, Artifact, Dataset


@component(
    base_image="europe-west1-docker.pkg.dev/hoodat-sandbox/hoodat-sandbox-kfp-components/bytetrack_from_video",
    output_component_file="component.yaml",
)
def bytetrack_from_video(
    input_video: Input[Artifact],
    input_weights: Input[Artifact],
    output_video: Output[Artifact],
    output_text_file_dataset: Output[Dataset],
    device: str = "gpu",  # Must be gpu or cpu
):
    import shutil
    from tools.demo_track import make_parser, main, get_exp

    if device == "gpu":
        arg_list = [
            "video",
            "-f",
            "/ByteTrack/exps/example/mot/yolox_x_mix_det.py",
            "-c",
            input_weights.path,
            "--path",
            input_video.path,
            "--fp16",
            "--fuse",
            "--save_result",
        ]
    elif device == "cpu":
        arg_list = [
            "video",
            "-f",
            "/ByteTrack/exps/example/mot/yolox_x_mix_det.py",
            "-c",
            input_weights.path,
            "--device",
            "cpu",
            "--path",
            input_video.path,
            "--fuse",
            "--save_result",
        ]

    args = make_parser().parse_args(arg_list)
    exp = get_exp(args.exp_file, args.name)
    main(exp=exp, args=args)

    source_dir = "/ByteTrack/YOLOX_outputs/yolox_x_mix_det/track_vis"
    source_video = f"{source_dir}/output.mp4"
    source_results = f"{source_dir}/results.txt"
    destination_video = output_video.path
    destination_results_dataset = output_text_file_dataset.path
    shutil.copyfile(source_video, destination_video)
    shutil.copyfile(source_results, destination_results_dataset)
