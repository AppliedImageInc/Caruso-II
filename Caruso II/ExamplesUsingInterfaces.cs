using System;
using System.Collections.Generic;
using Thorlabs.MotionControl.XA;
using Thorlabs.MotionControl.XA.DeviceFeatures;
using Thorlabs.MotionControl.XA.DC;

namespace DotNet_Windows_DLL_Examples
{
    /// <summary>
    /// These methods can be employed with any device, each feature interface implementation is checked before being called
    /// </summary>
    public class ExamplesUsingInterfaces
    {
        private TimeSpan _defaultTimeout = TimeSpan.FromSeconds(2);

        public void ChangeAnalogMonitorConfigurationParams(IDevice device)
        {
            var iAnalogMonitorConfigurationParams = device as IAnalogMonitorConfigurationParams;
            if (iAnalogMonitorConfigurationParams != null)
            {
                AnalogMonitorConfigurationParams parameters = iAnalogMonitorConfigurationParams.GetAnalogMonitorConfigurationParams(AnalogMonitorNumber.Monitor1, _defaultTimeout);
                // The Auxiliary I/O configuration parameters have been read from the controller
                parameters.MotorChannel = AnalogMonitorMotorChannel.Channel1;
                parameters.Offset = 0;
                parameters.SystemVariable = AnalogMonitorSystemVariable.PositionError;
                parameters.Scale = 10000;

                iAnalogMonitorConfigurationParams.SetAnalogMonitorConfigurationParams(AnalogMonitorNumber.Monitor1,parameters);
                // The new Auxiliary I/O configuration parameters have been sent to the controller
            }
        }

        public void ChangeAuxIoConfigurationParams(IDevice device)
        {
            var iAuxIoConfigurationParams = device as IAuxIoConfigurationParams;
            if (iAuxIoConfigurationParams != null)
            {
                AuxIoPortMode portMode = iAuxIoConfigurationParams.GetAuxIoPortMode(AuxIoPortNumber.Port1, _defaultTimeout);
                Int32 softwareStates = iAuxIoConfigurationParams.GetAuxIoSoftwareStates(_defaultTimeout);
                // The Auxiliary I/O configuration parameters have been read from the controller

                iAuxIoConfigurationParams.SetAuxIoPortMode(AuxIoPortNumber.Port1, AuxIoPortMode.SoftwareControlled);
                iAuxIoConfigurationParams.SetAuxIoSoftwareStates(0x0003);
                // The new Auxiliary I/O configuration parameters have been sent to the controller
            }
        }

        public void ChangeBowIndex(IDevice device)
        {
            var iBowIndex = device as IBowIndex;
            if (iBowIndex != null)
            {
                BowIndex bowIndex = iBowIndex.GetBowIndex(_defaultTimeout);

                iBowIndex.SetBowIndex(BowIndex.SCurve1, _defaultTimeout);
                // The new bow index has been sent to the controller
            }

        }

        internal void ChangeConnectedProductInfo(IDevice device)
        {
            var iConnectedProduct = device as IConnectedProduct;
            if (iConnectedProduct != null)
            {
                ConnectedProductInfo productInfo = iConnectedProduct.GetConnectedProductInfo();

                productInfo.DistanceScaleFactor = 19197;
                productInfo.VelocityScaleFactor = 429417;
                productInfo.AccelerationScaleFactor = 147;
                productInfo.AxisType = ConnectedProductAxis.Single;
                productInfo.MaxAcceleration = 2;
                productInfo.MaxPosition = 3;
                productInfo.MaxVelocity = 2;
                productInfo.MinPosition = 0.5;
                productInfo.MovementType = ConnectedProductMovement.Linear;
                productInfo.ProductName = "My Linear Actuator";
                productInfo.UnitType = Unit.Millimetres;

                iConnectedProduct.SetConnectedProductInfo(productInfo);
                // The new connected product information has been sent to the controller
            }
        }


        internal void ChangeConnectedProductByName(IDevice device)
        {
            var iConnectedProduct = device as IConnectedProduct;
            if (iConnectedProduct != null)
            {
                IList<string> supportedProducts = iConnectedProduct.GetSupportedConnectedProducts();
                // The 'supportedProducts' collection now contains the supported product names 

                iConnectedProduct.SetConnectedProduct("PRM1Z8");
                //The connected product has been set using the values for the PRM1Z8 product
            }
        }


        public void ChangeCurrentLoopParams(IDevice device)
        {
            var iCurrentLoopParams = device as ICurrentLoopParams;
            if (iCurrentLoopParams != null)
            {
                CurrentLoopParams parameters = iCurrentLoopParams.GetCurrentLoopParams(CurrentLoopScenario.Normal, _defaultTimeout);

                parameters.FeedForward = 500;
                parameters.Integral = 80;
                parameters.IntegralDeadBand = 0;
                parameters.IntegralLimit = 32767;
                parameters.Phase = CurrentLoopPhase.PhaseAB;
                parameters.Proportional = 20;

                iCurrentLoopParams.SetCurrentLoopParams(CurrentLoopScenario.Normal, parameters);
                // The new current loop parameters have been sent to the controller
            }
        }

        public void ChangeDcPidParams(IDevice device)
        {
            var iDcPidParams = device as IDcPidParams;
            if (iDcPidParams != null)
            {
                DcPidParams parameters = iDcPidParams.GetDcPidParams(_defaultTimeout);

                parameters.Derivative = 2720;
                parameters.FilterControl = DcPidUpdateFilters.All;
                parameters.Integral = 150;
                parameters.IntegralLimit = 50;
                parameters.Proportional = 850;

                iDcPidParams.SetDcPidParams(parameters);
                // The new DC PID parameters have been sent to the controller
            }
        }

        public void ChangeDigitalOutputStates(IDevice device)
        {
            var iDigitalOutputStates = device as IDigitalOutputStates;
            if (iDigitalOutputStates != null)
            {
                DigitalOutputStates digitalOutputStates = iDigitalOutputStates.GetDigitalOutputStates(_defaultTimeout);

                digitalOutputStates = DigitalOutputStates.OutputNoneSet;

                iDigitalOutputStates.SetDigitalOutputStates(digitalOutputStates);
                // The new digital output states have been sent to the controller
            }
        }

        public void ChangeEnableState(IDevice device)
        {
            var iEnableState = device as IEnableState;
            if (iEnableState != null)
            {
                EnableState enableState = iEnableState.GetEnableState(_defaultTimeout);
                // The enable state has been read from the controller

                iEnableState.SetEnableState(EnableState.Enabled, _defaultTimeout);
                // The controller enable state is 'enabled'
            }
        }

        public void ChangeEncodercounter(IDevice device)
        {
            var iEncoderCounter = device as IEncoderCounter;
            if (iEncoderCounter != null)
            {
                Int32 encoderCounter = iEncoderCounter.GetEncoderCounter(_defaultTimeout);
                // The encoder counter has been read from the controller

                encoderCounter = 2000;

                iEncoderCounter.SetEncoderCounter(encoderCounter);
                // The new encoder counter value has been sent to the controller
            }
        }

        public void ChangeGeneralMoveParams(IDevice device)
        {
            var iGeneralMoveParams = device as IGeneralMoveParams;
            if (iGeneralMoveParams != null)
            {
                GeneralMoveParams parameters = iGeneralMoveParams.GetGeneralMoveParams(_defaultTimeout);

                parameters.BacklashDistance = 1920;

                iGeneralMoveParams.SetGeneralMoveParams(parameters);
                // The new general move parameters have been sent to the controller
            }
        }

