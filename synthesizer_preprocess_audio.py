from synthesizer.preprocess import preprocess_librispeech, preprocess_custom
from synthesizer.hparams import hparams
from utils.argutils import print_args
from pathlib import Path
import argparse
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'  ## Supress Tensorflow warning and deprecated package messages

def run_custom(datasets_root, out_dir, n_processes=4, skip_existing=True):  
    datasets_root = Path(datasets_root)
    out_dir = Path(out_dir)
    preprocess_custom(datasets_root, out_dir, n_processes, skip_existing, hparams)

def main():
    parser = argparse.ArgumentParser(
        description="Preprocesses audio files from datasets, encodes them as mel spectrograms "
                    "and writes them to  the disk. Audio files are also saved, to be used by the "
                    "vocoder for training.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("datasets_root", type=Path, help=\
        "Path to the directory containing your LibriSpeech/TTS datasets.")
    parser.add_argument("-o", "--out_dir", type=Path, default=argparse.SUPPRESS, help=\
        "Path to the output directory that will contain the mel spectrograms, the audios and the "
        "embeds. Defaults to <datasets_root>/SV2TTS/synthesizer/")
    parser.add_argument("-n", "--n_processes", type=int, default=8, help=\
        "Number of processes in parallel.")
    parser.add_argument("-s", "--skip_existing", action="store_true", help=\
        "Whether to overwrite existing files with the same name. Useful if the preprocessing was "
        "interrupted.")
    parser.add_argument("--hparams", type=str, default="", help=\
        "Hyperparameter overrides as a comma-separated list of name-value pairs")
    parser.add_argument("-d", "--datasets", type=str,
                        default="librispeech_other")
    args = parser.parse_args()
    args.datasets = args.datasets.split(",")

    # Process the arguments
    if not hasattr(args, "out_dir"):
        args.out_dir = args.datasets_root.joinpath("SV2TTS", "synthesizer")

    # Create directories
    assert args.datasets_root.exists()
    args.out_dir.mkdir(exist_ok=True, parents=True)

    # Preprocess the dataset
    print_args(args, parser)
    args.hparams = hparams.parse(args.hparams)

    preprocess_func = {
        "custom": preprocess_custom,
        "librispeech_other": preprocess_librispeech,
    }
    args = vars(args)


    for dataset in args.pop("datasets"):
        print("Preprocessing %s" % dataset)
        preprocess_func[dataset](**args)

    # preprocess_librispeech(**vars(args))

if __name__ == "__main__":
    main()
