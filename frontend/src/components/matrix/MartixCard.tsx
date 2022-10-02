import { useState } from 'react';
import {
  VictoryChart,
  VictoryZoomContainer,
  VictoryArea,
  VictoryBrushContainer,
  VictoryAxis,
  VictoryLine,
} from 'victory';
import { SensorDataType } from '../../interfaces/sensor-data.interface';

const MatrixCard = ({
  sensorData,
  field,
}: {
  sensorData: SensorDataType[];
  field: 'capacity_remaining' | 'dustbin_lid_status';
}) => {
  const lastDate = new Date(sensorData[sensorData.length - 1].timestamp);
  const firstDate = new Date(sensorData[0].timestamp);

  const convertTimestampToDateTime = (timestamp: string) => {
    const date = new Date(timestamp);

    let dateDurationType;

    if (firstDate.getMonth() === lastDate.getMonth()) {
      dateDurationType = 'day';

      if (firstDate.getDate() === lastDate.getDate()) {
        dateDurationType = 'hour';

        if (firstDate.getHours() === lastDate.getHours()) {
          dateDurationType = 'minute';

          if (firstDate.getMinutes() === lastDate.getMinutes()) {
            dateDurationType = 'second';

            if (firstDate.getSeconds() === lastDate.getSeconds()) {
              dateDurationType = 'millisecond';
            }
          }
        }
      }
    }

    if (dateDurationType == 'day') {
      return `${date.getDate()}/${date.getMonth() + 1}`;
    } else if (dateDurationType == 'hour') {
      return `${date.getHours()}:${date.getMinutes()}`;
    } else if (dateDurationType == 'minute') {
      return `${date.getMinutes()}:${date.getSeconds()}`;
    } else if (dateDurationType == 'second') {
      return `${date.getSeconds()}.${date.getMilliseconds()}`;
    }
  };

  return (
    <div className="flex flex-col bg-blue-50">
      <div className="mx-auto my-2 text-xl">
        <span>
          {field === 'capacity_remaining'
            ? 'Capacity Remaining'
            : 'Dustbin Lid Status'}
        </span>
      </div>
      <VictoryChart
        scale={{ x: 'time' }}
        height={300}
        width={800}
        // containerComponent={
        //   <VictoryZoomContainer
        //     zoomDimension="x"
        //     zoomDomain={zoomDomain}
        //     onZoomDomainChange={handleZoom}
        //   />
        // }
        style={{}}
      >
        <VictoryArea
          style={{
            data: { fill: '#3b82f6', fillOpacity: 0.7, stroke: '#3b82f6' },
          }}
          data={sensorData.map((data) => ({
            x: convertTimestampToDateTime(data.timestamp),
            y: data[field],
          }))}
          x="x"
          y="y"
        />
      </VictoryChart>

      <div className="px-4 text-sm pb-3">
        Time Range: {firstDate.toLocaleString()} to{' '}
        {lastDate.toLocaleDateString() == firstDate.toLocaleDateString()
          ? lastDate.toLocaleTimeString()
          : lastDate.toLocaleString()}
      </div>
    </div>
  );
};

export default MatrixCard;
