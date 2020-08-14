from pathlib import Path
#------------------------------------------------------------------------------------
gpu_id = '0,1,2,3,4,5,6,7'

#------------------------------------------------------------------------------------

# DeepTalk encoder (model_GST: fCNN -> GST) trained on Librispeech, VoxCeleb1, and VoxCeleb2 Data
# Generic Model
# enc_model_fpath = Path('trained_models/Generic/Encoder/model_GST.pt')
# enc_module_name = "model_GST"
# syn_model_dir = Path('trained_models/Generic/Synthesizer/logs-model_GST/taco_pretrained/')
# voc_model_fpath = Path('trained_models/Generic/Vocoder/model_GST/model_GST.pt')

#------------------------------------------------------------------------------------

# DeepTalk encoder (model_GST: fCNN -> GST) trained on Librispeech, VoxCeleb1, and VoxCeleb2 Data 
# and finetuned on a specific male speaker
# enc_model_fpath = Path('trained_models/Sample_Male/Encoder/model_GST.pt')
# enc_module_name = "model_GST"
# syn_model_dir = Path('trained_models/Sample_Male/Synthesizer/logs-model_GST_ft/taco_pretrained/')
# voc_model_fpath = Path('trained_models/Sample_Male/Vocoder/model_GST_ft/model_GST_ft.pt')
#------------------------------------------------------------------------------------

# DeepTalk encoder (model_GST: fCNN -> GST) trained on Librispeech, VoxCeleb1, and VoxCeleb2 Data 
# and finetuned on a specific female speaker
# enc_model_fpath = Path('trained_models/Sample_Female/Encoder/model_GST.pt')
# enc_module_name = "model_GST"
# syn_model_dir = Path('trained_models/Sample_Female/Synthesizer/logs-model_GST_ft/taco_pretrained/')
# voc_model_fpath = Path('trained_models/Sample_Female/Vocoder/model_GST_ft/model_GST_ft.pt')

#------------------------------------------------------------------------------------
# DeepTalk encoder (model_GST: fCNN -> GST) trained on Librispeech, VoxCeleb1, and VoxCeleb2 Data
# and finetuned on Hannah
# enc_model_fpath = Path('trained_models/Hannah/Encoder/model_GST.pt')
# enc_module_name = "model_GST"
# syn_model_dir = Path('trained_models/Hannah/Synthesizer/logs-model_GST_ft/taco_pretrained/')
# voc_model_fpath = Path('trained_models/Hannah/Vocoder/model_GST_ft/model_GST_ft.pt')

#------------------------------------------------------------------------------------
# DeepTalk encoder (model_GST: fCNN -> GST) trained on Librispeech, VoxCeleb1, and VoxCeleb2 Data 
# and finetuned on Ted
# enc_model_fpath = Path('trained_models/Ted/Encoder/model_GST.pt')
# enc_module_name = "model_GST"
# syn_model_dir = Path('trained_models/Ted/Synthesizer/logs-model_GST_ft/taco_pretrained/')
# voc_model_fpath = Path('trained_models/Ted/Vocoder/model_GST_ft/model_GST_ft.pt')

#------------------------------------------------------------------------------------
# DeepTalk encoder (model_GST: fCNN -> GST) trained on Librispeech, VoxCeleb1, and VoxCeleb2 Data 
# and finetuned on Obama
enc_model_fpath = Path('trained_models/Obama/Encoder/model_GST.pt')
enc_module_name = "model_GST"
syn_model_dir = Path('trained_models/Obama/Synthesizer/logs-model_GST_ft/taco_pretrained/')
voc_model_fpath = Path('trained_models/Obama/Vocoder/model_GST_ft/model_GST_ft.pt')
