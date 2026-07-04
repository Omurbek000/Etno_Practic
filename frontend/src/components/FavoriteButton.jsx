import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { fetchFavorites, addFavorite, removeFavorite } from "../api/endpoints";
import { useAuth } from "../context/AuthContext";

// idKey: 'film_id' | 'series_id' | 'cartoon_id', matchKey: 'film' | 'series' | 'cartoon'
export default function FavoriteButton({ idKey, matchKey, itemId }) {
  const { user } = useAuth();
  const navigate = useNavigate();
  const [favoriteItemId, setFavoriteItemId] = useState(null);
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    if (!user) return;
    fetchFavorites()
      .then((data) => {
        const found = (data.film_item || []).find((fi) => fi[matchKey] && fi[matchKey].id === itemId);
        setFavoriteItemId(found ? found.id : null);
      })
      .catch(() => setFavoriteItemId(null));
  }, [user, itemId, matchKey]);

  const toggle = async () => {
    if (!user) {
      navigate("/login");
      return;
    }
    setBusy(true);
    try {
      if (favoriteItemId) {
        await removeFavorite(favoriteItemId);
        setFavoriteItemId(null);
      } else {
        const created = await addFavorite({ [idKey]: itemId });
        setFavoriteItemId(created.id);
      }
    } catch {
      // тихо игнорируем — например, дубликат в избранном
    } finally {
      setBusy(false);
    }
  };

  return (
    <button className={"btn" + (favoriteItemId ? " btn-primary" : "")} onClick={toggle} disabled={busy}>
      {favoriteItemId ? "★ В избранном" : "☆ В избранное"}
    </button>
  );
}