        public void ChangeHomeParams(IDevice device)
        {
            var iHomeParams = device as IHomeParams;
            if (iHomeParams != null)
            {
                HomeParams parameters = iHomeParams.GetHomeParams(_defaultTimeout);

                parameters.Direction = HomeDirection.Reverse;
                parameters.LimitSwitch = HomeLimitSwitches.Reverse;
                parameters.OffsetDistance = 7678;
                parameters.Velocity = 428997;

                iHomeParams.SetHomeParams(parameters);
                // The new homing parameters have been sent to the controller
            }
        }

        public void ChangeIoConfigurationParams(IDevice device)
        {
            var iIoConfigurationParams = device as IIoConfigurationParams;
            if (iIoConfigurationParams != null)
            {
                IoConfigurationParams parameters = iIoConfigurationParams.GetIoConfigurationParams(IoPortNumber.Port1, _defaultTimeout);

                parameters.PortMode = IoPortMode.DigitalOutput;
                parameters.PortSource = IoPortSource.Channel1;


                iIoConfigurationParams.SetIoConfigurationParams(IoPortNumber.Port1, parameters);
                // The new I/O configuration parameters have been sent to the controller
            }
        }


        public void ChangeIoPositionTriggerEnableState(IDevice device)
        {
            var iPositionTriggerEnableState = device as IIoPositionTriggerEnableState;
            if (iPositionTriggerEnableState != null)
            {
                IoPositionTriggerEnableState enableState = iPositionTriggerEnableState.GetIoPositionTriggerEnableState(_defaultTimeout);
                // The enable state has been read from the controller

                iPositionTriggerEnableState.SetIoPositionTriggerEnableState(IoPositionTriggerEnableState.TriggerArmed, _defaultTimeout);
                // The controller enable state is 'armed'
            }
        }

        public void ChangeIoTriggerParams(IDevice device)
        {
            var iIoTriggerParams = device as IIoTriggerParams;
            if (iIoTriggerParams != null)
            {
                IoTriggerParams parameters = iIoTriggerParams.GetIoTriggerParams(_defaultTimeout);
                parameters.ForwardInterval = 0;
                parameters.ForwardNumberOfPulses = 0;
                parameters.ForwardStartPosition = 0;
                parameters.NumberOfCycles = 0;
                parameters.PulseWidth = 0;
                parameters.ReverseInterval = 0;
                parameters.ReverseNumberOfPulses = 0;
                parameters.ReverseStartPosition = 0;
                parameters.TriggerInMode = IoTriggerInMode.TriggersAbsoluteMove;
                parameters.TriggerInPolarity = IoTriggerPolarity.ActiveIsLogicHigh;
                parameters.TriggerOutMode = IoTriggerOutMode.ActiveDuringMotion;
                parameters.TriggerOutPolarity = IoTriggerPolarity.ActiveIsLogicHigh;
                parameters.TriggerInSource = IoTriggerInSource.Io1;

                iIoTriggerParams.SetIoTriggerParams(parameters);
                // The new Io trigger parameters have been sent to the controller
            }
        }

        public void ChangeJogParams(IDevice device)
        {
            var iJogParams = device as Thorlabs.MotionControl.XA.DeviceFeatures.IJogParams;
            if (iJogParams != null)
            {
                JogParams parameters = iJogParams.GetJogParams(_defaultTimeout);

                parameters.Acceleration = 219;
                parameters.MaxVelocity = 643495;
                parameters.MinVelocity = 0;
                parameters.Mode = JogMode.Continuous;
                parameters.StepSize = 19196;
                parameters.StopMode = JogStopMode.Immediate;

                iJogParams.SetJogParams(parameters);
                // The new jog parameters have been sent to the controller
            }
        }

        public void ChangeJoystickParams(IDevice device)
        {
            var iJoystickParams = device as IJoystickParams;
            if (iJoystickParams != null)
            {
                JoystickParams parameters = iJoystickParams.GetJoystickParams(_defaultTimeout);

                parameters.LowGearMaxVelocity = 13421;
                parameters.HighGearMaxVelocity = 134217;
                parameters.LowGearAcceleration = 1374;
                parameters.HighGearAcceleration = 68;
                parameters.DirectionSense = JoystickDirectionSense.Positive;

                iJoystickParams.SetJoystickParams(parameters);
                // The new joystick parameters have been sent to the controller
            }
        }

        public void ChangeKcubeIoTriggerParams(IDevice device)
        {
            var iKcubeIoTriggerParams = device as Thorlabs.MotionControl.XA.DeviceFeatures.IKcubeIoTriggerParams;
            if (iKcubeIoTriggerParams != null)
            {
                Thorlabs.MotionControl.XA.KcubeIoTriggerParams parameters = iKcubeIoTriggerParams.GetKcubeIoTriggerParams(_defaultTimeout);

                parameters.Trigger1Mode = Thorlabs.MotionControl.XA.KcubeIoTriggerMode.GeneralPurposeInput;
                parameters.Trigger1Polarity = Thorlabs.MotionControl.XA.KcubeIoTriggerPolarity.ActiveIsLogicHigh;
                parameters.Trigger2Mode = Thorlabs.MotionControl.XA.KcubeIoTriggerMode.GeneralPurposeOutput;
                parameters.Trigger2Polarity = Thorlabs.MotionControl.XA.KcubeIoTriggerPolarity.ActiveIsLogicHigh;

                iKcubeIoTriggerParams.SetKcubeIoTriggerParams(parameters);
                // The new KCube trigger I/O parameters have been sent to the controller
            }
        }

        public void ChangeKcubeMmiLockState(IDevice device)
        {
            var iKcubeMmiLockState = device as IKcubeMmiLock;
            if (iKcubeMmiLockState != null)
            {
                KcubeMmiLockState state = iKcubeMmiLockState.GetKcubeMmiLockState(_defaultTimeout);

                
                iKcubeMmiLockState.SetKcubeMmiLockState(KcubeMmiLockState.KcubeMmiLocked);
                // The new KCube mmi lock state has been sent to the controller
            }
        }

        public void ChangeKcubeMmiParams(IDevice device)
        {
            var iKcubeMmiParams = device as Thorlabs.MotionControl.XA.DeviceFeatures.IKcubeMmiParams;
            if (iKcubeMmiParams != null)
            {
                Thorlabs.MotionControl.XA.KcubeMmiParams parameters = iKcubeMmiParams.GetKcubeMmiParams(_defaultTimeout);

                parameters.DisplayBrightness = 60;
                parameters.DisplayDimLevel = 2;
                parameters.DisplayTimeout = 10;
                parameters.JoystickAcceleration = 131;
                parameters.JoystickDirectionSense = Thorlabs.MotionControl.XA.KcubeMmiJoystickDirectionSense.Normal;
                parameters.PresetPosition1 = 0;
                parameters.PresetPosition2 = 0;
                parameters.PresetPosition3 = 0;

                iKcubeMmiParams.SetKcubeMmiParams(parameters);
                // The new KCube MMI parameters have been sent to the controller
            }
        }

