from synthesizer.hparams import hparams
from synthesizer.train import tacotron_train
from utils.argutils import print_args
from synthesizer import infolog
import argparse
import os


def run_custom(finetuned_model_name, pretrained_model_name, syn_files_dir, finetuned_syn_model_dir, gpu_id):

    class args_cls:
        def __init__(self, name, synthesizer_root, module_name, gpu_id):
            self.mode = "synthesis"
            self.GTA = "True"
            self.restore = True
            self.name = name
            self.synthesizer_root = synthesizer_root
            self.module_name = module_name
            self.gpu_id = gpu_id
            self.tacotron_train_steps = 750000
            self.checkpoint_interval = 2000
            self.summary_interval = 2500
            self.embedding_interval = 10000
            self.eval_interval = 100000
            self.tf_log_level = 1

        

    args = args_cls(finetuned_model_name, syn_files_dir, pretrained_model_name, gpu_id)
    log_dir = finetuned_syn_model_dir

    tacotron_train(args, log_dir, hparams)


def prepare_run(args):
    modified_hp = hparams.parse(args.hparams)
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = str(args.tf_log_level)
    run_name = args.name
    log_dir = os.path.join(args.models_dir, "logs-{}".format(run_name))
    os.makedirs(log_dir, exist_ok=True)
    infolog.init(os.path.join(log_dir, "Terminal_train_log"), run_name, args.slack_url)
    return log_dir, modified_hp

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("name", help="Name of the run and of the logging directory.")
    parser.add_argument("synthesizer_root", type=str, help=\
        "Path to the synthesizer training data that contains the audios and the train.txt file. "
        "If you let everything as default, it should be <datasets_root>/SV2TTS/synthesizer/.")
    parser.add_argument("-m", "--models_dir", type=str, default="synthesizer/saved_models/", help=\
        "Path to the output directory that will contain the saved model weights and the logs.")
    parser.add_argument("--mode", default="synthesis",
                        help="mode for synthesis of tacotron after training")
    parser.add_argument("--GTA", default="True",
                        help="Ground truth aligned synthesis, defaults to True, only considered "
							 "in Tacotron synthesis mode")
    parser.add_argument("--module_name", type=str, default="model_baseline")
    parser.add_argument("--restore", type=bool, default=True,
                        help="Set this to False to do a fresh training")
    parser.add_argument("--summary_interval", type=int, default=2500,
                        help="Steps between running summary ops")
    parser.add_argument("--embedding_interval", type=int, default=10000,
                        help="Steps between updating embeddings projection visualization")
    parser.add_argument("--checkpoint_interval", type=int, default=2000, # Was 5000
                        help="Steps between writing checkpoints")
    parser.add_argument("--eval_interval", type=int, default=100000, # Was 10000
                        help="Steps between eval on test data")
    parser.add_argument("--tacotron_train_steps", type=int, default=750000, # Was 100000
                        help="total number of tacotron training steps")
    parser.add_argument("--tf_log_level", type=int, default=1, help="Tensorflow C++ log level.")
    parser.add_argument("--slack_url", default=None,
                        help="slack webhook notification destination link")
    parser.add_argument("--hparams", default="",
                        help="Hyperparameter overrides as a comma-separated list of name=value "
							 "pairs")
    parser.add_argument("-gpuid", "--gpu_id", type=str, default='0', help= \
        "Select the GPU to run the code")

    args = parser.parse_args()
    print_args(args, parser)

    log_dir, hparams = prepare_run(args)

    tacotron_train(args, log_dir, hparams)


if __name__ == "__main__":
    main()
