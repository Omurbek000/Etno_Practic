import { fetchFilms } from "../api/endpoints";
import CatalogPage from "./CatalogPage";

export default function Films() {
  return (
    <CatalogPage
      title="Фильмы"
      frameNo="01"
      type="films"
      fetcher={fetchFilms}
      image={(item) => item.poster_image}
    />
  );
}
