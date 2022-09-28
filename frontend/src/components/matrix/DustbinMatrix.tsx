const MatrixCard = () => {
  return (
    <div className="bg-blue-200 px-3 py-3 rounded-sm shadow-sm">
      Matrix Card
    </div>
  );
};

const DustbinMatrix = () => {
  return (
    <div className="bg-blue-100 px-2 py-2 rounded-sm my-4">
      <h2 className="text-xl">Dustbin Matrix</h2>

      <div className="px-3 py-4 flex flex-row gap-3 flex-wrap justify-center">
        <MatrixCard />
        <MatrixCard />
        <MatrixCard />
      </div>
    </div>
  );
};

export default DustbinMatrix;
