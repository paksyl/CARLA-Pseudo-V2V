# pylot/pylot/prediction/flags.py

from absl import flags

flags.DEFINE_integer(
    'prediction_num_past_steps', None,
    'Number of past steps of each agent given to the prediction module.')
flags.DEFINE_integer(
    'prediction_num_future_steps', None,
    'Number of future steps outputted by the prediction module.')
flags.DEFINE_integer(
    'prediction_radius', 50,
    'Make predictions for agents within radius (in m) of the ego-vehicle.')
flags.DEFINE_boolean('prediction_ego_agent', False,
                     'Whether we make predictions for the ego agent')

# R2P2 Flags
flags.DEFINE_string('r2p2_model_path',
                    'dependencies/models/prediction/r2p2/r2p2-model.pt',
                    'Path to the model')
                    
                    
# Offset amount for synchronising simulator and scenario runner clocks
flags.DEFINE_float(
    'clock_offset', 0,
    'Amount of time in seconds the received scenario runner timestamp should be offset by. Default = 0.')
    
# Prediction interval multiplier
flags.DEFINE_integer(
    'prediction_interval_multiplier', 1,
    'Multiplier for changing the interval between prediction instances within a prediction loop. Default = 1.')                        
