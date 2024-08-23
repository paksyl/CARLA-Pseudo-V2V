# Creates a car following scenario in OpenSCENARIO (.xosc) format from time-series vehicle longitudinal velocity data
# given in .csv format. The longitudinal velocity is assigned to the lead vehicle.

import sys
import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime
from tqdm import tqdm


# Load CSV
file = input("Path to CSV file: ")
try:
    csvfile = pd.read_csv(file)
except:
    print("File not found. Please specify the correct path.")
    sys.exit(1)


# Save OpenSCENARIO file as
saveAs = input("Save .xosc as: ")
print("Creating %s.xosc..." % saveAs)


# OpenSCENARIO
OpenSCENARIO = ET.Element('OpenSCENARIO')


# FileHeader
FileHeader = ET.SubElement(OpenSCENARIO, 'FileHeader')
FileHeader.set('revMajor', '1')
FileHeader.set('revMinor', '0')
FileHeader.set('date', '%s' % datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'))
FileHeader.set('description', '%s scenario' % saveAs)
FileHeader.set('author', 'csv2xosc')

# ParameterDeclarations
ParameterDeclarations = ET.SubElement(OpenSCENARIO, 'ParameterDeclarations')

ParameterDeclaration = ET.SubElement(ParameterDeclarations, 'ParameterDeclaration')
ParameterDeclaration.set('name', 'LeadVehicle')
ParameterDeclaration.set('parameterType', 'string')
ParameterDeclaration.set('value', 'vehicle.tesla.model3')

ParameterDeclaration2 = ET.SubElement(ParameterDeclarations, 'ParameterDeclaration')
ParameterDeclaration2.set('name', 'HeroVehicle')
ParameterDeclaration2.set('parameterType', 'string')
ParameterDeclaration2.set('value', 'vehicle.lincoln.mkz_2017')

# CatalogLocations
CatalogLocations = ET.SubElement(OpenSCENARIO, 'CatalogLocations')

VehicleCatalog = ET.SubElement(CatalogLocations, 'VehicleCatalog')

Vehicle_Directory = ET.SubElement(VehicleCatalog, 'Directory')
Vehicle_Directory.set('path', 'catalogs')

# RouteCatalog = ET.SubElement(CatalogLocations, 'RouteCatalog')
#
# Route_Directory = ET.SubElement(RouteCatalog, 'Directory')
# Route_Directory.set('path', '../xosc/Catalogs/Routes')

# RoadNetwork
RoadNetwork = ET.SubElement(OpenSCENARIO, 'RoadNetwork')

LogicFile = ET.SubElement(RoadNetwork, 'LogicFile')
LogicFile.set('filepath', 'Town01')

# SceneGraphFile = ET.SubElement(RoadNetwork, 'SceneGraphFile')
# SceneGraphFile.set('filepath', '../models/fabriksgatan.osgb')


# Entities
Entities = ET.SubElement(OpenSCENARIO, 'Entities')

ScenarioObject = ET.SubElement(Entities, 'ScenarioObject')
ScenarioObject.set('name', 'npc_vehicle')

CatalogReference = ET.SubElement(ScenarioObject, 'CatalogReference')
CatalogReference.set('catalogName', 'VehicleCatalog')
CatalogReference.set('entryName', '$LeadVehicle')

ScenarioObject2 = ET.SubElement(Entities, 'ScenarioObject')
ScenarioObject2.set('name', 'hero')

CatalogReference2 = ET.SubElement(ScenarioObject2, 'CatalogReference')
CatalogReference2.set('catalogName', 'VehicleCatalog')
CatalogReference2.set('entryName', '$HeroVehicle')

# Storyboard
Storyboard = ET.SubElement(OpenSCENARIO, 'Storyboard')


# Init
Init = ET.SubElement(Storyboard, 'Init')

Actions = ET.SubElement(Init, 'Actions')

GlobalAction = ET.SubElement(Actions, 'GlobalAction')

EnvironmentAction = ET.SubElement(GlobalAction, 'EnvironmentAction')

Environment = ET.SubElement(EnvironmentAction, 'Environment')
Environment.set('name', 'Environment1')

TimeOfDay = ET.SubElement(Environment, 'TimeOfDay')
TimeOfDay.set('animation', 'false')
TimeOfDay.set('dateTime', '%s' % datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S'))

Weather = ET.SubElement(Environment, 'Weather')
Weather.set('cloudState', 'free')

Sun = ET.SubElement(Weather, 'Sun')
Sun.set('intensity', '0.85')
Sun.set('azimuth', '0')
Sun.set('elevation', '1.31')

Fog = ET.SubElement(Weather, 'Fog')
Fog.set('visualRange', '100000.0')

Precipitation = ET.SubElement(Weather, 'Precipitation')
Precipitation.set('precipitationType', 'dry')
Precipitation.set('intensity', '0.0')

RoadCondition = ET.SubElement(Environment, 'RoadCondition')
RoadCondition.set('frictionScaleFactor', '1.0')

Private = ET.SubElement(Actions, 'Private')
Private.set('entityRef', 'npc_vehicle')

PrivateAction = ET.SubElement(Private, 'PrivateAction')

LongitudinalAction = ET.SubElement(PrivateAction, 'LongitudinalAction')

SpeedAction = ET.SubElement(LongitudinalAction, 'SpeedAction')

SpeedActionDynamics = ET.SubElement(SpeedAction, 'SpeedActionDynamics')
SpeedActionDynamics.set('dynamicsShape', 'step')
SpeedActionDynamics.set('dynamicsDimension', 'time')
SpeedActionDynamics.set('value', '0')

SpeedActionTarget = ET.SubElement(SpeedAction, 'SpeedActionTarget')

AbsoluteTargetSpeed = ET.SubElement(SpeedActionTarget, 'AbsoluteTargetSpeed')
AbsoluteTargetSpeed.set('value', '%s' % csvfile.loc[0].at['Speed'])

Teleport_PrivateAction = ET.SubElement(Private, 'PrivateAction')

TeleportAction = ET.SubElement(Teleport_PrivateAction, 'TeleportAction')

Position = ET.SubElement(TeleportAction, 'Position')

# LanePosition = ET.SubElement(Position, 'LanePosition')
# LanePosition.set('roadId', '0')
# LanePosition.set('laneId', '-1')
# LanePosition.set('offset', '0')
# LanePosition.set('s', '10')

# WorldPosition = ET.SubElement(Position, 'WorldPosition')
# WorldPosition.set('x', '131') # x position
# WorldPosition.set('y', '199.1430054') # y position
# WorldPosition.set('p', '0') # pitch
# WorldPosition.set('h', '0.004655819852') # yaw
# WorldPosition.set('r', '0') # roll

# LanePosition = ET.SubElement(Position, 'LanePosition')
# LanePosition.set('roadId', '4')
# LanePosition.set('laneId', '-1')
# LanePosition.set('offset', '1.0')
# LanePosition.set('s', '53.58')

RelativeRoadPosition = ET.SubElement(Position, 'RelativeRoadPosition')
RelativeRoadPosition.set('entityRef', 'hero')
RelativeRoadPosition.set('ds', '10')
RelativeRoadPosition.set('dt', '0')

Controller_PrivateAction = ET.SubElement(Private, 'PrivateAction')

ControllerAction = ET.SubElement(Controller_PrivateAction, 'ControllerAction')

AssignControllerAction = ET.SubElement(ControllerAction, 'AssignControllerAction')

Controller = ET.SubElement(AssignControllerAction, 'Controller')
Controller.set('name', 'LeadAgent')

Controller_Properties = ET.SubElement(Controller, 'Properties')

Controller_Property = ET.SubElement(Controller_Properties, 'Property')
Controller_Property.set('name', 'module')
# Controller_Property.set('value', 'npc_vehicle_control')
Controller_Property.set('value', 'simple_vehicle_control')

Camera_Property = ET.SubElement(Controller_Properties, 'Property')
Camera_Property.set('name', 'attach_camera')
Camera_Property.set('value', 'True')

OverrideControllerValueAction = ET.SubElement(ControllerAction, 'OverrideControllerValueAction')

Throttle = ET.SubElement(OverrideControllerValueAction, 'Throttle')
Throttle.set('value', '0')
Throttle.set('active', 'false')

Brake = ET.SubElement(OverrideControllerValueAction, 'Brake')
Brake.set('value', '0')
Brake.set('active', 'false')

Clutch = ET.SubElement(OverrideControllerValueAction, 'Clutch')
Clutch.set('value', '0')
Clutch.set('active', 'false')

ParkingBrake = ET.SubElement(OverrideControllerValueAction, 'ParkingBrake')
ParkingBrake.set('value', '0')
ParkingBrake.set('active', 'false')

SteeringWheel = ET.SubElement(OverrideControllerValueAction, 'SteeringWheel')
SteeringWheel.set('value', '0')
SteeringWheel.set('active', 'false')

Gear = ET.SubElement(OverrideControllerValueAction, 'Gear')
Gear.set('number', '0')
Gear.set('active', 'false')

Private_Hero = ET.SubElement(Actions, 'Private')
Private_Hero.set('entityRef', 'hero')

Teleport_PrivateAction_Hero = ET.SubElement(Private_Hero, 'PrivateAction')

TeleportAction_Hero = ET.SubElement(Teleport_PrivateAction_Hero, 'TeleportAction')

Position_Hero = ET.SubElement(TeleportAction_Hero, 'Position')

LanePosition_Hero = ET.SubElement(Position_Hero, 'LanePosition')
LanePosition_Hero.set('roadId', '8')
LanePosition_Hero.set('laneId', '-1')
LanePosition_Hero.set('offset', '0.0')
LanePosition_Hero.set('s', '0.0')

Controller_PrivateAction_Hero = ET.SubElement(Private_Hero, 'PrivateAction')

ControllerAction_Hero = ET.SubElement(Controller_PrivateAction_Hero, 'ControllerAction')

AssignControllerAction_Hero = ET.SubElement(ControllerAction_Hero, 'AssignControllerAction')

Controller_Hero = ET.SubElement(AssignControllerAction_Hero, 'Controller')
Controller_Hero.set('name', 'HeroAgent')

Controller_Properties_Hero = ET.SubElement(Controller_Hero, 'Properties')

Controller_Property_Hero = ET.SubElement(Controller_Properties_Hero, 'Property')
Controller_Property_Hero.set('name', 'module')
Controller_Property_Hero.set('value', 'external_control')

OverrideControllerValueAction_Hero = ET.SubElement(ControllerAction_Hero, 'OverrideControllerValueAction')

Throttle_Hero = ET.SubElement(OverrideControllerValueAction_Hero, 'Throttle')
Throttle_Hero.set('value', '0')
Throttle_Hero.set('active', 'false')

Brake_Hero = ET.SubElement(OverrideControllerValueAction_Hero, 'Brake')
Brake_Hero.set('value', '0')
Brake_Hero.set('active', 'false')

Clutch_Hero = ET.SubElement(OverrideControllerValueAction_Hero, 'Clutch')
Clutch_Hero.set('value', '0')
Clutch_Hero.set('active', 'false')

ParkingBrake_Hero = ET.SubElement(OverrideControllerValueAction_Hero, 'ParkingBrake')
ParkingBrake_Hero.set('value', '0')
ParkingBrake_Hero.set('active', 'false')

SteeringWheel_Hero = ET.SubElement(OverrideControllerValueAction_Hero, 'SteeringWheel')
SteeringWheel_Hero.set('value', '0')
SteeringWheel_Hero.set('active', 'false')

Gear_Hero = ET.SubElement(OverrideControllerValueAction_Hero, 'Gear')
Gear_Hero.set('number', '0')
Gear_Hero.set('active', 'false')

# Story
Story = ET.SubElement(Storyboard, 'Story')
Story.set('name', '%s_Story' % saveAs)

Act = ET.SubElement(Story, 'Act')
Act.set('name', '%s_Act' % saveAs)

ManeuverGroup = ET.SubElement(Act, 'ManeuverGroup')
ManeuverGroup.set('maximumExecutionCount', '1')
ManeuverGroup.set('name', '%s_ManeuverGroup' % saveAs)

Actors = ET.SubElement(ManeuverGroup, 'Actors')
Actors.set('selectTriggeringEntities', 'false')

EntityRef = ET.SubElement(Actors, 'EntityRef')
EntityRef.set('entityRef', 'npc_vehicle')

Maneuver = ET.SubElement(ManeuverGroup, 'Maneuver')
Maneuver.set('name', '%s_Maneuver' % saveAs)

# Save the above xml elements temporarily
b_xml = ET.tostring(OpenSCENARIO)
with open("%s.xosc" % saveAs, 'wb') as f:
    f.write(b_xml)

# Generate route event
# Route_Event = ET.SubElement(Maneuver, 'Event')
# Route_Event.set('name', 'RouteFollowing')
# Route_Event.set('priority', 'parallel')
# Route_Event.set('maximumExecutionCount', '1')
#
# Route_Action = ET.SubElement(Route_Event, 'Action')
# Route_Action.set('name', 'RouteFollowing')
#
# Route_PrivateAction = ET.SubElement(Route_Action, 'PrivateAction')
#
# RoutingAction = ET.SubElement(Route_PrivateAction, 'RoutingAction')
#
# AssignRouteAction = ET.SubElement(RoutingAction, 'AssignRouteAction')
#
# Route = ET.SubElement(AssignRouteAction, 'Route')
# Route.set('name', 'CustomRoute')
# Route.set('closed', 'false')
#
# # Route_ParameterDeclaration = ET.SubElement(Route,'ParameterDeclarations')
#
# Waypoint = ET.SubElement(Route, 'Waypoint')
# Waypoint.set('routeStrategy', 'shortest')
#
# Route_Position = ET.SubElement(Waypoint, 'Position')
#
# Route_LanePosition = ET.SubElement(Route_Position, 'LanePosition')
# Route_LanePosition.set('roadId', '0')
# Route_LanePosition.set('laneId', '-1')
# Route_LanePosition.set('s', '10')
# Route_LanePosition.set('offset', '0')
#
# Waypoint2 = ET.SubElement(Route, 'Waypoint')
# Waypoint2.set('routeStrategy', 'shortest')
#
# Route_Position2 = ET.SubElement(Waypoint2, 'Position')
#
# Route_LanePosition2 = ET.SubElement(Route_Position2, 'LanePosition')
# Route_LanePosition2.set('roadId', '0')
# Route_LanePosition2.set('laneId', '-1')
# Route_LanePosition2.set('s', '20')
# Route_LanePosition2.set('offset', '0')
#
# Waypoint3 = ET.SubElement(Route, 'Waypoint')
# Waypoint3.set('routeStrategy', 'shortest')
#
# Route_Position3 = ET.SubElement(Waypoint3, 'Position')
#
# Route_LanePosition3 = ET.SubElement(Route_Position3, 'LanePosition')
# Route_LanePosition3.set('roadId', '0')
# Route_LanePosition3.set('laneId', '-1')
# Route_LanePosition3.set('s', '30')
# Route_LanePosition3.set('offset', '0')
#
# Route_StartTrigger = ET.SubElement(Route_Event, 'StartTrigger')
#
# Route_ConditionGroup = ET.SubElement(Route_StartTrigger, 'ConditionGroup')
#
# Route_Condition = ET.SubElement(Route_ConditionGroup, 'Condition')
# Route_Condition.set('name', 'RouteCondition')
# Route_Condition.set('delay', '0')
# Route_Condition.set('conditionEdge', 'none')
#
# Route_ByValueCondition = ET.SubElement(Route_Condition, 'ByValueCondition')
#
# Route_SimulationTimeCondition = ET.SubElement(Route_ByValueCondition, 'SimulationTimeCondition')
# Route_SimulationTimeCondition.set('value', '0')
# Route_SimulationTimeCondition.set('rule', 'greaterThan')

# Generate longitudinal speed events based on provided .csv file
for row in tqdm(range(len(csvfile)-1)):
# for row in tqdm(range(30)): # for debug only
    Event = ET.SubElement(Maneuver, 'Event')
    Event.set('name', 'Event_%s' % row)
    Event.set('priority', 'overwrite')
    Event.set('maximumExecutionCount', '1')

    Action = ET.SubElement(Event, 'Action')
    Action.set('name', 'Action_%s' % row)

    PrivateAction = ET.SubElement(Action, 'PrivateAction')

    LongitudinalAction = ET.SubElement(PrivateAction, 'LongitudinalAction')

    SpeedAction = ET.SubElement(LongitudinalAction, 'SpeedAction')

    SpeedActionDynamics = ET.SubElement(SpeedAction, 'SpeedActionDynamics')
    SpeedActionDynamics.set('dynamicsShape', 'linear')
    SpeedActionDynamics.set('value', '1')
    SpeedActionDynamics.set('dynamicsDimension', 'time')
    # SpeedActionDynamics.set('value', '%s' % csvfile.loc[row].at['Acceleration'])
    # SpeedActionDynamics.set('dynamicsDimension', 'rate')

    SpeedActionTarget = ET.SubElement(SpeedAction,'SpeedActionTarget')

    AbsoluteTargetSpeed = ET.SubElement(SpeedActionTarget, 'AbsoluteTargetSpeed')
    AbsoluteTargetSpeed.set('value', '%s' % csvfile.loc[row+1].at['Speed'])

    StartTrigger = ET.SubElement(Event, 'StartTrigger')

    ConditionGroup = ET.SubElement(StartTrigger, 'ConditionGroup')

    Condition = ET.SubElement(ConditionGroup, 'Condition')
    Condition.set('name', 'Condition_%s' % row)
    Condition.set('delay', '0')
    Condition.set('conditionEdge', 'none')

    ByValueCondition = ET.SubElement(Condition, 'ByValueCondition')

    SimulationTimeCondition = ET.SubElement(ByValueCondition, 'SimulationTimeCondition')
    SimulationTimeCondition.set('value', '%s' % row)
    SimulationTimeCondition.set('rule', 'greaterThan')

    # Save XML elements generated every loop
    b_xml_2 = ET.tostring(OpenSCENARIO)
    with open("%s.xosc" % saveAs, 'wb') as f:
        f.write(b_xml_2)


Act_StartTrigger = ET.SubElement(Act, 'StartTrigger')

Start_ConditionGroup = ET.SubElement(Act_StartTrigger, 'ConditionGroup')

Start_Condition = ET.SubElement(Start_ConditionGroup, 'Condition')
Start_Condition.set('name', 'Act_Condition')
Start_Condition.set('delay', '0')
Start_Condition.set('conditionEdge', 'none')

Start_ByValueCondition = ET.SubElement(Start_Condition, 'ByValueCondition')

Start_SimulationTimeCondition = ET.SubElement(Start_ByValueCondition, 'SimulationTimeCondition')
Start_SimulationTimeCondition.set('value', '0')
Start_SimulationTimeCondition.set('rule', 'greaterThan')

Storyboard_StopTrigger = ET.SubElement(Storyboard, 'StopTrigger')

Stop_ConditionGroup = ET.SubElement(Storyboard_StopTrigger, 'ConditionGroup')

Stop_Condition = ET.SubElement(Stop_ConditionGroup, 'Condition')
Stop_Condition.set('name', 'Stop_Condition')
Stop_Condition.set('delay', '0')
Stop_Condition.set('conditionEdge', 'none')

Stop_ByValueCondition = ET.SubElement(Stop_Condition, 'ByValueCondition')

Stop_StoryboardElementStateCondition = ET.SubElement(Stop_ByValueCondition, 'StoryboardElementStateCondition')
Stop_StoryboardElementStateCondition.set('storyboardElementType', 'event')
Stop_StoryboardElementStateCondition.set('storyboardElementRef', 'Event_%s' % (len(csvfile)-2))
# Stop_StoryboardElementStateCondition.set('storyboardElementRef', 'Event_%s' % 29) # for debug only
Stop_StoryboardElementStateCondition.set('state', 'completeState')

# Save final XML elements
b_xml_3 = ET.tostring(OpenSCENARIO)
with open("%s.xosc" % saveAs, 'wb') as f:
    f.write(b_xml_3)

print("Finished creating %s.xosc." % saveAs)
