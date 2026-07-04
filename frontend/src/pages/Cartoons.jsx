import { fetchCartoons } from "../api/endpoints";
import CatalogPage from "./CatalogPage";

export default function Cartoons() {
  return (
    <CatalogPage
      title="Мультфильмы"
      frameNo="03"
      type="cartoons"
      fetcher={fetchCartoons}
      image={(item) => item.cartoon_image}
      showAgeRating
    />
  );
}
