import { Suspense, lazy } from "react";
import { Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import { Loader } from "./components/States";

const Home = lazy(() => import("./pages/Home"));
const Films = lazy(() => import("./pages/Films"));
const Series = lazy(() => import("./pages/Series"));
const Cartoons = lazy(() => import("./pages/Cartoons"));
const FilmDetail = lazy(() => import("./pages/FilmDetail"));
const SeriesDetail = lazy(() => import("./pages/SeriesDetail"));
const CartoonDetail = lazy(() => import("./pages/CartoonDetail"));
const Login = lazy(() => import("./pages/Login"));
const Register = lazy(() => import("./pages/Register"));
const Profile = lazy(() => import("./pages/Profile"));
const Favorites = lazy(() => import("./pages/Favorites"));
const NotFound = lazy(() => import("./pages/NotFound"));

export default function App() {
  return (
    <div className="app-shell">
      <Navbar />
      <main style={{ flex: 1 }}>
        <Suspense fallback={<Loader label="Загрузка страницы" />}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/films" element={<Films />} />
            <Route path="/films/:id" element={<FilmDetail />} />
            <Route path="/series" element={<Series />} />
            <Route path="/series/:id" element={<SeriesDetail />} />
            <Route path="/cartoons" element={<Cartoons />} />
            <Route path="/cartoons/:id" element={<CartoonDetail />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route
              path="/profile"
              element={
                <ProtectedRoute>
                  <Profile />
                </ProtectedRoute>
              }
            />
            <Route
              path="/favorites"
              element={
                <ProtectedRoute>
                  <Favorites />
                </ProtectedRoute>
              }
            />
            <Route path="*" element={<NotFound />} />
          </Routes>
        </Suspense>
      </main>
      <footer>
        ТАСМА — учебный фронтенд для Etno_Practic · Django REST + React
      </footer>
    </div>
  );
}
