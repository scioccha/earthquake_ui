import logo from './logo.svg';
import './App.css';
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import Microservice from './pages/Microservice';

function App() {
  return (
    <div className="App">
      <BrowserRouter>
        {/* Define Routes */}
        <Routes>
          <Route path="/microservice/map/:lat&:long" element={<Microservice />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;
