import { SensorDataType } from '../../interfaces/sensor-data.interface';

import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

const MatrixCard = ({
  sensorData,
  field,
}: {
  sensorData: SensorDataType[];
  field: 'capacity_remaining' | 'dustbin_lid_status';
}) => {
  const getY = (data: string | number) => {
    if (field == 'capacity_remaining') {
      return data;
    } else if (field == 'dustbin_lid_status') {
      return data == 'open' ? 1 : 0;
    }
  };

  const formatDate = (date: string) => {
    const d = new Date(date);

    // change date from UTC to GMT
    const offset = d.getTimezoneOffset();
    d.setMinutes(d.getMinutes() - offset);

    return d.toLocaleTimeString();
  };

  return (
    <div>
      <div className="mx-auto my-1 text-center text-lg">
        {field == 'capacity_remaining'
          ? 'Capacity Remaining'
          : 'Dustbin Lid Status'}
      </div>
      {/* <ResponsiveContainer height={300} width="100%"> */}
      <AreaChart
        width={550}
        height={250}
        data={sensorData.map((data) => ({
          x: formatDate(data.timestamp),
          y: getY(data[field]),
          device: data['device_id'],
        }))}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="x" />
        <YAxis
        // type={field == 'capacity_remaining' ? 'number' : 'category'}
        />
        <Tooltip
          content={(props) => {
            return (
              <div
                style={{
                  backgroundColor: 'white',
                  padding: '6px',
                  border: '1px solid #ccc',
                  color: '#2859a9',
                }}
              >
                {/* @ts-ignore */}
                <div>{'Device: ' + props.payload[0]?.payload.device}</div>
                {/* @ts-ignore */}
                <div>{'Value: ' + props.payload[0]?.payload.y}</div>
                <div>{props.label}</div>
              </div>
            );
          }}
        />
        <Area type="monotone" dataKey="y" stroke="#8884d8" fill="#8884d8" />
      </AreaChart>
      {/* </ResponsiveContainer> */}
    </div>
  );
};

export default MatrixCard;
