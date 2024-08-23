import csv
import matplotlib.pyplot as plt
from srunner.metrics.examples.basic_metric import BasicMetric

class GetAdvLoc(BasicMetric):


    def _create_metric(self, town_map, log, criteria):
        ego_id = log.get_ego_vehicle_id()
        adv_id = log.get_actor_ids_with_role_name("npc_vehicle")[0]

        ttc_list = []
        ittc_list = []
        frames_list = []
        seconds_list = []
        adv_location_x_list = []
        adv_location_y_list = []
        adv_rotation_pitch_list = []
        adv_rotation_yaw_list = []
        adv_rotation_roll_list = []

        start_ego, end_ego = log.get_actor_alive_frames(ego_id)
        start_adv, end_adv = log.get_actor_alive_frames(adv_id)
        start = max(start_ego, start_adv)
        end = min(end_ego, end_adv)

        # Calculate TTC at every frame

        for i in range(start, end):
            # ego_location = log.get_actor_transform(ego_id, i).location
            # ego_velocity = log.get_actor_velocity(ego_id, i)
            # ego_acceleration = log.get_actor_acceleration(ego_id, i)

            adv_location = log.get_actor_transform(adv_id, i).location
            adv_rotation = log.get_actor_transform(adv_id, i).rotation
            # adv_velocity = log.get_actor_velocity(adv_id, i)
            # adv_acceleration = log.get_actor_acceleration(adv_id, i)

            if adv_location.z < -10:
                continue

            # dist_v = ego_location - adv_location
            # dist = math.sqrt(dist_v.x*dist_v.x + dist_v.y*dist_v.y + dist_v.z * dist_v.z)
            #
            # vel_v = ego_velocity - adv_velocity
            # vel = math.sqrt(vel_v.x*vel_v.x + vel_v.y*vel_v.y + vel_v.z*vel_v.z)

            #if (i % 20 == 0):
            #    seconds_list.append(i/20)
            #    adv_location_list.append([adv_location.x, adv_location.y])
            #    adv_rotation_list.append([adv_rotation.pitch, adv_rotation.yaw, adv_rotation.roll])
            
            adv_location_x_list.append(adv_location.x)
            adv_location_y_list.append(adv_location.y)
            adv_rotation_pitch_list.append(adv_rotation.pitch)
            adv_rotation_yaw_list.append(adv_rotation.yaw)
            adv_rotation_roll_list.append(adv_rotation.roll)


            frames_list.append(i)

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
        print('Frames', '   ', 'Adversary Location', '   ', 'Adversary Rotation')
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
          
        with open('Adversary_Locations.csv', 'w') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(zip(frames_list, adv_location_x_list,
            adv_location_y_list, adv_rotation_pitch_list, adv_rotation_yaw_list,
            adv_rotation_roll_list))
            #outfile.write('\n'.join(str(frames_list[j])+str(adv_location_list[j])+str(adv_rotation_list[j]) for j in len(frames_list)))
        
          
          
          
