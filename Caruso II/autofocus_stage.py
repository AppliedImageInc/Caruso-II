import platform
import thorlabs_xa
import clr

from thorlabs_xa.products.kdc101 import Kdc101, TLMC_EndOfMoveMessagesMode
from thorlabs_xa.shared.diagnostics_helper import DiagnosticsHelper
from thorlabs_xa.shared.system_manager import SystemManager
from thorlabs_xa.shared.enums import TLMC_DigitalOutput, TLMC_EnableState, TLMC_HardLimitOperatingMode, TLMC_HomeDirection, TLMC_HomeLimitSwitch, TLMC_JogMode, TLMC_JogStopMode, TLMC_MoveMode, TLMC_OperatingMode, TLMC_SoftLimitOperatingMode, TLMC_Wait
from thorlabs_xa.shared.params import TLMC_DcPidParams, TLMC_DeviceInfo, TLMC_GeneralMoveParams, TLMC_HomeParams, TLMC_JogParams, TLMC_LimitSwitchParams, TLMC_MoveAbsoluteParams, TLMC_MoveRelativeParams, TLMC_LcdMoveParams, TLMC_VelocityParams
from thorlabs_xa.shared.xa_error_factory import XADeviceException

KDC101_PART_NUMBER = "KDC101"
KDC101_SERIAL_NUMBER = "27272894"
# no idea what these numbers mean, but this seems to be the scale between values in mm here and values in mm that show up in the XA gui
D_SCALE = 34555
V_SCALE = 766618
A_SCALE = 264
SIMULATION_CONFIG_STRING = { "PartNumber" : KDC101_PART_NUMBER, "SerialNumber" : KDC101_SERIAL_NUMBER, "ActuatorType" : "Z906" }
DEFAULT_TIMEOUT = 5000 # ms

global device
device: Kdc101 | None = None

# if a controller is not found, make a simulation
def create_simulation(system_manager: SystemManager) -> TLMC_DeviceInfo:

    system_manager.create_simulation(SIMULATION_CONFIG_STRING)

    device_info = TLMC_DeviceInfo()

    device_info.device_type_description = SIMULATION_CONFIG_STRING["PartNumber"]
    device_info.device = SIMULATION_CONFIG_STRING["SerialNumber"]
    device_info.transport = ""

    return device_info

# show the parameters we set in the console window 
def display_params(params_set, params_returned, name):
    params_string = DiagnosticsHelper.object_as_string(params_set)
    params_returned_string = DiagnosticsHelper.object_as_string(params_returned)

    DiagnosticsHelper.console(f"Sent: {params_string}")
    DiagnosticsHelper.console(f"Received: {params_returned_string}")

    if params_string == params_returned_string:
        DiagnosticsHelper.console_green(name + " Params round trip test passed.")
    else:
        DiagnosticsHelper.console_error(name + " Params round trip test failed.")

# move the stage a specified amount
def move(distance):
    ##### trying to move omg #####
    position_counter_before_move = device.get_position_counter(DEFAULT_TIMEOUT)
    DiagnosticsHelper.console("about to move")
    # move_fr_params = TLMC_EndOfMoveMessagesMode()
    # move_fr_params.set_end_of_move_messages_mode = TLMC_EndOfMoveMessagesMode.TLMC_EndOfMoveMessagesMode_Enabled
    device.set_end_of_move_messages_mode(TLMC_EndOfMoveMessagesMode.TLMC_EndOfMoveMessagesMode_Enabled)
    # device.move(TLMC_MoveMode.TLMC_MoveMode_AbsoluteToProgrammedPosition, 1, DEFAULT_TIMEOUT)
    device.move(TLMC_MoveMode.TLMC_MoveMode_Relative, int(distance * D_SCALE), DEFAULT_TIMEOUT)

    position_counter_expected = position_counter_before_move + distance * D_SCALE
    position_counter_after_move = device.get_position_counter(DEFAULT_TIMEOUT)
    # DiagnosticsHelper.console_green("Position Counter before move: " + str(position_counter_before_move))
    DiagnosticsHelper.console_green("Position Counter expected: " + str(position_counter_expected))
    DiagnosticsHelper.console_green("Position Counter after move: " + str(position_counter_after_move))
    
    """
    if position_counter_expected == position_counter_after_move:
        DiagnosticsHelper.console_green("Position Counter round trip test passed.")
        device.set_position_counter(int(position_counter_expected))
    else:
        DiagnosticsHelper.console_error("Position Counter round trip test failed.")
        """


