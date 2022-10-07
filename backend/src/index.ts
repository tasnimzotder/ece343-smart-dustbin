import {
  QueryCommand,
  TimestreamQueryClient,
} from '@aws-sdk/client-timestream-query';
import * as dotenv from 'dotenv';
import { RecordType } from './interfaces/record.interface';
dotenv.config();

const DATABASE_NAME = process.env.DATABASE_NAME;
const TABLE_NAME = process.env.TABLE_NAME;
const DATABASE_REGION = process.env.DATABASE_REGION;

const queryClient = new TimestreamQueryClient({
  region: DATABASE_REGION,
});

const getRecords = async (row_count: number) => {
  if (row_count < 1) {
    row_count = 1;
  } else if (row_count > 5000) {
    row_count = 5000;
  }

  const query = `SELECT * FROM ${DATABASE_NAME}.${TABLE_NAME} ORDER BY time DESC LIMIT ${row_count}`;

  const queryData = await queryClient.send(
    new QueryCommand({
      QueryString: query,
    })
  );

  return queryData;
};

const FormatRecords = (u_records: any): RecordType[] => {
  let records: RecordType[] = [];

  u_records.Rows.forEach((row: any) => {
    if (
      !(
        records.length > 1 &&
        records[records.length - 1].timestamp == row.Data[4].ScalarValue
      )
    ) {
      records.push({
        device_id: row.Data[0].ScalarValue,
        capacity_remaining: parseInt(row.Data[1].ScalarValue),
        dustbin_lid_status: row.Data[2].ScalarValue,
        timestamp: row.Data[4].ScalarValue,
      });
    }
  });

  return records;
};

exports.handler = async (event: any = {}): Promise<any> => {
  let response;

  try {
    const { queryStringParameters } = event;

    const { row_count } = queryStringParameters;

    const queryData = await getRecords(parseInt(row_count));

    response = {
      statusCode: 200,
      body: JSON.stringify(FormatRecords(queryData)),
    };
  } catch (err) {
    response = {
      statusCode: 500,
      body: JSON.stringify(err),
    };
  }

  return response;
};
