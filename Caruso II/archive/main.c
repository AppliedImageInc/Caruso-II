#include <stdlib.h>

#include <tlmc_xa_native_api.h>

#ifdef _WIN32
#define MAIN_CALL __cdecl
#else
#define MAIN_CALL
#endif

void Example_ChangeAnalogMonitorConfigurationParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeAuxIoPortMode(const TLMC_DeviceHandle hDevice);
void Example_ChangeAuxIoSoftwareStates(const TLMC_DeviceHandle hDevice);
void Example_ChangeBowIndex(const TLMC_DeviceHandle hDevice);
void Example_ChangeButtonParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeConnectedProductInfo(const TLMC_DeviceHandle hDevice);
void Example_ChangeCurrentLoopParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeDcPidParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeDigitalOutputStates(const TLMC_DeviceHandle hDevice);
void Example_ChangeEnableState(const TLMC_DeviceHandle hDevice);
void Example_ChangeGeneralMoveParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeHomeParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeIoConfigurationParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeIoPositionTriggerEnableState(const TLMC_DeviceHandle hDevice);
void Example_ChangeIoTriggerParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeJogParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeJoystickParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeKcubeIoTriggerParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeKcubeMmiLockState(const TLMC_DeviceHandle hDevice);
void Example_ChangeKcubeMmiParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeKcubePositionTriggerParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeLcdDisplayParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeLcdMoveParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeLimitSwitchParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeMotorOutputParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeMoveAbsoluteParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeMoveRelativeParams(const TLMC_DeviceHandle hDevice);
void Example_ChangePositionLoopParams(const TLMC_DeviceHandle hDevice);
void Example_ChangePowerParams(const TLMC_DeviceHandle hDevice);
void Example_ChangePotentiometerParams(const TLMC_DeviceHandle hDevice);
void Example_ChangePresetConnectedProduct(const TLMC_DeviceHandle hDevice);
void Example_ChangeProfileModeParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeStageAxisParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeStepperLoopParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeTrackSettleParams(const TLMC_DeviceHandle hDevice);
void Example_ChangeTriggerParamsForDcBrushless(const TLMC_DeviceHandle hDevice);
void Example_ChangeTriggerParamsForStepper(const TLMC_DeviceHandle hDevice);
void Example_ChangeVelocityParams(const TLMC_DeviceHandle hDevice);
void Example_PZ_ChangeKpcIoSettingsParams(const TLMC_DeviceHandle hDevice);
void Example_PZ_ChangeKpcIoTriggerParams(const TLMC_DeviceHandle hDevice);
void Example_PZ_ChangeKpcMmiParams(const TLMC_DeviceHandle hDevice);
void Example_PZ_ChangeMaxOutputVoltageParams(const TLMC_DeviceHandle hDevice);
void Example_PZ_ChangeOutputVoltage(const TLMC_DeviceHandle hDevice);
void Example_PZ_ChangeOutputVoltageControlSourceParams(const TLMC_DeviceHandle hDevice);
void Example_PZ_ChangeOutputWaveformParams(const TLMC_DeviceHandle hDevice);
void Example_PZ_ChangePosition(const TLMC_DeviceHandle hDevice);
void Example_PZ_ChangePositionControlMode(const TLMC_DeviceHandle hDevice);
void Example_PZ_ChangePositionLoopParams(const TLMC_DeviceHandle hDevice);
void Example_PZ_ChangeSlewRateParams(const TLMC_DeviceHandle hDevice);
void Example_PZIM_ChangeAbnormalMoveDetectionParams(const TLMC_DeviceHandle hDevice);
void Example_PZIM_ChangeAmplifierOutputParams(const TLMC_DeviceHandle hDevice);
void Example_PZIM_ChangeClosedLoopMoveParams(const TLMC_DeviceHandle hDevice);
void Example_PZIM_ChangeClosedLoopParams(const TLMC_DeviceHandle hDevice);
void Example_PZIM_ChangeEthernetParams(const TLMC_DeviceHandle hDevice);
void Example_PZIM_ChangeExternalTriggerConfig(const TLMC_DeviceHandle hDevice);
void Example_PZIM_ChangeExternalTriggerParams(const TLMC_DeviceHandle hDevice);
void Example_PZIM_ChangeJogParams(const TLMC_DeviceHandle hDevice);
void Example_PZIM_ChangeOpenLoopMoveParams(const TLMC_DeviceHandle hDevice);

void Example_GetAdcInputs(const TLMC_DeviceHandle hDevice);
void Example_GetAllSettings(const TLMC_DeviceHandle hDevice);
void Example_GetAllSettingsAsString(const TLMC_DeviceHandle hDevice);
void Example_GetAllStatus(const TLMC_DeviceHandle hDevice);
void Example_GetApiVersion();
void Example_GetCalibrationState(const TLMC_DeviceHandle hDevice);
void Example_GetConnectedProductsSupported(const TLMC_DeviceHandle hDevice);
void Example_GetDeviceInfo(const TLMC_DeviceHandle hDevice);
void Example_GetDeviceList();
void Example_GetDigitalInputStates(const TLMC_DeviceHandle hDevice);
void Example_GetEncoderCounter(const TLMC_DeviceHandle hDevice);
void Example_GetFirmwareVersionInfo(const TLMC_DeviceHandle hDevice);
void Example_GetHardwareInfo(const TLMC_DeviceHandle hDevice);
void Example_GetIoConfigurationNumberOfPortsSupported(const TLMC_DeviceHandle hDevice);
void Example_GetPositionCounter(const TLMC_DeviceHandle hDevice);
void Example_GetRackBayOccupiedState(const TLMC_DeviceHandle hDevice);
void Example_GetSetting(const TLMC_DeviceHandle hDevice);
void Example_GetStatus(const TLMC_DeviceHandle hDevice);
void Example_GetStepperStatus(const TLMC_DeviceHandle hDevice);
void Example_GetUmcStatus(const TLMC_DeviceHandle hDevice);
void Example_GetUniversalStatus(const TLMC_DeviceHandle hDevice);
void Example_GetUniversalStatusBits(const TLMC_DeviceHandle hDevice);
void Example_PZ_GetMaxTravel(const TLMC_DeviceHandle hDevice);
void Example_PZ_GetStatus(const TLMC_DeviceHandle hDevice);
void Example_PZIM_GetCurrentPosition(const TLMC_DeviceHandle hDevice);
void Example_PZIM_GetStatus(const TLMC_DeviceHandle hDevice);
void Example_PZIM_GetTriggerTargetPosition(const TLMC_DeviceHandle hDevice);

void Example_SetEncoderCounter(const TLMC_DeviceHandle hDevice);
void Example_SetEndOfMoveMessagesMode(const TLMC_DeviceHandle hDevice);
void Example_SetPositionCounter(const TLMC_DeviceHandle hDevice);
void Example_SetSetting(const TLMC_DeviceHandle hDevice);
void Example_SetSettingsFromString(const TLMC_DeviceHandle hDevice);
void Example_SetStatusMode(const TLMC_DeviceHandle hDevice);
void Example_PZ_SetOutputWaveformLookupTableSample(const TLMC_DeviceHandle hDevice);
void Example_PZ_SetZero(const TLMC_DeviceHandle hDevice);

void Example_ActivateCalibration(const TLMC_DeviceHandle hDevice);
void Example_DeactivateCalibration(const TLMC_DeviceHandle hDevice);
void Example_Disconnect(const TLMC_DeviceHandle hDevice);
void Example_Home(const TLMC_DeviceHandle hDevice);
void Example_Identify(const TLMC_DeviceHandle hDevice);
void Example_LoadParams(const TLMC_DeviceHandle hDevice);
void Example_MoveAbsolute(const TLMC_DeviceHandle hDevice);
void Example_MoveContinuous(const TLMC_DeviceHandle hDevice);
void Example_MoveJog(const TLMC_DeviceHandle hDevice);
void Example_MoveRelative(const TLMC_DeviceHandle hDevice);
void Example_MoveSyncArray(const TLMC_DeviceHandle hDevice);
void Example_MoveSyncParams(const TLMC_DeviceHandle hDevice);
void Example_MoveSyncStart(const TLMC_DeviceHandle hDevice);
void Example_PersistParams(const TLMC_DeviceHandle hDevice);
void Example_RackIdentify(const TLMC_DeviceHandle hDevice);
void Example_RestoreFactoryDefaults(const TLMC_DeviceHandle hDevice);
void Example_SendNoFlashProgramming(const TLMC_DeviceHandle hDevice);
void Example_SendYesFlashProgramming(const TLMC_DeviceHandle hDevice);
void Example_Stop(const TLMC_DeviceHandle hDevice);
void Example_UnitConverter(const TLMC_DeviceHandle hDevice);
void Example_PZ_StartOutputWaveform(const TLMC_DeviceHandle hDevice);
void Example_PZ_StopOutputWaveform(const TLMC_DeviceHandle hDevice);
void Example_PZIM_PulseParaAcquire(const TLMC_DeviceHandle hDevice);

void Example_GetChannel(const TLMC_DeviceHandle hDevice);

void Example_RegisterLoggingHandler();
void Example_UnregisterLoggingHandler();
void __stdcall Example_LoggingHandlerCallbackFn(const char* pBuffer, const unsigned int bufferLength, const uintptr_t userData);

void Example_WritingRawPackets(const TLMC_DeviceHandle hDevice);
void Example_ReadingRawPackets(const TLMC_DeviceHandle hDevice);
void __stdcall Example_PacketHandler(const unsigned char* pBuffer, const size_t bufferLength, const uintptr_t userData);

void Example_ReceivingNotifications(const TLMC_DeviceHandle hDevice);
void __stdcall Example_NotificationHandlerCallbackFn(const struct TLMC_Notification* pNotification, const uintptr_t userData);

void Example_SimulationCreateAndRemove();

