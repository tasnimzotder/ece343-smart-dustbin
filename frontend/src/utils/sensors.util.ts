import { SensorDataType } from '../interfaces/sensor-data.interface';

const getUniqueDeviceCount = (data: SensorDataType[]) => {
  const uniqueDeviceIds = new Set(data.map((item) => item.device_id));
  const count = uniqueDeviceIds.size;

  return count;
};

export { getUniqueDeviceCount };
