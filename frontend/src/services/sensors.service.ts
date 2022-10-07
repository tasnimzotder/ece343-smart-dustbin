import { SensorDataType } from '../interfaces/sensor-data.interface';

const getSensorData = async (row_count: number) => {
  const options = {
    method: 'GET',
  };

  const response = await fetch(
    `${import.meta.env.VITE_LAMBDA_BACKEND_API}/?row_count=${row_count}`,
    options
  );

  const data = (await response.json()) as unknown as SensorDataType[];

  if (response.ok) {
    return data.reverse();
  } else {
    throw new Error('Something went wrong');
  }
};

export { getSensorData };
