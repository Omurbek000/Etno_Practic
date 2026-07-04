import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchFilms, fetchSeries, fetchCartoons } from "../api/endpoints";
import PosterCard from "../components/PosterCard";
import { Loader, ErrorState } from "../components/States";

function Row({ frameNo, title, to, children }) {
  return (
    <section>
      <div className="section-head">
        <h2 className="section-title">
          <span className="frame-no">{frameNo}</span> {title}
        </h2>
        <Link to={to} className="section-link">
          Смотреть все →
        </Link>
      </div>
      {children}
    </section>
  );
}

export default function Home() {
  const [films, setFilms] = useState(null);
  const [series, setSeries] = useState(null);
  const [cartoons, setCartoons] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    Promise.all([
      fetchFilms({ page: 1 }),
      fetchSeries({ page: 1 }),
      fetchCartoons({ page: 1 }),
    ])
      .then(([f, s, c]) => {
        setFilms((f.results || f).slice(0, 6));
        setSeries((s.results || s).slice(0, 6));
        setCartoons((c.results || c).slice(0, 6));
      })
      .catch(() => setError(true));
  }, []);

  return (
    <div className="container">
      <section className="hero">
        <p className="hero-eyebrow">кат. №001 — этно-кинотеатр онлайн</p>
        <h1 className="hero-title">
          Кино, сериалы <br /> и мульт<em>фильмы</em> в одной плёнке
        </h1>
        <p className="hero-sub">
          ТАСМА — фронтенд для Etno_Practic: каталог фильмов, сериалов и мультфильмов с
          фильтрами, рейтингами, отзывами и личным избранным. Подключается к твоему Django REST API.
        </p>
        <div className="hero-actions">
          <Link to="/films" className="btn btn-primary">
            Перейти к фильмам
          </Link>
          <Link to="/register" className="btn">
            Создать аккаунт
          </Link>
        </div>
      </section>

      {error && <ErrorState message="Бэкенд не отвечает. Проверь, что сервер Django запущен и доступен по адресу из .env" />}

      {!error && films === null && <Loader label="Перематываем плёнку" />}

      {films && (
        <Row frameNo="01" title="Фильмы" to="/films">
          <div className="grid">
            {films.map((f) => (
              <PosterCard key={f.id} item={f} type="films" image={f.poster_image} title={f.title} />
            ))}
          </div>
        </Row>
      )}

      {series && (
        <Row frameNo="02" title="Сериалы" to="/series">
          <div className="grid">
            {series.map((s) => (
              <PosterCard key={s.id} item={s} type="series" image={s.image} title={s.title} />
            ))}
          </div>
        </Row>
      )}

      {cartoons && (
        <Row frameNo="03" title="Мультфильмы" to="/cartoons">
          <div className="grid">
            {cartoons.map((c) => (
              <PosterCard key={c.id} item={c} type="cartoons" image={c.cartoon_image} title={c.title} />
            ))}
          </div>
        </Row>
      )}
    </div>
  );
}
