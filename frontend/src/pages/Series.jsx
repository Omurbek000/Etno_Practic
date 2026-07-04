import { fetchSeries } from "../api/endpoints";
import CatalogPage from "./CatalogPage";

export default function Series() {
  return (
    <CatalogPage
      title="Сериалы"
      frameNo="02"
      type="series"
      fetcher={fetchSeries}
      image={(item) => item.image}
    />
  );
}
