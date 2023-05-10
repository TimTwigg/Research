import { BrowserRouter, Routes, Route } from 'react-router-dom';
import './App.css';
import Home from './pages/home.jsx';
import Maze from './pages/maze';
import Help from './pages/help.jsx';

function App() {
  return (
    <BrowserRouter>
        <Routes>
            <Route path = "/" element = {<Home />} />
            <Route path = "/maze" element = {<Maze />} />
            <Route path = "/help" element = {<Help />} />
        </Routes>
    </BrowserRouter>
  );
}

export default App;
