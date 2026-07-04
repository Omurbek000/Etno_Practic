import { useAuth } from "../context/AuthContext";
import { mediaUrl } from "../api/client";
import { Loader } from "../components/States";

export default function Profile() {
  const { user, loading } = useAuth();

  if (loading) return <Loader />;
  if (!user) return null;

  return (
    <div className="container">
      <div className="section-head" style={{ marginTop: 36 }}>
        <h2 className="section-title">
          <span className="frame-no">06</span> Профиль
        </h2>
      </div>

      <div className="profile-card">
        {user.avatar ? (
          <img className="profile-avatar" src={mediaUrl(user.avatar)} alt={user.username} />
        ) : (
          <div className="profile-avatar" />
        )}
        <div>
          <p className="profile-name">{user.username}</p>
          <p className="profile-meta">{user.email}</p>
          <p className="profile-meta">
            Подписка: {user.subscription_status} · с {user.date_register?.slice(0, 10)}
          </p>
        </div>
      </div>
    </div>
  );
}
