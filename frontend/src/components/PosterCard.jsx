import { Link } from "react-router-dom";
import { mediaUrl } from "../api/client";

const ACCESS_LABEL = {
  Free: "Бесплатно",
  Subscription: "Подписка",
  Rent: "Аренда",
};

export default function PosterCard({ item, type, image, title }) {
  const to = `/${type}/${item.id}`;
  const accessClass = item.access_type === "Free" ? "" : item.access_type.toLowerCase();

  return (
    <Link to={to} className="poster-card">
      <div className="poster-frame">
        <div className="poster-sprockets" />
        {image ? (
          <img src={mediaUrl(image)} alt={title} loading="lazy" />
        ) : (
          <div className="state-box" style={{ padding: 0 }}>
            <span className="frame-no">нет кадра</span>
          </div>
        )}
        <div className="poster-sprockets right" />
        {item.access_type && (
          <span className={`poster-badge ${accessClass}`}>{ACCESS_LABEL[item.access_type] || item.access_type}</span>
        )}
      </div>
      <div className="poster-body">
        <p className="poster-title">{title}</p>
        <div className="poster-meta">
          <span>{item.year}</span>
          {typeof item.get_avg_rating !== "undefined" && (
            <span className="rating-chip">★ {item.get_avg_rating || "—"}</span>
          )}
        </div>
      </div>
    </Link>
  );
}