        public void ChangeKcubePositionTriggerParams(IDevice device)
        {
            var iKcubePositionTriggerParams = device as IKcubePositionTriggerParams;
            if (iKcubePositionTriggerParams != null)
            {
                KcubePositionTriggerParams parameters = iKcubePositionTriggerParams.GetKcubePositionTriggerParams(_defaultTimeout);

                parameters.ForwardInterval = 0;
                parameters.ForwardNumberOfPulses = 0;
                parameters.ForwardStartPosition = 0;
                parameters.NumberOfCycles = 0;
                parameters.PulseWidth = 100000;
                parameters.ReverseInterval = 0;
                parameters.ReverseNumberOfPulses = 0;
                parameters.ReverseStartPosition = 0;

                iKcubePositionTriggerParams.SetKcubePositionTriggerParams(parameters);
                // The new KCube position trigger parameters have been sent to the controller

            }
        }

        public void ChangeKpcIoSettingsParams(IDevice device)
        {
            var iIoSettingsParams = device as IKpcIoSettingsParams;
            if (iIoSettingsParams != null)
            {
                KpcIoSettingsParams parameters = iIoSettingsParams.GetIoSettingsParams(_defaultTimeout);

                parameters.AnalogInputSource = KpcAnalogInputSource.HubInputA;
                parameters.FilterCutOffFrequency = 40;
                parameters.ForceSense = 50;
                parameters.StrainGaugeOption = KpcStrainGaugeOption.ReadsPosition;
                parameters.VoltageLimit = 75;
                parameters.VoltageRange = KpcVoltageRange.Range75Volts;

                iIoSettingsParams.SetIoSettingsParams(parameters);
                // The new I/O settings parameters have been sent to the controller
            }
        }

        public void ChangeKpcIoTriggerParams(IDevice device)
        {
            var iKcubeIoTriggerParams = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.IKpcIoTriggerParams;
            if (iKcubeIoTriggerParams != null)
            {
                Thorlabs.MotionControl.XA.Piezo.KpcIoTriggerParams parameters = iKcubeIoTriggerParams.GetKpcIoTriggerParams(_defaultTimeout);

                parameters.Trigger1Mode = Thorlabs.MotionControl.XA.Piezo.KpcIoTriggerMode.GeneralPurposeInput;
                parameters.Trigger1Polarity = Thorlabs.MotionControl.XA.KcubeIoTriggerPolarity.ActiveIsLogicHigh;
                parameters.Trigger2Mode = Thorlabs.MotionControl.XA.Piezo.KpcIoTriggerMode.GeneralPurposeOutput;
                parameters.Trigger2Polarity = Thorlabs.MotionControl.XA.KcubeIoTriggerPolarity.ActiveIsLogicHigh;
                parameters.MonitorFilterCutOffFrequency = 20;
                parameters.MonitorOutputMode = KpcMonitorOutputMode.HighVoltage;
                parameters.MonitorOutputSoftwareValue = 20;
                parameters.StrainGaugeLowerLimit = 200;
                parameters.StrainGaugeUpperLimit = 800;
                parameters.SmoothingSamples = 15;

                iKcubeIoTriggerParams.SetKpcIoTriggerParams(parameters);
                // The new KPC KCube trigger I/O parameters have been sent to the controller
            }
        }

        public void ChangeKpcMmiParams(IDevice device)
        {
            var iKcubeMmiParams = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.IKpcMmiParams;
            if (iKcubeMmiParams != null)
            {
                Thorlabs.MotionControl.XA.Piezo.KpcMmiParams parameters = iKcubeMmiParams.GetKpcMmiParams(_defaultTimeout);

                parameters.JoystickMode = Thorlabs.MotionControl.XA.Piezo.KpcMmiJoystickMode.Jogs;
                parameters.JoystickGear = KcubeMmiJoystickGear.High;
                parameters.JoystickPositionStepSize = 40;
                parameters.JoystickVoltageStepSize = 20;
                parameters.JoystickDirectionSense = Thorlabs.MotionControl.XA.Piezo.KpcMmiJoystickDirectionSense.Normal;
                parameters.PresetPosition1 = 20;
                parameters.PresetPosition2 = 40;
                parameters.PresetVoltage1 = 10;
                parameters.PresetVoltage2 = 50;
                parameters.DisplayBrightness = 60;
                parameters.DisplayTimeout = 10;
                parameters.DisplayDimLevel = 2;

                iKcubeMmiParams.SetKpcMmiParams(parameters);
                // The new KPC KCube MMI parameters have been sent to the controller
            }
        }

        public void ChangeLcdDisplayParams(IDevice device)
        {
            var iLcdDisplayParams = device as ILcdDisplayParams;
            if (iLcdDisplayParams != null)
            {
                LcdDisplayParams parameters = iLcdDisplayParams.GetLcdDisplayParams(_defaultTimeout);
                parameters.DisplayBrightness = 100;
                parameters.DisplayDimLevel = 33;
                parameters.DisplayTimeout = 8;
                parameters.KnobSensitivity = 32767;
                iLcdDisplayParams.SetLcdDisplayParams(parameters);
                // The new LCD display parameters have been sent to the controller
            }
        }

        public void ChangeLcdMoveParams(IDevice device)
        {
            var iLcdMoveParams = device as ILcdMoveParams;
            if (iLcdMoveParams != null)
            {
                LcdMoveParams parameters = iLcdMoveParams.GetLcdMoveParams(_defaultTimeout);
                parameters.Acceleration = 13744;
                parameters.JogStepSize = 60000;
                parameters.JogStopMode = JogStopMode.Immediate;
                parameters.KnobMode = LcdKnobMode.Velocity;
                parameters.MaxVelocity = 6710886;
                parameters.PresetPosition1 = 60000;
                iLcdMoveParams.SetLcdMoveParams(parameters);
                // The new LCD move parameters have been sent to the controller
            }
        }


        public void ChangeLimitSwitchParams(IDevice device)
        {
            var iLimitSwitchParamsGetter = device as ILimitSwitchParamsGetter;
            if (iLimitSwitchParamsGetter != null)
            {
                LimitSwitchParams parameters = iLimitSwitchParamsGetter.GetLimitSwitchParams(_defaultTimeout);

                parameters.ClockwiseHardLimitOperatingMode = HardLimitOperatingModes.SwitchContactMakesWhenHoming;
                parameters.ClockwiseSoftLimit = 1073741824;
                parameters.CounterclockwiseHardLimitOperatingMode = HardLimitOperatingModes.SwitchIgnored;
                parameters.CounterclockwiseSoftLimit = -1073741824;
                parameters.SoftwareLimitMode = SoftLimitOperatingModes.Ignored;

                if (device is ILimitSwitchParamsSetter)
                {
                    ( device as ILimitSwitchParamsSetter ).SetLimitSwitchParams(parameters);
                    // The new limit switch parameters have been sent to the controller
                }
            }
        }

        public void ChangeMaxOutputVoltageParams(IDevice device)
        {
            var iMaxOutputVoltageParams = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.IMaxOutputVoltageParams;
            if (iMaxOutputVoltageParams != null)
            {
                Thorlabs.MotionControl.XA.Piezo.MaxOutputVoltageParams parameters
                    = iMaxOutputVoltageParams.GetMaxOutputVoltageParams(_defaultTimeout);

                parameters.MaxOutputVoltage = 74;

                iMaxOutputVoltageParams.SetMaxOutputVoltage(parameters.MaxOutputVoltage);
                // The new maximum output voltage been sent to the controller
            }
        }


        public void ChangeMotorOutputParams(IDevice device)
        {
            var iMotorOutputParams = device as IMotorOutputParams;
            if (iMotorOutputParams != null)
            {
                MotorOutputParams parameters = iMotorOutputParams.GetMotorOutputParams(_defaultTimeout);

                parameters.ContinuousCurrentLimit = 22937;
                parameters.EnergyLimit = 19660;
                parameters.MotorLimit = 32767;

                iMotorOutputParams.SetMotorOutputParams(parameters);
                // The new motor output parameters have been sent to the controller
            }
        }