int MAIN_CALL main()
{
    if (TLMC_Startup(NULL) == TLMC_Success)
    {
        TLMC_DeviceHandle hDevice;
        TLMC_ResultCode_Type resultCode = TLMC_Open("27000128", NULL, TLMC_OperatingMode_Default, &hDevice);

        if (resultCode == TLMC_Success)
        {
            TLMC_AddUserMessageToLog("READY");
            
            Example_GetChannel(hDevice);

            Example_SimulationCreateAndRemove();

            Example_ChangeAnalogMonitorConfigurationParams(hDevice); 
            Example_ChangeAuxIoPortMode(hDevice);
            Example_ChangeAuxIoSoftwareStates(hDevice);
            Example_ChangeBowIndex(hDevice);
            Example_ChangeButtonParams(hDevice);
            Example_ChangeConnectedProductInfo(hDevice);
            Example_ChangeCurrentLoopParams(hDevice);
            Example_ChangeDcPidParams(hDevice);
            Example_ChangeDigitalOutputStates(hDevice);
            Example_ChangeEnableState(hDevice);
            Example_ChangeGeneralMoveParams(hDevice);
            Example_ChangeHomeParams(hDevice);
            Example_ChangeIoConfigurationParams(hDevice);

            Example_ChangeIoPositionTriggerEnableState(hDevice);
            Example_ChangeIoTriggerParams(hDevice);
            Example_ChangeJogParams(hDevice);
            Example_ChangeJoystickParams(hDevice);
            Example_ChangeKcubeIoTriggerParams(hDevice);
            Example_ChangeKcubeMmiLockState(hDevice);
            Example_ChangeKcubeMmiParams(hDevice);
            Example_ChangeKcubePositionTriggerParams(hDevice);
            Example_ChangeLcdDisplayParams(hDevice);
            Example_ChangeLcdMoveParams(hDevice);
            Example_ChangeLimitSwitchParams(hDevice);
            Example_ChangeMotorOutputParams(hDevice);
            Example_ChangeMoveAbsoluteParams(hDevice);
            Example_ChangeMoveRelativeParams(hDevice);
            Example_ChangePositionLoopParams(hDevice);
            Example_ChangePotentiometerParams(hDevice);
            Example_ChangePowerParams(hDevice);
            Example_ChangePresetConnectedProduct(hDevice);
            Example_ChangeProfileModeParams(hDevice);
            Example_ChangeStageAxisParams(hDevice);
            Example_ChangeStepperLoopParams(hDevice);
            Example_ChangeTrackSettleParams(hDevice);
            Example_ChangeTriggerParamsForDcBrushless(hDevice);
            Example_ChangeTriggerParamsForStepper(hDevice);
            Example_ChangeVelocityParams(hDevice);
            Example_PZ_ChangeKpcIoSettingsParams(hDevice);
            Example_PZ_ChangeKpcIoTriggerParams(hDevice);
            Example_PZ_ChangeKpcMmiParams(hDevice);
            Example_PZ_ChangeMaxOutputVoltageParams(hDevice);
            Example_PZ_ChangeOutputVoltage(hDevice);
            Example_PZ_ChangeOutputVoltageControlSourceParams(hDevice);
            Example_PZ_ChangeOutputWaveformParams(hDevice);
            Example_PZ_ChangePosition(hDevice);
            Example_PZ_ChangePositionControlMode(hDevice);
            Example_PZ_ChangePositionLoopParams(hDevice);
            Example_PZ_ChangeSlewRateParams(hDevice);
            Example_PZIM_ChangeAbnormalMoveDetectionParams(hDevice);
			Example_PZIM_ChangeAmplifierOutputParams(hDevice);
            Example_PZIM_ChangeClosedLoopMoveParams(hDevice);
            Example_PZIM_ChangeClosedLoopParams(hDevice);
            Example_PZIM_ChangeEthernetParams(hDevice);
			Example_PZIM_ChangeExternalTriggerConfig(hDevice);
			Example_PZIM_ChangeExternalTriggerParams(hDevice);
            Example_PZIM_ChangeJogParams(hDevice);
            Example_PZIM_ChangeOpenLoopMoveParams(hDevice);

            Example_GetAdcInputs(hDevice);
            Example_GetAllSettings(hDevice);
            Example_GetAllSettingsAsString(hDevice);
            Example_GetAllStatus(hDevice);
            Example_GetApiVersion();
            Example_GetCalibrationState(hDevice);
            Example_GetConnectedProductsSupported(hDevice);
            Example_GetDeviceInfo(hDevice);
            Example_GetDeviceList();
            Example_GetDigitalInputStates(hDevice);
            Example_GetEncoderCounter(hDevice);
            Example_GetFirmwareVersionInfo(hDevice);
            Example_GetHardwareInfo(hDevice);
            Example_GetIoConfigurationNumberOfPortsSupported(hDevice);
            Example_GetPositionCounter(hDevice);
            Example_GetRackBayOccupiedState(hDevice);
            Example_GetSetting(hDevice);
            Example_GetStatus(hDevice);
            Example_GetStepperStatus(hDevice);
            Example_GetUniversalStatus(hDevice);
            Example_GetUmcStatus(hDevice);
            Example_GetUniversalStatusBits(hDevice);
            Example_PZ_GetMaxTravel(hDevice);
            Example_PZ_GetStatus(hDevice);
            Example_PZIM_GetCurrentPosition(hDevice);
            Example_PZIM_GetStatus(hDevice);
            Example_PZIM_GetTriggerTargetPosition(hDevice);

            Example_SetEncoderCounter(hDevice);
            Example_SetEndOfMoveMessagesMode(hDevice);
            Example_SetPositionCounter(hDevice);
            Example_SetSetting(hDevice);
            Example_SetSettingsFromString(hDevice);
            Example_SetStatusMode(hDevice);
            Example_PZ_SetOutputWaveformLookupTableSample(hDevice);
            Example_PZ_SetZero(hDevice);


            Example_ActivateCalibration(hDevice);
            Example_DeactivateCalibration(hDevice); Example_Disconnect(hDevice);
            Example_Home(hDevice);
            Example_Identify(hDevice);
            Example_LoadParams(hDevice);
            Example_MoveAbsolute(hDevice);
            Example_MoveContinuous(hDevice);
            Example_MoveJog(hDevice);
            Example_MoveRelative(hDevice);
            Example_MoveSyncArray(hDevice);
            Example_MoveSyncParams(hDevice);
            Example_MoveSyncStart(hDevice);
            Example_PersistParams(hDevice);
            Example_RackIdentify(hDevice);
            Example_RestoreFactoryDefaults(hDevice);
            Example_SendNoFlashProgramming(hDevice);
            Example_SendYesFlashProgramming(hDevice);
            Example_Stop(hDevice);
            Example_PZ_StartOutputWaveform(hDevice);
            Example_PZ_StopOutputWaveform(hDevice);
            Example_PZIM_PulseParaAcquire(hDevice);

            Example_RegisterLoggingHandler();
            Example_UnregisterLoggingHandler();
            Example_WritingRawPackets(hDevice);
            Example_ReadingRawPackets(hDevice);
            Example_ReceivingNotifications(hDevice);
            Example_UnitConverter(hDevice);

            TLMC_Close(hDevice);
        }

        TLMC_Shutdown();
    }

    return 0;
}

void Example_ChangeAnalogMonitorConfigurationParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_AnalogMonitorConfigurationParams params;

    if (TLMC_GetAnalogMonitorConfigurationParams(hDevice, TLMC_AnalogueMonitorNumber_1, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.motorChannel = TLMC_AnalogMonitorMotorChannel_1;
        params.offset = 0;
        params.scale = 10000;
        params.systemVariable = TLMC_AnalogMonitorSystemVariable_PositionError;

        if (TLMC_SetAnalogMonitorConfigurationParams(hDevice, TLMC_AnalogueMonitorNumber_1, &params) == TLMC_Success)
        {
            // The new analog monitor parameters for the monitor number one have been sent to the controller
        }
    }
}

void Example_ChangeAuxIoPortMode(const TLMC_DeviceHandle hDevice)
{
    TLMC_AuxIoPortMode_Type mode;

    if (TLMC_GetAuxIoPortMode(hDevice, TLMC_AuxIoPortNumber_Port1, &mode, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The current auxiliary I/O port mode was read from the controller and
        // copied to 'mode'

        mode = TLMC_AuxIoPortMode_SoftwareControlled;

        if (TLMC_SetAuxIoPortMode(hDevice, TLMC_AuxIoPortNumber_Port1, mode) == TLMC_Success)
        {
            // The new auxiliary I/O port mode has been sent to the controller
        }
    }
}

void Example_ChangeAuxIoSoftwareStates(const TLMC_DeviceHandle hDevice)
{
    uint16_t softwareStates;

    if (TLMC_GetAuxIoSoftwareStates(hDevice, &softwareStates, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The current auxiliary I/O software states were read from the controller
        // and copied to 'softwareStates'

        softwareStates = 0x0003;

        if (TLMC_SetAuxIoSoftwareStates(hDevice, softwareStates) == TLMC_Success)
        {
            // The new auxiliary I/O software states have been sent to the controller
        }
    }
}

void Example_ChangeBowIndex(const TLMC_DeviceHandle hDevice)
{
    TLMC_BowIndex_Type bowIndex;

    if (TLMC_GetBowIndex(hDevice, &bowIndex, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The bow index was read from the controller and copied to bowIndex

        if (TLMC_GetBowIndex(hDevice, &bowIndex, TLMC_NoWait) == TLMC_Success)
        {
            // The bow index previously retrieved from the controller has been copied
            // to bowIndex
        }
    }

    if (TLMC_SetBowIndex(hDevice, TLMC_BowIndex_Trapezoidal) == TLMC_Success)
    {
        // A request to set the bow index to the value specified has been sent to the
        // controller
    }
}

void Example_ChangeButtonParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_ButtonParams params;

    if (TLMC_GetButtonParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.buttonMode = TLMC_ButtonMode_PresetPosition;
        params.position1 = 0;
        params.position2 = 100;
        params.timeout1Milliseconds = 2000;
        params.timeout2Milliseconds = 2001;

        if (TLMC_SetButtonParams(hDevice, &params) == TLMC_Success)
        {
            // The new button parameters have been sent to the controller
        }
    }
}
void Example_ChangeConnectedProductInfo(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_ConnectedProductInfo productInfo;

    if (TLMC_GetConnectedProductInfo(hDevice, &productInfo) == TLMC_Success)
    {
        productInfo.productName[0] = 'A';
        productInfo.productName[1] = 'B';
        productInfo.productName[2] = 'C';
        productInfo.productName[3] = '\0';
        productInfo.axisType = TLMC_ConnectedProductAxisType_Single;
        productInfo.movementType = TLMC_ConnectedProductMovementType_Linear;
        productInfo.unitType = TLMC_Unit_Millimetres;
        productInfo.distanceScaleFactor = 19197;
        productInfo.velocityScaleFactor = 429417;
        productInfo.accelerationScaleFactor = 147;
        productInfo.minPosition = 0.5;
        productInfo.maxPosition = 3;
        productInfo.maxVelocity = 2;
        productInfo.maxAcceleration = 2;

        if (TLMC_SetConnectedProductInfo(hDevice, &productInfo) == TLMC_Success)
        {
            // The new connected product information have been set
        }
    }
}

void Example_ChangeCurrentLoopParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_CurrentLoopParams params;

    if (TLMC_GetCurrentLoopParams(hDevice, TLMC_CurrentLoopScenario_Settled, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.feedForward = 500;
        params.integral = 80;
        params.integralDeadBand = 0;
        params.integralLimit = 32767;
        params.phase = TLMC_CurrentLoopPhase_AB;
        params.proportional = 20;
        params.scalingFactor = 1.0f;

        if (TLMC_SetCurrentLoopParams(hDevice, TLMC_CurrentLoopScenario_Settled, &params) == TLMC_Success)
        {
            // The new current loop parameters for the settled scenario have been sent to the controller
        }
    }
}

void Example_ChangeDcPidParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_DcPidParams params;

    if (TLMC_GetDcPidParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.proportional = 850;
        params.integral = 150;
        params.derivative = 2720;
        params.integralLimit = 50;
        params.filterControl = TLMC_DcPidUpdateFilter_All;

        if (TLMC_SetDcPidParams(hDevice, &params) == TLMC_Success)
        {
            // The new DC PID parameters have been sent to the controller
        }
    }
}

void Example_ChangeDigitalOutputStates(const TLMC_DeviceHandle hDevice)
{
    TLMC_DigitalOutput_Type digitalOutputStates;

    if (TLMC_GetDigitalOutputStates(hDevice, &digitalOutputStates, TLMC_InfiniteWait) == TLMC_Success)
    {
        digitalOutputStates = TLMC_DigitalOutput_None;

        if (TLMC_SetDigitalOutputStates(hDevice, digitalOutputStates) == TLMC_Success)
        {
            // The new digital output states have been sent to the controller
        }
    }
}

void Example_ChangeEnableState(const TLMC_DeviceHandle hDevice)
{
    {
        TLMC_EnableState_Type enableState;

        if (TLMC_GetEnableState(hDevice, &enableState, TLMC_InfiniteWait) == TLMC_Success)
        {
            // The enable state has been read from the controller
        }
    }

    if (TLMC_SetEnableState(hDevice, TLMC_Enabled, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The controller enable state is 'enabled'
    }
}

void Example_ChangeGeneralMoveParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_GeneralMoveParams params;

    if (TLMC_GetGeneralMoveParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.backlashDistance = 1920;

        if (TLMC_SetGeneralMoveParams(hDevice, &params) == TLMC_Success)
        {
            // The new general move parameters have been sent to the controller
        }
    }
}

void Example_ChangeHomeParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_HomeParams params;

    if (TLMC_GetHomeParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.direction = TLMC_HomeDirection_Reverse;
        params.limitSwitch = TLMC_HomeLimitSwitch_Reverse;
        params.velocity = 428997;
        params.offsetDistance = 7678;

        if (TLMC_SetHomeParams(hDevice, &params) == TLMC_Success)
        {
            // The new homing parameters have been sent to the controller
        }
    }
}

void Example_ChangeIoConfigurationParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_IoConfigurationParams params;
    const TLMC_IoPortNumber_Type portNumber = TLMC_IoPortNumber_Port1;

    if (TLMC_GetIoConfigurationParams(hDevice, portNumber, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.mode = TLMC_IoPortMode_DigitalOutput;
        params.triggerOutSource = TLMC_IoPortSource_Channel1;

        if (TLMC_SetIoConfigurationParams(hDevice, portNumber, &params) == TLMC_Success)
        {
            // The new I/O configuration parameters have been sent to the controller
        }
    }
}

