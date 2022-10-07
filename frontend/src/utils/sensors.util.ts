import { SensorDataType } from '../interfaces/sensor-data.interface';

const getUniqueDeviceCount = (data: SensorDataType[]) => {
  const uniqueDeviceIds = new Set(data.map((item) => item.device_id));
  const count = uniqueDeviceIds.size;

  return count;
};

const getUniqueDevices = (data: SensorDataType[]): string[] => {
  let result: string[] = ['all'];

  data.forEach((item) => {
    if (!result.includes(item.device_id)) {
      result.push(item.device_id);
    }
  });

  return result;
};

const FilterDataByDeviceId = (data: SensorDataType[], deviceId: string) => {
  if (deviceId === 'all') {
    return data;
  }

  return data.filter((item) => item.device_id === deviceId);
};

export { getUniqueDeviceCount, getUniqueDevices, FilterDataByDeviceId };
