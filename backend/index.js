require('dotenv').config();
const {
  TimestreamQueryClient,
  QueryCommand,
} = require('@aws-sdk/client-timestream-query');

const DATABASE_NAME = process.env.DATABASE_NAME;
const TABLE_NAME = process.env.TABLE_NAME;
const DATABASE_REGION = process.env.DATABASE_REGION;

const queryClient = new TimestreamQueryClient({
  region: DATABASE_REGION,
});

const getRows = async (row_count) => {
  const query = `SELECT * FROM "${DATABASE_NAME}"."${TABLE_NAME}" ORDER BY time DESC LIMIT ${row_count}`;

  const queryCommand = new QueryCommand({
    QueryString: query,
  });

  const queryData = await queryClient.send(queryCommand);

  return queryData;
};

exports.handler = async (event, context) => {
  let response;

  const { requestContext } = event;
  const { method } = requestContext.http;

  if (method == 'GET') {
    const { rawQueryString } = event;
    const row_count = rawQueryString.split('=')[1];

    const queryData = await getRows(row_count);

    response = {
      statusCode: 200,
      body: JSON.stringify(queryData),
    };
  } else if (method == 'POST') {
    response = {
      statusCode: 200,
      body: JSON.stringify('POST request'),
    };
  }

  return response;
};
