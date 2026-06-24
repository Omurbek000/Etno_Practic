import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { LangProvider } from './context/LangContext';
import Navbar from './components/Navbar';
import ProtectedRoute from './components/ProtectedRoute';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Films from './pages/Films';
import FilmDetail from './pages/FilmDetail';
import SeriesPage from './pages/SeriesPage';
import SeriesDetail from './pages/SeriesDetail';
import Cartoons from './pages/Cartoons';
import CartoonDetail from './pages/CartoonDetail';
import Profile from './pages/Profile';
import Favorites from './pages/Favorites';
import './styles/global.css';

export default function App() {
  return (
    <BrowserRouter>
      <LangProvider>
        <AuthProvider>
          <Navbar />
          <main style={{ flex: 1 }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/films" element={<Films />} />
              <Route path="/films/:id" element={<FilmDetail />} />
              <Route path="/series" element={<SeriesPage />} />
              <Route path="/series/:id" element={<SeriesDetail />} />
              <Route path="/cartoons" element={<Cartoons />} />
              <Route path="/cartoons/:id" element={<CartoonDetail />} />
              <Route path="/profile" element={<ProtectedRoute><Profile /></ProtectedRoute>} />
              <Route path="/favorites" element={<ProtectedRoute><Favorites /></ProtectedRoute>} />
            </Routes>
          </main>
        </AuthProvider>
      </LangProvider>
    </BrowserRouter>
  );
}
