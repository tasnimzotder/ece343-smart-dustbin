import { useEffect, useState } from 'react';
import {
  VictoryArea,
  VictoryChart,
  VictoryGroup,
  VictoryLine,
  VictoryPortal,
  VictoryScatter,
  VictoryTooltip,
} from 'victory';
import { SensorDataType } from '../../interfaces/sensor-data.interface';
import { getSensorData } from '../../services/sensors.service';
import { getUniqueDeviceCount } from '../../utils/sensors.util';

const MatrixCard = () => {
  return (
    <div className="bg-blue-200 px-3 py-3 rounded-sm shadow-sm">
      Matrix Card
    </div>
  );
};

const Chart_X = ({ sensorData }: { sensorData: SensorDataType[] }) => {
  const convertTimestampToDateTime = (timestamp: string) => {
    const date = new Date(timestamp);
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const seconds = date.getSeconds();

    return `${hours}:${minutes}:${seconds}`;
  };

  return (
    <div>
      <VictoryChart width={1000} height={400} scale={'linear'}>
        <VictoryGroup
        // color="#c43a31"
        // labels={({ datum }) => `${datum.y}`}
        // labelComponent={<VictoryTooltip style={{ fontSize: 30 }} />}
        >
          <VictoryLine />
          <VictoryArea
            data={sensorData.map((data) => ({
              x: convertTimestampToDateTime(data.timestamp),
              y: data.capacity_remaining,
            }))}
            style={{
              data: { fill: '#3b82f6', fillOpacity: 0.7, stroke: 'blue' },
            }}
          />
          {/* <VictoryScatter
            data={sensorData.map((data) => ({
              x: convertTimestampToDateTime(data.timestamp),
              y: data.capacity_remaining,
            }))}
            style={{
              data: {
                fill: '#3b82f6',
                fillOpacity: 0.7,
                stroke: 'blue',
                strokeWidth: 40,
                strokeMiterlimit: 100,
                strokeLinecap: 'round',
              },
            }}
          /> */}
        </VictoryGroup>
      </VictoryChart>
    </div>
  );
};

const Chart_Y = ({ sensorData }: { sensorData: SensorDataType[] }) => {
  const convertTimestampToDateTime = (timestamp: string) => {
    const date = new Date(timestamp);
    const hours = date.getHours();
    const minutes = date.getMinutes();
    const seconds = date.getSeconds();

    return `${hours}:${minutes}:${seconds}`;
  };

  const convertDustbinLidStatusToBoolean = (status: string) => {
    if (status === 'open') {
      return true;
    } else {
      return false;
    }
  };

  return (
    <div>
      <VictoryChart width={1000} height={400} scale={'linear'}>
        <VictoryGroup>
          <VictoryLine />
          <VictoryArea
            data={sensorData.map((data) => ({
              x: convertTimestampToDateTime(data.timestamp),
              y: convertDustbinLidStatusToBoolean(data.dustbin_lid_status),
            }))}
            style={{
              data: { fill: '#3b82f6', fillOpacity: 0.7, stroke: 'blue' },
            }}
          />
        </VictoryGroup>
      </VictoryChart>
    </div>
  );
};

const DustbinMatrix = () => {
  const [sensorData, setSensorData] = useState<SensorDataType[]>();
  const [refreshTimer, setRefreshTimer] = useState<number>(120);
  const [indicatorBgColor, setIndicatorBgColor] =
    useState<string>('transparent'); // transparent

  const handleIndicatorColor = () => {
    // keep the indicator color red for 0.25 seconds
    setIndicatorBgColor('#FF0000');
    setTimeout(() => {
      setIndicatorBgColor('transparent');
    }, 250);
  };

  const handleSensorDataSet = () => {
    getSensorData(1000).then((data) => {
      setSensorData(data.slice(data.length - 25 - 2, data.length));
      handleIndicatorColor();

      console.log('refreshed');
    });
  };

  useEffect(() => {
    handleSensorDataSet();

    const interval = setInterval(() => {
      handleSensorDataSet();
    }, refreshTimer * 1000);

    return () => clearInterval(interval);
  }, [refreshTimer]);

  return (
    <div className="bg-blue-100 px-2 py-2 rounded-sm my-4">
      <h2 className="text-xl">Dustbin Matrix</h2>

      <div
        style={{
          height: '10px',
          width: '10px',
          backgroundColor: indicatorBgColor,
          margin: '5px',
          borderRadius: '50%',
        }}
      ></div>

      <input
        placeholder="Refresh Timer"
        name="refresh_timer"
        type={'number'}
        defaultValue={refreshTimer}
        onChange={(e) => {
          const value = Number(e.target.value);

          if (value < 5) {
            setRefreshTimer(5);
            e.target.value = '5';
          } else {
            setRefreshTimer(value);
          }
        }}
      />

      <div>
        Total Dustbins: {sensorData && getUniqueDeviceCount(sensorData)}
      </div>

      <div className="px-3 py-4 flex flex-row gap-3 flex-wrap justify-center">
        <MatrixCard />
        <MatrixCard />
        <MatrixCard />
      </div>

      {sensorData && <Chart_X sensorData={sensorData} />}
      {sensorData && <Chart_Y sensorData={sensorData} />}
    </div>
  );
};

export default DustbinMatrix;