        public void ChangeMoveAbsoluteParams(IDevice device)
        {
            var iMoveAbsoluteParams = device as IMoveAbsoluteParams;
            if (iMoveAbsoluteParams != null)
            {
                MoveAbsoluteParams parameters = iMoveAbsoluteParams.GetMoveAbsoluteParams(_defaultTimeout);

                parameters.AbsolutePosition = 86363;

                iMoveAbsoluteParams.SetMoveAbsoluteParams(parameters);
                // The new move absolute parameters have been sent to the controller
            }
        }

        public void ChangeMoveRelativeParams(IDevice device)
        {
            var iMoveRelativeParams = device as IMoveRelativeParams;
            if (iMoveRelativeParams != null)
            {
                MoveRelativeParams parameters = iMoveRelativeParams.GetMoveRelativeParams(_defaultTimeout);

                parameters.RelativeDistance = 86363;

                iMoveRelativeParams.SetMoveRelativeParams(parameters);
                // The new move relative parameters have been sent to the controller
            }
        }

        public void ChangeOutputVoltage(IDevice device)
        {
            var iOutputVoltage = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.IOutputVoltage;
            if (iOutputVoltage != null)
            {
                Int16 voltage = iOutputVoltage.GetOutputVoltage(_defaultTimeout);

                iOutputVoltage.SetOutputVoltage(50);
                // The new output voltage been sent to the controller
            }
        }

        public void ChangeOutputVoltageControlSourceParams(IDevice device)
        {
            var iOutputVoltageControlSourceParams = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.IOutputVoltageControlSourceParams;
            if (iOutputVoltageControlSourceParams != null)
            {
                Thorlabs.MotionControl.XA.Piezo.OutputVoltageControlSourceParams parameters = 
                    iOutputVoltageControlSourceParams.GetOutputVoltageControlSourceParams(_defaultTimeout);

                parameters.Sources = Thorlabs.MotionControl.XA.Piezo.OutputVoltageControlSources.SoftwareOnly;
                iOutputVoltageControlSourceParams.SetOutputVoltageControlSourceParams(parameters);
                // The new output voltage control source parameters have been sent to the controller
            }
        }

        public void ChangePiezoPositionLoopParams(IDevice device)
        {
            var iPositionLoopParams = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.IPositionLoopParams;
            if (iPositionLoopParams != null)
            {
                Thorlabs.MotionControl.XA.Piezo.PositionLoopParams parameters = iPositionLoopParams.GetPositionLoopParams(_defaultTimeout);

                parameters.Integral = 100;
                parameters.Proportional = 100;
                
                iPositionLoopParams.SetPositionLoopParams(parameters);
                // The new position loop parameters have been sent to the controller
            }
        }


        public void ChangePosition(IDevice device)
        {
            var iPosition = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.IPosition;
            if (iPosition != null)
            {
                Int16 position = iPosition.GetPosition(_defaultTimeout);

                position = 0;

                iPosition.SetPosition(position);
                // The new position has been sent to the controller
            }
        }

        public void ChangePositionControlMode(IDevice device)
        {
            var iPositionControlMode = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.IPositionControlMode;
            if (iPositionControlMode != null)
            {
                Thorlabs.MotionControl.XA.Piezo.PositionControlMode PositionControlMode =
                    iPositionControlMode.GetPositionControlMode(_defaultTimeout);
                // The position control mode has been read from the controller

                iPositionControlMode.SetPositionControlMode(Thorlabs.MotionControl.XA.Piezo.PositionControlMode.ClosedLoop,
                    _defaultTimeout);
                // The position control has been set to open loop
            }
        }

        public void ChangePositionLoopParams(IDevice device)
        {
            var iPositionLoopParams = device as Thorlabs.MotionControl.XA.DeviceFeatures.IPositionLoopParams;
            if (iPositionLoopParams != null)
            {
                Thorlabs.MotionControl.XA.PositionLoopParams parameters = 
                    iPositionLoopParams.GetPositionLoopParams(PositionLoopScenario.Single, _defaultTimeout);

                parameters.AccelerationFeedForward = 0;
                parameters.Derivative = 4500;
                parameters.ErrorLimit = 6553;
                parameters.Integral = 1800;
                parameters.IntegralLimit = 32767;
                parameters.Proportional = 2400;
                parameters.Scale = 4000;
                parameters.ServoCycles = 6;
                parameters.VelocityFeedForward = 0;

                iPositionLoopParams.SetPositionLoopParams(PositionLoopScenario.Single, parameters);
                // The new position loop parameters have been sent to the controller
            }
        }

        public void ChangePowerParams(IDevice device)
        {
            var iPowerParams = device as IPowerParams;
            if (iPowerParams != null)
            {
                PowerParams parameters = iPowerParams.GetPowerParams(_defaultTimeout);

                parameters.MoveFactor = 6;
                parameters.RestFactor = 1;
                iPowerParams.SetPowerParams(parameters);
                // The new power parameters have been sent to the controller
            }
        }

        public void ChangeProfileModeParams(IDevice device)
        {
            var iProfileModeParams = device as IProfileModeParams;
            if (iProfileModeParams != null)
            {
                ProfileModeParams parameters = iProfileModeParams.GetProfileModeParams(_defaultTimeout);

                parameters.Mode = ProfileMode.Trapezoidal;
                parameters.Jerk = 0x000e1279;
                iProfileModeParams.SetProfileModeParams(parameters);
                // The new profile mode parameters have been sent to the controller
            }
        }

        public void ChangeSlewRateParams(IDevice device)
        {
            var iSlewRateParams = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.ISlewRateParams;
            if (iSlewRateParams != null)
            {
                Thorlabs.MotionControl.XA.Piezo.SlewRateParams parameters = iSlewRateParams.GetSlewRateParams(_defaultTimeout);

                parameters.ClosedLoopSlewRate = 200;
                parameters.OpenLoopSlewRate = 200;

                iSlewRateParams.SetSlewRateParams(parameters);
                // The new slew rate parameters have been sent to the controller
            }
        }

        public void ChangeStageAxisParams(IDevice device)
        {
            var iStageAxisParams = device as IStageAxisParams;
            if (iStageAxisParams != null)
            {
                StageAxisParams parameters = iStageAxisParams.GetStageAxisParams(_defaultTimeout);

                parameters.MaxPosition = 100000;
                parameters.MinPosition = 0;
                iStageAxisParams.SetStageAxisParams(parameters);

                // The new stage axis parameters have been sent to the controller
            }
        }

        public void ChangeStepperLoopParams(IDevice device)
        {
            var feature = device as IStepperLoopParams;

            if (feature != null)
            {
                StepperLoopParams originalStepperLoopParams = feature.GetStepperLoopParams(_defaultTimeout);

                // The Stepper Loop Params have been retrieved from the controller.

                StepperLoopParams newStepperLoopParams = new StepperLoopParams
                {
                    OutputClip = 50000,
                    OutputTolerance = 1000,
                    Differential = 10000,
                    Integral = 10000,
                    Proportional = 10000
                };

                feature.SetStepperLoopParams(newStepperLoopParams);

                // The Stepper Loop Params have been set to the controller.                
            }
        }

