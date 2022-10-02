import {
  SensorDataType,
  SensorDataTypeRaw,
} from '../interfaces/sensor-data.interface';

const getSensorData = async (row_count: number) => {
  const options = {
    method: 'GET',
  };

  const response = await fetch(
    `${import.meta.env.VITE_LAMBDA_BACKEND_API}/?row_count=${row_count}`,
    options
  );

  let raw_data: SensorDataTypeRaw;

  if (response.ok) {
    raw_data = await response.json();
  } else {
    raw_data = (await response.text()) as unknown as SensorDataTypeRaw;
  }

  const data = arrangeSensorData(raw_data).reverse();

  console.log({ data });

  return data;
};

const arrangeSensorData = (raw_data: SensorDataTypeRaw) => {
  let data: SensorDataType[] = [];

  raw_data.Rows.forEach((row) => {
    // if previous row doesn't has same timestamp
    if (
      !(
        data.length > 1 &&
        data[data.length - 1].timestamp === row.Data[4].ScalarValue
      )
    ) {
      data.push({
        device_id: row.Data[0].ScalarValue,
        capacity_remaining: parseInt(row.Data[1].ScalarValue),
        dustbin_lid_status: row.Data[2].ScalarValue,
        timestamp: row.Data[4].ScalarValue,
      });
    }
  });

  return data;
};

export { getSensorData };
