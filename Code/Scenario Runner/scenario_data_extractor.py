import sys
import csv
import matplotlib.pyplot as plt
from srunner.metrics.examples.basic_metric import BasicMetric

class ScenarioDataExtractor(BasicMetric):
    
    def _create_metric(self, town_map, log, criteria):
        ego_id = log.get_ego_vehicle_id()
        adv_id = log.get_actor_ids_with_role_name("npc_vehicle")[0]

        #ttc_list = []
        #ittc_list = []
        frames_list = ['frames']
        #seconds_list = []
        elapsed_time_list = ['elapsed_time']
        delta_time_list = ['delta_time']
        
        adv_location_x_list = ['adv_loc_x']
        adv_location_y_list = ['adv_loc_y']
        adv_rotation_pitch_list = ['adv_pitch']
        adv_rotation_yaw_list = ['adv_yaw']
        adv_rotation_roll_list = ['adv_roll']
        adv_accel_x_list = ['adv_accel_x']
        adv_accel_y_list = ['adv_accel_y']
        adv_ang_vel_x_list = ['adv_ang_vel_x']
        adv_ang_vel_y_list = ['adv_ang_vel_y']
        adv_throttle_list = ['adv_throttle']
        adv_brake_list = ['adv_brake']
        adv_reverse_list = ['adv_reverse']
        adv_gear_list = ['adv_gear']
        adv_vel_x_list = ['adv_vel_x']
        adv_vel_y_list = ['adv_vel_y']

        ego_location_x_list = ['ego_loc_x']
        ego_location_y_list = ['ego_loc_y']
        ego_rotation_pitch_list = ['ego_pitch']
        ego_rotation_yaw_list = ['ego_yaw']
        ego_rotation_roll_list = ['ego_roll']
        ego_accel_x_list = ['ego_accel_x']
        ego_accel_y_list = ['ego_accel_y']
        ego_ang_vel_x_list = ['ego_ang_vel_x']
        ego_ang_vel_y_list = ['ego_ang_vel_y']
        ego_throttle_list = ['ego_throttle']
        ego_brake_list = ['ego_brake']
        ego_reverse_list = ['ego_reverse']
        ego_gear_list = ['ego_gear']
        ego_vel_x_list = ['ego_vel_x']
        ego_vel_y_list = ['ego_vel_y']

        start_ego, end_ego = log.get_actor_alive_frames(ego_id)
        start_adv, end_adv = log.get_actor_alive_frames(adv_id)
        start = max(start_ego, start_adv)
        end = min(end_ego, end_adv)


        for i in range(start, end):
            delta_time = log.get_delta_time(i)
            elapsed_time = log.get_elapsed_time(i)
        
            ego_location = log.get_actor_transform(ego_id, i).location
            ego_rotation = log.get_actor_transform(ego_id, i).rotation
            ego_velocity = log.get_actor_velocity(ego_id, i)
            ego_acceleration = log.get_actor_acceleration(ego_id, i)
            ego_control = log.get_vehicle_control(ego_id, i)
            ego_ang_vel = log.get_actor_angular_velocity(ego_id, i)

            adv_location = log.get_actor_transform(adv_id, i).location
            adv_rotation = log.get_actor_transform(adv_id, i).rotation
            adv_velocity = log.get_actor_velocity(adv_id, i)
            adv_acceleration = log.get_actor_acceleration(adv_id, i)
            adv_control = log.get_vehicle_control(adv_id, i)
            adv_ang_vel = log.get_actor_angular_velocity(adv_id, i)

            if adv_location.z < -10:
                continue
            
            
            ego_location_x_list.append(ego_location.x)
            ego_location_y_list.append(ego_location.y)
            ego_rotation_pitch_list.append(ego_rotation.pitch)
            ego_rotation_yaw_list.append(ego_rotation.yaw)
            ego_rotation_roll_list.append(ego_rotation.roll)
            ego_vel_x_list.append(ego_velocity.x)
            ego_vel_y_list.append(ego_velocity.y)
            ego_accel_x_list.append(ego_acceleration.x)
            ego_accel_y_list.append(ego_acceleration.y)
            ego_throttle_list.append(ego_control.throttle)
            ego_brake_list.append(ego_control.brake)
            ego_reverse_list.append(ego_control.reverse)
            ego_gear_list.append(ego_control.gear)
            ego_ang_vel_x_list.append(ego_ang_vel.x)
            ego_ang_vel_y_list.append(ego_ang_vel.y)            
            
            adv_location_x_list.append(adv_location.x)
            adv_location_y_list.append(adv_location.y)
            adv_rotation_pitch_list.append(adv_rotation.pitch)
            adv_rotation_yaw_list.append(adv_rotation.yaw)
            adv_rotation_roll_list.append(adv_rotation.roll)
            adv_vel_x_list.append(adv_velocity.x)
            adv_vel_y_list.append(adv_velocity.y)
            adv_accel_x_list.append(adv_acceleration.x)
            adv_accel_y_list.append(adv_acceleration.y)
            adv_throttle_list.append(adv_control.throttle)
            adv_brake_list.append(adv_control.brake)
            adv_reverse_list.append(adv_control.reverse)
            adv_gear_list.append(adv_control.gear)
            adv_ang_vel_x_list.append(adv_ang_vel.x)
            adv_ang_vel_y_list.append(adv_ang_vel.y)

            frames_list.append(i)
            elapsed_time_list.append(elapsed_time)
            delta_time_list.append(delta_time)
            

        # ax1 = plt.subplots()
        # ax1.plot(frames_list, ttc_list, color='red')
        # ax1.ylabel('Time to Collision [s]')
        # ax1.xlabel('Frame number')
        #
        # ax2 = ax1.twinx()
        # ax2.plot(frames_list, ittc_list, color='blue')
        # ax2.ylabel('Inverse Time to Collision [1/s]')
        #
        # plt.title('Instantaneous TTC and iTTC between the ego and adversary vehicles')
        # plt.show()
        #print('Frames', '   ', 'Adversary Location', '   ', 'Adversary Rotation')
        #with open('Adversary_Locations.txt', 'w') as outfile:
        #  outfile.write('Frames   Adversary Location   Adversary Rotation')
        
        
        #for j in range(len(frames_list)):
          #with open('Adversary_Locations.txt', 'w') as outfile:
            #outfile.write(str(frames_list[j])+str(adv_location_list[j]+str(adv_rotation_list[j]))
            #outfile.write('   ',)
            #outfile.write(str(adv_location_list[j]))
            #outfile.write('   ')
            #outfile.write(str(adv_rotation_list[j]))
            #outfile.write('\n')
          #print(frames_list[j], " ", adv_location_list[j], " ", adv_rotation_list[j])
       
        
        # Retrieve log file name from args 
        args = sys.argv
        keyword = '.log'
        log_file_name = None
        
        for arg in args:
            if keyword in arg:
                log_file = arg.replace('.log', '')
                log_file_name = log_file.split('/')
                log_file_name = log_file_name[-1]
        
        csv_file_name = log_file_name + '.csv'  
        with open(csv_file_name, 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(zip(frames_list, elapsed_time_list, delta_time_list, adv_location_x_list,
            adv_location_y_list, adv_rotation_pitch_list, adv_rotation_yaw_list,
            adv_rotation_roll_list, adv_vel_x_list, adv_vel_y_list, adv_accel_x_list, adv_accel_y_list, 
            adv_throttle_list, adv_brake_list, adv_reverse_list, adv_gear_list, adv_ang_vel_x_list, 
            adv_ang_vel_y_list, ego_location_x_list, ego_location_y_list, ego_rotation_pitch_list, 
            ego_rotation_yaw_list, ego_rotation_roll_list, ego_vel_x_list, ego_vel_y_list, ego_accel_x_list, 
            ego_accel_y_list, ego_throttle_list, ego_brake_list, ego_reverse_list, ego_gear_list, 
            ego_ang_vel_x_list, ego_ang_vel_y_list))
            #outfile.write('\n'.join(str(frames_list[j])+str(adv_location_list[j])+str(adv_rotation_list[j]) for j in len(frames_list)))
        
          
          
          