        public void ChangeTrackSettleParams(IDevice device)
        {
            var iTrackSettleParams = device as ITrackSettleParams;
            if (iTrackSettleParams != null)
            {
                TrackSettleParams parameters = iTrackSettleParams.GetTrackSettleParams(_defaultTimeout);

                parameters.SettleWindow = 4;
                parameters.SettleTime = 197;
                parameters.TrackWindow = 0;

                iTrackSettleParams.SetTrackSettleParams(parameters);
                // The new track settle parameters have been sent to the controller
            }
        }

        public void ChangeTriggerParamsForDcBrushless(IDevice device)
        {
            var iTriggerParams = device as ITriggerParamsForDcBrushless;
            if (iTriggerParams != null)
            {
                TriggerParamsForDcBrushless parameters = iTriggerParams.GetTriggerParamsForDcBrushless(_defaultTimeout);

                parameters.Modes = TriggerModesForDcBrushless.InputActiveIsLogicHigh | TriggerModesForDcBrushless.InputTriggersHomeMove;

                iTriggerParams.SetTriggerParamsForDcBrushless(parameters);
                // The new trigger parameters have been sent to the DC brushless controller
            }
        }

        public void ChangeTriggerParamsForStepper(IDevice device)
        {
            var feature = device as ITriggerParamsForStepper;

            if (feature != null)
            {
                var parameters = feature.GetTriggerParamsForStepper(_defaultTimeout);

                // The trigger parameters have been retrieved from the stepper controller.

                parameters.Modes = TriggerModesForStepper.OutputActiveUntilMoveEnd;

                feature.SetTriggerParamsForStepper(parameters);

                // The trigger parameters have been sent to the stepper controller
            }
        }

        public void ChangeVelocityParams(IDevice device)
        {
            var iVelocityParams = device as IVelocityParams;
            if (iVelocityParams != null)
            {
                VelocityParams parameters = iVelocityParams.GetVelocityParams(_defaultTimeout);

                parameters.Acceleration = 146;
                parameters.MaxVelocity = 428997;
                parameters.MinVelocity = 0;

                iVelocityParams.SetVelocityParams(parameters);
                // The new velocity parameters have been sent to the controller
            }
        }

        public void GetAdcInputs(IDevice device)
        {
            var feature = device as IAdcInputs;

            if (feature != null)
            {
                AdcInputs adcInputs = feature.GetAdcInputs(_defaultTimeout);

                // The Adc Inputs have been read from the controller.
            }
        }


        public void GetDigitalInputStates(IDevice device)
        {
            var iDigitalInputStates = device as IDigitalInputStates;
            if (iDigitalInputStates != null)
            {
                DigitalInputStates digitalInputs = iDigitalInputStates.GetDigitalInputStates(_defaultTimeout);
                // Digital input states have been loaded from the controller
            }
        }

        public void GetFirmwareVersionInfo(IDevice device)
        {
            var iFirmwareVersionInfo = device as IFirmwareVersionInfo;
            if (iFirmwareVersionInfo != null)
            {
                FirmwareVersionInfo fimwareVersionInfo = iFirmwareVersionInfo.GetFirmwareVersionInfo();
                // Firmware information has been copied to the firmwareVersionInfo object
            }
        }

        public void GetHardwareInfo(IDevice device)
        {
            var iHardwareInfo = device as IHardwareInfo;
            if (iHardwareInfo != null)
            {
                HardwareInfo hardwareInfo = iHardwareInfo.GetHardwareInfo(_defaultTimeout);
                // Hardware information has been loaded from the controller and copied to the
                // hardwareInfo object
            }
        }

        public void GetIoConfigurationNumberOfPortsSupported(IDevice device)
        {
            var iNumberOfPortsSupported = device as IIoConfigurationParams;
            if (iNumberOfPortsSupported != null)
            {
                Int16 numberOfPorts = iNumberOfPortsSupported.GetIoConfigurationNumberOfPortsSupported();
                // Number of I/O ports supported has been determined
            }
        }

        public void GetLimitSwitchParams(IDevice device)
        {
            var iLimitSwitchParams = device as ILimitSwitchParamsGetter;
            if (iLimitSwitchParams != null)
            {
                LimitSwitchParams limitSwitchParams = iLimitSwitchParams.GetLimitSwitchParams(_defaultTimeout);
                // Limit switch params previously retrieved from the controller have been copied to the
                // limitSwitchParams object

                limitSwitchParams = iLimitSwitchParams.GetLimitSwitchParams(Timeout.Zero);
                // This is functionally equivalent to the first call to  GetLimitSwitchParams.
                // Limit switch params previously retrieved from the controller have been copied to the
                // limitSwitchParams object

                var myCustomTimeout = TimeSpan.FromMilliseconds(2500);
                // myCustomTimespan has been set to a period of 2500 milliseconds

                limitSwitchParams = iLimitSwitchParams.GetLimitSwitchParams(myCustomTimeout);
                // Limit switch params have been loaded from the controller and copied to the
                // limitSwitchParams object using a timeout of 2500 milliseconds

                limitSwitchParams = iLimitSwitchParams.GetLimitSwitchParams(Timeout.Infinite);
                // Limit switch params have been loaded from the controller and copied to the
                // limitSwitchParams object using an infinite timeout
            }
        }

        public void GetMaxTravel(IDevice device)
        {
            var iPiezoStatus = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.IMaxTravel;
            if (iPiezoStatus != null)
            {
                Int32 maxTravel = iPiezoStatus.GetMaxTravel(_defaultTimeout);
            }
            // Piezo maximum travel was read the controller
        }

        public void GetOutputWaveformParams(IDevice device)
        {
            var iOutputWaveformParams = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.IOutputWaveformParamsGetter;
            if (iOutputWaveformParams != null)
            {
                Thorlabs.MotionControl.XA.Piezo.OutputWaveformParams parameters = 
                    iOutputWaveformParams.GetOutputWaveformParams(_defaultTimeout);
                // The output waveforem params have been loaded from the controller and copied to the
                // parameters object
            }
        }


        public void GetPiezoStatus(IDevice device)
        {
            var iPiezoStatus = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.IPiezoStatus;
            if (iPiezoStatus != null)
            {
                Thorlabs.MotionControl.XA.Piezo.PiezoStatus piezoStatus = iPiezoStatus.GetPiezoStatus(_defaultTimeout);
            }
            // Piezo status data has been loaded from the controller and copied to the
            // piezoStatus object
        }

        public void GetPiezoInertialMotorStatus(IDevice device)
        {
            var iPiezoInertialMotorStatus = device as Thorlabs.MotionControl.XA.PiezoInertialMotor.DeviceFeatures.IPiezoInertialMotorStatus;
            if (iPiezoInertialMotorStatus != null)
            {
                Thorlabs.MotionControl.XA.PiezoInertialMotor.PiezoInertialMotorStatus piezoInertialMotorStatus = iPiezoInertialMotorStatus.GetPiezoInertialMotorStatus(_defaultTimeout);
            }
            // Piezo inertial status data has been loaded from the controller and copied to the
            // piezoInertialMotorStatus object
        }

        public void GetPositionCounter(IDevice device)
        {
            var iPositionCounter = device as IPositionCounter;
            if (iPositionCounter != null)
            {
                int positionCounter = iPositionCounter.GetPositionCounter(_defaultTimeout);
                // The position counter was read from the controller and copied to positionCounter
            }
        }

        public void GetRackBayOccupiedState(IDevice device)
        {
            var iRackBayOccupiedState = device as IRackBayOccupiedState;
            if (iRackBayOccupiedState != null)
            {
                RackBayOccupiedState enableState = iRackBayOccupiedState.GetRackBayOccupiedState(RackBayNumber.Bay1, _defaultTimeout);
                // The rack bay occupied state has been read from the controller

            }
        }

