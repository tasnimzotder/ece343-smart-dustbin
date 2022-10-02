type SensorDataTypeRaw = {
  $metadata: any;
  ColumnInfo: ColumnInfoTypeRaw[];
  QueryId: string;
  QueryStatus: any;
  Rows: RowTypeRaw[];
};

type ColumnInfoTypeRaw = {
  Name: string;
  Type: any;
};

type RowTypeRaw = {
  Data: RowDataTypeRaw[];
};

type RowDataTypeRaw = {
  ScalarValue: string;
};

type SensorDataType = {
  timestamp: string;
  device_id: string;
  capacity_remaining: number;
  dustbin_lid_status: string;
};

export type { SensorDataTypeRaw, SensorDataType };
