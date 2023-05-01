import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './pages/home.jsx';
import Maze from './pages/maze';

function App() {
  return (
    <BrowserRouter>
        <Routes>
            <Route path = "/" element = {<Home />} />
            <Route path = "/maze" element = {<Maze />} />
        </Routes>
    </BrowserRouter>
  );
}

export default App;