void Example_ChangeIoPositionTriggerEnableState(const TLMC_DeviceHandle hDevice)
{
    {
        TLMC_IoPositionTriggerEnableState_Type state;

        if (TLMC_GetIoPositionTriggerEnableState(hDevice, &state, TLMC_InfiniteWait) == TLMC_Success)
        {
            // The position trigger enable state has been read from the controller
        }
    }

    if (TLMC_SetIoPositionTriggerEnableState(hDevice, TLMC_IoPositionTriggerEnableState_Armed, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The position trigger enable state is 'enabled'
    }
}

void Example_ChangeIoTriggerParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_IoTriggerParams params;

    if (TLMC_GetIoTriggerParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.triggerInMode = TLMC_IoTriggerInMode_TriggersAbsoluteMove;
        params.triggerInPolarity = TLMC_IoTriggerPolarity_ActiveIsLogicHigh;
        params.triggerInSource = TLMC_IoTriggerInSource_Io1;
        params.triggerOutMode = TLMC_IoTriggerOutMode_ActiveDuringMotion;
        params.triggerOutPolarity = TLMC_IoTriggerPolarity_ActiveIsLogicHigh;
        params.triggerOutForwardStartPosition = 0;
        params.triggerOutForwardInterval = 0;
        params.triggerOutForwardNumberOfPulses = 0;
        params.triggerOutReverseStartPosition = 0;
        params.triggerOutReverseInterval = 0;
        params.triggerOutReverseNumberOfPulses = 0;
        params.triggerOutPulseWidth = 0;
        params.triggerOutNumberOfCycles = 0;

        if (TLMC_SetIoTriggerParams(hDevice, &params) == TLMC_Success)
        {
            // The new I/O trigger parameters have been sent to the controller
        }
    }
}

void Example_ChangeJogParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_JogParams params;

    if (TLMC_GetJogParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.mode = TLMC_JogMode_Continuous;
        params.stepSize = 19196;
        params.acceleration = 219;
        params.maxVelocity = 643495;
        params.stopMode = TLMC_JogStopMode_Immediate;

        if (TLMC_SetJogParams(hDevice, &params) == TLMC_Success)
        {
            // The new jog parameters have been sent to the controller
        }
    }
}

void Example_ChangeJoystickParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_JoystickParams params;

    if (TLMC_GetJoystickParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.lowGearMaxVelocity = 13421;
        params.highGearMaxVelocity = 134217;
        params.lowGearAcceleration = 1374;
        params.highGearAcceleration = 68;
        params.directionSense = TLMC_JoystickDirectionSense_Positive;

        if (TLMC_SetJoystickParams(hDevice, &params) == TLMC_Success)
        {
            // The new joystick parameters have been sent to the controller
        }
    }
}

void Example_ChangeKcubeIoTriggerParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_KcubeIoTriggerParams params;

    if (TLMC_GetKcubeIoTriggerParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.trigger1Mode = TLMC_KcubeIoTriggerMode_GeneralPurposeInput;
        params.trigger1Polarity = TLMC_KcubeIoTriggerPolarity_ActiveIsLogicHigh;
        params.trigger2Mode = TLMC_KcubeIoTriggerMode_GeneralPurposeOutput;
        params.trigger2Polarity = TLMC_KcubeIoTriggerPolarity_ActiveIsLogicHigh;

        if (TLMC_SetKcubeIoTriggerParams(hDevice, &params) == TLMC_Success)
        {
            // The new K-Cube trigger I/O parameters have been sent to the controller
        }
    }
}

void Example_ChangeKcubeMmiLockState(const TLMC_DeviceHandle hDevice)
{
    TLMC_KcubeMmiLockState_Type lockState = TLMC_KcubeMmiLockState_Locked;

    if (TLMC_GetKcubeMmiLockState(hDevice, &lockState, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The MMI lock state has been loaded from the controller and copied to the
        // lockState variable.

        if (TLMC_GetKcubeMmiLockState(hDevice, &lockState, TLMC_NoWait) == TLMC_Success)
        {
            // The MMI lock state has been loaded from the controller and copied to the
            // lockState variable.
        }

        TLMC_KcubeMmiLockState_Type lockState = TLMC_KcubeMmiLockState_Locked;

        if (TLMC_SetKcubeMmiLockState(hDevice, lockState) == TLMC_Success)
        {
            // The MMI lock state has been sent to the controller.
        }
    }
}

void Example_ChangeKcubeMmiParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_KcubeMmiParams params;

    if (TLMC_GetKcubeMmiParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.joystickMode = TLMC_KcubeMmiJoystickMode_ControlsVelocity;
        params.joystickMaxVelocity = 966187;
        params.joystickAcceleration = 131;
        params.joystickDirectionSense = TLMC_KcubeMmiJoystickDirectionSense_Normal;
        params.presetPosition1 = 0;
        params.presetPosition2 = 0;
        params.displayBrightness = 60;
        params.displayTimeout = 10;
        params.displayDimLevel = 2;
        params.presetPosition3 = 0;
        params.joystickSensitivity = 0;

        if (TLMC_SetKcubeMmiParams(hDevice, &params) == TLMC_Success)
        {
            // The new K-Cube MMI parameters have been sent to the controller
        }
    }
}

void Example_ChangeKcubePositionTriggerParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_KcubePositionTriggerParams params;

    if (TLMC_GetKcubePositionTriggerParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.forwardStartPosition = 0;
        params.forwardInterval = 0;
        params.forwardNumberOfPulses = 0;
        params.reverseStartPosition = 0;
        params.reverseInterval = 0;
        params.reverseNumberOfPulses = 0;
        params.pulseWidth = 100000;
        params.numberOfCycles = 0;

        if (TLMC_SetKcubePositionTriggerParams(hDevice, &params) == TLMC_Success)
        {
            // The new K-Cube position trigger parameters have been sent to the controller
        }
    }
}

void Example_ChangeLcdDisplayParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_LcdDisplayParams params;

    if (TLMC_GetLcdDisplayParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.displayBrightness = 100;
        params.displayDimLevel = 33;
        params.displayTimeout = 8;
        params.knobSensitivity = 32767;

        if (TLMC_SetLcdDisplayParams(hDevice, &params) == TLMC_Success)
        {
            // The new LCD display parameters have been sent to the controller
        }
    }
}

void Example_ChangeLcdMoveParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_LcdMoveParams params;

    if (TLMC_GetLcdMoveParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.acceleration = 13744;
        params.jogStepSize = 60000;
        params.jogStopMode = TLMC_JogStopMode_Immediate;
        params.knobMode = TLMC_LcdKnobMode_Velocity;
        params.maxVelocity = 6710886;
        params.presetPosition[0] = 600000;

        if (TLMC_SetLcdMoveParams(hDevice, &params) == TLMC_Success)
        {
            // The new LCD move parameters have been sent to the controller
        }
    }
}

void Example_ChangeLimitSwitchParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_LimitSwitchParams params;

    if (TLMC_GetLimitSwitchParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.clockwiseHardLimitOperatingMode = TLMC_HardLimitOperatingMode_SwitchContactMakesWhenHoming;
        params.counterclockwiseHardLimitOperatingMode = TLMC_HardLimitOperatingMode_SwitchIgnored;
        params.clockwiseSoftLimit = 1073741824;
        params.counterclockwiseSoftLimit = -1073741824;
        params.softLimitOperatingMode = TLMC_SoftLimitOperatingMode_Ignored;

        if (TLMC_SetLimitSwitchParams(hDevice, &params) == TLMC_Success)
        {
            // The new limit switch parameters have been sent to the controller
        }
    }
}

void Example_ChangeMotorOutputParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_MotorOutputParams params;

    if (TLMC_GetMotorOutputParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.continuousCurrentLimit = 22937;
        params.energyLimit = 19660;
        params.motorLimit = 32767;

        if (TLMC_SetMotorOutputParams(hDevice, &params) == TLMC_Success)
        {
            // The new motor output parameters have been sent to the controller
        }
    }
}

void Example_ChangeMoveAbsoluteParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_MoveAbsoluteParams params;

    if (TLMC_GetMoveAbsoluteParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.absolutePosition = 86383;

        if (TLMC_SetMoveAbsoluteParams(hDevice, &params) == TLMC_Success)
        {
            // The new move absolute parameters have been sent to the controller
        }
    }
}

void Example_ChangeMoveRelativeParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_MoveRelativeParams params;

    if (TLMC_GetMoveRelativeParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.relativeDistance = 19196;

        if (TLMC_SetMoveRelativeParams(hDevice, &params) == TLMC_Success)
        {
            // The new move relative parameters have been sent to the controller
        }
    }
}

void Example_ChangePositionLoopParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PositionLoopParams params;

    if (TLMC_GetPositionLoopParams(hDevice, TLMC_PositionLoopScenario_Stationary, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.proportional = 2400;
        params.integral = 1800;
        params.integralLimit = 32767;
        params.derivative = 4500;
        params.servoCycles = 6;
        params.scale = 4000;
        params.velocityFeedForward = 0;
        params.accelerationFeedForward = 0;
        params.errorLimit = 6553;

        if (TLMC_SetPositionLoopParams(hDevice, TLMC_PositionLoopScenario_Stationary, &params) == TLMC_Success)
        {
            // The new position loop parameters have been sent to the controller
        }
    }
}

void Example_ChangePotentiometerParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PotentiometerParams params;

    if (TLMC_GetPotentiometerParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.deflection0 = 10;
        params.velocity1 = 10290;

        if (TLMC_SetPotentiometerParams(hDevice, &params) == TLMC_Success)
        {
            // The new potentiometer parameters have been sent to the controller
        }
    }
}

void Example_ChangePowerParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PowerParams powerParams;

    if (TLMC_GetPowerParams(hDevice, &powerParams, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The power params were retrieved from the controller and copied to powerParams.

        if (TLMC_GetPowerParams(hDevice, &powerParams, TLMC_NoWait) == TLMC_Success)
        {
            // The power params previously retrieved from the controller have been copied
            // to powerParams.
        }

        struct TLMC_PowerParams powerParams;

        powerParams.moveFactor = 6;
        powerParams.restFactor = 1;

        if (TLMC_SetPowerParams(hDevice, &powerParams) == TLMC_Success)
        {
            // The power params were set to the controller.
        }
    }
}

void Example_ChangePresetConnectedProduct(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_SetConnectedProduct(hDevice, "PRM1Z8") == TLMC_Success)
    {
        //The connected product has been set using the values for the PRM1Z8 product
    }
}

void Example_ChangeProfileModeParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_ProfileModeParams params;

    if (TLMC_GetProfileModeParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.mode = TLMC_ProfileMode_Trapezoidal;
        params.jerk = 922233;

        if (TLMC_SetProfileModeParams(hDevice, &params) == TLMC_Success)
        {
            // The new profile mode parameters have been sent to the controller
        }
    }
}

void Example_ChangeStageAxisParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_StageAxisParams params;

    if (TLMC_GetStageAxisParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.minPosition = 0;
        params.maxPosition = 100000;

        if (TLMC_SetStageAxisParams(hDevice, &params) == TLMC_Success)
        {
            // The new stage axis parameters have been sent to the controller
        }
    }
}

void Example_ChangeStepperLoopParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_StepperLoopParams stepperLoopParams;

    if (TLMC_GetStepperLoopParams(hDevice, &stepperLoopParams, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The StepperLoopParams have been retrieved from the controller.

        stepperLoopParams.outputClip = 50000;
        stepperLoopParams.outputTolerance = 1000;
        stepperLoopParams.differential = 10000;
        stepperLoopParams.integral = 10000;
        stepperLoopParams.loopMode = TLMC_StepperLoopMode_Closed;
        stepperLoopParams.proportional = 10000;

        if (TLMC_SetStepperLoopParams(hDevice, &stepperLoopParams) == TLMC_Success)
        {
            // StepperLoopParams data has been set to the controller.
        }
    }
}

void Example_ChangeTrackSettleParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_TrackSettleParams params;

    if (TLMC_GetTrackSettleParams(hDevice, &params, TLMC_NoWait) == TLMC_Success)
    {
        params.settleTime = 197;
        params.settleWindow = 4;
        params.trackWindow = 0;

        if (TLMC_SetTrackSettleParams(hDevice, &params) == TLMC_Success)
        {
            // The new track settle parameters have been sent to the controller
        }
    }
}

