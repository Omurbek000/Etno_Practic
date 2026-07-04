import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate("/");
  };

  return (
    <header className="navbar">
      <div className="container navbar-inner">
        <NavLink to="/" className="brand">
          <span className="brand-dot" />
          ТАСМА
        </NavLink>
        <nav className="nav-links">
          <NavLink to="/films" className={({ isActive }) => "nav-link" + (isActive ? " active" : "")}>
            Фильмы
          </NavLink>
          <NavLink to="/series" className={({ isActive }) => "nav-link" + (isActive ? " active" : "")}>
            Сериалы
          </NavLink>
          <NavLink to="/cartoons" className={({ isActive }) => "nav-link" + (isActive ? " active" : "")}>
            Мультфильмы
          </NavLink>
          {user && (
            <NavLink to="/favorites" className={({ isActive }) => "nav-link" + (isActive ? " active" : "")}>
              Избранное
            </NavLink>
          )}
        </nav>
        <div className="nav-auth">
          {user ? (
            <>
              <NavLink to="/profile" className="user-pill">
                {user.username}
                {user.subscription_status === "VIP" && <span className="tag accent">VIP</span>}
              </NavLink>
              <button className="btn btn-sm" onClick={handleLogout}>
                Выйти
              </button>
            </>
          ) : (
            <>
              <NavLink to="/login" className="btn btn-sm">
                Войти
              </NavLink>
              <NavLink to="/register" className="btn btn-sm btn-primary">
                Регистрация
              </NavLink>
            </>
          )}
        </div>
      </div>
      <div className="filmstrip-rule" />
    </header>
  );
}
