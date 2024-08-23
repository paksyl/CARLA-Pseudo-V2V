"""Implements an operator that fits a linear model to predict trajectories."""

import erdos
from erdos import Message, ReadStream, WriteStream

import numpy as np
import math
import time 
import redis as redis

from pylot.prediction.messages import PredictionMessage
from pylot.prediction.obstacle_prediction import ObstaclePrediction
from pylot.utils import Location, Transform, Rotation
import pylot.simulation.utils

import carla

import csv

# While redundant, leaving this in seems to reduce the max error in prediction evaluation - 
world = pylot.simulation.utils.get_world(host='172.17.0.1')
ego_vehicle = pylot.simulation.utils.wait_for_ego_vehicle(
    world[1])

# Required to implement counter
timestamp_list = []
           
# Load columns into separete lists at startup
frames, adv_x, adv_y, adv_pitch, adv_yaw, adv_roll = [], [], [], [], [], []
with open('/home/erdos/workspace/pylot/pylot/prediction/Adversary_Locations.csv') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        frames.append(row[0])
        adv_x.append(row[1])
        adv_y.append(row[2])
        adv_pitch.append(row[3])
        adv_yaw.append(row[4])
        adv_roll.append(row[5])

init_frame = int(frames[0])


class LinearPredictorOperator(erdos.Operator):
    """Operator that implements a linear predictor.

    It takes (x,y) locations of agents in past, and fits a linear model to
    these locations.

    Args:
        tracking_stream (:py:class:`erdos.ReadStream`): The stream on which
            :py:class:`~pylot.perception.messages.ObstacleTrajectoriesMessage`
            are received.
        linear_prediction_stream (:py:class:`erdos.WriteStream`): Stream on
            which the operator sends
            :py:class:`~pylot.prediction.messages.PredictionMessage` messages.
        flags (absl.flags): Object to be used to access absl flags.
    """
    def __init__(self, tracking_stream: ReadStream,
                 time_to_decision_stream: ReadStream,
                 linear_prediction_stream: WriteStream, flags):
        tracking_stream.add_callback(self.generate_predicted_trajectories,
                                     [linear_prediction_stream])
        time_to_decision_stream.add_callback(self.on_time_to_decision_update)
        self._logger = erdos.utils.setup_logging(self.config.name,
                                                 self.config.log_file_name)
        self._flags = flags
        
        self.redis = redis.Redis(host='172.17.0.1', port=6379, decode_responses=True)

    @staticmethod
    def connect(tracking_stream: ReadStream,
                time_to_decision_stream: ReadStream):
        """Connects the operator to other streams.

        Args:
            tracking_stream (:py:class:`erdos.ReadStream`): The stream on which
                :py:class:`~pylot.perception.messages.ObstacleTrajectoriesMessage`
                are received.

        Returns:
            :py:class:`erdos.WriteStream`: Stream on which the operator sends
            :py:class:`~pylot.prediction.messages.PredictionMessage` messages.
        """
        linear_prediction_stream = erdos.WriteStream()
        return [linear_prediction_stream]

    def destroy(self):
        self._logger.warn('destroying {}'.format(self.config.name))

    def on_time_to_decision_update(self, msg):
        self._logger.debug('@{}: {} received ttd update {}'.format(
            msg.timestamp, self.config.name, msg))

    @erdos.profile_method()
    def generate_predicted_trajectories(self, msg: Message,
                                        linear_prediction_stream: WriteStream):
        self._logger.debug('@{}: received trajectories message'.format(
            msg.timestamp))
        obstacle_predictions_list = []

        nearby_obstacle_trajectories, nearby_obstacles_ego_transforms = \
            msg.get_nearby_obstacles_info(self._flags.prediction_radius)
        num_predictions = len(nearby_obstacle_trajectories)

        self._logger.info(
            '@{}: Getting linear predictions for {} obstacles'.format(
                msg.timestamp, num_predictions))

        for idx in range(len(nearby_obstacle_trajectories)):
            obstacle_trajectory = nearby_obstacle_trajectories[idx]
            predictions = []
                        
            framerate = self._flags.simulator_fps
            offset = self._flags.clock_offset
            interval_multiplier = self._flags.prediction_interval_multiplier
            
            # Get current timestamp from Scenario Runner via redis 
            sr_time = self.redis.get('SR_Time')
            #print('SR time: ', sr_time)
            current_timestamp = int(float(sr_time) + offset)

            # Adds current_timestamp to a list and counts how many instances of current_timestamp exist in the list - counter implementation w/o looping
            timestamp_list.append(str(current_timestamp))         
            counter = timestamp_list.count(str(current_timestamp))  
                        
            # Counter advances current frame by the number of occurrences of current_timestamp in the list         
            frame = current_timestamp*framerate + counter

            # Retrieve current world state from CARLA
            world = pylot.simulation.utils.get_world(host='172.17.0.1')
            ego_vehicle = pylot.simulation.utils.wait_for_ego_vehicle(world[1])
            ego_loc = ego_vehicle.get_location()
            ego_yaw = ego_vehicle.get_transform().rotation.yaw

            for t in range(self._flags.prediction_num_future_steps):
                
                # If current frame + number of frames to next prediction is greater than number of frames in dataset, inject last entry in dataset
                if (frame + t*interval_multiplier) > (init_frame + len(frames)-1):
                    rel_adv_trajectory_x = float(adv_x[len(adv_x)-1]) - ego_loc.x
                    rel_adv_trajectory_y = float(adv_y[len(adv_y)-1]) - ego_loc.y
                    #print(rel_adv_trajectory_x, ' ', 'if', ' frame: ', frame, ' len frames: ', len(frames) )
                    adv_rot = Rotation(pitch=float(adv_pitch[len(adv_pitch)-1]),
                                       yaw=float(adv_yaw[len(adv_yaw)-1]) - ego_yaw,
                                       roll=float(adv_roll[len(adv_roll)-1]))

                # If current frae + number of frames to next prediction is less than the starting frame in the dataset, inject first entry in dataset
                elif (frame + t*interval_multiplier) < init_frame:
                    rel_adv_trajectory_x = float(adv_x[0]) - ego_loc.x
                    rel_adv_trajectory_y = float(adv_y[0]) - ego_loc.y
                    #print(rel_adv_trajectory_x, ' ', 'elif')
                    adv_rot = Rotation(pitch=float(adv_pitch[0]),
                                       yaw=float(adv_yaw[0]) - ego_yaw,
                                       roll=float(adv_roll[0]))

                # 
                else:
                    rel_adv_trajectory_x = float(adv_x[frame-init_frame+t*interval_multiplier]) - ego_loc.x
                    rel_adv_trajectory_y = float(adv_y[frame-init_frame+t*interval_multiplier]) - ego_loc.y
                    #print(rel_adv_trajectory_x, ' ', 'else')
                    adv_rot = Rotation(pitch=float(adv_pitch[frame-init_frame+t*interval_multiplier]),
                                       yaw=float(adv_yaw[frame-init_frame+t*interval_multiplier]) - ego_yaw,
                                       roll=float(adv_roll[frame-init_frame+t*interval_multiplier]))

                adv_trajectory_x = np.cos(math.radians(-ego_yaw))*rel_adv_trajectory_x - np.sin(math.radians(-ego_yaw))*rel_adv_trajectory_y
                adv_trajectory_y = np.cos(math.radians(-ego_yaw))*rel_adv_trajectory_y + np.sin(math.radians(-ego_yaw))*rel_adv_trajectory_x

                # Prediction is expected in terms of relative coordinates from the ego vehicle, and is converted back to global coordinates during evaluation
                predictions.append(Transform(location=Location(x=adv_trajectory_x, y=adv_trajectory_y),
                                             rotation=adv_rot))
                                             

            obstacle_predictions_list.append(
                ObstaclePrediction(obstacle_trajectory,
                                   obstacle_trajectory.obstacle.transform, 1.0,
                                   predictions))
            
            # Monitor wheel angle
            #wheel_FL = str(ego_vehicle.get_wheel_steer_angle(carla.VehicleWheelLocation.FL_Wheel))
            #wheel_FR = str(ego_vehicle.get_wheel_steer_angle(carla.VehicleWheelLocation.FR_Wheel))
            #wheel_BL = str(ego_vehicle.get_wheel_steer_angle(carla.VehicleWheelLocation.BL_Wheel))
            #wheel_BR = str(ego_vehicle.get_wheel_steer_angle(carla.VehicleWheelLocation.BR_Wheel))
                  
            #with open('EgoWheelSteerAngle.csv', 'a') as outfile:
            #    writer = csv.writer(outfile)
            #    writer.writerows(zip(['FL: ',wheel_FL,'FR: ',wheel_FR,'BL: ',wheel_BL,'BR: ',wheel_BR]))                       

        linear_prediction_stream.send(
            PredictionMessage(msg.timestamp, obstacle_predictions_list))
