using System;
using System.Collections.Generic;
using Thorlabs.MotionControl.XA;
using Thorlabs.MotionControl.XA.Products;

namespace DotNet_Windows_DLL_Examples
{
    class Program
    {
        private static string _deviceId = "28251608";

        static void Main(string[] args)
        {
            //UseSimulatedDeviceExample();

            SystemManager systemManager = SystemManager.Create();
            systemManager.Startup();

            systemManager.AddUserMessageToLog("Ready (C# Examples).");

            Thorlabs.MotionControl.XA.IDevice device = null;

            //OpenOptionsExample(systemManager);

            //GetApiVersionExample(systemManager);

            GetDeviceListExample(systemManager);

            if (systemManager.TryOpenDevice(_deviceId, "", OperatingModes.Default,out device))
            {
                var exampleCode = new ExamplesUsingInterfaces();

                exampleCode.GetLimitSwitchParams(device);

                exampleCode.SubscribeToNotificationRaised(device);

                exampleCode.ChangeAnalogMonitorConfigurationParams(device);
                exampleCode.ChangeAuxIoConfigurationParams(device);
                exampleCode.ChangeBowIndex(device);
                exampleCode.ChangeConnectedProductByName(device);
                exampleCode.ChangeConnectedProductInfo(device);
                exampleCode.ChangeCurrentLoopParams(device);
                exampleCode.ChangeDcPidParams(device);
                exampleCode.ChangeDigitalOutputStates(device);
                exampleCode.ChangeEnableState(device);
                exampleCode.ChangeGeneralMoveParams(device);
                exampleCode.ChangeHomeParams(device);
                exampleCode.ChangeIoConfigurationParams(device);
                exampleCode.ChangeIoPositionTriggerEnableState(device);
                exampleCode.ChangeIoTriggerParams(device);
                exampleCode.ChangeJogParams(device);
                exampleCode.ChangeJoystickParams(device);
                exampleCode.ChangeKcubeIoTriggerParams(device);
                exampleCode.ChangeKcubeMmiParams(device);
                exampleCode.ChangeKcubePositionTriggerParams(device);
                exampleCode.ChangeLcdDisplayParams(device);
                exampleCode.ChangeLcdMoveParams(device);
                exampleCode.ChangeLimitSwitchParams(device);
                exampleCode.ChangeMaxOutputVoltageParams(device);
                exampleCode.ChangeMotorOutputParams(device);
                exampleCode.ChangeMoveAbsoluteParams(device);
                exampleCode.ChangeMoveRelativeParams(device);
                exampleCode.ChangeOutputVoltage(device);
                exampleCode.ChangeOutputVoltageControlSourceParams(device);
                exampleCode.ChangePiezoPositionLoopParams(device);
                exampleCode.ChangePosition(device);
                exampleCode.ChangePositionControlMode(device);
                exampleCode.ChangePositionLoopParams(device);
                exampleCode.ChangeProfileModeParams(device);
                exampleCode.ChangeSlewRateParams(device);
                exampleCode.ChangeStageAxisParams(device);
                exampleCode.ChangeTrackSettleParams(device);
                exampleCode.ChangeVelocityParams(device);

                exampleCode.GetDigitalInputStates(device);
                exampleCode.GetFirmwareVersionInfo(device);
                exampleCode.GetHardwareInfo(device);
                exampleCode.GetLimitSwitchParams(device);
                exampleCode.GetIoConfigurationNumberOfPortsSupported(device);
                exampleCode.GetMaxTravel(device);
                exampleCode.GetOutputWaveformParams(device);
                exampleCode.GetPiezoStatus(device);
                exampleCode.GetPiezoInertialMotorStatus(device);
                exampleCode.GetPositionCounter(device);
                exampleCode.GetRackBayOccupiedState(device);
                exampleCode.GetAllStatus(device);
                exampleCode.GetStatus(device);
                exampleCode.GetUniversalStatus(device);
                exampleCode.GetUniversalStatusBits(device);

                exampleCode.SetEndOfMoveMessagesMode(device);
                exampleCode.SetPositionCounter(device);
                exampleCode.SetStatusMode(device);
                exampleCode.SetZero(device);

                exampleCode.Device(device);
                exampleCode.Disconnect(device);
                exampleCode.Home(device);
                exampleCode.Identify(device);
                exampleCode.LoadParams(device);
                exampleCode.MoveAbsolute(device);
                exampleCode.MoveContinuous(device);
                exampleCode.MoveJog(device);
                exampleCode.MoveRelative(device);
                exampleCode.OutputWaveform(device);
                exampleCode.PersistParams(device);
                exampleCode.PiezoInertialMotorPulseParaAcquire(device);
                exampleCode.RackIdentify(device);
                exampleCode.RestoreFactoryDefaults(device);
                exampleCode.Stop(device);
                exampleCode.UnitConverter(device);

                exampleCode.GetSubchannel(device);

                exampleCode.WritePackets(device);
                exampleCode.SubscribeToPacketReceived(device);
                exampleCode.SubscribeToNotificationRaised(device);

                device.Close();
            }

            systemManager.Shutdown();
        }