void Example_ChangeTriggerParamsForDcBrushless(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_TriggerParamsForDcBrushless params;

    if (TLMC_GetTriggerParamsForDcBrushless(hDevice, &params, TLMC_NoWait) == TLMC_Success)
    {
        params.modes = TLMC_TriggerModesForDcBrushless_InputActiveIsLogicHigh | TLMC_TriggerModesForDcBrushless_InputTriggersHomeMove;

        if (TLMC_SetTriggerParamsForDcBrushless(hDevice, &params) == TLMC_Success)
        {
            // The new trigger parameters have been sent to the DC brushless controller
        }
    }
}

void Example_ChangeTriggerParamsForStepper(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_TriggerParamsForStepper triggerParamsForStepper;

    if (TLMC_GetTriggerParamsForStepper(hDevice, &triggerParamsForStepper, TLMC_InfiniteWait) == TLMC_Success)
    {
        // Stepper trigger params have been loaded from the controller
    }

    if (TLMC_SetTriggerParamsForStepper(hDevice, &triggerParamsForStepper) == TLMC_Success)
    {
        // Stepper trigger params have been set to the controller
    }
}

void Example_ChangeVelocityParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_VelocityParams params;

    if (TLMC_GetVelocityParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.minVelocity = 0;
        params.acceleration = 146;
        params.maxVelocity = 428997;

        if (TLMC_SetVelocityParams(hDevice, &params) == TLMC_Success)
        {
            // The new velocity parameters have been sent to the controller
        }
    }
}

void Example_PZ_ChangeKpcIoSettingsParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZ_KpcIoSettingsParams params;

    if (TLMC_PZ_GetKpcIoSettingsParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.analogInputSource = TLMC_PZ_KpcAnalogInputSource_HubInputA;
        params.filterCutOffFrequency = 40;
        params.forceSense = 50;
        params.strainGaugeOption = TLMC_PZ_KpcStrainGaugeOption_Position;
        params.voltageLimit = 75;
        params.voltageRange = TLMC_PZ_KpcVoltageRange_75Volts;

        if (TLMC_PZ_SetKpcIoSettingsParams(hDevice, &params) == TLMC_Success)
        {
            // The new KPC I/O settings parameters have been sent to the controller
        }
    }
}

void Example_PZ_ChangeKpcIoTriggerParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZ_KpcIoTriggerParams params;

    if (TLMC_PZ_GetKpcIoTriggerParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.trigger1Mode = TLMC_PZ_KpcIoTriggerMode_GeneralPurposeInput;
        params.trigger1Polarity = TLMC_KcubeIoTriggerPolarity_ActiveIsLogicHigh;
        params.trigger2Mode = TLMC_PZ_KpcIoTriggerMode_GeneralPurposeOutput;
        params.trigger2Polarity = TLMC_KcubeIoTriggerPolarity_ActiveIsLogicHigh;
        params.monitorFilterCutOffFrequency = 20;
        params.monitorOutputMode = TLMC_PZ_KpcMonitorOutputMode_HighVoltage;
        params.monitorOutputSoftwareValue = 20;
        params.strainGaugeLowerLimit = 200;
        params.strainGaugeUpperLimit = 800;
        params.smoothingSamples = 15;

        if (TLMC_PZ_SetKpcIoTriggerParams(hDevice, &params) == TLMC_Success)
        {
            // The new KPC trigger I/O parameters have been sent to the controller
        }
    }
}

void Example_PZ_ChangeKpcMmiParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZ_KpcMmiParams params;

    if (TLMC_PZ_GetKpcMmiParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.joystickMode = TLMC_PZ_KpcMmiJoystickMode_Jogs;
        params.joystickGear = TLMC_KcubeMmiJoystickGear_High;
        params.joystickPositionStepSize = 40;
        params.joystickVoltageStepSize = 20;
        params.joystickDirectionSense = TLMC_PZ_KpcMmiJoystickDirectionSense_Normal;
        params.presetPosition1 = 20;
        params.presetPosition2 = 40;
        params.presetVoltage1 = 10;
        params.presetVoltage2 = 50;
        params.displayBrightness = 60;
        params.displayTimeout = 10;
        params.displayDimLevel = 2;

        if (TLMC_PZ_SetKpcMmiParams(hDevice, &params) == TLMC_Success)
        {
            // The new KPC MMI parameters have been sent to the controller
        }
    }
}

void Example_PZ_ChangeMaxOutputVoltageParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZ_MaxOutputVoltageParams params;

    if (TLMC_PZ_GetMaxOutputVoltageParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        uint16_t maxOutputVoltage = 74;

        if (TLMC_PZ_SetMaxOutputVoltage(hDevice, maxOutputVoltage) == TLMC_Success)
        {
            // The new maximum output voltage been sent to the controller
        }
    }
}

void Example_PZ_ChangeOutputVoltage(const TLMC_DeviceHandle hDevice)
{
    int16_t outputVoltage;

    if (TLMC_PZ_GetOutputVoltage(hDevice, &outputVoltage, TLMC_InfiniteWait) == TLMC_Success)
    {
        outputVoltage = 0;

        if (TLMC_PZ_SetOutputVoltage(hDevice, outputVoltage) == TLMC_Success)
        {
            // The new output voltage been sent to the controller
        }
    }
}

void Example_PZ_ChangeOutputVoltageControlSourceParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZ_OutputVoltageControlSourceParams outputVoltageControlSourceParams;

    if (TLMC_PZ_GetOutputVoltageControlSourceParams(hDevice, &outputVoltageControlSourceParams, TLMC_InfiniteWait) == TLMC_Success)
    {
        outputVoltageControlSourceParams.source = TLMC_PZ_OutputVoltageControlSource_SoftwareOnly;

        if (TLMC_PZ_SetOutputVoltageControlSourceParams(hDevice, &outputVoltageControlSourceParams) == TLMC_Success)
        {
            // The new output voltage control source parameters have been sent to the controller
        }
    }
}

void Example_PZ_ChangeOutputWaveformParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZ_OutputWaveformParams params;

    if (TLMC_PZ_GetOutputWaveformParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.interSampleDelay = 10;
        params.mode = TLMC_PZ_OutputWaveformOperatingMode_Continuous;
        params.numberOfCycles = 0;
        params.numberOfSamplesBetweenTriggerRepetition = 10;
        params.numberOfSamplesPerCycle = 500;
        params.outputTriggerStartIndex = 0;
        params.outputTriggerWidth = 0;
        params.postCycleDelay = 0;
        params.preCycleDelay = 0;

        if (TLMC_PZ_SetOutputWaveformParams(hDevice, &params) == TLMC_Success)
        {
            // The new output waveform parameters have been sent to the controller
        }
    }
}

void Example_PZ_ChangePosition(const TLMC_DeviceHandle hDevice)
{
    int16_t position;

    if (TLMC_PZ_GetPosition(hDevice, &position, TLMC_InfiniteWait) == TLMC_Success)
    {
        position = 0;

        if (TLMC_PZ_SetPosition(hDevice, position) == TLMC_Success)
        {
            // The new position been sent to the controller
        }
    }
}

void Example_PZ_ChangePositionControlMode(const TLMC_DeviceHandle hDevice)
{
    TLMC_PZ_PositionControlMode_Type positionControlMode;

    if (TLMC_PZ_GetPositionControlMode(hDevice, &positionControlMode, TLMC_InfiniteWait) == TLMC_Success)
    {
        positionControlMode = TLMC_PZ_PositionControlMode_OpenLoop;

        if (TLMC_PZ_SetPositionControlMode(hDevice, positionControlMode, TLMC_InfiniteWait) == TLMC_Success)
        {
            // The new position control mode been sent to the controller
        }
    }
}

void Example_PZ_ChangePositionLoopParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZ_PositionLoopParams params;

    if (TLMC_PZ_GetPositionLoopParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.integral = 100;
        params.proportional = 100;

        if (TLMC_PZ_SetPositionLoopParams(hDevice, &params) == TLMC_Success)
        {
            // The new position loop params been sent to the controller
        }
    }
}

void Example_PZ_ChangeSlewRateParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZ_SlewRateParams params;

    if (TLMC_PZ_GetSlewRateParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.closedLoopSlewRate = 200;
        params.openLoopSlewRate = 200;

        if (TLMC_PZ_SetSlewRateParams(hDevice, &params) == TLMC_Success)
        {
            // The new slew rate params been sent to the controller
        }
    }
}

void Example_PZIM_ChangeAbnormalMoveDetectionParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZIM_AbnormalMoveDetectionParams params;

    if (TLMC_PZIM_GetAbnormalMoveDetectionParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        if (params.state == TLMC_PZIM_AbnormalMoveDetectionState_Disabled)
        {
            params.state = TLMC_PZIM_AbnormalMoveDetectionState_Enabled;
        }
        else
        {
            params.state = TLMC_PZIM_AbnormalMoveDetectionState_Disabled;
        }

        if (TLMC_PZIM_SetAbnormalMoveDetectionParams(hDevice, &params) == TLMC_Success)
        {
            // The new abnormal move detection parameters have been sent to the controller
        }
    }
}

void Example_PZIM_ChangeAmplifierOutputParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZIM_AmplifierOutputParams params;

    if (TLMC_PZIM_GetAmplifierOutputParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.forwardAmplifierLevel -= 1;

        if (TLMC_PZIM_SetAmplifierOutputParams(hDevice, &params) == TLMC_Success)
        {
            // The new amplifier output parameters have been sent to the controller
        }
    }
}

void Example_PZIM_ChangeClosedLoopMoveParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZIM_ClosedLoopMoveParams params;

    if (TLMC_PZIM_GetClosedLoopMoveParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.desiredPosition -= 1;

        if (TLMC_PZIM_SetClosedLoopMoveParams(hDevice, &params) == TLMC_Success)
        {
            // The new closed loop move parameters have been sent to the controller
        }
    }
}

void Example_PZIM_ChangeClosedLoopParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZIM_ClosedLoopParams params;

    if (TLMC_PZIM_GetClosedLoopParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.referenceSpeed -= 1;

        if (TLMC_PZIM_SetClosedLoopParams(hDevice, &params) == TLMC_Success)
        {
            // The new closed loop parameters have been sent to the controller
        }
    }
}

void Example_PZIM_ChangeEthernetParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZIM_EthernetParams params;
    if (TLMC_PZIM_GetEthernetParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        if (params.ipAddressAssignmentMode == TLMC_PZIM_IpAddressAssignmentMode_FromDHCP)
        {
            params.ipAddressAssignmentMode = TLMC_PZIM_IpAddressAssignmentMode_FromParameters;
        }
        else
        {
            params.ipAddressAssignmentMode = TLMC_PZIM_IpAddressAssignmentMode_FromDHCP;
        }
        if (TLMC_PZIM_SetEthernetParams(hDevice, &params) == TLMC_Success)
        {
            // The new ethernet parameters have been sent to the controller
        }
    }
}

void Example_PZIM_ChangeExternalTriggerConfig(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZIM_ExternalTriggerConfig externalTriggerConfig;
	if (TLMC_PZIM_GetExternalTriggerConfig(hDevice, &externalTriggerConfig, TLMC_InfiniteWait) == TLMC_Success)
	{
        externalTriggerConfig.mode = TLMC_PZIM_ExternalTriggerMode_AnalogInWithRisingTriggerEdge;
        if (TLMC_PZIM_SetExternalTriggerConfig(hDevice, &externalTriggerConfig) == TLMC_Success)
        {
            // The new external trigger config has been sent to the controller
        }
	}
}

void Example_PZIM_ChangeExternalTriggerParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZIM_ExternalTriggerParams params;
    if (TLMC_PZIM_GetExternalTriggerParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.risingEdgeRelativeDistance += 1;
        if (TLMC_PZIM_SetExternalTriggerParams(hDevice, &params) == TLMC_Success)
        {
            // The new external trigger parameters have been sent to the controller
        }
    }
}

void Example_PZIM_ChangeJogParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZIM_JogParams params;

    if (TLMC_PZIM_GetJogParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.openLoopStepSize -= 1;

        if (TLMC_PZIM_SetJogParams(hDevice, &params) == TLMC_Success)
        {
            // The new jog parameters have been sent to the controller
        }
    }
}

