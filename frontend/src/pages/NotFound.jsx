import { Link } from "react-router-dom";

export default function NotFound() {
  return (
    <div className="container">
      <div className="state-box">
        <p className="frame-no">кадр не найден — 404</p>
        <p style={{ margin: "12px 0 20px" }}>Такой страницы нет в плёнке.</p>
        <Link to="/" className="btn btn-primary">
          На главную
        </Link>
      </div>
    </div>
  );
}