        public void GetAllStatus(IDevice device)
        {
            var iStatusItem = device as IStatusItems;
            if (iStatusItem != null)
            {
                // This example gets all of the available status for the device handled by 'device'

                // First, find out how many status items are available
                int numberOfStatusItemsAvailable = iStatusItem.GetStatusItemCount();
                // The number of status items available was read from the controller
                // and copied to numberOfStatusItemsAvailable

                // Lastly, request 'numberOfStatusItemsAvailable' items starting at item zero. This will
                // get all of them.
                IList<StatusItem> statusItems = iStatusItem.GetStatusItems(0, numberOfStatusItemsAvailable);
            }
        }

        public void GetStatus(IDevice device)
        {
            var iStatusItem = device as IStatusItems;
            if (iStatusItem != null)
            {
                // Get the current position for the 'device'

                StatusItem statusItem = iStatusItem.GetStatusItem(StatusItemId.Position);

                // Position information has been successfully copied to the local status item

                // The members of a status item class are:
                // Id           - Identifies the device property this status item relates to. In this case, it
                //                will be the one we requested i.e., StatusItemId.Position
                // GetBoolean() - Returns the boolean value of the status item. If statusItem is not of the boolean
                //                type, accessing this property will throw an InvalidOperationException
                // GetInteger() - The Int64 value of the status item. If statusItem is not of the integer type,
                //                accessing this property will throw an InvalidOperationException
                // GetString()  - The string value of the status item. If statusItem is not of the string type,
                //                accessing this property will throw an InvalidOperationException
                // IsBoolean    - Returns true if status item is of the boolean type, false if not. Use this to
                //                verify that GetBoolean() is the correct property to retrieve the status item value
                // IsInteger    - Returns true if status item is of the integer type, false if not. Used this to
                //                verify that GetInteger() is the correct property to retrieve the status item value
                // IsString     - Returns true if status item is of the string type, false if not. Used this to
                //                verify that GetString() is the correct property to retrieve the status item value

                // Let's examine the position we've just retrieved to see if it's beyond 1234:

                // From previously looking at 'IsInteger' we know that the position value is always 
                // an integer. So we can access the value using GetInteger() method.
                Int64 currentPosition = statusItem.GetInteger();

                if (currentPosition > 1234)
                {
                    // ...
                }
            }
        }

        public void GetStepperStatus(IDevice device)
        {
            var iStepperStatus = device as IStepperStatus;
            if (iStepperStatus != null)
            {
                StepperStatus stepperStatus = iStepperStatus.GetStepperStatus(_defaultTimeout);
                // Stepper status data has been loaded from the controller and copied to the
                // stepperStatus variable
            }
        }

        public void GetUniversalStatus(IDevice device)
        {
            var iUniversalStatus = device as IUniversalStatus;
            if (iUniversalStatus != null)
            {
                UniversalStatus universalStatus = iUniversalStatus.GetUniversalStatus(_defaultTimeout);
                // Universal status data has been loaded from the controller and copied to the
                // universalStatus variable
            }
        }

        public void GetUniversalStatusBits(IDevice device)
        {
            var iUniversalStatusBits = device as IUniversalStatusBits;
            if (iUniversalStatusBits != null)
            {
                UniversalStatusBits universalStatusBits = iUniversalStatusBits.GetUniversalStatusBits(_defaultTimeout);
                // Universal status bits have been loaded from the controller and copied to
                // universalStatusBits variable
            }
        }

        public void SetEndOfMoveMessagesMode(IDevice device)
        {
            var iEndOfMessagesMode = device as IEndOfMoveMessagesMode;
            if (iEndOfMessagesMode != null)
            {
                iEndOfMessagesMode.SetEndOfMoveMessagesMode(EndOfMoveMessageMode.Disabled);
                // A request has been sent to the controller instructing it to stop sending end of move messages.

                iEndOfMessagesMode.SetEndOfMoveMessagesMode(EndOfMoveMessageMode.Enabled);
                // A request has been sent to the controller instructing it to start sending end of move messages.

            }
        }

        public void SendNoFlashProgramming(IDevice device)
        {
            var iNoFlashProgramming = device as INoFlashProgramming;
            if (iNoFlashProgramming != null)
            {
                iNoFlashProgramming.SendNoFlashProgramming();

                // The "no flash programming" message has been sent to the controller.
            }
        }

        public void SendYesFlashProgramming(IDevice device)
        {
            var iYesFlashProgramming = device as IYesFlashProgramming;
            if (iYesFlashProgramming != null)
            {
                iYesFlashProgramming.SendYesFlashProgramming();

                // The "yes flash programming" message has been sent to the controller.
            }
        }

        public void SetPositionCounter(IDevice device)
        {
            var iPositionCounter = device as IPositionCounter;
            if (iPositionCounter != null)
            {
                iPositionCounter.SetPositionCounter(1000);
                // A request to set the position counter to the value specified has been sent
                // to the controller

                iPositionCounter.SetPositionCounter(0);
                // A request to zero the position counter has been sent to the controller
            }

        }


        public void SetStatusMode(IDevice device)
        {
            var iStatusMode = device as IStatusMode;
            if (iStatusMode != null)
            {
                iStatusMode.SetStatusMode(OperatingModes.ManualStatusPolling);
                // A request has been sent to the controller instructing it to stop sending regular status updates.
                // Status update requests will not automatically be sent to the controller.

                iStatusMode.SetStatusMode(OperatingModes.StatusPushedByController);
                // A request has been sent to the controller instructing it to start sending regular status updates.
                // Status update requests will not automatically be sent to the controller.

                iStatusMode.SetStatusMode(OperatingModes.AutomaticStatusPolling);
                // A request has been sent to the controller instructing it to stop sending regular status updates.
                // Status update requests will automatically be sent to the controller.
            }
        }

        public void SetZero(IDevice device)
        {
            var iZero = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.IZero;
            if (iZero != null)
            {
                iZero.SetZero(Timeout.Infinite);
                // Zeroing of the actuator completed successfully
            }

        }

        public void Device(IDevice device)
        {
            //Generic information about a device
            DeviceFamily deviceFamily = device.DeviceFamily;
            string deviceId = device.DeviceId;
            string deviceTypeDescription = device.DeviceTypeDescription;
            string partNumber = device.PartNumber;
            string transport = device.Transport;
        }

        public void Disconnect(IDevice device)
        {
            var iDisconnect = device as IDisconnect;
            if (iDisconnect != null)
            {
                iDisconnect.Disconnect();
                // A disconnect notification has been sent to the controller.
                // This instructs the controller that we intend to imminently close the connection.
            }
        }

        public void Home(IDevice device)
        {
            var iHome = device as IHome;
            if (iHome != null)
            {
                iHome.Home(Timeout.Infinite);
                // Homing of the actuator completed successfully

                iHome.Home(Timeout.Zero);
                // A request to start homing the actuator has been sent to the controller
            }
        }

        public void Identify(IDevice device)
        {
            var iIdentify = device as IIdentify;
            if (iIdentify != null)
            {
                iIdentify.Identify();
                // A request to visual identify itself has been sent to the controller
            }

        }

        public void LoadParams(IDevice device)
        {
            var iLoadParams = device as ILoadParams;
            if (iLoadParams != null) 
            {
                iLoadParams.LoadParams();
                // All parameters have been loaded from the controller
            }
        }