void Example_PZIM_ChangeOpenLoopMoveParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZIM_OpenLoopMoveParams params;

    if (TLMC_PZIM_GetOpenLoopMoveParams(hDevice, &params, TLMC_InfiniteWait) == TLMC_Success)
    {
        params.targetStepSize -= 1;

        if (TLMC_PZIM_SetOpenLoopMoveParams(hDevice, &params) == TLMC_Success)
        {
            // The new open loop move parameters have been sent to the controller
        }
    }
}

void Example_GetAllSettings(const TLMC_DeviceHandle hDevice)
{
    // This example gets all of the available settings for the device handled by 'hDevice'

    // As with status items, there are two methods:

    // METHOD 1: Find out how many settings items there are, allocate a buffer large enough
    //           for all of them and request them with one call

    {
        uint16_t numberOfItemsAvailable;

        if (TLMC_GetSettingCount(hDevice, &numberOfItemsAvailable) == TLMC_Success) // Finds out how many settings items are available on this device
        {
            // Allocate a block of memory large enough to hold all of the settings items
            size_t memoryBlockSize = numberOfItemsAvailable * sizeof(struct TLMC_Setting);
            struct TLMC_Setting* pMemoryBlock = (struct TLMC_Setting*)malloc(memoryBlockSize);

            if (pMemoryBlock != NULL)
            {
                uint16_t numberOfItemsCopied = 0;

                // Request 'numberOfItemsAvailable' items starting at the first one (item zero).
                if ((TLMC_GetSettings(hDevice, 0, numberOfItemsAvailable, pMemoryBlock, &numberOfItemsCopied) == TLMC_Success) &&
                    (numberOfItemsCopied == numberOfItemsAvailable))
                {
                    // 'pMemoryBlock' now contains a copy of all settings items.

                    // > Process settings information here <
                }

                free(pMemoryBlock); // Don't forget to free the buffer
            }
        }
    }

    // METHOD 2: Repeatedly get a fixed number of settings items until no more are available

    {
        #define NUMBER_OF_ITEMS_PER_CALL 5
        struct TLMC_Setting settingsItems[NUMBER_OF_ITEMS_PER_CALL];
        uint16_t numberOfItemsCopied = 0;
        uint16_t sourceStartItemIndex = 0;

        // Repeatedly call TLMC_GetSettings until no more items are available
        while (TLMC_GetSettings(hDevice, sourceStartItemIndex, NUMBER_OF_ITEMS_PER_CALL, settingsItems, &numberOfItemsCopied) == TLMC_Success)
        {
            // 'settingsItems' now contains a copy of 'numberOfItemsCopied' settings items.
            // Note that 'numberOfItemsCopied' might be zero, in which case no items were copied.

            // > Process settings information here <

            if (numberOfItemsCopied < NUMBER_OF_ITEMS_PER_CALL)
            {
                break; // No more items
            }

            // Increase the 'startItemIndex' for the next call
            sourceStartItemIndex += NUMBER_OF_ITEMS_PER_CALL;
        }
    }
}

void Example_GetAllSettingsAsString(const TLMC_DeviceHandle hDevice)
{
    // This example gets all of the settings for the device handled by 'hDevice'.
    // The format returned may be any of the formats available in the TLMC_SettingStringFormats enumeration.

    {
        unsigned int charactersExpected;

        if (TLMC_GetSettingsAsString(hDevice, NULL, 0, &charactersExpected, TLMC_SettingStringFormat_Json, true) == TLMC_Success) // Obtain the buffer length required
        {
            // Create a buffer large enough to store the entire settings string (not forgetting to allow an extra element for the NULL-terminator)

            unsigned int bufferSize = charactersExpected + 1; // +1 to allow for null-termination
            char* pBuffer = (char*)malloc(bufferSize);

            if (pBuffer != NULL)
            {
                unsigned int charactersCopied;

                // We can now use our newly allocated buffer and it's length as arguments to retrieve a copy of the settings string

                if (TLMC_GetSettingsAsString(hDevice, pBuffer, bufferSize, &charactersCopied, TLMC_SettingStringFormat_Json, true) == TLMC_Success)
                {
                    // Our buffer will now contain the names of all settings provided on 'hDevice' along with their current values.

                    // > Process settings here <

                    // All strings returned by TLMC_GetSettingsAsString can be passed into the TLMC_SetSettingsFromString
                    // function. This gives you a convenient way of saving, then later restoring, a known device
                    // configuration. You could, for instance, save the text returned by TLMC_GetSettingsAsString to a
                    // file. Subquently, you could read this back in and pass it to TLMC_SetSettingsFromString to easily
                    // return the device to that state.
                }

                free(pBuffer); // Don't forget to free the buffer
            }
        }
    }
}

void Example_GetAllStatus(const TLMC_DeviceHandle hDevice)
{
    // This example gets all of the available status for the device handled by 'hDevice'

    // As with settings items, there are two methods:

    // METHOD 1: Find out how many status items there are, allocate a buffer large enough
    //           for all of them and request them with one call

    {
        uint16_t numberOfItemsAvailable;

        if (TLMC_GetStatusItemCount(hDevice, &numberOfItemsAvailable) == TLMC_Success) // Finds out how many status items are available on this device
        {
            // Allocate a block of memory large enough to hold all of the status items
            size_t memoryBlockSize = numberOfItemsAvailable * sizeof(struct TLMC_StatusItem);
            struct TLMC_StatusItem* pMemoryBlock = (struct TLMC_StatusItem*)malloc(memoryBlockSize);

            if (pMemoryBlock != NULL)
            {
                uint16_t numberOfItemsCopied = 0;

                // Request 'numberOfItemsAvailable' items starting at the first one (item zero).
                if ((TLMC_GetStatusItems(hDevice, 0, numberOfItemsAvailable, pMemoryBlock, &numberOfItemsCopied) == TLMC_Success) &&
                    (numberOfItemsCopied == numberOfItemsAvailable))
                {
                    // 'pMemoryBlock' now contains a copy of all status items

                    // > Process status items here <
                }

                free(pMemoryBlock); // Don't forget to free the buffer
            }
        }
    }

    // METHOD 2: Repeatedly get a fixed number of status items until no more are available

    {
        #define NUMBER_OF_ITEMS_PER_CALL 5
        struct TLMC_StatusItem statusItems[NUMBER_OF_ITEMS_PER_CALL];
        uint16_t numberOfItemsCopied = 0;
        uint16_t sourceStartItemIndex = 0;

        // Repeatedly call TLMC_GetStatusItems until no more items are available
        while (TLMC_GetStatusItems(hDevice, sourceStartItemIndex, NUMBER_OF_ITEMS_PER_CALL, statusItems, &numberOfItemsCopied) == TLMC_Success)
        {
            // 'statusItems' now contains a copy of 'numberOfItemsCopied' status items.
            // Note that 'numberOfItemsCopied' might be zero, in which case no items were copied.

            // > Process status items here <

            if (numberOfItemsCopied < NUMBER_OF_ITEMS_PER_CALL)
            {
                break; // No more items
            }

            // Increase the 'startItemIndex' for the next call
            sourceStartItemIndex += NUMBER_OF_ITEMS_PER_CALL;
        }
    }
}

void Example_GetAdcInputs(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_AdcInputs state;

    if (TLMC_GetAdcInputs(hDevice, &state, TLMC_InfiniteWait) == TLMC_Success)
    {
        // Digital input states have been loaded from the controller
    }
}

void Example_GetApiVersion()
{
    struct TLMC_ApiVersion apiVersion;

    if (TLMC_GetApiVersion(&apiVersion) == TLMC_Success)
    {
        // Version information for the native API has been copied to the apiVersion structure
    }
}

void Example_GetCalibrationState(const TLMC_DeviceHandle hDevice)
{
    TLMC_CalibrationState_Type state;

    if (TLMC_GetCalibrationState(hDevice, &state) == TLMC_Success)
    {
        // Calibration state has been copied to the 'state' variable
    }
}

void Example_GetConnectedProductsSupported(const TLMC_DeviceHandle hDevice)
{
    // First, we find out how large our buffer needs to be to hold the entire "connected products supported" string.
    // We do this by passing in a NULL buffer to TLMC_GetConnectedProductsSupported.
    unsigned int charactersExpected;

    if (TLMC_GetConnectedProductsSupported(hDevice, NULL, 0, &charactersExpected) == TLMC_Success)
    {
        // Now we create a buffer large enough to store the string (don't forget to add one to
        // allow space for the null-terminator)

        unsigned int bufferSize = charactersExpected + 1; // +1 to allow for null-termination
        char* pBuffer = (char*)malloc(bufferSize);

        if (pBuffer != NULL)
        {
            unsigned int charactersCopied;

            if (TLMC_GetConnectedProductsSupported(hDevice, pBuffer, bufferSize, &charactersCopied) == TLMC_Success)
            {
                // The 'supportedProducts' variable now contains the list of supported product names
            }

            free(pBuffer); // Don't forget to free the buffer
        }
    }
}

void Example_GetDeviceInfo(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_DeviceInfo deviceInfo;

    if (TLMC_GetDeviceInfo(hDevice, &deviceInfo) == TLMC_Success)
    {
        // Device information has been copied to the 'deviceInfo' structure
    }
}


void Example_GetDeviceList()
{
    uint16_t deviceCount;

    if (TLMC_GetDeviceListItemCount(&deviceCount) == TLMC_Success) // Finds out how many device list entries are available
    {
        // Allocate a block of memory large enough to hold all of the items
        size_t memoryBlockSize = deviceCount * sizeof(struct TLMC_DeviceInfo);
        struct TLMC_DeviceInfo* pMemoryBlock = (struct TLMC_DeviceInfo*)malloc(memoryBlockSize);

        if (pMemoryBlock != NULL)
        {
            uint16_t numberOfItemsCopied = 0;

            // Request all items starting with the first one (index zero).
            if ((TLMC_GetDeviceListItems(0, deviceCount, pMemoryBlock, &numberOfItemsCopied) == TLMC_Success) &&
                (numberOfItemsCopied == deviceCount))
            {
                // 'pMemoryBlock' now contains a copy of all device list entries

                // > Process device list entries here <
            }

            free(pMemoryBlock); // Don't forget to free the buffer
        }
    }
}

void Example_GetDigitalInputStates(const TLMC_DeviceHandle hDevice)
{
    TLMC_DigitalInput_Type state;

    if (TLMC_GetDigitalInputStates(hDevice, &state, TLMC_InfiniteWait) == TLMC_Success)
    {
        // Digital input states have been loaded from the controller
    }
}

