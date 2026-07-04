import { useEffect, useState } from "react";
import { fetchGenres, fetchCountries } from "../api/endpoints";

const ACCESS_TYPES = ["Free", "Subscription", "Rent"];
const LANGUAGES = ["Kyrgyz", "Russian", "Other"];
const AGE_RATINGS = ["0+", "6+", "12+", "16+", "18+"];

export default function FilterBar({ filters, setFilters, showAgeRating }) {
  const [genres, setGenres] = useState([]);
  const [countries, setCountries] = useState([]);

  useEffect(() => {
    fetchGenres().then(setGenres).catch(() => setGenres([]));
    fetchCountries().then(setCountries).catch(() => setCountries([]));
  }, []);

  const update = (key, value) => {
    setFilters((prev) => ({ ...prev, [key]: value || undefined, page: 1 }));
  };

  return (
    <div className="filter-bar">
      <div className="filter-field">
        <label>Жанр</label>
        <select value={filters.genres || ""} onChange={(e) => update("genres", e.target.value)}>
          <option value="">Любой</option>
          {genres.map((g) => (
            <option key={g.id} value={g.id}>
              {g.name}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-field">
        <label>Страна</label>
        <select value={filters.country || ""} onChange={(e) => update("country", e.target.value)}>
          <option value="">Любая</option>
          {countries.map((c) => (
            <option key={c.id} value={c.id}>
              {c.country}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-field">
        <label>Доступ</label>
        <select value={filters.access_type || ""} onChange={(e) => update("access_type", e.target.value)}>
          <option value="">Любой</option>
          {ACCESS_TYPES.map((a) => (
            <option key={a} value={a}>
              {a}
            </option>
          ))}
        </select>
      </div>

      <div className="filter-field">
        <label>Язык</label>
        <select value={filters.language || ""} onChange={(e) => update("language", e.target.value)}>
          <option value="">Любой</option>
          {LANGUAGES.map((l) => (
            <option key={l} value={l}>
              {l}
            </option>
          ))}
        </select>
      </div>

      {showAgeRating && (
        <div className="filter-field">
          <label>Возраст</label>
          <select value={filters.age_rating || ""} onChange={(e) => update("age_rating", e.target.value)}>
            <option value="">Любой</option>
            {AGE_RATINGS.map((a) => (
              <option key={a} value={a}>
                {a}
              </option>
            ))}
          </select>
        </div>
      )}

      <div className="filter-field">
        <label>Год от</label>
        <input
          type="number"
          placeholder="1990"
          value={filters.year__gt || ""}
          onChange={(e) => update("year__gt", e.target.value)}
        />
      </div>

      <div className="filter-field">
        <label>Год до</label>
        <input
          type="number"
          placeholder="2026"
          value={filters.year__lt || ""}
          onChange={(e) => update("year__lt", e.target.value)}
        />
      </div>
    </div>
  );
}
