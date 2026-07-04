import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { fetchReviews, createReview, deleteReview } from "../api/endpoints";
import { useAuth } from "../context/AuthContext";

// idKey: 'film_id' | 'series_id' | 'cartoon_id'
export default function ReviewSection({ idKey, itemId }) {
  const { user } = useAuth();
  const [reviews, setReviews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [stars, setStars] = useState(0);
  const [text, setText] = useState("");
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState("");

  const load = () => {
    setLoading(true);
    fetchReviews({ [idKey]: itemId })
      .then((data) => setReviews(data.results || data))
      .catch(() => setReviews([]))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    load();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [itemId]);

  const submit = async (e) => {
    e.preventDefault();
    setError("");
    if (!text.trim() && !stars) {
      setError("Напишите текст или поставьте оценку");
      return;
    }
    setSubmitting(true);
    try {
      await createReview({ [idKey]: itemId, stars: stars || null, text: text || null });
      setText("");
      setStars(0);
      load();
    } catch (err) {
      setError(err?.response?.data?.detail || "Не получилось отправить отзыв");
    } finally {
      setSubmitting(false);
    }
  };

  const remove = async (id) => {
    try {
      await deleteReview(id);
      setReviews((prev) => prev.filter((r) => r.id !== id));
    } catch {
      setError("Не получилось удалить отзыв");
    }
  };

  return (
    <div>
      <div className="section-head" style={{ margin: "0 0 14px" }}>
        <h2 className="section-title">
          Отзывы <span className="frame-no">{reviews.length}</span>
        </h2>
      </div>

      {loading && <p className="frame-no">загрузка…</p>}
      {!loading && reviews.length === 0 && <p style={{ color: "var(--text-faint)" }}>Пока нет отзывов — будьте первым.</p>}

      {reviews.map((r) => (
        <div className="review-card" key={r.id}>
          <div className="review-head">
            <span className="review-user">{r.user_review?.username || "Пользователь"}</span>
            {r.stars ? <span className="review-stars">★ {r.stars}/10</span> : null}
          </div>
          {r.text && <p className="review-text">{r.text}</p>}
          <div className="review-head" style={{ marginTop: 8, marginBottom: 0 }}>
            <span className="review-date">{r.created_date?.slice(0, 10)}</span>
            {user && r.user_review?.id === user.id && (
              <button className="btn btn-sm btn-danger" onClick={() => remove(r.id)}>
                Удалить
              </button>
            )}
          </div>
        </div>
      ))}

      {user ? (
        <form className="review-form" onSubmit={submit}>
          {error && <div className="form-error">{error}</div>}
          <div>
            <label style={{ fontSize: 12, color: "var(--text-dim)", marginBottom: 6, display: "block" }}>
              Оценка (1–10)
            </label>
            <div className="star-picker">
              {Array.from({ length: 10 }, (_, i) => i + 1).map((n) => (
                <button
                  type="button"
                  key={n}
                  className={n <= stars ? "filled" : ""}
                  onClick={() => setStars(n === stars ? 0 : n)}
                >
                  ★
                </button>
              ))}
            </div>
          </div>
          <textarea
            placeholder="Что думаете об этом фильме?"
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
          <button className="btn btn-primary" disabled={submitting} type="submit">
            {submitting ? "Отправка…" : "Оставить отзыв"}
          </button>
        </form>
      ) : (
        <p className="form-note">
          Чтобы оставить отзыв, нужно <Link to="/login">войти в аккаунт</Link>.
        </p>
      )}
    </div>
  );
}