void Example_GetEncoderCounter(const TLMC_DeviceHandle hDevice)
{
    int32_t encoderCounter;

    if (TLMC_GetEncoderCounter(hDevice, &encoderCounter, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The encoder counter was read from the controller and copied to encoderCounter

        if (TLMC_GetEncoderCounter(hDevice, &encoderCounter, TLMC_NoWait) == TLMC_Success)
        {
            // The encoder counter previously retrieved from the controller has been copied to encoderCounter
        }
    }
}

void Example_GetFirmwareVersionInfo(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_FirmwareVersion deviceFirmwareVersion;
    struct TLMC_FirmwareVersion requiredFirmwareVersion;

    if (TLMC_GetFirmwareVersionInfo(hDevice, &deviceFirmwareVersion, &requiredFirmwareVersion) == TLMC_Success)
    {
        // Firmware information has been copied to the 'deviceFirmwareVersion' and 'requiredFirmwareVersion' structures
    }
}

void Example_GetHardwareInfo(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_HardwareInfo hardwareInfo;

    if (TLMC_GetHardwareInfo(hDevice, &hardwareInfo, TLMC_InfiniteWait) == TLMC_Success)
    {
        // Hardware information has been loaded from the controller and copied to the
        // hardwareInfo structure
    }

    if (TLMC_GetHardwareInfo(hDevice, &hardwareInfo, TLMC_NoWait) == TLMC_Success)
    {
        // The hardware information previously retrieved from the controller has been
        // copied to the hardwareInfo structure
    }
}

void Example_GetIoConfigurationNumberOfPortsSupported(const TLMC_DeviceHandle hDevice)
{
    uint8_t numberOfPorts = 0;

    if (TLMC_GetIoConfigurationNumberOfPortsSupported(hDevice, &numberOfPorts) == TLMC_Success)
    {
        // Number of ports supported has been loaded from the controller
    }
}

void Example_GetPositionCounter(const TLMC_DeviceHandle hDevice)
{
    int32_t positionCounter;

    if (TLMC_GetPositionCounter(hDevice, &positionCounter, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The position counter was read from the controller and copied to positionCounter

        if (TLMC_GetPositionCounter(hDevice, &positionCounter, TLMC_NoWait) == TLMC_Success)
        {
            // The position counter previously retrieved from the controller has been copied
            // to positionCounter
        }
    }
}

void Example_GetRackBayOccupiedState(const TLMC_DeviceHandle hDevice)
{
    TLMC_RackBayOccupiedState_Type state;
    TLMC_RackBayNumber_Type bayNumber = TLMC_RackBayNumber_1;

    if (TLMC_GetRackBayOccupiedState(hDevice, bayNumber, &state, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The rack bay occupied state has been read from the controller
    }
}

void Example_GetSetting(const TLMC_DeviceHandle hDevice)
{
    // This example gets a named setting ("home/offsetDistance") on the device handled by 'hDevice'

    struct TLMC_Setting settingItem;

    if (TLMC_GetSetting(hDevice, "home.offsetDistance", &settingItem, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The home offset distance has been reloaded from the controller and copied to the
        // settingItem variable along with the associated meta data
    }

    if (TLMC_GetSetting(hDevice, "home.offsetDistance", &settingItem, TLMC_NoWait) == TLMC_Success)
    {
        // The home offset distance previously loaded from the controller is copied to the settingItem
        // variable along with the associated meta data
    }
}

void Example_GetStatus(const TLMC_DeviceHandle hDevice)
{
    // Get the current position for the device handled by 'hDevice'
    struct TLMC_StatusItem statusItem;

    if (TLMC_GetStatusItem(hDevice, TLMC_StatusItemId_Position, &statusItem) == TLMC_Success)
    {
        // Position information has been successfully copied to the local status item

        // The members of a status item are:
        // id        - Identifies the device property this status item relates to. In this case, it
        //             will be the one we requested i.e., TLMC_StatusItemIds::TLMC_StatusItemId_Position
        // value     - A union holding the current value. Refer to the 'valueType' field to determine
        //             which union entry is correct
        // valueType - Specifies which entry in the 'value' union has the correct value.
        //             Note that the underlying storage type used by status item for a particular
        //             device property will never change i.e., Position status items will always be
        //             64-bit signed integers

        // Let's examine the position we've just retrieved to see if it's beyond 1234:

        // From previously looking at 'valueType' we know that the position value is always stored in
        // 'int64Value'. We can make a copy of that field or use it directly. Here we make a copy.
        int64_t currentPosition = statusItem.value.int64Value;

        if (currentPosition > 1234)
        {
            // User code
        }
    }
}

void Example_GetStepperStatus(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_StepperStatus stepperStatus;

    if (TLMC_GetStepperStatus(hDevice, &stepperStatus, TLMC_InfiniteWait) == TLMC_Success)
    {
        // Stepper status data has been loaded from the controller and copied to the
        // stepperStatus variable

        if (TLMC_GetStepperStatus(hDevice, &stepperStatus, TLMC_NoWait) == TLMC_Success)
        {
            // The stepper status data previously retrieved from the controller has been
            // copied to the stepperStatus variable
        }
    }
}

void Example_GetUmcStatus(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_UmcStatus umcStatus;

    if (TLMC_GetUmcStatus(hDevice, &umcStatus, TLMC_InfiniteWait) == TLMC_Success)
    {
        // UMC (Universal Motor Controller) status data has been loaded from the controller and copied to the
        // umcStatus variable
    }

    if (TLMC_GetUmcStatus(hDevice, &umcStatus, TLMC_NoWait) == TLMC_Success)
    {
        // The UMC (Universal Motor Controller) status data previously retrieved from the controller has been
        // copied to the umcStatus variable
    }
}

void Example_GetUniversalStatus(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_UniversalStatus universalStatus;

    if (TLMC_GetUniversalStatus(hDevice, &universalStatus, TLMC_InfiniteWait) == TLMC_Success)
    {
        // Universal status data has been loaded from the controller and copied to the
        // universalStatus variable
    }

    if (TLMC_GetUniversalStatus(hDevice, &universalStatus, TLMC_NoWait) == TLMC_Success)
    {
        // The universal status data previously retrieved from the controller has been
        // copied to the universalStatus variable
    }
}

void Example_GetUniversalStatusBits(const TLMC_DeviceHandle hDevice)
{
    TLMC_UniversalStatusBit_Type universalStatusBits;

    if (TLMC_GetUniversalStatusBits(hDevice, &universalStatusBits, TLMC_InfiniteWait) == TLMC_Success)
    {
        // Universal status bits have been loaded from the controller and copied to
        // universalStatusBits
    }

    if (TLMC_GetUniversalStatusBits(hDevice, &universalStatusBits, TLMC_NoWait) == TLMC_Success)
    {
        // The universal status bits previously retrieved from the controller have been
        // copied to universalStatusBits
    }
}

void Example_PZ_GetMaxTravel(const TLMC_DeviceHandle hDevice)
{
    uint16_t maxTravel;

    if (TLMC_PZ_GetMaxTravel(hDevice, &maxTravel, TLMC_InfiniteWait) == TLMC_Success)
    {
        // Piezo maximum travel was read the controller and copied to maxTravel
    }

    if (TLMC_PZ_GetMaxTravel(hDevice, &maxTravel, TLMC_NoWait) == TLMC_Success)
    {
        // The maximum travel previously retrieved from the controller has been copied
        // to maxTravel
    }
}

void Example_PZ_GetStatus(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZ_Status piezoStatus;

    if (TLMC_PZ_GetStatus(hDevice, &piezoStatus, TLMC_InfiniteWait) == TLMC_Success)
    {
        // Piezo status data has been loaded from the controller and copied to the
        // piezoStatus structure
    }

    if (TLMC_PZ_GetStatus(hDevice, &piezoStatus, TLMC_NoWait) == TLMC_Success)
    {
        // The piezo status data previously retrieved from the controller has been
        // copied to the piezoStatus structure
    }
}

void Example_PZIM_GetCurrentPosition(const TLMC_DeviceHandle hDevice)
{
    int32_t position;

    if (TLMC_PZIM_GetCurrentPosition(hDevice, &position, TLMC_InfiniteWait) == TLMC_Success)
    {
    }
}

void Example_PZIM_GetStatus(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZIM_Status piezoInertialMotorStatus;

    if (TLMC_PZIM_GetStatus(hDevice, &piezoInertialMotorStatus, TLMC_InfiniteWait) == TLMC_Success)
    {
        // Piezo inertial motor status data has been loaded from the controller and copied to the
        // piezoInertialMotorStatus structure
    }

    if (TLMC_PZIM_GetStatus(hDevice, &piezoInertialMotorStatus, TLMC_NoWait) == TLMC_Success)
    {
        // The piezo inertial motor status data previously retrieved from the controller has been
        // copied to the piezoInertialMotorStatus structure
    }
}

void Example_PZIM_GetTriggerTargetPosition(const TLMC_DeviceHandle hDevice)
{
    int32_t position;

    if (TLMC_PZIM_GetTriggerTargetPosition(hDevice, &position, TLMC_InfiniteWait) == TLMC_Success)
    {
    }
}

void Example_SetEncoderCounter(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_SetEncoderCounter(hDevice, 1000) == TLMC_Success)
    {
        // A request to set the encoder counter to the value specified has been sent to the controller
    }
}

void Example_SetEndOfMoveMessagesMode(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_SetEndOfMoveMessagesMode(hDevice, TLMC_EndOfMoveMessagesMode_Disabled) == TLMC_Success)
    {
        // A request has been sent to the controller instructing it to stop sending end of move messages.
    }

    if (TLMC_SetEndOfMoveMessagesMode(hDevice, TLMC_EndOfMoveMessagesMode_Enabled) == TLMC_Success)
    {
        // A request has been sent to the controller instructing it to start sending end of move messages.
    }
}

void Example_SetPositionCounter(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_SetPositionCounter(hDevice, 1000) == TLMC_Success)
    {
        // A request to set the position counter to the value specified has been sent to the controller
    }
}

void Example_SetSetting(const TLMC_DeviceHandle hDevice)
{
    // This example sets a named setting ("home.offsetDistance") on the device handled by 'hDevice'

    union TLMC_Value newValue;

    // Take care to use the correct union member. If unsure, use TLMC_GetSetting to obtain a
    // TLMC_Setting structure for the setting. This will tell you the correct union member to use.
    newValue.int64Value = 10;

    if (TLMC_SetSetting(hDevice, "home.offsetDistance", &newValue) == TLMC_Success)
    {
        // A request to set the home offset distance to the value specified has been sent
        // to the controller
    }
}

void Example_SetSettingsFromString(const TLMC_DeviceHandle hDevice)
{
    // This example shows how to use set several settings at the same time on the device handled by 'hDevice'.
    // Note that the settings specified are only examples and may not apply to all devices.

    // Pass in a JSON string to set some settings
    if (TLMC_SetSettingsFromString(hDevice, "{\"controlLoops.current.proportional\" : 20, \"io1.mode\" : 0, \"io1.polarity\" : 2") == TLMC_Success)
    {
        // The device will have been updated to use the setting values provided
    }

    // Pass in a semi-structured string to set some settings
    if (TLMC_SetSettingsFromString(hDevice, "controlLoops.current.proportional=20\n, io1.mode=0\n io1.polarity=2") == TLMC_Success)
    {
        // The device will have been updated to use the setting values provided
    }
}

void Example_SetStatusMode(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_SetStatusMode(hDevice, TLMC_OperatingMode_ManualStatusPolling) == TLMC_Success)
    {
        // A request has been sent to the controller instructing it to stop sending regular status updates.
        // Status update requests will not automatically be sent to the controller.
    }

    if (TLMC_SetStatusMode(hDevice, TLMC_OperatingMode_StatusPushedByController) == TLMC_Success)
    {
        // A request has been sent to the controller instructing it to start sending regular status updates.
        // Status update requests will not automatically be sent to the controller.
    }

    if (TLMC_SetStatusMode(hDevice, TLMC_OperatingMode_AutomaticStatusPolling) == TLMC_Success)
    {
        // A request has been sent to the controller instructing it to stop sending regular status updates.
        // Status update requests will automatically be sent to the controller.
    }
}

void Example_PZ_SetOutputWaveformLookupTableSample(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_PZ_OutputWaveformLookupTableSample sample;

    sample.index = 0;
    sample.voltage = 0;

    if (TLMC_PZ_SetOutputWaveformLookupTableSample(hDevice, &sample) == TLMC_Success)
    {
        // A request has been sent to the controller instructing it to set the lookup table sample
    }
}

void Example_PZ_SetZero(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_PZ_SetZero(hDevice, TLMC_InfiniteWait) == TLMC_Success)
    {
        // Zeroing of the controller completed successfully
    }

    if (TLMC_PZ_SetZero(hDevice, TLMC_NoWait) == TLMC_Success)
    {
        // A request to start zeroing has been sent to the controller
    }
}

void Example_ActivateCalibration(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_ActivateCalibration(hDevice) == TLMC_Success)
    {
        // Calibration has been activated
    }
}

void Example_DeactivateCalibration(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_DeactivateCalibration(hDevice) == TLMC_Success)
    {
        // Calibration has been deactivated
    }
}

void Example_Disconnect(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_Disconnect(hDevice) == TLMC_Success)
    {
        // A disconnect notification message has been sent to the device
    }
}

void Example_Home(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_Home(hDevice, TLMC_InfiniteWait) == TLMC_Success)
    {
        // Homing of the actuator completed successfully
    }

    if (TLMC_Home(hDevice, TLMC_NoWait) == TLMC_Success)
    {
        // A request to start homing the actuator has been sent to the controller
    }
}

void Example_Identify(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_Identify(hDevice) == TLMC_Success)
    {
        // A request to visual identify itself has been sent to the controller
    }
}

void Example_LoadParams(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_LoadParams(hDevice) == TLMC_Success)
    {
        // All parameters have been loaded from the controller
    }
}

