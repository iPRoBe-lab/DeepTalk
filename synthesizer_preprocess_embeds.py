from synthesizer.preprocess import create_embeddings
from utils.argutils import print_args
from pathlib import Path
import argparse, os

def run_custom(synthesizer_root, encoder_model_fpath, module_name, n_processes, gpu_id):
    create_embeddings(Path(synthesizer_root), Path(encoder_model_fpath), module_name, n_processes, gpu_id)

def main():
    parser = argparse.ArgumentParser(
        description="Creates embeddings for the synthesizer from the LibriSpeech utterances.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("synthesizer_root", type=Path, help=\
        "Path to the synthesizer training data that contains the audios and the train.txt file. "
        "If you let everything as default, it should be <datasets_root>/SV2TTS/synthesizer/.")
    parser.add_argument("-e", "--encoder_model_fpath", type=Path,
                        default="encoder/saved_models/pretrained.pt", help=\
        "Path your trained encoder model.")

    parser.add_argument("--module_name", type=str, default="model_baseline")

    parser.add_argument("-n", "--n_processes", type=int, default=8, help= \
        "Number of parallel processes. An encoder is created for each, so you may need to lower "
        "this value on GPUs with low memory. Set it to 1 if CUDA is unhappy.")
    parser.add_argument("-gpuid", "--gpu_id", type=str, default='0', help= \
        "Select the GPU to run the code")
    args = parser.parse_args()

    # Preprocess the dataset
    print_args(args, parser)
    create_embeddings(**vars(args))


if __name__ == "__main__":
    main()