        private static void GetApiVersionExample(SystemManager systemManager)
        {
            ApiVersion apiversion = systemManager.GetApiVersion();
            // Version information for the .NET API has been copied to the apiVersion structure
        }

        private static void GetDeviceListExample(SystemManager systemManager)
        {
            IList<DeviceInfo> deviceList = systemManager.GetDeviceList();
            // We can enumerate over the returned list to determine what devices are connected
        }

        private static void OpenOptionsExample(SystemManager systemManager)
        {
            // The different methods available for opening a device.

            // 1. Use the non-generic method, open the device as generalized type IDevice. If the device is unavailable XADeviceNotFoundException will be thrown
            try
            {
                IDevice device = systemManager.OpenDevice(_deviceId, "", OperatingModes.Default);
                //

            }
            catch (XADeviceNotFoundException)
            {
                // The device is unavailable
            }

            // 2. Use the generic method, open the device as a specialized type (Kdc). If the device is unavailable XADeviceNotFoundException will be thrown
            try
            {
                Kdc101 device = systemManager.OpenDevice<Kdc101>(_deviceId, "", OperatingModes.Default);
                //

            }
            catch (XADeviceNotFoundException)
            {
                // The device is unavailable
            }

            // 3. 'Try' non-generic method, open the device as generalized type IDevice.
            // If the device is unavailable XADeviceNotFoundException will be suppressed and false returned by the method
            {
                IDevice device;
                if (systemManager.TryOpenDevice(_deviceId, "", OperatingModes.Default, out device))
                {
                    //
                }
                else
                {
                    //device is unavailable
                }
            }

            // 4. Use the generic method, open the device as a specialized type (Kdc).
            // If the device is unavailable XADeviceNotFoundException will be suppressed and false returned by the method
            {
                Kdc101 device;
                if (systemManager.TryOpenDevice<Kdc101>(_deviceId, "", OperatingModes.Default, out device))
                {
                    //
                }
                else
                {
                    //device is unavailable
                }
            }

        }

        private static void UseSimulatedDeviceExample()
        {
            SystemManager systemManager = SystemManager.Create();
            systemManager.Startup();

            //string kdc101SimulationDescription = 
            //@"{
            //    ""PartNumber"": ""KDC101"",
            //    ""SerialNumber"" : ""27001234"",
            //    ""ActuatorType"" : ""MTS25-Z8""
            //})";

            string bbd303SimulationDescription =
                @"{
                    ""PartNumber"": ""BBD303"",
                    ""SerialNumber"": ""103003334"",
                    ""Channels"": 
                    [
                        {
                            ""BayNumber"": ""1"",    
                            ""SerialNumber"": ""104003335"",    
                            ""ActuatorType"": ""DDS600""    
                        },
                        {
                            ""BayNumber"": ""2"",    
                            ""SerialNumber"": ""104003336"",    
                            ""ActuatorType"": ""DDS300""
                        },
                        {
                            ""BayNumber"": ""3"",    
                            ""SerialNumber"": ""104003337"",    
                            ""ActuatorType"": ""DDS600""
                        }					
                    ]
                }";

            systemManager.CreateSimulation(bbd303SimulationDescription);

            Thorlabs.MotionControl.XA.Products.Bbd30xLogicalChannel simulatedBbd30xChannel = null;

            //Open channel 1 of the simulated device
            if (systemManager.TryOpenDevice("104003335", "", OperatingModes.Default, out simulatedBbd30xChannel))
            {
                //All features of the real device can now be called on the simulation
                var hardwareInfo = simulatedBbd30xChannel.GetHardwareInfo(Thorlabs.MotionControl.XA.Timeout.Zero);
            }

            systemManager.RemoveSimulation(bbd303SimulationDescription);

            systemManager.Shutdown();

        }

    }
}
