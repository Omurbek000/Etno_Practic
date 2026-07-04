import { useEffect, useState } from "react";
import PosterCard from "../components/PosterCard";
import FilterBar from "../components/FilterBar";
import Pagination from "../components/Pagination";
import { Loader, EmptyState, ErrorState } from "../components/States";

const PAGE_SIZE = 20;

// config: { title, frameNo, type, fetcher, image: (item) => url, showAgeRating }
export default function CatalogPage({ title, frameNo, type, fetcher, image, showAgeRating }) {
  const [filters, setFilters] = useState({ page: 1 });
  const [data, setData] = useState(null);
  const [error, setError] = useState(false);

  useEffect(() => {
    setData(null);
    setError(false);
    const params = { ...filters };
    fetcher(params)
      .then((res) => setData(res))
      .catch(() => setError(true));
  }, [filters, fetcher]);

  const items = data ? data.results || data : [];
  const count = data ? data.count ?? items.length : 0;

  return (
    <div className="container">
      <div className="section-head" style={{ marginTop: 36 }}>
        <h2 className="section-title">
          <span className="frame-no">{frameNo}</span> {title}
        </h2>
      </div>

      <FilterBar filters={filters} setFilters={setFilters} showAgeRating={showAgeRating} />

      {error && <ErrorState />}
      {!error && data === null && <Loader />}
      {!error && data !== null && items.length === 0 && <EmptyState hint="Попробуй ослабить фильтры." />}

      {items.length > 0 && (
        <div className="grid">
          {items.map((item) => (
            <PosterCard key={item.id} item={item} type={type} image={image(item)} title={item.title} />
          ))}
        </div>
      )}

      {data && (
        <Pagination
          page={filters.page}
          count={count}
          pageSize={PAGE_SIZE}
          onChange={(p) => setFilters((prev) => ({ ...prev, page: p }))}
        />
      )}
    </div>
  );
}
