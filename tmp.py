{
  "simples": [
    {
      "text": "I-24013OC Section: [F-7600] New OC Section: 09 Navigation and Entertainment / Acoustic Vehicle Alerting System (AVAS)Description: UC Setting up external audio tracks for External audio accompaniment when the vehicle is moving at speeds up to 32 km/hGoal: Selection of audio tracks for notification of an external soundtrack about a moving vehicle up to 32 km/hScope of application and description of the system: The driver is in the vehicle and, according to his preference, can choose an audio track for external sound about a moving car up to 32 km/hActors: Driver.Preconditions:1) The vehicle is in drive mode P.2) Audio track No. 1 is selected by default, or the driver chose a different track in the settings.The main scenario:1) The vehicle is in drive mode P.2) The driver enters the vehicle's sound settings on the SWP and selects an audio track for an external soundtrack about a moving car up to 32 km/h.3) The user sees a list of sounds in which the previously assigned sound is selected (default is Audio track No. 1)4) The user selects one of the sounds on the in_2.SWP Android and in_10. Front buttons steering wheel. The list of available audio tracks in the settings window:3.1. Audio track No. 1;3.2. Audio track No. 2;3.3. Audio track No. 3;3.4. Audio track No. 4;3.5. Audio track No. 5. 4) The driver is asked to confirm the selected audio track;5) Previously, the driver can listen to the audio track through the out_27. AVAS of the vehicle. The corresponding sound is played when the driver has selected it in the settings;5.1. If the driver has confirmed the selection, the new audio track settings are saved;5.2. The selected audio track is saved in the driver's profile.5.3. If the driver has canceled the selection, the audio track settings remain the same, the new values are not saved.Alternative scenariosMalfunction of the external sound system:1. If the out_27. AVAS of the vehicle are malfunctioning or not working, the driver will not be able to pre-listen to the sound of the track;2. If the vehicle is in motion, the audio track setting is not available, the vehicle must be in drive mode to adjust it.Priority: NormalType: Use Case CF",
      "folders_ids": [
        "7e95c17a-036e-4356-8386-9d81e1f3191d",
      ]
    },
    {
      "text": "I-6605OC Section: [F-7600] New OC Section: 09 Navigation and Entertainment / Acoustic Vehicle Alerting System (AVAS)Description: UC Pedestrian Warning System UsagePreconditions- driving below approximately 32 km/h or while driving in reverseMain Scenario- Car emit sound out_27, because EV operate quietly, and this sound helps to alert pedestrians of your oncoming vehiclePost conditions- Pedestrians know that car is nearPriority: NormalType: Use Case CF",
      "folders_ids": [
        "7e95c17a-036e-4356-8386-9d81e1f3191d",
      ]
    }
  ]
}