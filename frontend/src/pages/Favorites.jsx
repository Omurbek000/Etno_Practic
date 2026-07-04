import { useEffect, useState } from "react";
import { fetchFavorites, removeFavorite } from "../api/endpoints";
import PosterCard from "../components/PosterCard";
import { Loader, EmptyState, ErrorState } from "../components/States";

export default function Favorites() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    fetchFavorites()
      .then(setData)
      .catch(() => setError(true));
  }, []);

  const remove = async (id) => {
    await removeFavorite(id);
    setData((prev) => ({ ...prev, film_item: prev.film_item.filter((fi) => fi.id !== id) }));
  };

  return (
    <div className="container">
      <div className="section-head" style={{ marginTop: 36 }}>
        <h2 className="section-title">
          <span className="frame-no">07</span> Избранное
        </h2>
      </div>

      {error && <ErrorState />}
      {!error && !data && <Loader />}
      {data && data.film_item?.length === 0 && (
        <EmptyState title="Пока пусто" hint="Добавляйте фильмы, сериалы и мультфильмы кнопкой «В избранное» на странице контента." />
      )}

      {data && data.film_item?.length > 0 && (
        <div className="grid">
          {data.film_item.map((fi) => {
            const film = fi.film;
            const series = fi.series;
            const cartoon = fi.cartoon;
            const item = film || series || cartoon;
            const type = film ? "films" : series ? "series" : "cartoons";
            const image = film?.poster_image || series?.image || cartoon?.cartoon_image;
            if (!item) return null;
            return (
              <div key={fi.id} style={{ position: "relative" }}>
                <PosterCard item={item} type={type} image={image} title={item.title} />
                <button
                  className="btn btn-sm btn-danger"
                  style={{ width: "100%", marginTop: 8 }}
                  onClick={() => remove(fi.id)}
                >
                  Убрать
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
