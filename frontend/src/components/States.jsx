export function Loader({ label = "Загрузка плёнки" }) {
  return (
    <div className="state-box">
      <div className="spinner" />
      <span className="frame-no">{label}…</span>
    </div>
  );
}

export function EmptyState({ title = "Кадров не найдено", hint }) {
  return (
    <div className="state-box">
      <p className="frame-no">{title}</p>
      {hint && <p style={{ marginTop: 8, fontSize: 13 }}>{hint}</p>}
    </div>
  );
}

export function ErrorState({ message = "Не удалось получить данные с бэкенда" }) {
  return (
    <div className="state-box">
      <p className="frame-no">Обрыв пленки</p>
      <p style={{ marginTop: 8, fontSize: 13 }}>{message}</p>
    </div>
  );
}
