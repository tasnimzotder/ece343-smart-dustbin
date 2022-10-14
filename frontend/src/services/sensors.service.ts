import { SensorDataType } from '../interfaces/sensor-data.interface';

const getSensorData = async (row_count: number, currentDevice: string) => {
  const response = await fetch(
    `${
      import.meta.env.VITE_LAMBDA_BACKEND_API
    }/sensor-data?row_count=${row_count}&dustbin=${currentDevice}`
  );

  const data = (await response.json()) as unknown as SensorDataType[];

  if (response.ok) {
    return data.reverse();
  } else {
    throw new Error('Something went wrong');
  }
};

export { getSensorData };
