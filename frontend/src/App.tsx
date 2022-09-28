import DustbinCtrl from './components/ctrl/DustbinCtrl';
import DustbinMatrix from './components/matrix/DustbinMatrix';

function App() {
  return (
    <div className="px-3 py-3 max-w-3xl mx-auto">
      <DustbinMatrix />
      <DustbinCtrl />
    </div>
  );
}

export default App;
