import { useEffect, useState } from 'react';
import { SensorDataType } from '../../interfaces/sensor-data.interface';
import { getSensorData } from '../../services/sensors.service';
import {
  FilterDataByDeviceId,
  getUniqueDeviceCount,
  getUniqueDevices,
} from '../../utils/sensors.util';
import MatrixCard from './MatrixCard';

type TimerOptionType = {
  name: string;
  duration: number;
};

const timerOptions: TimerOptionType[] = [
  {
    name: '5s',
    duration: 5,
  },
  {
    name: '15s',
    duration: 15,
  },
  {
    name: '1m',
    duration: 60,
  },
  {
    name: '5m',
    duration: 5 * 60,
  },
  {
    name: '1h',
    duration: 60 * 60,
  },
];

const dataSampleOptions = [
  {
    name: '10',
    count: 10,
  },
  {
    name: '20',
    count: 20,
  },
  {
    name: '50',
    count: 50,
  },
  {
    name: '100',
    count: 100,
  },
  {
    name: '250',
    count: 250,
  },
];

const DustbinMatrix = () => {
  const [sensorData, setSensorData] = useState<SensorDataType[]>();
  const [refreshTimer, setRefreshTimer] = useState<number>(
    timerOptions[timerOptions.length - 1].duration
  );
  const [indicatorBgColor, setIndicatorBgColor] =
    useState<string>('transparent'); // transparent
  const [dataSampleCount, setDataSampleCount] = useState<number>(
    dataSampleOptions[1].count
  );
  const [currentDevice, setCurrentDevice] = useState<string>('all');
  const [uniqueDevices, setUniqueDevices] = useState<string[]>(['all']);

  const handleSetDataSampleCount = (count: number) => {
    setDataSampleCount(count);

    setRefreshTimer(refreshTimer + 0.00001);

    console.log({ count });
  };

  const handleIndicatorColor = () => {
    // keep the indicator color red for 0.25 seconds
    setIndicatorBgColor('#FF0000');
    setTimeout(() => {
      setIndicatorBgColor('transparent');
    }, 250);
  };

  const handleSensorDataSet = () => {
    getSensorData(dataSampleCount * 2).then((data) => {
      setSensorData(FilterDataByDeviceId(data, currentDevice));
      handleIndicatorColor();
    });
  };

  useEffect(() => {
    setUniqueDevices(getUniqueDevices(sensorData || []));
  }, [sensorData]);

  // useEffect(() => {
  //   handleSensorDataSet(
  //     Fil
  //   )
  // }, [currentDevice]);

  useEffect(() => {
    handleSensorDataSet();

    const interval = setInterval(() => {
      handleSensorDataSet();
    }, refreshTimer * 1000);

    return () => clearInterval(interval);
  }, [refreshTimer, currentDevice]);

  return (
    <div className="px-2 py-2 rounded-sm my-4">
      {/* <h2 className="text-2xl">Dustbin Matrix</h2> */}

      {/* control panel */}
      <div className="flex flex-col gap-3 p-3">
        {/* data refresh */}
        <div className="flex flex-row justify-end items-center gap-5">
          <div>
            {/* select devices */}
            <select
              name="unique_devices"
              id="unique_devices"
              defaultValue={uniqueDevices[0]}
              onChange={(e) => {
                const value = e.target.value;
                console.log({ value });
                setCurrentDevice(value);
              }}
              className="bg-blue-500 p-2 text-white"
            >
              {uniqueDevices?.map((option) => (
                <option
                  key={option}
                  value={option}
                  className="bg-blue-300 p-2 text-gray-700"
                >
                  {option}
                </option>
              ))}
            </select>
          </div>

          {/* data samples */}
          <div>
            <select
              name="data_sample_count"
              id="data_sample_count"
              defaultValue={dataSampleCount}
              onChange={(e) => {
                const value = Number(e.target.value);

                handleSetDataSampleCount(value);
              }}
              className="bg-blue-500 p-2 text-white"
            >
              {dataSampleOptions?.map((option) => (
                <option
                  key={option.name}
                  value={option.count}
                  className="bg-blue-300 p-2 text-gray-700"
                >
                  {option.name}
                </option>
              ))}
            </select>
          </div>

          {/* refresh duration */}
          <div>
            <select
              name="refresh_timer"
              id="refresh_timer"
              defaultValue={refreshTimer}
              onChange={(e) => {
                const value = Number(e.target.value);

                setRefreshTimer(value);
              }}
              className="bg-blue-500 p-2 text-white"
            >
              {timerOptions.map((option) => (
                <option
                  key={option.name}
                  value={option.duration}
                  className="bg-blue-300 p-2 text-gray-700"
                >
                  {option.name}
                </option>
              ))}
            </select>
          </div>
          <div
            style={{
              height: '10px',
              width: '10px',
              backgroundColor: indicatorBgColor,
              margin: '5px',
              borderRadius: '50%',
            }}
          ></div>
          {/* </div> */}
        </div>

        {/* stats */}
        <div className="mx-auto text-center bg-blue-200 p-1">
          <div className="text-xl">
            {sensorData && getUniqueDeviceCount(sensorData)}
          </div>
          <div>Dustbin Count</div>
        </div>
      </div>

      {sensorData && (
        <div className="px-3 py-4 flex flex-row gap-2 justify-center sm:flex-wrap ">
          <MatrixCard sensorData={sensorData} field="capacity_remaining" />
          <MatrixCard sensorData={sensorData} field="dustbin_lid_status" />
        </div>
      )}
    </div>
  );
};;

export default DustbinMatrix;