        public void MoveAbsolute(IDevice device)
        {
            var iMove = device as IMove;
            if (iMove != null)
            {
                iMove.Move(MoveMode.AbsoluteToProgrammedPosition, 0, Timeout.Infinite);
                // The stage has been move to the preprogrammed absolute position (previously set with MoveAbsoluteParams).
                // The 'parameter' argument is unused when a programmed option is specified

                iMove.Move(MoveMode.Absolute, (int)( ( (double)45.0 ) * ( (double)1919.6418578623391 ) ), Timeout.Infinite);
                // The stage has been move to the specified absolute position
            }
        }

        public void MoveContinuous(IDevice device)
        {
            var iMove = device as IMove;
            if (iMove != null)
            {
                iMove.Move(MoveMode.ContinuousForward, 0, Timeout.Infinite);
                // The stage has been move to the preprogrammed absolute position (previously set with MoveAbsoluteParams).
                // The 'parameter' argument is unused when a continuous option is specified
            }
        }

        public void MoveJog(IDevice device)
        {
            var iMove = device as IMove;
            if (iMove != null)
            {
                iMove.Move(MoveMode.JogReverse, 0, Timeout.Infinite);
                // The stage was jogged in the reverse direction
                // The 'parameter' argument is unused when jog option is specified
            }
        }

        public void MoveRelative(IDevice device)
        {
            var iMove = device as IMove;
            if (iMove != null)
            {
                iMove.Move(MoveMode.RelativeByProgrammedDistance, 0, Timeout.Infinite);
                // The stage has been moved by the preprogrammed relative distance (previously set with MoveRelativeParams).
                // The 'parameter' argument is unused when a programmed option is specified

                iMove.Move(MoveMode.RelativeMove, (int)( ( (double)45.0 ) * ( (double)1919.6418578623391 ) ), Timeout.Infinite);
                // The stage has been moved by the specified relative distance
            }
        }

        public void OutputWaveform(IDevice device)
        {
            var iOutputWaveform = device as Thorlabs.MotionControl.XA.Piezo.DeviceFeatures.IOutputWaveform;
            if (iOutputWaveform != null)
            {
                Thorlabs.MotionControl.XA.Piezo.OutputWaveformLookupTableSample sample = 
                    new Thorlabs.MotionControl.XA.Piezo.OutputWaveformLookupTableSample();
                sample.Index = 0;
                sample.Voltage = 0;
                iOutputWaveform.SetOutputWaveformLookupTableSampleParams(sample);
                // A request has been sent to the controller instructing it to set the lookup table sample

                Thorlabs.MotionControl.XA.Piezo.OutputWaveformParams parameters =
                    new Thorlabs.MotionControl.XA.Piezo.OutputWaveformParams();
                parameters.InterSampleDelay = 10;
                parameters.Mode = Thorlabs.MotionControl.XA.Piezo.OutputWaveformOperatingModes.Continuous;
                parameters.NumberOfCycles = 0;
                parameters.NumberOfSamplesBetweenTriggerRepetition = 10;
                parameters.NumberOfSamplesPerCycle = 500;
                parameters.OutputTriggerStartIndex = 0;
                parameters.OutputTriggerWidth = 0;
                parameters.PostCycleDelay = 0;
                parameters.PreCycleDelay = 0;
                iOutputWaveform.SetOutputWaveformParams(parameters);
                // A request has been sent to the controller instructing it to set the output waveform parameters

                iOutputWaveform.StartOutputWaveform();
                // A request has been sent to the controller instructing it to start generating the output waveform

                iOutputWaveform.StopOutputWaveform();
                // A request has been sent to the controller instructing it to stop generating the output waveform



            }
        }



        public void PersistParams(IDevice device)
        {
            var iPersistParams = device as IPersistParams;
            if (iPersistParams != null)
            {
                iPersistParams.PersistParams(ParameterGroupId.Unspecified);
                // A request to persist parameters has been sent to the controller
            }
        }

        public void PiezoInertialMotorPulseParaAcquire(IDevice device)
        {
            var iPiezoInertialMotorPulseParaAcquire = device as IPulseParaAcquire;
            if (iPiezoInertialMotorPulseParaAcquire != null)
            {
                iPiezoInertialMotorPulseParaAcquire.PulseParaAcquire(Timeout.Infinite);
                // A request has been sent to the controller instructing it to acquire pulse parameters
            }
        }

        public void RackIdentify(IDevice device)
        {
            var iRackIdentify = device as IRackIdentify;
            if (iRackIdentify != null)
            {
                byte channel1 = 0x01;
                iRackIdentify.RackIdentify(channel1);
                // A request to visually dentify itself has been sent to the controller
            }

        }


        public void RestoreFactoryDefaults(IDevice device)
        {
            var iRestoreFactoryDefaults = device as IRestoreFactoryDefaults;
            if (iRestoreFactoryDefaults != null)
            {
                iRestoreFactoryDefaults.RestoreFactoryDefaults();
                // A request to reset to factory defaults has been sent to the controller
            }
        }

        public void Stop(IDevice device)
        {
            var iStop = device as IStop;
            if (iStop != null)
            {
                iStop.Stop(StopMode.Immediate, Timeout.Infinite);
                // Stage movement has been immediately stopped

                iStop.Stop(StopMode.Profiled, Timeout.Zero);
                // A request to stop stage movement in a profilled manner has been sent to the controller
            }
        }

        public void UnitConverter(IDevice device)
        {
            var iUnitConverter = device as IUnitConverter;
            if (iUnitConverter != null)
            {
                Int64 distanceInDeviceUnits = 19196;
                Int64 velocityInDeviceUnits = 429416;
                Int64 accelerationInDeviceUnits = 146;

                UnitConversionResult distanceResult = iUnitConverter.FromDeviceUnitToPhysical(ScaleType.Distance, distanceInDeviceUnits);
                // The 'distanceInDeviceUnits' value has been converted to the physical unit value and copied to the 'distanceResult.Value' member. 
                // The converter physical unit type has been copied to the 'distanceResult.ConverterUnit' member 

                distanceInDeviceUnits = iUnitConverter.FromPhysicalToDeviceUnit(ScaleType.Distance, distanceResult.UnitType, distanceResult.Value);
                // The 'distanceResult.Value' in 'distanceResult.ConverterUnit' units been converted back to the device unit value and assigned
                // to the distanceInDeviceUnits variable.

                UnitConversionResult velocityResult = iUnitConverter.FromDeviceUnitToPhysical(ScaleType.Velocity, velocityInDeviceUnits);
                // The 'velocityInDeviceUnits' value has been converted to the physical unit value and copied to the 'velocityResult.Value' member. 
                // The converter physical unit type has been copied to the 'velocityResult.ConverterUnit' member 

                velocityInDeviceUnits = iUnitConverter.FromPhysicalToDeviceUnit(ScaleType.Velocity, velocityResult.UnitType, velocityResult.Value);
                // The 'velocityResult.Value' in 'velocityResult.ConverterUnit' units been converted back to the device unit value and assigned
                // to the velocityInDeviceUnits variable.

                UnitConversionResult accelerationResult = iUnitConverter.FromDeviceUnitToPhysical(ScaleType.Acceleration, accelerationInDeviceUnits);
                // The 'accelerationInDeviceUnits' value has been converted to the physical unit value and copied to the 'accelerationResult.Value' member. 
                // The converter physical unit type has been copied to the 'accelerationResult.ConverterUnit' member 

                accelerationInDeviceUnits = iUnitConverter.FromPhysicalToDeviceUnit(ScaleType.Acceleration, accelerationResult.UnitType, accelerationResult.Value);
                // The 'accelerationResult.Value' in 'accelerationResult.ConverterUnit' units been converted back to the device unit value and assigned
                // to the accelerationInDeviceUnits variable.
            }
        }