def main() -> None:
    global device
    system_manager = SystemManager.instance()

    if platform.system() == "Linux":
        # If using Linux, we are required to state the port explicitly. Replace if you require an alternative port.
        system_manager.startup("deviceDiscovery.connections=/dev/ttyUSB0")
    else:
        system_manager.startup()

    devices = system_manager.get_device_list()
    device_info: TLMC_DeviceInfo | None = None

    # if a controller is not found, make a simulation
    if not devices:
        print("No devices found, check that your device is powered and is visible to your system. Continuing with simulation!")
        device_info = create_simulation(system_manager)
    else:
        print("Devices found:")
        for listed_device_info in devices:
            print (f"{listed_device_info.device_type_description}:{listed_device_info.device} found at {listed_device_info.transport} ({listed_device_info.part_number})")

            if listed_device_info.part_number == KDC101_PART_NUMBER:
                device_info = listed_device_info

        if not device_info:
            print("No KDC101 devices found, check that your device is powered and is visible to your system. Continuing with simulation!")
            device_info = create_simulation(system_manager)

    try:
        # Create device object and enable device.
        device = system_manager.open_device_as(device_info.device, device_info.transport, TLMC_OperatingMode.TLMC_OperatingMode_Default, Kdc101)

        DiagnosticsHelper.console("Enabling KDC101...")
        device.set_enable_state(TLMC_EnableState.TLMC_Enabled)

        enable_state = device.get_enable_state(DEFAULT_TIMEOUT)

        if enable_state == TLMC_EnableState.TLMC_Enabled:
            DiagnosticsHelper.console_green("KDC101 enabled.")
        else:
            DiagnosticsHelper.console_error("KDC101 not enabled as expected.")
            return

        DiagnosticsHelper.console(f"Device part number is {device.get_hardware_info(TLMC_Wait.TLMC_InfiniteWait).part_number}")

        ##### start setting parameters, found under settings in the xa gui #####
        ##### Control Loops tab #####
        # PID, under the Control Loops tab in the GUI
        DiagnosticsHelper.console("Testing round trip of DC PID Params...")
        dc_pid_params = TLMC_DcPidParams()
        dc_pid_params.proportional = 435
        dc_pid_params.integral = 195
        dc_pid_params.derivative = 993
        dc_pid_params.integral_limit = 195
        dc_pid_params.filter_control = 0b00001111 # not sure what this is
        
        device.set_dc_pid_params(dc_pid_params)
        dc_pid_params_returned = device.get_dc_pid_params(DEFAULT_TIMEOUT)
        display_params(dc_pid_params, dc_pid_params_returned, "DC PID")
     
        ##### Move Tab #####
        # general move params seems to just be backlash distance under the move tab
        DiagnosticsHelper.console("Testing round trip of general move params...")
        general_move_params = TLMC_GeneralMoveParams()
        general_move_params.backlash_distance = int(0.3 * D_SCALE)

        device.set_general_move_params(general_move_params)
        general_move_params_returned = device.get_general_move_params(DEFAULT_TIMEOUT)
        display_params(general_move_params, general_move_params_returned, "general move")

        # preset absolute position
        DiagnosticsHelper.console("Testing round trip of move absolute params...")

        move_absolute_params = TLMC_MoveAbsoluteParams()
        move_absolute_params.absolute_position = 1 * D_SCALE

        device.set_move_absolute_params(move_absolute_params)
        move_absolute_params_returned = device.get_move_absolute_params(DEFAULT_TIMEOUT)
        display_params(move_absolute_params, move_absolute_params_returned, "move absolute")

        # preset relative distance
        DiagnosticsHelper.console("Testing round trip of move relative params...")

        move_relative_params = TLMC_MoveRelativeParams()
        move_relative_params.relative_distance = 2 * D_SCALE

        device.set_move_relative_params(move_relative_params)
        move_relative_params_returned = device.get_move_relative_params(DEFAULT_TIMEOUT)
        display_params(move_relative_params, move_relative_params_returned, "move relative")

        # min/max velocity and acceleration
        DiagnosticsHelper.console_green("Testing round trip of Velocity/Acceleration Params...")
        vel_params = TLMC_VelocityParams()
        vel_params.min_velocity = 0 * V_SCALE 
        vel_params.acceleration = int(1 * A_SCALE) # defaul is 1.5
        vel_params.max_velocity = int(1 * V_SCALE) # the default is 2.8, but the Z motors have a max recommended speed of 2.3
        
        device.set_velocity_params(vel_params)
        vel_params_returned = device.get_velocity_params(DEFAULT_TIMEOUT)
        display_params(vel_params, vel_params_returned, "velocity and acceleration")

        ##### Home tab #####
        DiagnosticsHelper.console("Testing round trip of home params...")
        home_params = TLMC_HomeParams()
        home_params.direction = TLMC_HomeDirection.TLMC_HomeDirection_Reverse
        home_params.limit_switch = TLMC_HomeLimitSwitch.TLMC_HomeLimitSwitch_Reverse
        home_params.offset_distance = int(0.3 * D_SCALE)
        home_params.velocity = 1 * V_SCALE

        device.set_home_params(home_params)
        home_params_returned = device.get_home_params(DEFAULT_TIMEOUT)
        display_params(home_params, home_params_returned, "home")

        ##### Jog tab #####
        DiagnosticsHelper.console("Testing round trip of jog params...")
        jog_params = TLMC_JogParams()
        jog_params.mode = TLMC_JogMode.TLMC_JogMode_SingleStep
        jog_params.step_size = int(0.1 * D_SCALE)
        jog_params.min_velocity = 0 * V_SCALE
        jog_params.acceleration = 2 * A_SCALE
        jog_params.max_velocity = 2 * V_SCALE
        jog_params.stop_mode = TLMC_JogStopMode.TLMC_JogStopMode_Profiled

        device.set_jog_params(jog_params)
        jog_params_returned = device.get_jog_params(DEFAULT_TIMEOUT)
        display_params(jog_params, jog_params_returned, "jog")

        ##### I/O tabs #####  # stuff missing from here
        DiagnosticsHelper.console("Testing round trip of digital output states...")
        # digital_params = TLMC_DigitalOutput()
        digital_output_1 = TLMC_DigitalOutput.TLMC_DigitalOutput_1
        digital_output_2 = TLMC_DigitalOutput.TLMC_DigitalOutput_2

        device.set_digital_output_states(digital_output_1)
        digital_params_returned = device.get_digital_output_states(DEFAULT_TIMEOUT)
        display_params(digital_output_1, digital_params_returned, "digital")

        ##### Joystick tab #####

        ##### Display tab #####

        ##### Trigger tab #####

        ##### Limits tab #####
        DiagnosticsHelper.console("Testing round trip of limit switch params...")
        limit_switch_params = TLMC_LimitSwitchParams()
        limit_switch_params.clockwise_limit_mode = TLMC_HardLimitOperatingMode.TLMC_HardLimitOperatingMode_SwitchContactMakes
        limit_switch_params.counterclockwise_limit_mode = TLMC_HardLimitOperatingMode.TLMC_HardLimitOperatingMode_SwitchContactMakes
        limit_switch_params.clockwise_soft_limit = int(-31073.450 * D_SCALE) # when i changed these to something that looked more reasonable (-1 for the reverse limit and 6 for the forward limit), the soft limit  
        limit_switch_params.counterclockwise_soft_limit = int(31073.450 * D_SCALE) # indicators in the gui were j always on? so i don't think these numbers mean what i think they mean
        limit_switch_params.soft_limit_operating_mode = TLMC_SoftLimitOperatingMode.TLMC_SoftLimitOperatingMode_Ignored # seems odd to j ignore it but ok

        device.set_limit_switch_params(limit_switch_params)
        limit_switch_params_returned = device.get_limit_switch_params(DEFAULT_TIMEOUT)
        display_params(limit_switch_params, limit_switch_params_returned, "limit switch")

        ##### universal status #####
        DiagnosticsHelper.console("Getting universal status...")
        universal_status = device.get_universal_status(DEFAULT_TIMEOUT)

        DiagnosticsHelper.console(DiagnosticsHelper.object_as_string(universal_status))

        DiagnosticsHelper.console("Getting universal status bits...")
        universal_status_bits = device.get_universal_status_bits(DEFAULT_TIMEOUT)

        DiagnosticsHelper.console(DiagnosticsHelper.object_as_string(universal_status_bits))
    
    except XADeviceException as e:
        print("Encountered error, code: ", e.error_code)

    # shutdown
    """
    finally:
        if device is not None:
            DiagnosticsHelper.console("Shutting down KDC101...")
            device.disconnect()
            device.close()

        DiagnosticsHelper.console("Shutting down system...")
        system_manager.shutdown()

    DiagnosticsHelper.console("Completed.")"""

# main()