void Example_MoveAbsolute(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_Move(hDevice, TLMC_MoveMode_AbsoluteToProgrammedPosition, TLMC_Unused, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The stage has been move to the preprogrammed absolute position (previously set with MoveAbsoluteParams)
    }

    if (TLMC_Move(hDevice, TLMC_MoveMode_Absolute, (int)(((double)45.0) * ((double)1919.6418578623391)), TLMC_InfiniteWait) == TLMC_Success)
    {
        // The stage has been move to the specified absolute position
    }
}

void Example_MoveContinuous(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_Move(hDevice, TLMC_MoveMode_ContinuousForward, TLMC_Unused, TLMC_NoWait) == TLMC_Success)
    {
        // A request to move the stage continuously in the forward direction has been sent to the controller
    }
}

void Example_MoveJog(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_Move(hDevice, TLMC_MoveMode_JogReverse, TLMC_Unused, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The stage was jogged in the reverse direction
    }
}

void Example_MoveRelative(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_Move(hDevice, TLMC_MoveMode_RelativeByProgrammedDistance, TLMC_Unused, TLMC_InfiniteWait) == TLMC_Success)
    {
        // The stage has been moved by the preprogrammed relative distance (previously set with MoveRelativeParams)
    }

    if (TLMC_Move(hDevice, TLMC_MoveMode_Relative, (int)(((double)45.0) * ((double)1919.6418578623391)), TLMC_InfiniteWait) == TLMC_Success)
    {
        // The stage has been moved by the specified relative distance
    }
}

void Example_MoveSyncArray(const TLMC_DeviceHandle hDevice)
{
    int32_t timePositions[] = {
        0,1100000,1150000 ,250,1119781,1149511 ,250,1139515,1148043 ,250,1159151,1145602 ,250,1178643,1142193 ,250,1197942,1137824 ,250,1217001,1132506 ,250,1235774,1126252 ,
        250,1254215,1119077 ,250,1272279,1110999 ,250,1289921,1102037 ,250,1307098,1092214 ,250,1323768,1081554 ,250,1339891,1070082 ,250,1355427,1057827 ,250,1370337,1044818 ,
        250,1384586,1031088 ,250,1398139,1016670 ,250,1410962,1001600 ,250,1423024,985914 ,250,1434296,969650 ,250,1444749,952850 ,250,1454359,935552 ,250,1463102,917801 ,
        250,1470956,899639 ,250,1477902,881110 ,250,1483924,862261 ,250,1489006,843138 ,250,1493136,823786 ,250,1496304,804254 ,250,1498502,784588 ,250,1499725,764839 ,
        250,1499969,745053 ,250,1499235,725279 ,250,1497524,705565 ,250,1494840,685961 ,250,1491190,666513 ,250,1486583,647269 ,250,1481029,628277 ,250,1474544,609582 ,
        250,1467141,591232 ,250,1458840,573269 ,250,1449661,555740 ,250,1439626,538685 ,250,1428761,522148 ,250,1417090,506168 ,250,1404644,490785 ,250,1391452,476037 ,
        250,1377547,461959 ,250,1362963,448586 ,250,1347735,435950 ,250,1331901,424083 ,250,1315499,413013 ,250,1298570,402768 ,250,1281155,393373 ,250,1263297,384851 ,
        250,1245039,377222 ,250,1226427,370505 ,250,1207504,364717 ,250,1188319,359872 ,250,1168918,355982 ,250,1149348,353056 ,250,1129657,351101 ,250,1109894,350122 ,
        250,1090106,350122 ,250,1070343,351101 ,250,1050652,353056 ,250,1031082,355982 ,250,1011681,359872 ,250,992496,364717 ,250,973574,370505 ,250,954961,377222 ,
        250,936703,384851 ,250,918845,393373 ,250,901430,402768 ,250,884501,413013 ,250,868099,424083 ,250,852265,435950 ,250,837037,448585 ,250,822453,461959 ,
        250,808548,476037 ,250,795356,490785 ,250,782910,506169 ,250,771239,522148 ,250,760374,538685 ,250,750339,555740 ,250,741160,573269 ,250,732859,591232 ,
        250,725456,609582 ,250,718971,628277 ,250,713417,647269 ,250,708810,666513 ,250,705160,685961 ,250,702476,705565 ,250,700765,725279 ,250,700031,745053 ,
        250,700275,764839 ,250,701498,784588 ,250,703696,804254 ,250,706864,823786 ,250,710994,843138 ,250,716076,862261 ,250,722098,881110 ,250,729044,899639 ,
        250,736898,917801 ,250,745641,935552 ,250,755251,952850 ,250,765704,969650 ,250,776976,985914 ,250,789038,1001600 ,250,801861,1016670 ,250,815414,1031088 ,
        250,829663,1044818 ,250,844573,1057827 ,250,860109,1070082 ,250,876232,1081554 ,250,892902,1092214 ,250,910079,1102037 ,250,927721,1110999 ,250,945785,1119077 ,
        250,964226,1126252 ,250,982999,1132506 ,250,1002058,1137824 ,250,1021358,1142193 ,250,1040849,1145602 ,250,1060485,1148043 ,250,1080218,1149511 ,250,1100000,1150000 ,
        250,1119782,1149511 ,250,1139515,1148043 ,250,1159151,1145602 ,250,1178643,1142193 ,250,1197942,1137824 ,250,1217001,1132506 ,250,1235774,1126252 ,250,1254215,1119077 ,
        250,1272279,1110999 ,250,1289921,1102037 ,250,1307098,1092214 ,250,1323768,1081554 ,250,1339891,1070082 ,250,1355427,1057826 ,250,1370337,1044818 ,250,1384586,1031088 ,
        250,1398139,1016670 ,250,1410962,1001600 ,250,1423024,985914 ,250,1434296,969651 ,250,1444749,952849 ,250,1454359,935552 ,250,1463102,917801 ,250,1470956,899639 ,
        250,1477902,881110 ,250,1483924,862261 ,250,1489006,843137 ,250,1493136,823786 ,250,1496304,804254 ,250,1498502,784589 ,250,1499725,764839 ,250,1499969,745053 ,
        250,1499235,725279 ,250,1497524,705565 ,250,1494840,685961 ,250,1491190,666513 ,250,1486583,647269 ,250,1481029,628277 ,250,1474544,609582 ,250,1467141,591232 ,
        250,1458840,573270 ,250,1449661,555740 ,250,1439626,538685 ,250,1428761,522148 ,250,1417090,506168 ,250,1404644,490786 ,250,1391452,476037 ,250,1377547,461959 ,
        250,1362963,448586 ,250,1347735,435950 ,250,1331901,424083 ,250,1315499,413013 ,250,1298570,402768 ,250,1281155,393373 ,250,1263297,384851 ,250,1245039,377222 ,
        250,1226426,370505 ,250,1207504,364717 ,250,1188319,359872 ,250,1168918,355982 ,250,1149348,353056 ,250,1129657,351101 ,250,1109894,350122 ,250,1090106,350122 ,
        250,1070343,351101 ,250,1050652,353056 ,250,1031082,355982 ,250,1011681,359872 ,250,992496,364717 ,250,973574,370505 ,250,954961,377222 ,250,936703,384851 ,
        250,918845,393373 ,250,901430,402768 ,250,884501,413013 ,250,868099,424083 ,250,852265,435950 ,250,837037,448586 ,250,822453,461959 ,250,808548,476037 ,
        250,795356,490786 ,250,782910,506168 ,250,771239,522148 ,250,760374,538685 ,250,750339,555740 ,250,741160,573270 ,250,732859,591232 ,250,725456,609582 ,
        250,718971,628277 ,250,713417,647269 ,250,708810,666513 ,250,705160,685961 ,250,702476,705565 ,250,700765,725279 ,250,700031,745053 ,250,700275,764839 ,
        250,701498,784588 ,250,703696,804254 ,250,706864,823786 ,250,710994,843138 ,250,716076,862261 ,250,722098,881110 ,250,729044,899639 ,250,736898,917801 ,
        250,745641,935552 ,250,755251,952850 ,250,765704,969651 ,250,776976,985914 ,250,789038,1001600 ,250,801861,1016670 ,250,815413,1031088 ,250,829663,1044818 ,
        250,844573,1057827 ,250,860109,1070082 ,250,876232,1081554 ,250,892902,1092214 ,250,910079,1102037 ,250,927721,1110999 ,250,945785,1119077 ,250,964226,1126252 ,
        250,982999,1132506 ,250,1002058,1137824 ,250,1021357,1142193 ,250,1040849,1145602 ,250,1060485,1148043 ,250,1080219,1149511 ,250,1100000,1150000 ,250,1100000,1150000 };

    struct TLMC_MoveSyncArray moveSyncArray;
    moveSyncArray.arrayId = 1;
    moveSyncArray.channels = 3;
    moveSyncArray.numPoints = 256;
    moveSyncArray.startIndex = 0;
    moveSyncArray.timePositions = timePositions;

    if (TLMC_SetMoveSyncArray(hDevice, &moveSyncArray) == TLMC_Success)
    {
        // The new move sync array have been sent to the controller
    }
}

void Example_MoveSyncParams(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_MoveSyncParams moveSyncParams;
    moveSyncParams.arrayId = 1;
    moveSyncParams.cycleStartIndex = 127;
    moveSyncParams.cycleEndIndex = 254;
    moveSyncParams.numberOfCycles = 1;
    moveSyncParams.endIndex = 255;
    moveSyncParams.deceleration = 10000;
    if (TLMC_SetMoveSyncParams(hDevice, &moveSyncParams) == TLMC_Success)
    {
        // The new move sync parameters have been sent to the controller
    }
}

void Example_MoveSyncStart(const TLMC_DeviceHandle hDevice)
{
    struct TLMC_MoveSyncStartParams moveSyncStartParams;
    moveSyncStartParams.arrayId = 1;
    moveSyncStartParams.channels = 3;
    moveSyncStartParams.trigger = TLMC_MoveSyncStartTrigger_Software;

    if (TLMC_MoveSyncStart(hDevice, &moveSyncStartParams) == TLMC_Success)
    {
        // The new move sync start parameters have been sent to the controller and will start move sync immediately
    }
}

void Example_RackIdentify(const TLMC_DeviceHandle hDevice)
{
    uint8_t channel1 = 1;
    if (TLMC_RackIdentify(hDevice, channel1) == TLMC_Success)
    {
        // A request to visually dentify itself has been sent to the controller
    }
}

void Example_PersistParams(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_PersistParams(hDevice, TLMC_ParameterGroupId_Unspecified) == TLMC_Success)
    {
        // A request to persist parameters has been sent to the controller
    }
}

void Example_RestoreFactoryDefaults(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_RestoreFactoryDefaults(hDevice) == TLMC_Success)
    {
        // A request to reset to factory defaults has been sent to the controller
    }
}

void Example_SendNoFlashProgramming(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_SendNoFlashProgramming(hDevice) == TLMC_Success)
    {
        // A "no flash programming" message has been sent to the controller
    }
}

void Example_SendYesFlashProgramming(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_SendYesFlashProgramming(hDevice) == TLMC_Success)
    {
        // A "yes flash programming" message has been sent to the controller
    }
}

void Example_Stop(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_Stop(hDevice, TLMC_StopMode_Immediate, TLMC_InfiniteWait) == TLMC_Success)
    {
        // Stage movement has been immediately stopped
    }

    if (TLMC_Stop(hDevice, TLMC_StopMode_Profiled, TLMC_NoWait) == TLMC_Success)
    {
        // A request to stop stage movement in a profiled manner has been sent to the controller
    }
}

