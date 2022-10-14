const getAllDustbins = async () => {
  const response = await fetch(
    `${import.meta.env.VITE_LAMBDA_BACKEND_API}/dustbins`
  );

  const data = (await response.json()) as unknown as string[];

  if (response.ok) {
    return data;
  }

  throw new Error('Something went wrong');
};

export { getAllDustbins };