        public void GetSubchannel(IDevice device)
        {
            var iGetSubchannel = device as IGetSubchannel;
            if (iGetSubchannel != null)
            {
                ISubchannel iSubChannel2 = iGetSubchannel.GetSubchannel(2);
                // iSubChannel2 can be used to control channel 2 of the device
            }
        }

        public void WritePackets(IDevice device)
        {
            var iPacketWriter = device as IPacketWriter;
            if (iPacketWriter != null)
            {
                iPacketWriter.WriteBytes(new byte[] { 0x05, 0x00, 0x00, 0x00, 0x50, 0x01 });// Hardware information request
                // The bytes in writeBuffer has been successfully written to the device
            }
        }

        public void SubscribeToPacketReceived(IDevice device)
        {
            var iPacketReceived = device as IPacketReceived;
            if(iPacketReceived != null)
            {
                iPacketReceived.PacketReceived += OnPacketReceived;
                // The function OnPacketReceived has subscribed to the PacketReceived event. It will be called
                // whenever a packet is received in relation to the device.

                // ...

                iPacketReceived.PacketReceived -= OnPacketReceived;
                // The function OnPacketReceived has unsubscribed from the PacketReceived event.
                // It will no longer be called.
            }
        }

        private void OnPacketReceived(object sender, PacketReceivedEventArgs e)
        {
            // This function will be called whenever a packet related to the relevant device handle is received.

            // Example of inspecting the packet to extract a command identifier
            byte[] packet = e.Packet;
            if (packet.Length > 2)
            {
                UInt16 commandId = Convert.ToUInt16(packet[0] | (packet[1] << 8));

                switch (commandId)
                {
                    case 0x0006: // Response to a hardware information request
                                 // ...
                        break;
                }
            }
        }

        public void SubscribeToNotificationRaised(IDevice device)
        {
            var iNotificationRaised = device as INotificationRaised;
            if (iNotificationRaised != null)
            {
                iNotificationRaised.NotificationRaised += OnNotificationRaised;
                // The function OnNotificationRaised has subscribed to the NotificationRaised event. It will be called
                // whenever a notification is available relating to the device.

                // ...
                // Normally, you would leave the function subscribed until immediately before closing the device.
                // Here we remove our subscription straight away to show you how it's done.
                iNotificationRaised.NotificationRaised -= OnNotificationRaised;
                // The function OnNotificationRaised has been unsubscribed from the NotificationRaised event.
                // It will no longer be called.
            }
        }

        private void OnNotificationRaised(object sender, NotificationRaisedEventArgs e)
        {
            NotificationId notificationId = e.NotificationId;
            
            switch (notificationId)
            {
                case NotificationId.AnalogMonitorConfigurationParamsChanged:

                    // Analog monitor notifications use a specialized type providing extra information
                    var analogMonitorEvent = e as AnalogMonitorConfigurationParamsChangedEventArgs;
                    ProcessAnalogMonitorNotification(sender as IAnalogMonitorConfigurationParams, analogMonitorEvent.MonitorNumber);
                    break;
                case NotificationId.StatusItemChanged:
                    // Status item notifications use a specialized type providing extra information
                    var statusItemNotificationRaisedEventArgs = e as StatusItemChangedEventArgs;
                    ProcessStatusItemNotification(sender as IStatusItems, statusItemNotificationRaisedEventArgs.StatusItemIds);
                    break;
                case NotificationId.CurrentLoopParamsChanged:
                    // Current loop notifications use a specialized type providing extra information
                    var currentLoopNotificationRaisedEventArgs = e as CurrentLoopParamsChangedEventArgs;
                    ProcessCurrentLoopNotification(sender as ICurrentLoopParams, currentLoopNotificationRaisedEventArgs.CurrentLoopScenario);
                    break;
                case NotificationId.HomeParamsChanged:
                    // An example of a standard notification
                    ProcessHomeParamsNotification(sender as IHomeParams);
                    break;
                case NotificationId.IoConfigurationParamsChanged:
                    // I/O configuration notifications use a specialized type providing extra information
                    var ioConfigurationEventArgs = e as IoConfigurationParamsChangedEventArgs;
                    ProcessIoConfigurationNotification(sender as IIoConfigurationParams, ioConfigurationEventArgs.PortNumber);
                    break;
                case NotificationId.PositionLoopParamsChanged:
                    // Position loop notifications use a specialized type providing extra information
                    var positionLoopNotificationRaisedEventArgs = e as PositionLoopParamsChangedEventArgs;
                    ProcessPositionLoopNotification(sender as Thorlabs.MotionControl.XA.DeviceFeatures.IPositionLoopParams, positionLoopNotificationRaisedEventArgs.PositionLoopScenario);
                    break;
                default:
                    //...
                    break;
            }
        }

        private void ProcessAnalogMonitorNotification(IAnalogMonitorConfigurationParams device, AnalogMonitorNumber monitorNumber)
        {
            AnalogMonitorConfigurationParams parameters = device.GetAnalogMonitorConfigurationParams(monitorNumber, _defaultTimeout);
            // The changed analog monitor configuration parameters have been copied into the local 'parameters' variable
        }

        private void ProcessCurrentLoopNotification(ICurrentLoopParams device, CurrentLoopScenario currentLoopScenario)
        {
            CurrentLoopParams parameters = device.GetCurrentLoopParams(currentLoopScenario, _defaultTimeout);
            // The changed current loop parameters have been copied into the local 'parameters' variable
        }

        private void ProcessHomeParamsNotification(IHomeParams device)
        {
            HomeParams parameters = device.GetHomeParams(_defaultTimeout);
            // The changed home parameters have been copied into the local 'parameters' variable
        }

        private void ProcessIoConfigurationNotification(IIoConfigurationParams device, IoPortNumber portNumber)
        {
            IoConfigurationParams parameters = device.GetIoConfigurationParams(portNumber, _defaultTimeout);
            // The changed I/O configuration parameters have been copied into the local 'parameters' variable
        }

        private void ProcessPositionLoopNotification(Thorlabs.MotionControl.XA.DeviceFeatures.IPositionLoopParams device, PositionLoopScenario positionLoopScenario)
        {
            Thorlabs.MotionControl.XA.PositionLoopParams parameters = device.GetPositionLoopParams(positionLoopScenario, _defaultTimeout);
            // The changed position loop parameters have been copied into the local 'parameters' variable
        }

        private void ProcessStatusItemNotification(IStatusItems device, StatusItemId[] updatedStatusItemIds)
        {
            // Loop through the status item identifiers that changed as part of this notification
            foreach (StatusItemId statusItemId in updatedStatusItemIds)
            {
                StatusItem statusItem = device.GetStatusItem(statusItemId);

                if (statusItem.IsBoolean)
                {
                    // This status item contains a boolean, therefore 'statusItem.GetBoolean()'
                    // holds the value
                }

                if (statusItem.IsInteger)
                {
                    // This status item contains an integer, therefore 'statusItem.GetInteger()'
                    // holds the value
                }
                
                if (statusItem.IsString)
                {
                    // This status item contains a string, therefore 'statusItem.GetString()'
                    // holds the value
                }
            }
        }
    }
}