void Example_UnitConverter(const TLMC_DeviceHandle hDevice)
{
    int64_t distanceInDeviceUnits = 19196;
    int64_t velocityInDeviceUnits = 429416;
    int64_t accelerationInDeviceUnits = 146;

    double distanceInPhysicalUnits;
    double velocityInPhysicalUnits;
    double accelerationInPhysicalUnits;

    TLMC_Unit_Type converterUnit;

    if (TLMC_ConvertFromDeviceToPhysical(hDevice, TLMC_ScaleType_Distance, distanceInDeviceUnits, &distanceInPhysicalUnits, &converterUnit) == TLMC_Success)
    {
        // The 'distanceInDeviceUnits' value has been converted to the physical unit value and copied to the 'distanceInPhysicalUnits' variable. 
        // The converter physical unit type has been copied to the 'converterUnit' variable 
    }

    if (TLMC_ConvertFromPhysicalToDevice(hDevice, TLMC_ScaleType_Distance, TLMC_Unit_Millimetres, distanceInPhysicalUnits, &distanceInDeviceUnits) == TLMC_Success)
    {
        // The 'distanceInPhysicalUnits' value has been converted to the device unit value and copied to the 'distanceInDeviceUnits' variable. 
    }

    if (TLMC_ConvertFromDeviceToPhysical(hDevice, TLMC_ScaleType_Velocity, velocityInDeviceUnits, &velocityInPhysicalUnits, &converterUnit) == TLMC_Success)
    {
        // The 'velocityInDeviceUnits' value has been converted to the physical unit value and copied to the 'velocityInPhysicalUnits' variable. 
        // The converter physical unit type has been copied to the 'converterUnit' variable 
    }

    if (TLMC_ConvertFromPhysicalToDevice(hDevice, TLMC_ScaleType_Velocity, TLMC_Unit_Millimetres, velocityInPhysicalUnits, &velocityInDeviceUnits) == TLMC_Success)
    {
        // The 'velocityInPhysicalUnits' value has been converted to the device unit value and copied to the 'velocityInDeviceUnits' variable. 
    }

    if (TLMC_ConvertFromDeviceToPhysical(hDevice, TLMC_ScaleType_Acceleration, accelerationInDeviceUnits, &accelerationInPhysicalUnits, &converterUnit) == TLMC_Success)
    {
        // The 'accelerationInDeviceUnits' value has been converted to the physical unit value and copied to the 'accelerationInPhysicalUnits' variable. 
        // The converter physical unit type has been copied to the 'converterUnit' variable 
    }

    if (TLMC_ConvertFromPhysicalToDevice(hDevice, TLMC_ScaleType_Acceleration, TLMC_Unit_Millimetres, accelerationInPhysicalUnits, &accelerationInDeviceUnits) == TLMC_Success)
    {
        // The 'accelerationInPhysicalUnits' value has been converted to the device unit value and copied to the 'accelerationInDeviceUnits' variable. 
    }
}

void Example_PZ_StartOutputWaveform(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_PZ_StartOutputWaveform(hDevice) == TLMC_Success)
    {
        // A request has been sent to the controller instructing it to start output waveform generation
    }
}

void Example_PZ_StopOutputWaveform(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_PZ_StopOutputWaveform(hDevice) == TLMC_Success)
    {
        // A request has been sent to the controller instructing it to stop output waveform generation
    }
}

void Example_PZIM_PulseParaAcquire(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_PZIM_PulseParaAcquire(hDevice, TLMC_InfiniteWait) == TLMC_Success)
    {
        // A request has been sent to the controller instructing it to acquire pulse parameters
    }
}

void Example_GetChannel(const TLMC_DeviceHandle hDevice)
{
    TLMC_DeviceHandle channelHandle;
    const uint8_t channelNumber = 2;

    if (TLMC_GetChannel(hDevice, channelNumber, &channelHandle) == TLMC_Success)
    {
        //The channel handle has been created and can be used for operations on channel 2 of the device
    }
}

void Example_RegisterLoggingHandler()
{
    if (TLMC_RegisterLoggingHandler(Example_LoggingHandlerCallbackFn, TLMC_LogLevel_Information,
        TLMC_LogCategoryFilter_User, 0x1234) == TLMC_Success)
    {
        // We have successfully registered our callback handler, 'Example_LoggingHandlerCallbackFn'.
        // It will be called for all subsequent log entries created that match the specfied criteria.
    }
}

void Example_UnregisterLoggingHandler()
{
    if (TLMC_UnregisterLoggingHandler(Example_LoggingHandlerCallbackFn) == TLMC_Success)
    {
        // We have successfully unregistered our callback handler, 'Example_LoggingHandlerCallbackFn'.
        // It will no longer be called.
    }
}

void __stdcall Example_LoggingHandlerCallbackFn(const char* pBuffer, const unsigned int bufferLength, const uintptr_t userData)
{
    // Once registered, this function will be called for all subsequent log entries created that match the specfied criteria.
    // 'userData' will be the value we passed in at registration (0x1234 in this case).
}

void Example_WritingRawPackets(const TLMC_DeviceHandle hDevice)
{
    unsigned char writeBuffer[6];

    // Hardware information request packet
    writeBuffer[0] = 0x05;
    writeBuffer[1] = 0x00;
    writeBuffer[2] = 0x00;
    writeBuffer[3] = 0x00;
    writeBuffer[4] = 0x50;
    writeBuffer[5] = 0x01;

    if (TLMC_WritePacket(hDevice, writeBuffer, sizeof(writeBuffer)) == TLMC_Success)
    {
        // The bytes in writeBuffer has been successfully written to the device handled by hDevice
    }
}

void Example_ReadingRawPackets(const TLMC_DeviceHandle hDevice)
{
    if (TLMC_RegisterPacketHandler(hDevice, Example_PacketHandler, 1) == TLMC_Success)
    {
        // The function Example_PacketHandler has been registered. It will be called
        // whenever a packet is received in relation to the device handled by hDevice.

        // Normally, you would leave the callback function registered until immediately before closing the device.
        // Here we unregister immediately for demonstration purposes.
        if (TLMC_UnregisterPacketHandler(hDevice, Example_PacketHandler) == TLMC_Success)
        {
            // The callback function Example_PacketHandler has been unregistered.
            // It will no longer be called.
        }
    }
}

void __stdcall Example_PacketHandler(const unsigned char* pBuffer, const size_t bufferLength, const uintptr_t userData)
{
    // This function will be called whenever a packet is received in relation to the device handled by hDevice.
    // See Example_ReadingRawPackets for an example of how to register this function as a callback.

    // userData is the user-specified value that was passed into TLMC_RegisterPacketHandler. The XA API does not
    // perform any processing on this and simply passes it to the callback handler. You can use this to pass
    // anything you want. Perhaps the device handle, or a special unique value allowing you to use the same
    // Example_PacketHandler function to process received packets from several devices.

    // Example of filtering based on the userData field
    if (userData != 1)
    {
        return;
    }

    // Example of inspecting the packet to extract a command identifier
    if (bufferLength > 1)
    {
        uint16_t commandId = pBuffer[0] | (pBuffer[1] << 8);

        switch (commandId)
        {
            case 0x0006: // Response to a hardware information request
                // Insert code for handling 0x0006 here
                break;
        }
    }
}

void Example_ReceivingNotifications(const TLMC_DeviceHandle hDevice)
{
    uintptr_t myUserData = hDevice; // myUserData is passed into the registration function. The value
                                    // provided will be made available to our handler in the 'userData'
                                    // argument.
                                    // You can use this field to pass in anything your handler may need.
                                    // A common use case is to pass the relevant device handle (as in this
                                    // example). This gives the handler access to the device associated
                                    // with the registration and notification.
                                    // If your handler doesn't make use of the user data argument, it's a
                                    // good idea to specify zero or NULL in the registration.

    if (TLMC_RegisterNotificationHandler(hDevice, Example_NotificationHandlerCallbackFn, myUserData) == TLMC_Success)
    {
        // We have successfully registered the callback function Example_NotificationHandlerCallbackFn. It will
        // be called whenever a notification is available relating to the device handled by hDevice.

        // Normally, you would leave the callback function registered until immediately before closing the device.
        // Here we remove our subscription straight away to demonstrate how this is accomplished.
        if (TLMC_UnregisterNotificationHandler(hDevice, Example_NotificationHandlerCallbackFn) == TLMC_Success)
        {
            // The callback function Example_NotificationHandlerCallbackFn has been unregistered.
            // It will no longer be called.
        }
    }
}

void __stdcall Example_NotificationHandlerCallbackFn(const struct TLMC_Notification* pNotification, const uintptr_t userData)
{
    switch (pNotification->id)
    {
        case TLMC_NotificationId_StatusItemChanged:
            {
                // Status item notifications contain extra data in the 'data' field
                struct TLMC_StatusItemChangedNotificationData* pExtraData = (struct TLMC_StatusItemChangedNotificationData*)(pNotification->data);

                // TLMC_StatusItemChangedNotificationData has the following fields:
                // count - The number of status items that have been updated
                // ids   - A pointer to a block of memory holding an array of 'TLMC_StatusItemId_Type'
                //         elements. There will be 'count' elements in the array

                // Loop through the status item identifiers that changed as part of this notification
                {
                    size_t index = 0;

                    while (index < pExtraData->count)
                    {
                        TLMC_StatusItemId_Type statusItemId = pExtraData->ids[index];

                        // To retrieve the new value of the status item, use one of the 'TLMC_GetStatusItem'
                        // functions. It is safe to call from within this callback function

                        // Here we use TLMC_GetStatusItem() to retrieve the updated value
                        {
                            TLMC_DeviceHandle hDevice = (TLMC_DeviceHandle)userData;
                            struct TLMC_StatusItem statusItem;

                            if (TLMC_GetStatusItem(hDevice, statusItemId, &statusItem) == TLMC_Success)
                            {
                                switch (statusItem.valueType)
                                {
                                    case TLMC_ValueType_bool:
                                        // This status item contains a boolean, therefore 'statusItem.value.boolValue'
                                        // holds the value
                                        break;

                                    case TLMC_ValueType_int64:
                                        // This status item contains a 64-bit signed integer, therefore
                                        // 'statusItem.value.int64Value' holds the value
                                        break;
                                }
                            }
                        }

                        index++;
                    } // while
                }
            }
            break;

        // To retrieve the updated parameters, use the relevant 'TLMC_Get...Params' function
        // It is safe to call from within this callback function

        // Here we detect the home parameters have changed and retrieve the new values
        case TLMC_NotificationId_HomeParamsChanged:
            {
                TLMC_DeviceHandle hDevice = (TLMC_DeviceHandle)userData;
                struct TLMC_HomeParams params;

                if (TLMC_GetHomeParams(hDevice, &params, TLMC_NoWait) == TLMC_Success)
                {
                    // The new homing parameters have been copeid into the local 'params' buffer
                }
            }
            break;

        // Here we process receiving rich response notifications
        case TLMC_NotificationId_RichResponseChanged:
            {
                TLMC_DeviceHandle hDevice = (TLMC_DeviceHandle)userData;
                struct TLMC_RichResponse richResponse;

                if (TLMC_GetRichResponse(hDevice, &richResponse) == TLMC_Success)
                {
                    // The rich response information has been copied to the 'richResponse' variable
                }
            }
            break;

        default:
            break;
    }
}

void Example_SimulationCreateAndRemove()
{
    const char* pSimulationDescription = "{ \
        \"PartNumber\": \"BBD303\", \
        \"SerialNumber\": \"103003334\", \
        \"Channels\": \
        [ \
            { \
                \"BayNumber\": \"1\", \
                \"SerialNumber\": \"104003335\", \
                \"ActuatorType\": \"DDS600\" \
            }, \
            { \
                \"BayNumber\": \"2\", \
                \"SerialNumber\": \"104003336\", \
                \"ActuatorType\": \"DDS300\" \
            }, \
            { \
                \"BayNumber\": \"3\", \
                \"SerialNumber\": \"104003337\", \
                \"ActuatorType\": \"DDS600\" \
            } \
        ] }";

    // The following commented out code is an example of a simpler device that only has a single actuator:

    //const char* pSimulationDescription = "{ \
    //    \"PartNumber\": \"KDC101\", \
    //    \"SerialNumber\": \"27001234\", \
    //    \"ActuatorType\": \"MTS25-Z8\" }";

    TLMC_ResultCode_Type resultCode = TLMC_CreateSimulation(pSimulationDescription);

    if (resultCode == TLMC_Success)
    {
        TLMC_DeviceHandle hDevice;

        // Open channel 1 of the simulated device
        resultCode = TLMC_Open("104003335", NULL, TLMC_OperatingMode_Default, &hDevice);

        if (resultCode == TLMC_Success)
        {
            // All features of a real device can now be called on the simulation
            Example_GetHardwareInfo(hDevice);

            TLMC_Close(hDevice);
        }

        TLMC_RemoveSimulation(pSimulationDescription);
    }
}